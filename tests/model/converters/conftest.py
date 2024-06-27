from datetime import datetime

import pytest

from src.api.database.models import AllianceDB, AllianceHistoryDB, CollectionDB, UserDB, UserHistoryDB


@pytest.fixture(scope="function")
def alliance_db() -> AllianceDB:
    return _create_alliance_db()


@pytest.fixture(scope="function")
def alliance_history_db() -> AllianceHistoryDB:
    return (_create_collection_db(), _create_alliance_db())


@pytest.fixture(scope="function")
def collection_db() -> CollectionDB:
    return _create_collection_db()


@pytest.fixture(scope="function")
def user_db() -> UserDB:
    return _create_user_db()


@pytest.fixture(scope="function")
def user_history_db() -> UserHistoryDB:
    return (_create_collection_db(), _create_user_db())


def _create_alliance_db() -> AllianceDB:
    return AllianceDB(collection_id=1, alliance_id=1, alliance_name="A1", score=0, division_design_id=0, trophy=5000, championship_score=0, number_of_members=1, number_of_approved_members=0)


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
