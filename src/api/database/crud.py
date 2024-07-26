from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel, col, extract, func, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select

from .. import utils
from ..models.enums import ParameterInterval
from .models import AllianceDB, AllianceHistoryDB, CollectionDB, UserDB, UserHistoryDB


async def drop_tables(engine: AsyncEngine):
    """Drops all tables from the SQLModel metadata.

    Args:
        engine (AsyncEngine): The engine used for the connection to the database.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


async def create_tables(engine: AsyncEngine):
    """Creates all tables from the SQLModel metadata.

    Args:
        engine (AsyncEngine): The engine used for the connection to the database.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def delete_collection(session: AsyncSession, collection_id: int) -> bool:
    """Attempts to delete the collection with the provided `collection_id`.

    Args:
        session (Session): The database session to use.
        collection_id (int): The `collection_id` of the Collection to delete.

    Returns:
        bool: Returns `True`, if such a collection exists and is deleted successfully. Returns `False`, if an error occured while deleting the collection.
    """
    async with session:
        collection = await get_collection(session, collection_id, True, True)
        try:
            await session.delete(collection)
            await session.commit()
            return True
        except Exception as e:
            print(e)
            return False


async def get_alliance_from_collection(session: AsyncSession, collection_id: int, alliance_id: int) -> Optional[AllianceHistoryDB]:
    """Retrieves information about a specific Alliance from a specific Collection.

    Args:
        session (Session): The database session to use.
        collection_id (int): The `collection_id` of the Collection to retrieve the data from.
        alliance_id (int): The `alliance_id` of the Alliance to retrieve.

    Returns:
        Optional[AllianceDB]: Returns the specified Alliance from the specified Collection, if there's one with the specified `alliance_id`. Else, it returns `None`. If an Alliance is returned and `include_users` is `True`, then the property `users` will be populated. Else, it will be empty.
    """
    async with session:
        alliance_query = (
            select(AllianceDB, CollectionDB)
            .join(CollectionDB, AllianceDB.collection_id == CollectionDB.collection_id)
            .where(AllianceDB.collection_id == collection_id)
            .where(AllianceDB.alliance_id == alliance_id)
        )
        alliance_history = (await session.exec(alliance_query)).first()
        if not alliance_history:
            return None

        alliance, collection = alliance_history

        if alliance and collection:
            user_query = select(UserDB).where(UserDB.collection_id == collection_id).where(UserDB.alliance_id == alliance_id)
            users = (await session.exec(user_query)).all()
            alliance.users = list(users)
            for user in alliance.users:
                user.alliance = alliance

        return (collection, alliance)


async def get_alliance_history(
    session: AsyncSession,
    alliance_id: int,
    include_users: bool = True,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    interval: ParameterInterval = ParameterInterval.MONTHLY,
    desc: bool = False,
    skip: int = 0,
    take: int = 100,
) -> list[AllianceHistoryDB]:
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
    async with session:
        query = (
            select(AllianceDB, CollectionDB)
            .join(CollectionDB, AllianceDB.collection_id == CollectionDB.collection_id)
            .where(AllianceDB.alliance_id == alliance_id)
        )
        query = _apply_select_parameters_to_query(query, from_date, to_date, interval, desc)
        query = query.offset(skip).limit(take)
        if include_users:
            query = query.options(selectinload(AllianceDB.users))

        results = (await session.exec(query)).all()
        return [(collection, alliance) for alliance, collection in results]


async def get_collection(session: AsyncSession, collection_id: int, include_alliances: bool, include_users: bool) -> Optional[CollectionDB]:
    """Retrieves the Collection with the specified `collection_id`.

    Args:
        session (Session): The database session to use.
        collection_id (int): The `collection_id` of the Collection to retrieve.
        include_alliances (bool): Determines, whether to also retrieve the Alliances related to the Collection.
        include_users (bool): Determines, whether to also retrieve the Users related to the Collection.

    Returns:
        Optional[CollectionDB]: The requested Collection, if it exists. Else, None. If a Collection is returned and `include_alliances` is `True`, then the property `alliances` will be populated. Else, it will be empty. If a Collection is returned and `include_users` is `True`, then the property `users` will be populated. Else, it will be empty.
    """
    async with session:
        collection = await session.get(CollectionDB, collection_id)
        if not collection or (not include_alliances and not include_users):
            return collection

        if include_alliances:  # Split up retrieving alliances, because getting all data at once was significantly slower
            query = select(AllianceDB).where(AllianceDB.collection_id == collection_id)
            alliances = (await session.exec(query)).all()
            collection.alliances = alliances
            for alliance in collection.alliances:
                alliance.collection = collection

        if include_users:  # Split up retrieving users, because getting all data at once was significantly slower
            query = select(UserDB).where(UserDB.collection_id == collection_id)
            users = (await session.exec(query)).all()
            collection.users = users
            for user in collection.users:
                user.collection = collection

        return collection


async def get_collection_by_timestamp(session: AsyncSession, collected_at: datetime) -> Optional[CollectionDB]:
    """Retrieves the Collection with the given `collected_at` datetime.

    Args:
        session (Session): The database session to use.
        collected_at (datetime): The `collected_at` of the Collection to look for.

    Returns:
        bool: The Collection with the specified `collected_at` value, if such a collection exists in the database. Else, `None`.
    """
    collected_at = utils.remove_timezone(collected_at)

    async with session:
        collection_query = select(CollectionDB).where(CollectionDB.collected_at == collected_at)
        collection = (await session.exec(collection_query)).first()
        return collection


async def get_collections(
    session: AsyncSession,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    interval: ParameterInterval = ParameterInterval.MONTHLY,
    desc: bool = False,
    skip: int = 0,
    take: int = 100,
) -> list[CollectionDB]:
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
    async with session:
        query = select(CollectionDB)
        query = _apply_select_parameters_to_query(query, from_date, to_date, interval, desc)
        query = query.offset(skip).limit(take)

        results = await session.exec(query)
        return list(results.all())


async def get_top_100_from_collection(session: AsyncSession, collection_id: int, skip: int = 0, take: int = 100) -> list[UserDB]:
    """_summary_

    Args:
        session (Session): The database session to use.
        collection_id (int): The `collection_id` of the Collection to retrieve the data from.
        skip (int, optional): Skip this number of results from the result set. Defaults to 0.
        take (int, optional): Limit the number of results returned. Defaults to 100.

    Returns:
        list[UserDB]: A (filtered) list of top 100 Users in the requested Collection ordered descending by Trophies.
    """
    async with session:
        query = select(UserDB).where(UserDB.collection_id == collection_id).order_by(col(UserDB.trophy).desc())
        query = query.offset(skip).limit(take)

        results = await session.exec(query)
        return list(results.all())


async def get_user_from_collection(session: AsyncSession, collection_id: int, user_id: int) -> Optional[UserHistoryDB]:
    """Retrieves information about a specific User from a specific collection.

    Args:
        session (Session): The database session to use.
        collection_id (int): The `collection_id` of the Collection to retrieve the data from.
        user_id (int): The `user_id` of the User to retrieve.

    Returns:
        Optional[UserDB]: Returns the specified User from the specified Collection, if there's one with the specified `user_id`. Else, it returns `None`. If a User is returned, `include_alliance` is `True` and the User was in an Alliance, then the property `alliance` will be populated. Else, it will be `None`.
    """
    async with session:
        user_history_query = (
            select(UserDB, CollectionDB)
            .join(CollectionDB, UserDB.collection_id == CollectionDB.collection_id)
            .where(UserDB.collection_id == collection_id)
            .where(UserDB.user_id == user_id)
            .options(selectinload(UserDB.alliance))
        )
        user_history = (await session.exec(user_history_query)).first()
        if not user_history:
            return None

        user, collection = user_history

        return (collection, user)


async def get_user_history(
    session: AsyncSession,
    user_id: int,
    include_alliance: bool = True,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    interval: ParameterInterval = ParameterInterval.MONTHLY,
    desc: bool = False,
    skip: int = 0,
    take: int = 100,
) -> list[UserHistoryDB]:
    """Retrieve an User's history over time.

    Args:
        session (Session): The database session to use.
        user_id (int): The `user_id` of the User to retrieve data for.
        include_alliance (bool): Determines, whether to also retrieve the Alliance of the User. Defaults to True.
        from_date (datetime, optional): Return only data collected after this date and time or exactly at this point. Defaults to None.
        to_date (datetime, optional): Return only data collected before this date and time or exactly at this point. Defaults to None.
        interval (ParameterInterval): Specify the interval of the data returned. Defaults to ParameterInterval.MONTHLY.
        desc (bool, optional): Determines, whether the data should be returned in descending order by the collection date and time. Defaults to False.
        skip (int, optional): Skip this number of results from the result set. Defaults to 0.
        take (int, optional): Limit the number of results returned. Defaults to 100.

    Returns:
        list[tuple[CollectionDB, UserDB]]: A list of tuples representing entries in the User history. A tuple contains the metadata of the respective Collection and the User's data from that Collection.
    """
    async with session:
        query = select(UserDB, CollectionDB).join(CollectionDB, UserDB.collection_id == CollectionDB.collection_id).where(UserDB.user_id == user_id)
        query = _apply_select_parameters_to_query(query, from_date, to_date, interval, desc)
        query = query.offset(skip).limit(take)

        if include_alliance:
            query = query.options(selectinload(UserDB.alliance))

        results = (await session.exec(query)).all()
        return [(collection, user) for user, collection in results]


async def has_alliance_history(session: AsyncSession, alliance_id: int) -> bool:
    """Checks, if there's any recorded history for an Alliance with the given `alliance_id`.

    Args:
        session (Session): The database session to use.
        alliance_id (int): The `alliance_id` of the Alliance to look for.

    Returns:
        bool: `True`, if any recorded history for the requested Alliance exists in the database. Else, `False`.
    """
    async with session:
        alliance_history_count_query = select(func.count()).select_from(AllianceDB).where(AllianceDB.alliance_id == alliance_id)
        alliance_history_count = (await session.exec(alliance_history_count_query)).one()
        return alliance_history_count > 0


async def has_collection(session: AsyncSession, collection_id: int) -> bool:
    """Checks, if a Collection with the given `collection_id` exists.

    Args:
        session (Session): The database session to use.
        collection_id (int): The `collection_id` of the Collection to look for.

    Returns:
        bool: `True`, if a collection exists in the database. Else, `False`.
    """
    return bool(await get_collection(session, collection_id, False, False))


async def has_collection_with_timestamp(session: AsyncSession, collected_at: datetime) -> bool:
    """Checks, if a Collection with the given `collected_at` exists.

    Args:
        session (Session): The database session to use.
        collected_at (datetime): The `collected_at` of the Collection to look for.

    Returns:
        bool: `True`, if such a collection exists in the database. Else, `False`.
    """
    collected_at = utils.remove_timezone(collected_at)

    async with session:
        collection_query = select(CollectionDB).where(CollectionDB.collected_at == collected_at)
        collection = (await session.exec(collection_query)).first()
        return bool(collection)


async def has_user_history(session: AsyncSession, user_id: int) -> bool:
    """Checks, if there's any recorded history for a User with the given `user_id`.

    Args:
        session (Session): The database session to use.
        user_id (int): The `user_id` of the User to look for.

    Returns:
        bool: `True`, if any recorded history for the requested User exists in the database. Else, `False`.
    """
    async with session:
        user_history_count_query = select(func.count()).select_from(UserDB).where(UserDB.user_id == user_id)
        user_history_count = (await session.exec(user_history_count_query)).one()
        return user_history_count > 0


async def save_collection(session: AsyncSession, collection: CollectionDB, include_alliances: bool, include_users: bool) -> CollectionDB:
    """Inserts a Collection into the database or updates an existing one.

    Args:
        session (Session): The database session to use.
        collection (CollectionDB): The Collection to be saved.
        include_alliances (bool): Determines, if the `alliances` related to the Collection should be saved to the database, too.
        include_users (bool): Determines, if the `alliances` related to the Collection should be saved to the database, too.

    Returns:
        CollectionDB: The inserted or updated Collection.
    """
    async with session:
        session.add(collection)
        if include_alliances and collection.alliances:
            for alliance in collection.alliances:
                session.add(alliance)
        if include_users and collection.users:
            for user in collection.users:
                session.add(user)
        await session.commit()
        await session.refresh(collection)
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
    create_tables.__name__,
    delete_collection.__name__,
    drop_tables.__name__,
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
