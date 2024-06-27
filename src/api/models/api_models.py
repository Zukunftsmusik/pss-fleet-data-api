from datetime import datetime, timedelta, timezone
from typing import Optional, Union

import dateutil
import dateutil.parser
from pydantic import BaseModel

AllianceCreate2 = tuple[int, str, int]
"""(
    0: alliance_id,
    1: alliance_name,
    2: score
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-3
"""


AllianceCreate3 = tuple[int, str, int, int]
"""(
    0: alliance_id,
    1: alliance_name,
    2: score,
    3: division_design_id
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-3
"""


AllianceCreate4 = tuple[int, str, int, int, int]
"""(
    0: alliance_id,
    1: alliance_name,
    2: score,
    3: division_design_id,
    4: trophy
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-4
"""


AllianceCreate5 = AllianceCreate4
"""(
    0: alliance_id,
    1: alliance_name,
    2: score,
    3: division_design_id,
    4: trophy
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-5
"""


AllianceCreate6 = tuple[int, str, int, int, int, int]
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


AllianceCreate7 = tuple[int, str, int, int, int, int, int, int]
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


class CollectionBase(BaseModel):
    """
    A snapshot of fleet and player data in PSS.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions
    """

    metadata: "CollectionMetadataCreateBase"
    """The metadata of this Collection."""
    fleets: list
    """The fleets recorded in this Collection."""
    users: list
    """The players recorded in this Collection."""


class CollectionCreate2(CollectionBase):
    """
    A snapshot of fleet and player data in PSS. Schema version 3, _without_ `division_design_id` in fleet tuples.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-3
    """

    fleets: list["AllianceCreate2"]
    """The fleets recorded in this Collection."""
    users: list["UserCreate3"]
    """The players recorded in this Collection."""
    data: list["UserDataCreate3"]


class CollectionCreate3(CollectionBase):
    """
    A snapshot of fleet and player data in PSS. Schema version 3, _with_ `division_design_id` in fleet tuples.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-3
    """

    fleets: list["AllianceCreate3"]
    """The fleets recorded in this Collection."""
    users: list["UserCreate3"]
    """The IDs and names of the players recorded in this Collection."""
    data: list["UserDataCreate3"]
    """The players' data recorded in this Collection."""


class CollectionCreate4(CollectionBase):
    """
    A snapshot of fleet and player data in PSS. Schema version 4.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-5
    """

    metadata: "CollectionMetadataCreate4"
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

    metadata: "CollectionMetadataCreate4"
    """The metadata of this Collection."""
    fleets: list["AllianceCreate5"]
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

    metadata: "CollectionMetadataCreate9"
    """The metadata of this Collection."""
    users: list["UserCreate9"]
    """The players recorded in this Collection."""


class CollectionMetadataCreateBase(BaseModel):
    """
    Base class for all metadata of a Collection.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions
    """

    timestamp: datetime
    """The timestamp of the moment the data in this Collection was started to get recorded."""
    duration: float
    """The time it took to record the data in this Collection. In seconds."""
    fleet_count: int
    """The number of fleets recorded in this Collection."""
    user_count: int
    """The number of players recorded in this Collection."""
    tourney_running: bool
    """Determines, whether a monthly fleet tournament was running at the time of recording the data in this Collection."""


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


UserCreate3 = tuple[int, str]
"""(
    0: user_id,
    1: user_name
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-3
"""


UserCreate4 = tuple[int, str, int, int, Optional[int], int, Optional[datetime], datetime, Optional[datetime], Optional[int], Optional[int], int, int, int, int, int, int]
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
    16: pvp_defence_draws
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-5
"""


UserCreate6 = tuple[int, str, int, int, Optional[int], int, Optional[datetime], datetime, Optional[datetime], Optional[int], Optional[int], int, int, int, int, int, int, int]
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
    17: championship_score
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-6
"""


UserCreate8 = tuple[int, str, int, int, Optional[int], int, Optional[datetime], datetime, Optional[datetime], Optional[int], Optional[int], int, int, int, int, int, int, int, int]
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
    18: highest_trophy
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-8
"""


UserCreate9 = tuple[int, str, int, int, Optional[int], int, Optional[datetime], datetime, Optional[datetime], Optional[int], Optional[int], int, int, int, int, int, int, int, int, int]
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


UserDataCreate3 = tuple[int, int, int, Optional[int], Optional[str], Optional[datetime], datetime]
"""(
    0: user_id,
    1: alliance_id,
    2: trophy,
    3: alliance_score,
    4: alliance_membership,
    5: alliance_join_date,
    6: last_login_date
)
See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-3
"""


class CollectionOut(CollectionCreate9):
    """
    A snapshot of fleet and player data in PSS of the latest schema version.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions
    """

    metadata: "CollectionMetadataOut"
    """The metadata of this Collection."""
    fleets: list["AllianceOut"]
    """The fleets recorded in this Collection."""
    users: list["UserOut"]
    """The players recorded in this Collection."""


class CollectionMetadataOut(CollectionMetadataCreate9):
    """
    The metadata for a Collection of the latest schema version.
    See also: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-version-9
    """

    collection_id: int
    """The ID of the collection in the database."""


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

    collection: CollectionOut
    """The metadata of the Collection that represents the point in the history of the Alliance."""
    fleet: AllianceOut
    """The recorded Alliance data."""
    users: list[UserOut]
    """The members of the Alliance at the time of recording the Alliance data."""


class UserHistoryOut(BaseModel):
    """
    A point in the recorded history of a User.
    """

    collection: CollectionOut
    """The metadata of the Collection that represents the point in the history of the Alliance."""
    user: UserOut
    """The recorded User data."""
    fleet: Optional[AllianceOut]
    """The Alliance of the User at the time of recording the User data. May be `None`, if the User was not in an Alliance at the time."""


def add_utc_to_datetime(value: Union[datetime, int, str]) -> datetime:
    """Parses a `str` or `int` to `datetime` or takes the passed `datetime` and then adds `timezone.utc` to it.

    Args:
        value (Union[datetime, int, str]): Either a `datetime`, an `int` representing the number of seconds since Jan 1st, 2016 (PSS start date) or a `str` representing a `datetime`.

    Returns:
        datetime: A timezone-aware `datetime` object with the UTC timezone set.
    """
    if value:
        if isinstance(value, int):
            # If it's an integer value, then it's likely encoded as seconds from Jan 6th, 2016 00:00 UTC
            value = datetime(2016, 1, 6) + timedelta(seconds=value)
        elif isinstance(value, str):
            value = dateutil.parser.parse(value)
        if not value.tzinfo:
            value = value.replace(tzinfo=timezone.utc)
    return value
