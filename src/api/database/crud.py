from datetime import datetime, timedelta, timezone
from typing import Optional, Union

from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel, col, extract, func, select, text
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select, SelectOfScalar

from .. import utils
from ..config import CONSTANTS
from ..models.enums import ParameterInterval, ParameterOnMissing
from .models import AllianceDB, AllianceHistoryDB, CollectionDB, UserDB, UserHistoryDB


DATE_TRUNC_TYPE_BY_INTERVAL: dict[ParameterInterval, str] = {
    ParameterInterval.HOURLY: "hour",
    ParameterInterval.DAILY: "day",
    ParameterInterval.MONTHLY: "month",
}


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
    on_missing: ParameterOnMissing = ParameterOnMissing.SKIP,
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
        on_missing (ParameterInterval, optional): Specify, how to handle missing collections.

    Returns:
        list[tuple[CollectionDB, AllianceDB]]: A list of tuples representing entries in the Alliance history. A tuple contains the metadata of the respective Collection and the Alliance's data from that Collection.
    """
    async with session:
        collections = await get_collections(session, from_date, to_date, interval, desc, skip, take, on_missing)
        collection_ids = [collection.collection_id for collection in collections if collection is not None and collection.collection_id is not None]

        query = (
            select(AllianceDB, CollectionDB)
            .join(CollectionDB, AllianceDB.collection_id == CollectionDB.collection_id)
            .where(col(CollectionDB.collection_id).in_(collection_ids))
            .where(AllianceDB.alliance_id == alliance_id)
        )
        if include_users:
            query = query.options(selectinload(AllianceDB.users))

        result = (await session.exec(query)).all()

        alliance_histories_by_collection_id = {collection.collection_id: (alliance, collection) for alliance, collection in result}
        alliance_histories = []

        for collection in collections:
            if collection is None and on_missing == ParameterOnMissing.NULL:
                alliance_histories.append(None)
            elif collection.collection_id is None and on_missing == ParameterOnMissing.EMPTY:
                alliance_histories.append((collection, None))
            else:
                alliance, _ = alliance_histories_by_collection_id.get(collection.collection_id, (None, None))
                if alliance:
                    alliance_histories.append((collection, alliance))

        return alliance_histories


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
    on_missing: ParameterOnMissing = ParameterOnMissing.SKIP,
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
        on_missing (ParameterInterval, optional): Specify, how to handle missing collections.

    Returns:
        list[CollectionDB]: A list of Collections without any Alliances or Users.
    """
    if not on_missing:
        on_missing = ParameterOnMissing.SKIP

    match on_missing:
        case ParameterOnMissing.SKIP:
            return await _get_collections_on_missing_skip(session, from_date, to_date, interval, desc, skip, take)
        case ParameterOnMissing.EMPTY:
            return await _get_collections_on_missing_empty_or_null(session, from_date, to_date, interval, desc, skip, take, on_missing)
        case ParameterOnMissing.NULL:
            return await _get_collections_on_missing_empty_or_null(session, from_date, to_date, interval, desc, skip, take, on_missing)
        case ParameterOnMissing.LAST:
            if interval == ParameterInterval.HOURLY:
                return await _get_collections_on_missing_skip(session, from_date, to_date, interval, desc, skip, take)

            return await _get_collections_on_missing_last(session, from_date, to_date, interval, desc, skip, take)


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
    on_missing: ParameterOnMissing = ParameterOnMissing.SKIP,
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
        on_missing (ParameterInterval, optional): Specify, how to handle missing collections.

    Returns:
        list[tuple[CollectionDB, UserDB]]: A list of tuples representing entries in the User history. A tuple contains the metadata of the respective Collection and the User's data from that Collection.
    """
    async with session:
        collections = await get_collections(session, from_date, to_date, interval, desc, skip, take, on_missing)
        collection_ids = [collection.collection_id for collection in collections if collection is not None and collection.collection_id is not None]

        query = (
            select(UserDB, CollectionDB)
            .join(CollectionDB, UserDB.collection_id == CollectionDB.collection_id)
            .where(col(CollectionDB.collection_id).in_(collection_ids))
            .where(UserDB.user_id == user_id)
        )
        if include_alliance:
            query = query.options(selectinload(UserDB.alliance))

        result = (await session.exec(query)).all()

        user_histories_by_collection_id = {collection.collection_id: (user, collection) for user, collection in result}
        user_histories = []

        for collection in collections:
            if collection is None and on_missing == ParameterOnMissing.NULL:
                user_histories.append(None)
            elif collection.collection_id is None and on_missing == ParameterOnMissing.EMPTY:
                user_histories.append((collection, None))
            else:
                user, _ = user_histories_by_collection_id.get(collection.collection_id, (None, None))
                if user:
                    user_histories.append((collection, user))

        return user_histories


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


async def update_collection(session: AsyncSession, collection_id: int, new_collection: CollectionDB) -> CollectionDB:
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
        collection = await get_collection(session, collection_id, True, True)

        collection.duration = new_collection.duration
        collection.fleet_count = new_collection.fleet_count
        collection.max_tournament_battle_attempts = new_collection.max_tournament_battle_attempts
        collection.tournament_running = new_collection.tournament_running
        collection.user_count = new_collection.user_count

        new_alliances = {alliance.alliance_id: alliance for alliance in new_collection.alliances}
        new_users = {user.user_id: user for user in new_collection.users}

        for alliance in collection.alliances:
            alliance_in = new_alliances[alliance.alliance_id]

            alliance.alliance_name = alliance_in.alliance_name
            alliance.score = alliance_in.score
            alliance.division_design_id = alliance_in.division_design_id
            alliance.trophy = alliance_in.trophy
            alliance.championship_score = alliance_in.championship_score
            alliance.number_of_members = alliance_in.number_of_members
            alliance.number_of_approved_members = alliance_in.number_of_approved_members

        for user in collection.users:
            user_in = new_users[user.user_id]

            user.user_name = user_in.user_name
            user.trophy = user_in.trophy
            user.alliance_score = user_in.alliance_score
            user.alliance_membership = user_in.alliance_membership
            user.alliance_join_date = user_in.alliance_join_date
            user.last_login_date = user_in.last_login_date
            user.last_heartbeat_date = user_in.last_heartbeat_date
            user.crew_donated = user_in.crew_donated
            user.crew_received = user_in.crew_received
            user.pvp_attack_wins = user_in.pvp_attack_wins
            user.pvp_attack_losses = user_in.pvp_attack_losses
            user.pvp_attack_draws = user_in.pvp_attack_draws
            user.pvp_defence_wins = user_in.pvp_defence_wins
            user.pvp_defence_losses = user_in.pvp_defence_losses
            user.pvp_defence_draws = user_in.pvp_defence_draws
            user.championship_score = user_in.championship_score
            user.highest_trophy = user_in.highest_trophy
            user.tournament_bonus_score = user_in.tournament_bonus_score

        session.add(collection)
        for alliance in collection.alliances:
            session.add(alliance)
        for user in collection.users:
            session.add(user)
        await session.commit()
        await session.refresh(collection)
        return collection


# ----- Helper functions -----


def _apply_select_parameters_to_query(
    query: Union[SelectOfScalar, Select],
    from_date: Optional[datetime],
    to_date: Optional[datetime],
    interval: ParameterInterval,
    desc: bool,
    *,
    entity_type: type = CollectionDB,
) -> Union[SelectOfScalar, Select]:
    """Applies the specified query parameters to the given Select `query`.

    Args:
        query (Select): The query to be modified.
        from_date (datetime): Specifies the earliest date to return data from.
        to_date (datetime): Specifies the latest date to return data from.
        interval (ParameterInterval): Specifies the interval of the data to be returned.
        desc (bool): Specifies the sort direction of the returned data.
        on_missing (ParameterOnMissing): Specifies how to handle missing data.

    Returns:
        Select: The modified query.
    """
    query = _apply_datetime_limits_to_query(query, from_date, to_date, entity_type)
    query = _apply_interval_to_query(query, interval, entity_type)
    query = _apply_order_by_collected_at_to_query(query, desc, entity_type)

    return query


def _apply_datetime_limits_to_query(
    query: Union[SelectOfScalar, Select], from_date: Optional[datetime], to_date: Optional[datetime], entity_type: type = CollectionDB
) -> Union[SelectOfScalar, Select]:
    """Applies date limits to the given select `query`.

    Args:
        query (Select): The query to be modified.
        from_date (datetime): Specifies the earliest date to return data from.
        to_date (datetime): Specifies the latest date to return data from.

    Returns:
        Select: The modified query.
    """
    if from_date:
        query = query.where(entity_type.collected_at >= from_date)
    if to_date:
        query = query.where(entity_type.collected_at <= to_date)
    return query


def _apply_interval_to_query(
    query: Union[SelectOfScalar, Select], interval: ParameterInterval, entity_type: type = CollectionDB
) -> Union[SelectOfScalar, Select]:
    """Applies an interval to the given Select `query`.

    Args:
        query (Select): The query to be modified.
        interval (ParameterInterval): Specifies the interval of the data to be returned.

    Returns:
        Select: The modified query.
    """
    match interval:
        case ParameterInterval.DAILY:
            return query.where(extract("hour", entity_type.collected_at) == 23)
        case ParameterInterval.MONTHLY:
            return query.where(extract("month", entity_type.collected_at) != extract("month", (entity_type.collected_at + timedelta(hours=1))))
    return query


def _apply_order_by_collected_at_to_query(
    query: Union[SelectOfScalar, Select], desc: bool, entity_type: type = CollectionDB
) -> Union[SelectOfScalar, Select]:
    """Applies a sort direction to the given Select `query`.

    Args:
        query (Select): The query to be modified.
        desc (bool): Specifies the sort direction of the returned data.

    Returns:
        Select: The modified query.
    """
    if desc:
        query = query.order_by(col(entity_type.collected_at).desc())
    else:
        query = query.order_by(col(entity_type.collected_at).asc())
    return query


async def _get_collections_on_missing_empty_or_null(
    session: AsyncSession,
    from_date: Optional[datetime],
    to_date: Optional[datetime],
    interval: ParameterInterval,
    desc: bool,
    skip: int,
    take: int,
    on_missing: ParameterOnMissing,
) -> list[CollectionDB]:
    """Retrieves collections with handling for missing data by filling with empty or null entries.

    Args:
        session (AsyncSession): The database session.
        from_date (Optional[datetime]): The start date for the query.
        to_date (Optional[datetime]): The end date for the query.
        interval (ParameterInterval): The interval for data aggregation.
        desc (bool): Whether to sort in descending order.
        skip (int): Number of records to skip.
        take (int): Number of records to take.
        on_missing (ParameterOnMissing): How to handle missing data.

    Returns:
        list[CollectionDB]: The list of collections with missing data handled.
    """
    from_date, to_date = _get_date_defaults(from_date, to_date)

    hour_series = select(
        func.generate_series(
            from_date + timedelta(minutes=59),
            to_date + timedelta(minutes=59),
            text("interval '1 hour'"),
        ).label("collected_at")
    ).cte("hour_series")

    async with session:
        query_hour_series = select(hour_series)
        query_hour_series = _apply_select_parameters_to_query(query_hour_series, from_date, to_date, interval, desc, entity_type=hour_series.c)
        query_hour_series = query_hour_series.offset(skip).limit(take)

        timestamps = (await session.exec(query_hour_series)).all()

        query_collections = select(CollectionDB).where(col(CollectionDB.collected_at).in_(timestamps))

        collections = (await session.exec(query_collections)).all()
        collections_by_timestamp = {collection.collected_at: collection for collection in collections}

        result = []
        for timestamp in timestamps:
            if timestamp in collections_by_timestamp.keys():
                result.append(collections_by_timestamp[timestamp])
            else:
                if on_missing == ParameterOnMissing.EMPTY:
                    result.append(
                        CollectionDB(
                            collected_at=timestamp,
                            data_version=0,
                            duration=0.0,
                            fleet_count=0,
                            user_count=0,
                            tournament_running=False,
                        )
                    )
                elif on_missing == ParameterOnMissing.NULL:
                    result.append(None)

        return result


async def _get_collections_on_missing_last(
    session: AsyncSession,
    from_date: Optional[datetime],
    to_date: Optional[datetime],
    interval: ParameterInterval,
    desc: bool,
    skip: int,
    take: int,
) -> list[CollectionDB]:
    """Retrieves collections within the specified date range, filling missing intervals with the last available collection for that interval.

    Args:
        session (AsyncSession): The database session to use.
        from_date (Optional[datetime]): The start date for the query. If None, defaults to the PSS start date.
        to_date (Optional[datetime]): The end date for the query. If None, defaults to the current UTC time.
        interval (ParameterInterval): The interval to group collections by (e.g., HOURLY, DAILY).
        desc (bool): Whether to order the results in descending order by collected_at.
        skip (int): The number of results to skip.
        take (int): The number of results to take.

    Returns:
        list[CollectionDB]: A list of CollectionDB objects, with missing intervals filled by the last collection in that interval.
    """
    from_date, to_date = _get_date_defaults(from_date, to_date)

    async with session:
        date_trunc_type = DATE_TRUNC_TYPE_BY_INTERVAL.get(interval)
        date_trunc = func.date_trunc(date_trunc_type, CollectionDB.collected_at)

        subquery = (
            select(CollectionDB)
            .where(CollectionDB.collected_at >= from_date)
            .where(CollectionDB.collected_at <= to_date)
            .distinct(date_trunc)
            .order_by(date_trunc.desc(), col(CollectionDB.collected_at).desc())
            .subquery()
        )

        query = (
            select(*[subquery.c[name] for name in subquery.c.keys()])
            .order_by(subquery.c.collected_at.desc() if desc else subquery.c.collected_at.asc())
            .offset(skip)
            .limit(take)
        )

        print(query)

        collections = (await session.exec(query)).all()
        return sorted(collections, key=lambda collection: collection.collected_at, reverse=desc)


async def _get_collections_on_missing_skip(
    session: AsyncSession,
    from_date: Optional[datetime],
    to_date: Optional[datetime],
    interval: ParameterInterval,
    desc: bool,
    skip: int,
    take: int,
) -> list[CollectionDB]:
    """Retrieves collections within the specified date range, skipping missing intervals.

    Args:
        session (AsyncSession): The database session to use.
        from_date (Optional[datetime]): The start date for the query. If None, defaults to the PSS start date.
        to_date (Optional[datetime]): The end date for the query. If None, defaults to the current UTC time.
        interval (ParameterInterval): The interval to group collections by (e.g., HOURLY, DAILY).
        desc (bool): Whether to order the results in descending order by collected_at.
        skip (int): The number of results to skip.
        take (int): The number of results to take.

    Returns:
        list[CollectionDB]: A list of CollectionDB objects.
    """
    async with session:
        entity_type = CollectionDB
        query = select(entity_type)
        query = _apply_select_parameters_to_query(query, from_date, to_date, interval, desc, entity_type=entity_type)
        query = query.offset(skip).limit(take)

        collections = (await session.exec(query)).all()
        return list(collections)


def _get_date_defaults(from_date: Optional[datetime], to_date: Optional[datetime]) -> tuple[datetime, datetime]:
    """Returns default values for `from_date` and `to_date` if they are not provided.

    Args:
        from_date (Optional[datetime]): The provided `from_date`, or None if not provided.
        to_date (Optional[datetime]): The provided `to_date`, or None if not provided.

    Returns:
        tuple[datetime, datetime]: A tuple containing the `from_date` and `to_date`, with defaults applied if necessary. If `from_date` is None, it defaults to the PSS start date. If `to_date` is None, it defaults to the current UTC time.
    """
    if not from_date:
        from_date = utils.remove_timezone(CONSTANTS.pss_start_date)
    if not to_date:
        to_date = utils.remove_timezone(datetime.now(timezone.utc))
    return from_date, to_date


__all__ = [
    "create_tables",
    "delete_collection",
    "drop_tables",
    "get_alliance_from_collection",
    "get_alliance_history",
    "get_collection",
    "get_collections",
    "get_top_100_from_collection",
    "get_user_from_collection",
    "get_user_history",
    "has_collection",
    "save_collection",
]
