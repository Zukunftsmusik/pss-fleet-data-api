from datetime import timezone

import pytest

from src.api.database.models import AllianceDB, AllianceHistoryDB, CollectionDB, UserDB, UserHistoryDB
from src.api.models import AllianceHistoryOut, AllianceOut, CollectionMetadataOut, CollectionOut, UserHistoryOut, UserOut
from src.api.models.converters import FromDB


@pytest.mark.usefixtures("alliance_db")
def test_to_alliance(alliance_db: AllianceDB):
    alliance = FromDB.to_alliance(alliance_db)

    _check_alliance_out(alliance)


@pytest.mark.usefixtures("alliance_history_db")
def test_to_alliance_history(alliance_history_db: AllianceHistoryDB):
    alliance_history = FromDB.to_alliance_history(alliance_history_db)

    assert isinstance(alliance_history, AllianceHistoryOut)

    _check_collection_out(alliance_history.collection)
    _check_alliance_out(alliance_history.fleet)

    assert isinstance(alliance_history.users, list)
    for user in alliance_history.users:
        _check_user_out(user)


@pytest.mark.usefixtures("collection_db")
def test_to_collection(collection_db: CollectionDB):
    collection = FromDB.to_collection(collection_db, True, True)

    _check_collection_out(collection)


@pytest.mark.usefixtures("user_db")
def test_to_user(user_db: UserDB):
    user = FromDB.to_user(user_db)

    _check_user_out(user)


@pytest.mark.usefixtures("user_history_db")
def test_to_user_history(user_history_db: UserHistoryDB):
    user_history = FromDB.to_user_history(user_history_db)

    assert isinstance(user_history, UserHistoryOut)

    _check_collection_out(user_history.collection)
    _check_user_out(user_history.user)
    if user_history.fleet:
        _check_alliance_out(user_history.fleet)


# Helpers


def _check_alliance_out(alliance: AllianceOut):
    assert alliance
    assert isinstance(alliance, tuple)
    assert len(alliance) == 8


def _check_collection_out(collection: CollectionOut):
    assert collection
    assert isinstance(collection, CollectionOut)
    _check_collection_metatadata_out(collection.metadata)

    assert isinstance(collection.fleets, list)
    for fleet in collection.fleets:
        _check_alliance_out(fleet)

    assert isinstance(collection.users, list)
    for user in collection.users:
        _check_user_out(user)


def _check_collection_metatadata_out(collection_metadata: CollectionMetadataOut):
    assert collection_metadata
    assert isinstance(collection_metadata, CollectionMetadataOut)
    assert collection_metadata.timestamp.tzinfo == timezone.utc


def _check_user_out(user: UserOut):
    assert user
    assert isinstance(user, tuple)
    assert len(user) == 20
