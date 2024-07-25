from datetime import datetime
from typing import Annotated, Optional, Union

from pydantic import BaseModel, Field, field_validator

from .. import utils
from ..config import CONSTANTS
from .enums import UserAllianceMembershipEncoded


DATETIME = Annotated[datetime, Field(ge=CONSTANTS.pss_start_date)]
FLOAT_GE_0 = Annotated[float, Field(ge=0.0)]
INT_GE_0 = Annotated[int, Field(ge=0)]
INT_GE_1 = Annotated[int, Field(ge=1)]
STR_LENGTH_GE_1 = Annotated[str, Field(min_length=1)]

OPTIONAL_INT_GE_0 = Annotated[Optional[int], Field(ge=0, default=None)]
OPTIONAL_STR_LENGTH_GE_1 = Annotated[Optional[str], Field(min_length=1, default=None)]


AllianceCreate2 = tuple[STR_LENGTH_GE_1, STR_LENGTH_GE_1, STR_LENGTH_GE_1]
"""(
    0: alliance_id (int),
    1: alliance_name (str),
    2: score (int)
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-3
"""


AllianceCreate3 = tuple[STR_LENGTH_GE_1, STR_LENGTH_GE_1, STR_LENGTH_GE_1, STR_LENGTH_GE_1]
"""(
    0: alliance_id (int),
    1: alliance_name (str),
    2: score (int),
    3: division_design_id (int)
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-3
"""


AllianceCreate4 = tuple[INT_GE_1, STR_LENGTH_GE_1, INT_GE_0, INT_GE_0, INT_GE_0]
"""(
    0: alliance_id,
    1: alliance_name,
    2: score,
    3: division_design_id,
    4: trophy
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-4
"""


AllianceCreate6 = tuple[INT_GE_1, STR_LENGTH_GE_1, INT_GE_0, INT_GE_0, INT_GE_0, INT_GE_0]
"""(
    0: alliance_id,
    1: alliance_name,
    2: score,
    3: division_design_id,
    4: trophy,
    5: championship_score
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-6
"""


AllianceCreate7 = tuple[INT_GE_1, STR_LENGTH_GE_1, INT_GE_0, INT_GE_0, INT_GE_0, INT_GE_0, INT_GE_0, INT_GE_0]
"""(
    0: alliance_id,
    1: alliance_name,
    2: score,
    3: division_design_id,
    4: trophy,
    5: championship_score,
    6: number_of_members,
    7: number_of_approved_members
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-7
"""


class CollectionCreateBase(BaseModel):
    """
    A snapshot of fleet and player data in PSS.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions
    """

    meta: "CollectionMetadataCreateBase"
    """The metadata of this Collection."""
    fleets: list
    """The fleets recorded in this Collection."""
    users: list
    """The players recorded in this Collection."""


class CollectionCreate3(CollectionCreateBase):
    """
    A snapshot of fleet and player data in PSS. Schema version 3.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-3
    """

    fleets: list[Union["AllianceCreate2", "AllianceCreate3"]]
    """The fleets recorded in this Collection."""
    users: list["UserCreate3"]
    """The IDs and names of the players recorded in this Collection."""
    data: list["UserDataCreate3"]
    """The players' data recorded in this Collection."""


class CollectionCreate4(CollectionCreateBase):
    """
    A snapshot of fleet and player data in PSS. Schema version 4.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-5
    """

    meta: "CollectionMetadataCreate4"
    """The metadata of this Collection."""
    fleets: list["AllianceCreate4"]
    """The fleets recorded in this Collection."""
    users: list["UserCreate4"]
    """The players recorded in this Collection."""


class CollectionCreate5(CollectionCreate4):
    """
    A snapshot of fleet and player data in PSS. Schema version 5.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-4
    """

    meta: "CollectionMetadataCreate4"
    """The metadata of this Collection."""
    fleets: list["AllianceCreate4"]
    """The fleets recorded in this Collection."""
    users: list["UserCreate5"]
    """The players recorded in this Collection."""


class CollectionCreate6(CollectionCreate5):
    """
    A snapshot of fleet and player data in PSS. Schema version 6.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-6
    """

    fleets: list["AllianceCreate6"]
    """The fleets recorded in this Collection."""
    users: list["UserCreate6"]
    """The players recorded in this Collection."""


class CollectionCreate7(CollectionCreate6):
    """
    A snapshot of fleet and player data in PSS. Schema version 7.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-7
    """

    fleets: list["AllianceCreate7"]
    """The fleets recorded in this Collection."""


class CollectionCreate8(CollectionCreate7):
    """
    A snapshot of fleet and player data in PSS. Schema version 8.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-8
    """

    users: list["UserCreate8"]
    """The players recorded in this Collection."""


class CollectionCreate9(CollectionCreate8):
    """
    A snapshot of fleet and player data in PSS. Schema version 9.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-9
    """

    meta: "CollectionMetadataCreate9"
    """The metadata of this Collection."""
    users: list["UserCreate9"]
    """The players recorded in this Collection."""


class CollectionMetadataCreateBase(BaseModel):
    """
    Base class for all metadata of a Collection.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions
    """

    timestamp: DATETIME
    """The timestamp of the moment the data in this Collection was started to get recorded."""
    duration: FLOAT_GE_0
    """The time it took to record the data in this Collection. In seconds."""
    fleet_count: INT_GE_0
    """The number of fleets recorded in this Collection."""
    user_count: INT_GE_0
    """The number of players recorded in this Collection."""
    tourney_running: bool
    """Determines, whether a monthly fleet tournament was running at the time of recording the data in this Collection."""
    data_version: Optional[int] = Field(ge=3, nullable=True, default=None)
    """The schema version with which this data was first collected and stored."""

    @field_validator("timestamp", mode="before")
    @staticmethod
    def transform_timestamp(value: Union[datetime, str]) -> datetime:
        if not value:
            return value

        if isinstance(value, str):
            value = utils.parse_datetime(value)

        return utils.localize_to_utc(value)


class CollectionMetadataCreate3(CollectionMetadataCreateBase):
    """
    The metadata for a Collection of schema version 4.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-3
    """


class CollectionMetadataCreate4(CollectionMetadataCreateBase):
    """
    The metadata for a Collection of schema version 4.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-4
    """

    schema_version: int
    """The version of the schema of the data in this Collection."""


class CollectionMetadataCreate9(CollectionMetadataCreate4):
    """
    The metadata for a Collection of schema version 9.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-9
    """

    max_tournament_battle_attempts: int
    """The maximum number of tournament battles any given player can do on a given monthly fleet tournament day."""


UserCreate3 = tuple[STR_LENGTH_GE_1, STR_LENGTH_GE_1]
"""(
    0: user_id (int),
    1: user_name (str)
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-3
"""


UserCreate4 = tuple[
    INT_GE_1,
    STR_LENGTH_GE_1,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    UserAllianceMembershipEncoded,
    OPTIONAL_INT_GE_0,
    INT_GE_0,
    OPTIONAL_INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
]
"""(
    0: user_id,
    1: user_name,
    2: alliance_id,
    3: trophy,
    4: alliance_score,
    5: alliance_membership (encoded),
    6: alliance_join_date (encoded),
    7: last_login_date (encoded),
    8: last_heartbeat_date (encoded),
    9: crew_donated,
    10: crew_received,
    11: pvp_attack_wins,
    12: pvp_attack_losses,
    13: pvp_attack_draws,
    14: pvp_defence_wins,
    15: pvp_defence_losses,
    16: pvp_defence_draws
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-4
"""


UserCreate5 = UserCreate4
"""(
    0: user_id,
    1: user_name,
    2: alliance_id,
    3: trophy,
    4: alliance_score,
    5: alliance_membership (encoded),
    6: alliance_join_date (encoded),
    7: last_login_date (encoded),
    8: last_heartbeat_date (encoded),
    9: crew_donated,
    10: crew_received,
    11: pvp_attack_wins,
    12: pvp_attack_losses,
    13: pvp_attack_draws,
    14: pvp_defence_wins,
    15: pvp_defence_losses,
    16: pvp_defence_draws
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-5
"""


UserCreate6 = tuple[
    INT_GE_1,
    STR_LENGTH_GE_1,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    UserAllianceMembershipEncoded,
    OPTIONAL_INT_GE_0,
    INT_GE_0,
    OPTIONAL_INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
]
"""(
    0: user_id,
    1: user_name,
    2: alliance_id,
    3: trophy,
    4: alliance_score,
    5: alliance_membership (encoded),
    6: alliance_join_date (encoded),
    7: last_login_date (encoded),
    8: last_heartbeat_date (encoded),
    9: crew_donated,
    10: crew_received,
    11: pvp_attack_wins,
    12: pvp_attack_losses,
    13: pvp_attack_draws,
    14: pvp_defence_wins,
    15: pvp_defence_losses,
    16: pvp_defence_draws,
    17: championship_score
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-6
"""


UserCreate8 = tuple[
    INT_GE_1,
    STR_LENGTH_GE_1,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    UserAllianceMembershipEncoded,
    OPTIONAL_INT_GE_0,
    INT_GE_0,
    OPTIONAL_INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
]
"""(
    0: user_id,
    1: user_name,
    2: alliance_id,
    3: trophy,
    4: alliance_score,
    5: alliance_membership (encoded),
    6: alliance_join_date (encoded),
    7: last_login_date (encoded),
    8: last_heartbeat_date (encoded),
    9: crew_donated,
    10: crew_received,
    11: pvp_attack_wins,
    12: pvp_attack_losses,
    13: pvp_attack_draws,
    14: pvp_defence_wins,
    15: pvp_defence_losses,
    16: pvp_defence_draws,
    17: championship_score,
    18: highest_trophy
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-8
"""


UserCreate9 = tuple[
    INT_GE_1,
    STR_LENGTH_GE_1,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    UserAllianceMembershipEncoded,
    OPTIONAL_INT_GE_0,
    INT_GE_0,
    OPTIONAL_INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
    INT_GE_0,
]
"""(
    0: user_id,
    1: user_name,
    2: alliance_id,
    3: trophy,
    4: alliance_score,
    5: alliance_membership (encoded),
    6: alliance_join_date (encoded),
    7: last_login_date (encoded),
    8: last_heartbeat_date (encoded),
    9: crew_donated,
    10: crew_received,
    11: pvp_attack_wins,
    12: pvp_attack_losses,
    13: pvp_attack_draws,
    14: pvp_defence_wins,
    15: pvp_defence_losses,
    16: pvp_defence_draws,
    17: championship_score,
    18: highest_trophy,
    19: tournament_bonus_score
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-9
"""


UserDataCreate3 = tuple[
    STR_LENGTH_GE_1, STR_LENGTH_GE_1, STR_LENGTH_GE_1, OPTIONAL_STR_LENGTH_GE_1, OPTIONAL_STR_LENGTH_GE_1, OPTIONAL_STR_LENGTH_GE_1, STR_LENGTH_GE_1
]
"""(
    0: user_id (int),
    1: alliance_id (int),
    2: trophy (int),
    3: alliance_score (int),
    4: alliance_membership (str),
    5: alliance_join_date (datetime),
    6: last_login_date (datetime)
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-3
"""


class CollectionOut(CollectionCreate9):
    """
    A snapshot of fleet and player data in PSS of the latest schema version.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions
    """

    meta: "CollectionMetadataOut"
    """The metadata of this Collection."""
    fleets: list["AllianceOut"]
    """The fleets recorded in this Collection."""
    users: list["UserOut"]
    """The players recorded in this Collection."""


class CollectionWithFleetsOut(BaseModel):
    """
    A snapshot of fleet and player data in PSS of the latest schema version, but without user information.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions
    """

    meta: "CollectionMetadataOut"
    """The metadata of this Collection."""
    fleets: list["AllianceOut"]
    """The fleets recorded in this Collection."""


class CollectionWithUsersOut(BaseModel):
    """
    A snapshot of fleet and player data in PSS of the latest schema version, but without fleet information.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions
    """

    meta: "CollectionMetadataOut"
    """The metadata of this Collection."""
    users: list["UserOut"]
    """The players recorded in this Collection."""


class CollectionMetadataOut(CollectionMetadataCreate9):
    """
    The metadata for a Collection of the latest schema version.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-9
    """

    collection_id: int
    """The ID of the collection in the database."""
    max_tournament_battle_attempts: Optional[int]
    """The maximum number of tournament battles any given player can do on a given monthly fleet tournament day."""


AllianceOut = AllianceCreate7
"""(
    0: alliance_id,
    1: alliance_name,
    2: score,
    3: division_design_id,
    4: trophy,
    5: championship_score,
    6: number_of_members,
    7: number_of_approved_members
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-7
"""


UserOut = UserCreate9
"""(
    0: user_id,
    1: user_name,
    2: alliance_id,
    3: trophy,
    4: alliance_score,
    5: alliance_membership,
    6: alliance_join_date,
    7: last_login_date,
    8: last_heartbeat_date,
    9: crew_donated,
    10: crew_received,
    11: pvp_attack_wins,
    12: pvp_attack_losses,
    13: pvp_attack_draws,
    14: pvp_defence_wins,
    15: pvp_defence_losses,
    16: pvp_defence_draws,
    17: championship_score,
    18: highest_trophy,
    19: tournament_bonus_score
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-9
"""


class AllianceHistoryOut(BaseModel):
    """
    A point in the recorded history of an Alliance.
    """

    collection: CollectionMetadataOut
    """The metadata of the Collection that represents the point in the history of the Alliance."""
    fleet: AllianceOut
    """The recorded Alliance data."""
    users: list[UserOut]
    """The members of the Alliance at the time of recording the Alliance data."""


class UserHistoryOut(BaseModel):
    """
    A point in the recorded history of a User.
    """

    collection: CollectionMetadataOut
    """The metadata of the Collection that represents the point in the history of the Alliance."""
    user: UserOut
    """The recorded User data."""
    fleet: Optional[AllianceOut]
    """The Alliance of the User at the time of recording the User data. May be `None`, if the User was not in an Alliance at the time."""


all = [
    AllianceCreate2.__name__,
    AllianceCreate3.__name__,
    AllianceCreate4.__name__,
    AllianceCreate6.__name__,
    AllianceCreate7.__name__,
    AllianceOut.__name__,
    AllianceHistoryOut.__name__,
    CollectionCreate3.__name__,
    CollectionCreate4.__name__,
    CollectionCreate5.__name__,
    CollectionCreate6.__name__,
    CollectionCreate7.__name__,
    CollectionCreate8.__name__,
    CollectionCreate9.__name__,
    CollectionMetadataOut.__name__,
    CollectionOut.__name__,
    CollectionWithFleetsOut.__name__,
    CollectionWithUsersOut.__name__,
    UserCreate3.__name__,
    UserCreate4.__name__,
    UserCreate5.__name__,
    UserCreate6.__name__,
    UserCreate8.__name__,
    UserCreate9.__name__,
    UserDataCreate3.__name__,
    UserHistoryOut.__name__,
    UserOut.__name__,
]
