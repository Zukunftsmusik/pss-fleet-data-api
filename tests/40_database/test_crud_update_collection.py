from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api.database.crud import save_collection, update_collection
from src.api.database.models import CollectionDB


test_cases = [
    # include_alliances, include_users
    pytest.param(False, False, id="no_alliances_no_users"),
    pytest.param(True, False, id="with_alliances_no_users"),
    pytest.param(False, True, id="no_alliances_with_users"),
    pytest.param(True, True, id="with_alliances_with_users"),
]

test_cases_non_unique = [
    # override_id, override_timestamp, expected_exception
    pytest.param(1, None, pytest.raises(IntegrityError), id="non_unique collection_id"),
    pytest.param(None, datetime(2024, 4, 30, 23, 59), pytest.raises(IntegrityError), id="non_unique timestamp"),
]


@pytest.mark.usefixtures("new_collection")
async def test_update_collection(session: AsyncSession, old_collection: CollectionDB, updated_collection: CollectionDB):
    old_collection = await save_collection(session, old_collection, True, True)
    collection_id = old_collection.collection_id

    collection: CollectionDB = await update_collection(session, collection_id, updated_collection)

    assert collection.collection_id == collection_id
    assert collection.collected_at == updated_collection.collected_at
    assert collection.duration == updated_collection.duration
    assert collection.fleet_count == updated_collection.fleet_count
    assert collection.max_tournament_battle_attempts == updated_collection.max_tournament_battle_attempts
    assert collection.tournament_running == updated_collection.tournament_running
    assert collection.user_count == updated_collection.user_count

    updated_alliances = {alliance.alliance_id: alliance for alliance in updated_collection.alliances}

    for alliance in collection.alliances:
        updated_alliance = updated_alliances[alliance.alliance_id]

        assert alliance.alliance_name == updated_alliance.alliance_name
        assert alliance.score == updated_alliance.score
        assert alliance.division_design_id == updated_alliance.division_design_id
        assert alliance.trophy == updated_alliance.trophy
        assert alliance.championship_score == updated_alliance.championship_score
        assert alliance.number_of_members == updated_alliance.number_of_members
        assert alliance.number_of_approved_members == updated_alliance.number_of_approved_members

    updated_users = {user.user_id: user for user in updated_collection.users}

    for user in collection.users:
        updated_user = updated_users[user.user_id]

        assert user.user_name == updated_user.user_name
        assert user.trophy == updated_user.trophy
        assert user.alliance_score == updated_user.alliance_score
        assert user.alliance_membership == updated_user.alliance_membership
        assert user.alliance_join_date == updated_user.alliance_join_date
        assert user.last_login_date == updated_user.last_login_date
        assert user.last_heartbeat_date == updated_user.last_heartbeat_date
        assert user.crew_donated == updated_user.crew_donated
        assert user.crew_received == updated_user.crew_received
        assert user.pvp_attack_wins == updated_user.pvp_attack_wins
        assert user.pvp_attack_losses == updated_user.pvp_attack_losses
        assert user.pvp_attack_draws == updated_user.pvp_attack_draws
        assert user.pvp_defence_wins == updated_user.pvp_defence_wins
        assert user.pvp_defence_losses == updated_user.pvp_defence_losses
        assert user.pvp_defence_draws == updated_user.pvp_defence_draws
        assert user.championship_score == updated_user.championship_score
        assert user.highest_trophy == updated_user.highest_trophy
        assert user.tournament_bonus_score == updated_user.tournament_bonus_score
