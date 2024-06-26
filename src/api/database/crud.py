import json
from datetime import datetime, timedelta
from typing import Optional, Sequence

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

        with Session(engine) as session:
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

                collection = save_collection(session, collection)


def delete_collection(session: Session, collection_id: int) -> bool:
    """Attempts to delete the collection with the provided `collection_id`.
    Returns `True`, if such a collection exists and is deleted successfully.
    Returns `False`, if no collection with the provided `collection_id` exists."""
    with session:
        collection = session.get(CollectionDB, collection_id)
        if collection:
            session.delete(collection)
            session.commit()
            return True
        else:
            return False


def get_alliance_from_collection(session: Session, collection_id: int, alliance_id: int, include_users: bool = True) -> Optional[AllianceDB]:
    with session:
        alliance_query = select(AllianceDB).where(AllianceDB.collection_id == collection_id).where(AllianceDB.alliance_id == alliance_id)
        alliance = session.exec(alliance_query).first()

        if alliance and include_users:
            user_query = select(UserDB).where(UserDB.collection_id == collection_id).where(UserDB.alliance_id == alliance_id)
            users = session.exec(user_query).all()
            alliance.users = list(users)
            for user in alliance.users:
                user.alliance = alliance

        return alliance


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
) -> list[tuple[CollectionDB, AllianceDB]]:
    """Retrieve an alliance's history over time.

    Args:
        session (Session): The database session to use.
        alliance_id (int): The `alliance_id` of the Alliance to retrieve data for.
        include_users (bool): Determines, if the alliance's members should be included in the results.
        from_date (datetime, optional): Return only data collected after this date and time or exactly at this point. Defaults to None.
        to_date (datetime, optional): Return only data collected before this date and time or exactly at this point. Defaults to None.
        interval (ParameterInterval, optional): Specify the interval of the data returned. Defaults to ParameterInterval.MONTHLY.
        desc (bool, optional): Determines, whether the data should be returned in descending order by the collection date and time. Defaults to False.
        skip (int, optional): Skip this number of results from the result set. Defaults to 0.
        take (int, optional): Limit the number of results returned. Defaults to 100.

    Returns:
        list[tuple[CollectionDB, AllianceDB]]: A list of tuples representing entries in the alliance history. A tuple contains the metadata of the respective collection and the alliance's data from that collection.
    """
    with session:
        query = select(AllianceDB, CollectionDB).join(CollectionDB, AllianceDB.collection_id == CollectionDB.collection_id).where(AllianceDB.alliance_id == alliance_id)
        query = _apply_select_parameters_to_query(query, from_date, to_date, interval, desc)
        query = query.offset(skip).limit(take)

        if include_users:
            query = query.options(selectinload(AllianceDB.users))

        results = session.exec(query).all()
        return [(collection, alliance) for alliance, collection in results]


def get_collection(session: Session, collection_id: int, include_alliances: bool = True, include_users: bool = True) -> Optional[CollectionDB]:
    with session:
        collection = session.get(CollectionDB, collection_id)
        if not collection or (not include_alliances and not include_users):
            return collection

        if include_alliances:  # Split up retrieving alliances, because getting all data at once was significantly slower
            query = select(AllianceDB).where(AllianceDB.collection_id == collection_id)
            alliances = session.exec(query).all()
            collection.alliances = alliances
            for alliance in collection.alliances:
                alliance.collection = collection

        if include_users:  # Split up retrieving users, because getting all data at once was significantly slower
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


def get_top_100_from_collection(session: Session, collection_id: int, skip: int = 0, take: int = 100) -> Sequence[UserDB]:
    with session:
        query = select(UserDB).where(UserDB.collection_id == collection_id).order_by(col(UserDB.trophy).desc())
        query = query.offset(skip).limit(take)

        results = session.exec(query)
        return results.all()


def get_user_from_collection(session: Session, collection_id: int, user_id: int, include_alliance: bool = True) -> Optional[UserDB]:
    with session:
        user_query = select(UserDB).where(UserDB.collection_id == collection_id).where(UserDB.user_id == user_id)
        if include_alliance:
            user_query = user_query.options(selectinload(UserDB.alliance))

        result = session.exec(user_query)
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
        query = select(UserDB, CollectionDB).join(CollectionDB, UserDB.collection_id == CollectionDB.collection_id).where(UserDB.user_id == user_id)
        query = _apply_select_parameters_to_query(query, from_date, to_date, interval, desc)
        query = query.offset(skip).limit(take)

        if include_alliance:
            query = query.options(selectinload(UserDB.alliance))

        results = session.exec(query).all()
        return [(collection, user) for user, collection in results]


def has_collection(session: Session, collection_id: int) -> bool:
    return bool(get_collection(session, collection_id, include_alliances=False, include_users=False))


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


__all__ = [
    create_dummy_data.__name__,
    delete_collection.__name__,
    get_alliance_from_collection.__name__,
    get_alliance_history.__name__,
    get_collection.__name__,
    get_collections.__name__,
    get_top_100_from_collection.__name__,
    get_user_from_collection.__name__,
    get_user_history.__name__,
    has_collection.__name__,
    save_collection.__name__,
]
