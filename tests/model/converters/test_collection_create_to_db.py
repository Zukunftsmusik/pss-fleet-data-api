import pytest

from src.api.database.models import AllianceDB, CollectionDB, UserDB
from src.api.models.api_models import CollectionCreate3
from src.api.models.converters import ToDB

pytest.mark.usefixtures("collection_create_2")


def test_from_collection_create_2(collection_create_2: CollectionCreate3):
    collection_db = ToDB.from_collection_2(collection_create_2)
    _check_collection_db_from_2(collection_db)


pytest.mark.usefixtures("collection_create_3")


def test_from_collection_create_3(collection_create_3: CollectionCreate3):
    collection_db = ToDB.from_collection_3(collection_create_3)
    _check_collection_db_from_2(collection_db)


pytest.mark.usefixtures("collection_create_4")


def test_from_collection_create_4(collection_create_4: CollectionCreate3):
    collection_db = ToDB.from_collection_4(collection_create_4)
    _check_collection_db_from_2(collection_db)


pytest.mark.usefixtures("collection_create_5")


def test_from_collection_create_5(collection_create_5: CollectionCreate3):
    collection_db = ToDB.from_collection_5(collection_create_5)
    _check_collection_db_from_2(collection_db)


pytest.mark.usefixtures("collection_create_6")


def test_from_collection_create_6(collection_create_6: CollectionCreate3):
    collection_db = ToDB.from_collection_6(collection_create_6)
    _check_collection_db_from_2(collection_db)


pytest.mark.usefixtures("collection_create_7")


def test_from_collection_create_7(collection_create_7: CollectionCreate3):
    collection_db = ToDB.from_collection_7(collection_create_7)
    _check_collection_db_from_2(collection_db)


pytest.mark.usefixtures("collection_create_8")


def test_from_collection_create_8(collection_create_8: CollectionCreate3):
    collection_db = ToDB.from_collection_8(collection_create_8)
    _check_collection_db_from_2(collection_db)


pytest.mark.usefixtures("collection_create_9")


def test_from_collection_create_9(collection_create_9: CollectionCreate3):
    collection_db = ToDB.from_collection_9(collection_create_9)
    _check_collection_db_from_9(collection_db)


# Helpers


def _check_collection_db_from_2(collection_db: CollectionDB):
    assert collection_db
    assert isinstance(collection_db, CollectionDB)

    assert collection_db.collected_at is not None
    assert collection_db.duration is not None
    assert collection_db.fleet_count is not None
    assert collection_db.user_count is not None
    assert collection_db.tournament_running is not None

    assert collection_db.alliances
    assert isinstance(collection_db.alliances, list)
    for alliance in collection_db.alliances:
        assert alliance
        assert isinstance(alliance, AllianceDB)

    assert collection_db.users
    assert isinstance(collection_db.users, list)
    for user in collection_db.users:
        assert user
        assert isinstance(user, UserDB)


def _check_collection_db_from_9(collection_db: CollectionDB):
    _check_collection_db_from_2(collection_db)

    assert collection_db.max_tournament_battle_attempts
