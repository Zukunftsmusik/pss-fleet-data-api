from datetime import datetime

import pytest

from src.api.database.models import AllianceDB, AllianceHistoryDB, CollectionDB, UserDB, UserHistoryDB
from src.api.models.api_models import (
    AllianceCreate2,
    AllianceCreate3,
    AllianceCreate4,
    AllianceCreate6,
    AllianceCreate7,
    CollectionCreate3,
    CollectionCreate4,
    CollectionCreate5,
    CollectionCreate6,
    CollectionCreate7,
    CollectionCreate8,
    CollectionCreate9,
    CollectionMetadataCreate3,
    CollectionMetadataCreate4,
    CollectionMetadataCreate9,
    CollectionMetadataCreateBase,
    UserCreate3,
    UserCreate4,
    UserCreate5,
    UserCreate6,
    UserCreate8,
    UserCreate9,
    UserDataCreate3,
)


@pytest.fixture(scope="function")
def alliance_create_2() -> AllianceCreate2:
    return _create_alliance_create_2()


@pytest.fixture(scope="function")
def alliance_create_3() -> AllianceCreate3:
    return _create_alliance_create_3()


@pytest.fixture(scope="function")
def alliance_create_4() -> AllianceCreate4:
    return _create_alliance_create_4()


@pytest.fixture(scope="function")
def alliance_create_5() -> AllianceCreate4:
    return _create_alliance_create_5()


@pytest.fixture(scope="function")
def alliance_create_6() -> AllianceCreate6:
    return _create_alliance_create_6()


@pytest.fixture(scope="function")
def alliance_create_7() -> AllianceCreate7:
    return _create_alliance_create_7()


@pytest.fixture(scope="function")
def alliance_db() -> AllianceDB:
    return _create_alliance_db()


@pytest.fixture(scope="function")
def alliance_history_db() -> AllianceHistoryDB:
    return (_create_collection_db(), _create_alliance_db())


@pytest.fixture(scope="function")
def collection_create_3() -> CollectionCreate3:
    return _create_collection_create_3()


@pytest.fixture(scope="function")
def collection_create_4() -> CollectionCreate4:
    return _create_collection_create_4()


@pytest.fixture(scope="function")
def collection_create_5() -> CollectionCreate5:
    return _create_collection_create_5()


@pytest.fixture(scope="function")
def collection_create_6() -> CollectionCreate6:
    return _create_collection_create_6()


@pytest.fixture(scope="function")
def collection_create_7() -> CollectionCreate7:
    return _create_collection_create_7()


@pytest.fixture(scope="function")
def collection_create_8() -> CollectionCreate8:
    return _create_collection_create_8()


@pytest.fixture(scope="function")
def collection_create_9() -> CollectionCreate9:
    return _create_collection_create_9()


@pytest.fixture(scope="function")
def collection_db() -> CollectionDB:
    return _create_collection_db()


@pytest.fixture(scope="function")
def user_create_3() -> UserCreate3:
    return _create_user_create_3()


@pytest.fixture(scope="function")
def user_create_4() -> UserCreate4:
    return _create_user_create_4()


@pytest.fixture(scope="function")
def user_create_5() -> UserCreate5:
    return _create_user_create_5()


@pytest.fixture(scope="function")
def user_create_6() -> UserCreate6:
    return _create_user_create_6()


@pytest.fixture(scope="function")
def user_create_8() -> UserCreate8:
    return _create_user_create_8()


@pytest.fixture(scope="function")
def user_create_9() -> UserCreate9:
    return _create_user_create_9()


@pytest.fixture(scope="function")
def user_data_create_3() -> UserDataCreate3:
    return _create_user_data_create_3()


@pytest.fixture(scope="function")
def user_db() -> UserDB:
    return _create_user_db()


@pytest.fixture(scope="function")
def user_history_db() -> UserHistoryDB:
    return (_create_collection_db(), _create_user_db())


# Helpers


def _create_alliance_create_2() -> AllianceCreate2:
    return ("1", "A1", "0")


def _create_alliance_create_3() -> AllianceCreate3:
    return (*_create_alliance_create_2(), "0")


def _create_alliance_create_4() -> AllianceCreate4:
    return (1, "A1", 0, 0, 1000)


def _create_alliance_create_5() -> AllianceCreate4:
    return _create_alliance_create_4()


def _create_alliance_create_6() -> AllianceCreate6:
    return (*_create_alliance_create_5(), 0)


def _create_alliance_create_7() -> AllianceCreate7:
    return (*_create_alliance_create_6(), 1, 0)


def _create_alliance_db() -> AllianceDB:
    return AllianceDB(
        collection_id=1,
        alliance_id=1,
        alliance_name="A1",
        score=0,
        division_design_id=0,
        trophy=5000,
        championship_score=0,
        number_of_members=1,
        number_of_approved_members=0,
    )


def _create_collection_create_3() -> CollectionCreate3:
    return CollectionCreate3(
        metadata=_create_collection_metadata_create_3(),
        fleets=[_create_alliance_create_3()],
        users=[_create_user_create_3()],
        data=[_create_user_data_create_3()],
    )


def _create_collection_create_4() -> CollectionCreate4:
    return CollectionCreate4(metadata=_create_collection_metadata_create_4(), fleets=[_create_alliance_create_4()], users=[_create_user_create_4()])


def _create_collection_create_5() -> CollectionCreate5:
    return CollectionCreate5(
        metadata=_create_collection_metadata_create_4(schema_version=5), fleets=[_create_alliance_create_5()], users=[_create_user_create_5()]
    )


def _create_collection_create_6() -> CollectionCreate6:
    return CollectionCreate6(
        metadata=_create_collection_metadata_create_4(schema_version=6), fleets=[_create_alliance_create_6()], users=[_create_user_create_6()]
    )


def _create_collection_create_7() -> CollectionCreate7:
    return CollectionCreate7(
        metadata=_create_collection_metadata_create_4(schema_version=7), fleets=[_create_alliance_create_7()], users=[_create_user_create_6()]
    )


def _create_collection_create_8() -> CollectionCreate8:
    return CollectionCreate8(
        metadata=_create_collection_metadata_create_4(schema_version=8), fleets=[_create_alliance_create_7()], users=[_create_user_create_8()]
    )


def _create_collection_create_9() -> CollectionCreate9:
    return CollectionCreate9(metadata=_create_collection_metadata_create_9(), fleets=[_create_alliance_create_7()], users=[_create_user_create_9()])


def _create_collection_db() -> CollectionDB:
    return CollectionDB(
        collection_id=1,
        collected_at=datetime(2016, 1, 6, 23, 59),
        duration=11.2,
        fleet_count=1,
        user_count=1,
        tournament_running=False,
        max_tournament_battle_attempts=6,
        alliances=[_create_alliance_db()],
        users=[_create_user_db()],
    )


def _create_collection_metadata_create_2() -> CollectionMetadataCreateBase:
    return CollectionMetadataCreateBase(timestamp=datetime(2016, 1, 6, 23, 59), duration=11.2, fleet_count=1, user_count=1, tourney_running=False)


def _create_collection_metadata_create_3() -> CollectionMetadataCreate3:
    return CollectionMetadataCreate3(timestamp=datetime(2016, 1, 6, 23, 59), duration=11.2, fleet_count=1, user_count=1, tourney_running=False)


def _create_collection_metadata_create_4(schema_version: int = None) -> CollectionMetadataCreate4:
    return CollectionMetadataCreate4(
        timestamp=datetime(2016, 1, 6, 23, 59), duration=11.2, fleet_count=1, user_count=1, tourney_running=False, schema_version=schema_version or 4
    )


def _create_collection_metadata_create_9() -> CollectionMetadataCreate9:
    return CollectionMetadataCreate9(
        timestamp=datetime(2016, 1, 6, 23, 59),
        duration=11.2,
        fleet_count=1,
        user_count=1,
        tourney_running=False,
        schema_version=9,
        max_tournament_battle_attempts=6,
    )


def _create_user_create_3() -> UserCreate3:
    return ("1", "U1")


def _create_user_create_4() -> UserCreate4:
    return (
        1,
        "U1",
        1,
        1000,
        0,
        0,
        int((datetime(2016, 6, 1, 8, 12, 34) - datetime(2016, 1, 6)).total_seconds()),
        int((datetime(2016, 6, 1, 23, 58) - datetime(2016, 1, 6)).total_seconds()),
        int((datetime(2016, 6, 1, 23, 58) - datetime(2016, 1, 6)).total_seconds()),
        0,
        0,
        5,
        2,
        1,
        1,
        8,
        0,
    )


def _create_user_create_5() -> UserCreate5:
    return _create_user_create_4()


def _create_user_create_6() -> UserCreate6:
    return (*_create_user_create_5(), 0)


def _create_user_create_8() -> UserCreate8:
    return (*_create_user_create_6(), 1000)


def _create_user_create_9() -> UserCreate9:
    return (*_create_user_create_8(), 0)


def _create_user_data_create_3() -> UserDataCreate3:
    return (
        "1",
        "1",
        "1000",
        "0",
        "Ensign",
        datetime(2016, 1, 6, 8, 12, 34).strftime("%Y-%m-%dT%H:%M:%S"),
        datetime(2016, 1, 6, 23, 58).strftime("%Y-%m-%dT%H:%M:%S"),
    )


def _create_user_db() -> UserDB:
    return UserDB(
        collection_id=1,
        user_id=1,
        alliance_id=1,
        user_name="U1",
        trophy=1000,
        alliance_score=0,
        alliance_membership="FleetAdmiral",
        alliance_join_date=datetime(2016, 1, 6, 8, 12, 34),
        last_login_date=datetime(2016, 1, 6, 23, 58),
        last_heartbeat_date=datetime(2016, 1, 6, 23, 58),
        crew_donated=0,
        crew_received=0,
        pvp_attack_wins=5,
        pvp_attack_losses=2,
        pvp_attack_draws=1,
        pvp_defence_wins=1,
        pvp_defence_losses=8,
        pvp_defence_draws=0,
        championship_score=0,
        highest_trophy=1000,
        tournament_bonus_score=0,
        alliance=_create_alliance_db(),
    )
