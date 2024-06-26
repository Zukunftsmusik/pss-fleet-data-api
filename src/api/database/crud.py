import json
from datetime import datetime, timedelta
from typing import Sequence

from sqlalchemy import Engine
from sqlalchemy.orm import selectinload
from sqlmodel import Session, SQLModel, col, extract, select
from sqlmodel.sql.expression import Select

from ..models.enums import ParameterInterval
from .models import AllianceDB, CollectionDB, UserDB


def drop_tables(engine: Engine):
    SQLModel.metadata.drop_all(engine)


def create_tables(engine: Engine):
    SQLModel.metadata.create_all(engine)


def create_dummy_data(engine: Engine, base_path: str):
    files = [
        f"{base_path}/generated_dummy_data.json",
        # f"{base_path}/pss-top-100_20191009-235900_import.json",
        # f"{base_path}/pss-top-100_20191107-115900_import.json",
        # f"{base_path}/pss-top-100_20191130-235900_import.json",
        # f"{base_path}/pss-top-100_20240229-235900_import.json",
        # f"{base_path}/pss-top-100_20240315-235900_import.json",
        # f"{base_path}/pss-top-100_20240331-235900_import.json",
        # f"{base_path}/pss-top-100_20240609-125900_import.json",
    ]
    data = {}
    for file in files:
        with open(file, "r") as fp:
            data = json.load(fp)

        if not isinstance(data, list):
            data = [data]

        for collected_data in data:
            alliances = [AllianceDB(**alliance) for alliance in collected_data["fleets"]]
            users = [UserDB(**user) for user in collected_data["users"]]

            collection = CollectionDB(**(collected_data["metadata"]), alliances=alliances, users=users)

            for i, alliance in enumerate(alliances):
                if not alliance.trophy:
                    alliance.trophy = sum(user.trophy for user in users if user.alliance_id == alliance.alliance_id)

                if collection.tournament_running and not alliance.division_design_id:
                    if i < 8:
                        alliance.division_design_id = 1
                    elif i < 20:
                        alliance.division_design_id = 2
                    elif i < 50:
                        alliance.division_design_id = 3
                    else:
                        alliance.division_design_id = 4

            collection = save_collection(engine, collection)


def delete_collection(session: Session, collection: CollectionDB) -> bool:
    with session:
        session.delete(collection)
        try:
            session.commit()
            return True
        except Exception as e:
            print(e)
            return False


def delete_collection_by_id(session: Session, collection_id) -> bool:
    with session:
        collection = session.get(CollectionDB, collection_id)
        session.delete(collection)
        try:
            session.commit()
            return True
        except Exception as e:
            print(e)
            return False


def get_alliance_from_collection(session: Session, collection_id: int, alliance_id: int, include_members: bool = True) -> CollectionDB:
    with session:
        query = select(AllianceDB).where(AllianceDB.collection_id == collection_id and AllianceDB.alliance_id == alliance_id)
        if include_members:
            query = query.join(UserDB)

        result = session.exec(query)
        return result.first()


def get_alliance_history(
    session: Session,
    alliance_id: int,
    include_users: bool,
    from_date: datetime = None,
    to_date: datetime = None,
    interval: ParameterInterval = ParameterInterval.MONTHLY,
    desc: bool = False,
    skip: int = 0,
    take: int = 100,
) -> Sequence[tuple[CollectionDB, AllianceDB]]:
    with session:
        query = select(CollectionDB, AllianceDB).join(AllianceDB).where(AllianceDB.alliance_id == alliance_id)
        query = _apply_select_parameters_to_query(query, from_date, to_date, interval, desc)
        query = query.offset(skip).limit(take)
        if include_users:
            query = query.options(selectinload(AllianceDB.users))

        results = session.exec(query)
        return results.all()


def get_collection(session: Session, collection_id: int, include_alliances: bool = True, include_users: bool = True) -> CollectionDB:
    with session:
        collection = session.get(CollectionDB, collection_id)
        if not collection or (not include_alliances and not include_users):
            return collection

        if include_alliances:
            query = select(AllianceDB).where(AllianceDB.collection_id == collection_id)
            alliances = session.exec(query).all()
            collection.alliances = alliances
            for alliance in collection.alliances:
                alliance.collection = collection

        if include_users:
            query = select(UserDB).where(UserDB.collection_id == collection_id)
            users = session.exec(query).all()
            collection.users = users
            for user in collection.users:
                user.collection = collection

        return collection


def get_collections(
    session: Session, from_date: datetime = None, to_date: datetime = None, interval: ParameterInterval = ParameterInterval.MONTHLY, desc: bool = False, skip: int = 0, take: int = 100
) -> Sequence[CollectionDB]:
    with session:
        query = select(CollectionDB)
        query = _apply_select_parameters_to_query(query, from_date, to_date, interval, desc)
        query = query.offset(skip).limit(take)

        results = session.exec(query)
        return results.all()


def get_top_100_from_collection(session: Session, collection_id: int, skip: int = 0, take: int = 100) -> list[UserDB]:
    with session:
        query = select(UserDB).where(UserDB.collection_id == collection_id).order_by(col(UserDB.trophy).desc())
        query = query.offset(skip).limit(take)

        results = session.exec(query)
        return results.all()


def get_user_from_collection(session: Session, collection_id: int, user_id: int, include_alliance: bool = True) -> CollectionDB:
    with session:
        query = select(UserDB).where(UserDB.collection_id == collection_id and UserDB.user_id == user_id)
        if include_alliance:
            query = query.join(AllianceDB)

        result = session.exec(query)
        return result.first()


def get_user_history(
    session: Session,
    user_id: int,
    include_alliance: bool,
    from_date: datetime = None,
    to_date: datetime = None,
    interval: ParameterInterval = ParameterInterval.MONTHLY,
    desc: bool = False,
    skip: int = 0,
    take: int = 100,
) -> Sequence[tuple[CollectionDB, UserDB]]:
    with session:
        query = select(CollectionDB, UserDB).join(UserDB).where(UserDB.user_id == user_id)
        if include_alliance:
            query = query.options(selectinload(UserDB.alliance))
        query = _apply_select_parameters_to_query(query, from_date, to_date, interval, desc)
        query = query.offset(skip).limit(take)

        results = session.exec(query)
        return results.all()


def has_collection(session: Session, collection_id: int) -> bool:
    with session:
        return bool(session.get(CollectionDB, collection_id))


def save_collection(session: Session, collection: CollectionDB, include_alliances: bool = True, include_users: bool = True) -> CollectionDB:
    with session:
        session.add(collection)
        if include_alliances and collection.alliances:
            for alliance in collection.alliances:
                session.add(alliance)
        if include_users and collection.users:
            for user in collection.users:
                session.add(user)
        session.commit()
        session.refresh(collection)
        return collection


def _apply_select_parameters_to_query(query: Select, from_date: datetime, to_date: datetime, interval: ParameterInterval, desc: bool) -> Select:
    query = _apply_datetime_limits_to_query(query, from_date, to_date)
    query = _apply_interval_to_query(query, interval)
    query = _apply_order_by_collected_at_to_query(query, desc)
    return query


def _apply_datetime_limits_to_query(query: Select, from_date: datetime, to_date: datetime) -> Select:
    if from_date:
        query = query.where(CollectionDB.collected_at >= from_date)
    if to_date:
        query = query.where(CollectionDB.collected_at <= to_date)
    return query


def _apply_interval_to_query(query: Select, interval: ParameterInterval) -> Select:
    match interval:
        case ParameterInterval.DAILY:
            return query.where(extract("hour", CollectionDB.collected_at) == 23)
        case ParameterInterval.MONTHLY:
            return query.where(extract("month", CollectionDB.collected_at) != extract("month", (CollectionDB.collected_at + timedelta(hours=1))))
    return query


def _apply_order_by_collected_at_to_query(query: Select, desc: bool) -> Select:
    if desc:
        query = query.order_by(col(CollectionDB.collected_at).desc())
    else:
        query = query.order_by(col(CollectionDB.collected_at).asc())
    return query


__all__ = [delete_collection.__name__, get_alliance_history.__name__, get_collection.__name__, get_collections.__name__, get_user_history.__name__, save_collection.__name__]
