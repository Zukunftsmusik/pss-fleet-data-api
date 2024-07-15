from contextlib import AbstractContextManager
from datetime import datetime
from typing import Any, Optional

import pytest

from src.api.models.enums import UserAllianceMembership, UserAllianceMembershipEncoded
from src.api.utils import decode_alliance_membership


test_cases_invalid = [
    # value, expected_exception
    pytest.param(None, pytest.raises(ValueError), id="none"),
    pytest.param(1234, pytest.raises(ValueError), id="int"),
    pytest.param("1234", pytest.raises(TypeError), id="str"),
    pytest.param(True, pytest.raises(TypeError), id="bool"),
    pytest.param(12.34, pytest.raises(TypeError), id="float"),
    pytest.param(complex("-1.23+4.5j"), pytest.raises(TypeError), id="complex"),
    pytest.param([5020], pytest.raises(TypeError), id="list[int]"),
    pytest.param({"seconds": 5020}, pytest.raises(TypeError), id="dict[str, int]"),
    pytest.param((datetime(2016, 1, 1),), pytest.raises(TypeError), id="tuple[datetime]"),
]


test_cases_valid = [
    # value, expected_result
    pytest.param(-1, UserAllianceMembership.NONE, id="rank_none_as_int"),
    pytest.param(6, UserAllianceMembership.CANDIDATE, id="rank_candidate_as_int"),
    pytest.param(5, UserAllianceMembership.ENSIGN, id="rank_ensign_as_int"),
    pytest.param(4, UserAllianceMembership.LIEUTENANT, id="rank_lieutenant_as_int"),
    pytest.param(3, UserAllianceMembership.MAJOR, id="rank_major_as_int"),
    pytest.param(2, UserAllianceMembership.COMMANDER, id="rank_commander_as_int"),
    pytest.param(1, UserAllianceMembership.VICE_ADMIRAL, id="rank_vice_admiral_as_int"),
    pytest.param(0, UserAllianceMembership.FLEET_ADMIRAL, id="rank_fleet_admiral_as_int"),
    pytest.param(UserAllianceMembershipEncoded.NONE, UserAllianceMembership.NONE, id="rank_none_as_enum"),
    pytest.param(UserAllianceMembershipEncoded.CANDIDATE, UserAllianceMembership.CANDIDATE, id="rank_candidate_as_enum"),
    pytest.param(UserAllianceMembershipEncoded.ENSIGN, UserAllianceMembership.ENSIGN, id="rank_ensign_as_enum"),
    pytest.param(UserAllianceMembershipEncoded.LIEUTENANT, UserAllianceMembership.LIEUTENANT, id="rank_lieutenant_as_enum"),
    pytest.param(UserAllianceMembershipEncoded.MAJOR, UserAllianceMembership.MAJOR, id="rank_major_as_enum"),
    pytest.param(UserAllianceMembershipEncoded.COMMANDER, UserAllianceMembership.COMMANDER, id="rank_commander_as_enum"),
    pytest.param(UserAllianceMembershipEncoded.VICE_ADMIRAL, UserAllianceMembership.VICE_ADMIRAL, id="rank_vice_admiral_as_enum"),
    pytest.param(UserAllianceMembershipEncoded.FLEET_ADMIRAL, UserAllianceMembership.FLEET_ADMIRAL, id="rank_fleet_admiral_as_enum"),
]


@pytest.mark.parametrize(["value", "expected_exception"], test_cases_invalid)
def test_decode_alliance_membership_invalid(value: Any, expected_exception: AbstractContextManager):
    with expected_exception:
        _ = decode_alliance_membership(value)


@pytest.mark.parametrize(["value", "expected_result"], test_cases_valid)
def test_decode_alliance_membership_valid(value: Optional[datetime], expected_result: Optional[datetime]):
    result = decode_alliance_membership(value)
    assert result == expected_result
