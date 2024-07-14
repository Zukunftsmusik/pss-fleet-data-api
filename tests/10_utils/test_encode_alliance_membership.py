from contextlib import AbstractContextManager
from datetime import datetime
from typing import Any, Optional

import pytest

from src.api.models.enums import UserAllianceMembership
from src.api.utils import encode_alliance_membership


test_cases_invalid = [
    # value, expected_exception
    pytest.param(None, pytest.raises(ValueError), id="none"),
    pytest.param("1234", pytest.raises(ValueError), id="str"),
    pytest.param(True, pytest.raises(TypeError), id="bool"),
    pytest.param(12.34, pytest.raises(TypeError), id="float"),
    pytest.param(1234, pytest.raises(TypeError), id="int"),
    pytest.param(complex("-1.23+4.5j"), pytest.raises(TypeError), id="complex"),
    pytest.param([5020], pytest.raises(TypeError), id="list[int]"),
    pytest.param({"seconds": 5020}, pytest.raises(TypeError), id="dict[str, int]"),
    pytest.param((datetime(2016, 1, 1),), pytest.raises(TypeError), id="tuple[datetime]"),
]


test_cases_valid = [
    # value, expected_result
    pytest.param("None", -1, id="rank_none_as_str"),
    pytest.param("Candidate", 6, id="rank_candidate_as_str"),
    pytest.param("Ensign", 5, id="rank_ensign_as_str"),
    pytest.param("Lieutenant", 4, id="rank_lieutenant_as_str"),
    pytest.param("Major", 3, id="rank_major_as_str"),
    pytest.param("Commander", 2, id="rank_commander_as_str"),
    pytest.param("ViceAdmiral", 1, id="rank_vice_admiral_as_str"),
    pytest.param("FleetAdmiral", 0, id="rank_fleet_admiral_as_str"),
    pytest.param(UserAllianceMembership.NONE, -1, id="rank_none_as_enum"),
    pytest.param(UserAllianceMembership.CANDIDATE, 6, id="rank_candidate_as_enum"),
    pytest.param(UserAllianceMembership.ENSIGN, 5, id="rank_ensign_as_enum"),
    pytest.param(UserAllianceMembership.LIEUTENANT, 4, id="rank_lieutenant_as_enum"),
    pytest.param(UserAllianceMembership.MAJOR, 3, id="rank_major_as_enum"),
    pytest.param(UserAllianceMembership.COMMANDER, 2, id="rank_commander_as_enum"),
    pytest.param(UserAllianceMembership.VICE_ADMIRAL, 1, id="rank_vice_admiral_as_enum"),
    pytest.param(UserAllianceMembership.FLEET_ADMIRAL, 0, id="rank_fleet_admiral_as_enum"),
]


@pytest.mark.parametrize(["value", "expected_exception"], test_cases_invalid)
def test_encode_alliance_membership_invalid(value: Any, expected_exception: AbstractContextManager):
    with expected_exception:
        _ = encode_alliance_membership(value)


@pytest.mark.parametrize(["value", "expected_result"], test_cases_valid)
def test_encode_alliance_membership_valid(value: Optional[datetime], expected_result: Optional[datetime]):
    result = encode_alliance_membership(value)
    assert result == expected_result
