from datetime import timezone
from typing import Union

import pytest

from src.api.database.models import AllianceDB, AllianceHistoryDB, CollectionDB, UserDB, UserHistoryDB
from src.api.models import (
    AllianceHistoryOut,
    AllianceOut,
    CollectionMetadataOut,
    CollectionOut,
    CollectionWithFleetsOut,
    CollectionWithUsersOut,
    UserHistoryOut,
    UserOut,
)
from src.api.models.converters import FromDB


@pytest.mark.usefixtures("alliance_db")
def test_to_alliance(alliance_db: AllianceDB):
    alliance = FromDB.to_alliance(alliance_db)

    _check_alliance_out(alliance)


@pytest.mark.usefixtures("alliance_history_db")
def test_to_alliance_history(alliance_history_db: AllianceHistoryDB):
    alliance_history = FromDB.to_alliance_history(alliance_history_db)

    assert isinstance(alliance_history, AllianceHistoryOut)

    _check_collection_metadata_out(alliance_history.collection)
    _check_alliance_out(alliance_history.fleet)

    assert isinstance(alliance_history.users, list)
    assert not alliance_history.users


@pytest.mark.usefixtures("alliance_history_db_with_member")
def test_to_alliance_history_with_members(alliance_history_db_with_member: AllianceHistoryDB):
    alliance_history = FromDB.to_alliance_history(alliance_history_db_with_member)

    assert isinstance(alliance_history, AllianceHistoryOut)

    _check_collection_metadata_out(alliance_history.collection)
    _check_alliance_out(alliance_history.fleet)

    assert isinstance(alliance_history.users, list)
    assert alliance_history.users
    for user in alliance_history.users:
        _check_user_out(user)


@pytest.mark.usefixtures("collection_db")
def test_to_collection(collection_db: CollectionDB):
    collection = FromDB.to_collection(collection_db, True, True)

    _check_collection_out(collection)


@pytest.mark.usefixtures("collection_db")
def test_to_collection_metadata(collection_db: CollectionDB):
    collection_metadata = FromDB.to_collection_metadata(collection_db)

    _check_collection_metadata_out(collection_metadata)


@pytest.mark.usefixtures("collection_db")
def test_to_collection_with_fleets(collection_db: CollectionDB):
    collection = FromDB.to_collection_with_fleets(collection_db)

    _check_collection_with_fleets_out(collection)


@pytest.mark.usefixtures("collection_db")
def test_to_collection_with_users(collection_db: CollectionDB):
    collection = FromDB.to_collection_with_users(collection_db)

    _check_collection_with_users_out(collection)


@pytest.mark.usefixtures("user_db")
def test_to_user(user_db: UserDB):
    user = FromDB.to_user(user_db)

    _check_user_out(user)


@pytest.mark.usefixtures("user_history_db")
def test_to_user_history(user_history_db: UserHistoryDB):
    user_history = FromDB.to_user_history(user_history_db)

    assert isinstance(user_history, UserHistoryOut)

    _check_collection_metadata_out(user_history.collection)
    _check_user_out(user_history.user)
    assert not user_history.fleet


@pytest.mark.usefixtures("user_history_db_with_alliance")
def test_to_user_history_with_alliance(user_history_db_with_alliance: UserHistoryDB):
    user_history = FromDB.to_user_history(user_history_db_with_alliance)

    assert isinstance(user_history, UserHistoryOut)

    _check_collection_metadata_out(user_history.collection)
    _check_user_out(user_history.user)
    _check_alliance_out(user_history.fleet)


# Helpers


def _check_alliance_out(alliance: AllianceOut):
    assert alliance
    assert isinstance(alliance, tuple)
    assert len(alliance) == 8


def _check_collection_out(collection: Union[CollectionOut, CollectionWithFleetsOut, CollectionWithUsersOut]):
    assert collection
    assert isinstance(collection, CollectionOut)
    _check_collection_metadata_out(collection.metadata)

    assert isinstance(collection.fleets, list)
    for fleet in collection.fleets:
        _check_alliance_out(fleet)

    assert isinstance(collection.users, list)
    for user in collection.users:
        _check_user_out(user)


def _check_collection_with_fleets_out(collection: CollectionWithFleetsOut):
    assert collection
    assert isinstance(collection, CollectionWithFleetsOut)
    _check_collection_metadata_out(collection.metadata)

    assert isinstance(collection.fleets, list)
    for fleet in collection.fleets:
        _check_alliance_out(fleet)

    assert not hasattr(collection, "users")


def _check_collection_with_users_out(collection: CollectionWithUsersOut):
    assert collection
    assert isinstance(collection, CollectionWithUsersOut)
    _check_collection_metadata_out(collection.metadata)

    assert not hasattr(collection, "fleets")

    assert isinstance(collection.users, list)
    for user in collection.users:
        _check_user_out(user)


def _check_collection_metadata_out(collection_metadata: CollectionMetadataOut):
    assert collection_metadata
    assert isinstance(collection_metadata, CollectionMetadataOut)
    assert collection_metadata.timestamp.tzinfo == timezone.utc
    assert collection_metadata.timestamp is not None
    assert collection_metadata.duration is not None
    assert collection_metadata.fleet_count is not None
    assert collection_metadata.user_count is not None
    assert collection_metadata.tourney_running is not None
    assert collection_metadata.schema_version is not None
    assert collection_metadata.data_version is not None

    if collection_metadata.data_version >= 9:
        assert collection_metadata.max_tournament_battle_attempts is not None


def _check_user_out(user: UserOut):
    assert user
    assert isinstance(user, tuple)
    assert len(user) == 20
