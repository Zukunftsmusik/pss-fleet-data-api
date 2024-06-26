import json
from datetime import datetime, timedelta
from typing import Optional

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


def create_dummy_data(engine: Engine, file_paths: list[str]):
    """Adds dummy data to the database.

    Args:
        engine (Engine): The engine to use to create a database session.
        file_paths (list[str]): The paths to the files containing dummy data.
    """
    data = {}
    for file in file_paths:
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

    Args:
        session (Session): The database session to use.
        collection_id (int): The `collection_id` of the Collection to delete.

    Returns:
        bool: Returns `True`, if such a collection exists and is deleted successfully. Returns `False`, if no collection with the provided `collection_id` exists.
    """
    with session:
        collection = session.get(CollectionDB, collection_id)
        if collection:
            session.delete(collection)
            session.commit()
            return True
        else:
            return False


def get_alliance_from_collection(session: Session, collection_id: int, alliance_id: int, include_users: bool) -> Optional[AllianceDB]:
    """Retrieves information about a specific Alliance from a specific Collection.

    Args:
        session (Session): The database session to use.
        collection_id (int): The `collection_id` of the Collection to retrieve the data from.
        alliance_id (int): The `alliance_id` of the Alliance to retrieve.
        include_users (bool, optional): Determines, whether to also retrieve the members of the Alliance. Defaults to True.

    Returns:
        Optional[AllianceDB]: Returns the specified Alliance from the specified Collection, if there's one with the specified `alliance_id`. Else, it returns `None`. If an Alliance is returned and `include_users` is `True`, then the property `users` will be populated. Else, it will be empty.
    """
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
    from_date: datetime,
    to_date: datetime,
    interval: ParameterInterval,
    desc: bool,
    skip: int,
    take: int,
) -> list[tuple[CollectionDB, AllianceDB]]:
    """Retrieve an Alliance's history over time.

    Args:
        session (Session): The database session to use.
        alliance_id (int): The `alliance_id` of the Alliance to retrieve data for.
        include_users (bool): Determines, if the Alliance's members should be included in the results.
        from_date (datetime, optional): Return only data collected after this date and time or exactly at this point. Defaults to None.
        to_date (datetime, optional): Return only data collected before this date and time or exactly at this point. Defaults to None.
        interval (ParameterInterval, optional): Specify the interval of the data returned. Defaults to ParameterInterval.MONTHLY.
        desc (bool, optional): Determines, whether the data should be returned in descending order by the collection date and time. Defaults to False.
        skip (int, optional): Skip this number of results from the result set. Defaults to 0.
        take (int, optional): Limit the number of results returned. Defaults to 100.

    Returns:
        list[tuple[CollectionDB, AllianceDB]]: A list of tuples representing entries in the Alliance history. A tuple contains the metadata of the respective Collection and the Alliance's data from that Collection.
    """
    with session:
        query = select(AllianceDB, CollectionDB).join(CollectionDB, AllianceDB.collection_id == CollectionDB.collection_id).where(AllianceDB.alliance_id == alliance_id)
        query = _apply_select_parameters_to_query(query, from_date, to_date, interval, desc)
        query = query.offset(skip).limit(take)

        if include_users:
            query = query.options(selectinload(AllianceDB.users))

        results = session.exec(query).all()
        return [(collection, alliance) for alliance, collection in results]


def get_collection(session: Session, collection_id: int, include_alliances: bool, include_users: bool) -> Optional[CollectionDB]:
    """Retrieves the Collection with the specified `collection_id`.

    Args:
        session (Session): The database session to use.
        collection_id (int): The `collection_id` of the Collection to retrieve.
        include_alliances (bool, optional): Determines, whether to also retrieve the Alliances related to the Collection. Defaults to True.
        include_users (bool, optional): Determines, whether to also retrieve the Users related to the Collection. Defaults to True.

    Returns:
        Optional[CollectionDB]: The requested Collection, if it exists. Else, None. If a Collection is returned and `include_alliances` is `True`, then the property `alliances` will be populated. Else, it will be empty. If a Collection is returned and `include_users` is `True`, then the property `users` will be populated. Else, it will be empty.
    """
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


def get_collections(session: Session, from_date: datetime, to_date: datetime, interval: ParameterInterval, desc: bool, skip: int, take: int) -> list[CollectionDB]:
    """Retrieves metadata of Collections meeting the specified criteria.

    Args:
        session (Session): The database session to use.
        from_date (datetime, optional): Return only data collected after this date and time or exactly at this point. Defaults to None.
        to_date (datetime, optional): Return only data collected before this date and time or exactly at this point. Defaults to None.
        interval (ParameterInterval, optional): Specify the interval of the data returned. Defaults to ParameterInterval.MONTHLY.
        desc (bool, optional): Determines, whether the data should be returned in descending order by the collection date and time. Defaults to False.
        skip (int, optional): Skip this number of results from the result set. Defaults to 0.
        take (int, optional): Limit the number of results returned. Defaults to 100.

    Returns:
        list[CollectionDB]: A list of Collections without any Alliances or Users.
    """
    with session:
        query = select(CollectionDB)
        query = _apply_select_parameters_to_query(query, from_date, to_date, interval, desc)
        query = query.offset(skip).limit(take)

        results = session.exec(query)
        return list(results.all())


def get_top_100_from_collection(session: Session, collection_id: int, skip: int, take: int) -> list[UserDB]:
    """_summary_

    Args:
        session (Session): The database session to use.
        collection_id (int): _description_
        skip (int, optional): Skip this number of results from the result set. Defaults to 0.
        take (int, optional): Limit the number of results returned. Defaults to 100.

    Returns:
        list[UserDB]: _description_
    """
    with session:
        query = select(UserDB).where(UserDB.collection_id == collection_id).order_by(col(UserDB.trophy).desc())
        query = query.offset(skip).limit(take)

        results = session.exec(query)
        return list(results.all())


def get_user_from_collection(session: Session, collection_id: int, user_id: int, include_alliance: bool) -> Optional[UserDB]:
    """Retrieves information about a specific User from a specific collection.

    Args:
        session (Session): The database session to use.
        collection_id (int): The `collection_id` of the Collection to retrieve the data from.
        user_id (int): The `user_id` of the User to retrieve.
        include_alliance (bool, optional): Determines, whether to also retrieve the Alliance of the User. Defaults to True.

    Returns:
        Optional[UserDB]: Returns the specified User from the specified Collection, if there's one with the specified `user_id`. Else, it returns `None`. If a User is returned, `include_alliance` is `True` and the User was in an Alliance, then the property `alliance` will be populated. Else, it will be `None`.
    """
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
    from_date: datetime,
    to_date: datetime,
    interval: ParameterInterval,
    desc: bool,
    skip: int,
    take: int,
) -> list[tuple[CollectionDB, UserDB]]:
    """Retrieve an User's history over time.

    Args:
        session (Session): The database session to use.
        user_id (int): The `user_id` of the User to retrieve data for.
        include_alliance (bool, optional): Determines, whether to also retrieve the Alliance of the User. Defaults to True.
        from_date (datetime, optional): Return only data collected after this date and time or exactly at this point. Defaults to None.
        to_date (datetime, optional): Return only data collected before this date and time or exactly at this point. Defaults to None.
        interval (ParameterInterval, optional): Specify the interval of the data returned. Defaults to ParameterInterval.MONTHLY.
        desc (bool, optional): Determines, whether the data should be returned in descending order by the collection date and time. Defaults to False.
        skip (int, optional): Skip this number of results from the result set. Defaults to 0.
        take (int, optional): Limit the number of results returned. Defaults to 100.

    Returns:
        list[tuple[CollectionDB, UserDB]]: A list of tuples representing entries in the User history. A tuple contains the metadata of the respective Collection and the User's data from that Collection.
    """
    with session:
        query = select(UserDB, CollectionDB).join(CollectionDB, UserDB.collection_id == CollectionDB.collection_id).where(UserDB.user_id == user_id)
        query = _apply_select_parameters_to_query(query, from_date, to_date, interval, desc)
        query = query.offset(skip).limit(take)

        if include_alliance:
            query = query.options(selectinload(UserDB.alliance))

        results = session.exec(query).all()
        return [(collection, user) for user, collection in results]


def has_collection(session: Session, collection_id: int) -> bool:
    """Checks, if a Collection with the given `collection_id` exists.

    Args:
        session (Session): The database session to use.
        collection_id (int): The `collection_id` of the Collection to look for.

    Returns:
        bool: `True`, if a collection exists in the database. Else, `False`.
    """
    return bool(get_collection(session, collection_id, False, False))


def save_collection(session: Session, collection: CollectionDB, include_alliances: bool, include_users: bool) -> CollectionDB:
    """Inserts a Collection into the database or updates an existing one.

    Args:
        session (Session): The database session to use.
        collection (CollectionDB): The Collection to be saved.
        include_alliances (bool, optional): Determines, if the `alliances` related to the Collection should be saved to the database, too.
        include_users (bool, optional): Determines, if the `alliances` related to the Collection should be saved to the database, too.

    Returns:
        CollectionDB: The inserted or updated Collection.
    """
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
    """Applies the specified query parameters to the given Select `query`.

    Args:
        query (Select): The query to be modified.
        from_date (datetime): Specifies the earliest date to return data from.
        to_date (datetime): Specifies the latest date to return data from.
        interval (ParameterInterval): Specifies the interval of the data to be returned.
        desc (bool): Specifies the sort direction of the returned data.

    Returns:
        Select: The modified query.
    """
    query = _apply_datetime_limits_to_query(query, from_date, to_date)
    query = _apply_interval_to_query(query, interval)
    query = _apply_order_by_collected_at_to_query(query, desc)
    return query


def _apply_datetime_limits_to_query(query: Select, from_date: datetime, to_date: datetime) -> Select:
    """Applies date limits to the given select `query`.

    Args:
        query (Select): The query to be modified.
        from_date (datetime): Specifies the earliest date to return data from.
        to_date (datetime): Specifies the latest date to return data from.

    Returns:
        Select: The modified query.
    """
    if from_date:
        query = query.where(CollectionDB.collected_at >= from_date)
    if to_date:
        query = query.where(CollectionDB.collected_at <= to_date)
    return query


def _apply_interval_to_query(query: Select, interval: ParameterInterval) -> Select:
    """Applies an interval to the given Select `query`.

    Args:
        query (Select): The query to be modified.
        interval (ParameterInterval): Specifies the interval of the data to be returned.

    Returns:
        Select: The modified query.
    """
    match interval:
        case ParameterInterval.DAILY:
            return query.where(extract("hour", CollectionDB.collected_at) == 23)
        case ParameterInterval.MONTHLY:
            return query.where(extract("month", CollectionDB.collected_at) != extract("month", (CollectionDB.collected_at + timedelta(hours=1))))
    return query


def _apply_order_by_collected_at_to_query(query: Select, desc: bool) -> Select:
    """Applies a sort direction to the given Select `query`.

    Args:
        query (Select): The query to be modified.
        desc (bool): Specifies the sort direction of the returned data.

    Returns:
        Select: The modified query.
    """
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
