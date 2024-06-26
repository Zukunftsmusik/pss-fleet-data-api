from datetime import datetime, timedelta, timezone
from typing import Optional, Union

import dateutil
import dateutil.parser
from pydantic import BaseModel, Field, field_validator

AllianceCreate2 = tuple[int, str, int]
"""_summary_

Returns:
    _type_: _description_
"""
AllianceCreate3 = tuple[int, str, int, int]
AllianceCreate4 = tuple[int, str, int, int, int]
AllianceCreate5 = AllianceCreate4
AllianceCreate6 = tuple[int, str, int, int, int, int]
AllianceCreate7 = tuple[int, str, int, int, int, int, int, int]


class CollectionBase(BaseModel):
    """A snapshot of fleet and player data in PSS."""

    metadata: "CollectionMetadataCreateBase"
    fleets: list
    users: list


class CollectionCreate2(CollectionBase):
    users: list["UserCreate3"]
    data: list["UserDataCreate3"]


class CollectionCreate3(CollectionBase):
    fleets: list["AllianceCreate3"]
    users: list["UserCreate3"]
    data: list["UserDataCreate3"]


class CollectionCreate4(CollectionBase):
    metadata: "CollectionMetadataCreate4"
    fleets: list["AllianceCreate4"]
    users: list["UserCreate4"]


class CollectionCreate5(CollectionCreate4):
    metadata: "CollectionMetadataCreate4"
    fleets: list["AllianceCreate5"]
    users: list["UserCreate5"]


class CollectionCreate6(CollectionCreate5):
    fleets: list["AllianceCreate6"]
    users: list["UserCreate6"]


class CollectionCreate7(CollectionCreate6):
    fleets: list["AllianceCreate7"]


class CollectionCreate8(CollectionCreate7):
    users: list["UserCreate8"]


class CollectionCreate9(CollectionCreate8):
    metadata: "CollectionMetadataCreate9"
    users: list["UserCreate9"]


class CollectionMetadataCreateBase(BaseModel):
    timestamp: datetime
    duration: float
    fleet_count: int
    user_count: int
    tourney_running: bool


class CollectionMetadataCreate4(CollectionMetadataCreateBase):
    schema_version: int


class CollectionMetadataCreate9(CollectionMetadataCreate4):
    max_tournament_battle_attempts: int


UserCreate3 = tuple[int, str]
UserCreate4 = tuple[int, str, int, int, Optional[int], int, Optional[datetime], datetime, Optional[datetime], Optional[int], Optional[int], int, int, int, int, int, int]
UserCreate5 = UserCreate4
UserCreate6 = tuple[int, str, int, int, Optional[int], int, Optional[datetime], datetime, Optional[datetime], Optional[int], Optional[int], int, int, int, int, int, int, int]
UserCreate8 = tuple[int, str, int, int, Optional[int], int, Optional[datetime], datetime, Optional[datetime], Optional[int], Optional[int], int, int, int, int, int, int, int, int]
UserCreate9 = tuple[int, str, int, int, Optional[int], int, Optional[datetime], datetime, Optional[datetime], Optional[int], Optional[int], int, int, int, int, int, int, int, int, int]
UserDataCreate3 = tuple[int, int, int, Optional[int], Optional[str], Optional[datetime], datetime]


class CollectionOut(CollectionCreate9):
    metadata: "CollectionMetadataOut"
    fleets: list["AllianceOut"]
    users: list["UserOut"]


class CollectionMetadataOut(CollectionMetadataCreate9):
    collection_id: int


AllianceOut = AllianceCreate7
UserOut = UserCreate9


class AllianceHistoryOut(BaseModel):
    collection: CollectionOut
    fleet: AllianceOut
    users: list[UserOut]


class UserHistoryOut(BaseModel):
    collection: CollectionOut
    user: UserOut
    fleet: AllianceOut


# ########## LEGACY CODE ##########


class AllianceCreateLegacy(BaseModel):
    """A partial PSS Alliance (fleet)."""

    alliance_id: int = Field(ge=0)
    """The PSS property `AllianceId` of the Alliance as returned by the PSS API."""
    alliance_name: str = Field(min_length=1)
    """The PSS property `AllianceName` of the Alliance as returned by the PSS API."""
    score: int = Field(ge=0)
    """The PSS property `Score` of the Alliance as returned by the PSS API."""
    division_design_id: Optional[int] = Field(ge=0)
    """The PSS property `DivisionDesignId` of the Alliance as returned by the PSS API."""
    trophy: int = Field(ge=0)
    """The PSS property `Trophy` of the Alliance as returned by the PSS API."""
    championship_score: Optional[int] = Field(ge=0, default=None)
    """The PSS property `ChampionshipScore` of the Alliance as returned by the PSS API."""
    number_of_members: Optional[int] = Field(ge=0, le=100, default=None)
    """The PSS property `NumberOfMembers` of the Alliance as returned by the PSS API."""
    number_of_approved_members: Optional[int] = Field(ge=0, le=100, default=None)
    """The PSS property `NumberOfApprovedMembers` of the Alliance as returned by the PSS API."""


class UserCreateLegacy(BaseModel):
    """A partial PSS User (player)."""

    user_id: int = Field(primary_key=True, index=True, ge=0)
    """The PSS property `Id` of the User as returned by the PSS API."""
    alliance_id: int = Field(index=True, ge=0, default=0)
    """The PSS property `AllianceId` of the User as returned by the PSS API."""

    user_name: str = Field(min_length=1)
    """The PSS property `Name` of the User as returned by the PSS API."""
    trophy: int = Field(ge=0)
    """The PSS property `Trophy` of the User as returned by the PSS API."""
    alliance_score: int = Field(ge=0, default=0)
    """The PSS property `AllianceScore` (stars) of the User as returned by the PSS API."""
    alliance_membership: Optional[str] = Field(default=None)
    """The PSS property `AllianceMembership` (fleet rank) of the User as returned by the PSS API."""
    alliance_join_date: Optional[datetime] = Field(default=None)
    """The PSS property `AllianceJoinDate` of the User as returned by the PSS API."""
    last_login_date: datetime
    """The PSS property `LastLoginDate` of the User as returned by the PSS API."""
    last_heartbeat_date: Optional[datetime] = Field(default=None)
    """The PSS property `LastHeartBeatDate` of the User as returned by the PSS API."""
    crew_donated: Optional[int] = Field(ge=0)
    """The PSS property `CrewDonated` of the User as returned by the PSS API."""
    crew_received: Optional[int] = Field(ge=0)
    """The PSS property `CrewReceived` (crew borrowed) of the User as returned by the PSS API."""
    pvp_attack_wins: Optional[int] = Field(ge=0)
    """The PSS property `PvPAttackWins` of the User as returned by the PSS API."""
    pvp_attack_losses: Optional[int] = Field(ge=0)
    """The PSS property `PvPAttackLosses` of the User as returned by the PSS API."""
    pvp_attack_draws: Optional[int] = Field(ge=0)
    """The PSS property `PvPAttackDraws` of the User as returned by the PSS API."""
    pvp_defence_wins: Optional[int] = Field(ge=0)
    """The PSS property `PvPDefenceWins` of the User as returned by the PSS API."""
    pvp_defence_losses: Optional[int] = Field(ge=0)
    """The PSS property `PvPDefenceLosses` of the User as returned by the PSS API."""
    pvp_defence_draws: Optional[int] = Field(ge=0)
    """The PSS property `PvPDefenceDraws` of the User as returned by the PSS API."""
    championship_score: Optional[int] = Field(ge=0, default=None)
    """The PSS property `ChampionshipScore` of the User as returned by the PSS API."""
    highest_trophy: Optional[int] = Field(ge=0, default=None)
    """The PSS property `HighestTrophy` of the User as returned by the PSS API."""
    tournament_bonus_score: Optional[int] = Field(ge=0, default=None)
    """The PSS property `TournamentBonusScore` of the User as returned by the PSS API."""

    @field_validator("alliance_join_date", mode="before")
    @classmethod
    def transform_alliance_join_date(cls, value: Union[datetime, int, str]) -> datetime:
        return add_utc_to_datetime(value)

    @field_validator("last_login_date", mode="before")
    @classmethod
    def transform_last_login_date(cls, value: Union[datetime, int, str]) -> datetime:
        return add_utc_to_datetime(value)

    @field_validator("last_heartbeat_date", mode="before")
    @classmethod
    def transform_last_heartbeat_date(cls, value: Union[datetime, int, str]) -> datetime:
        return add_utc_to_datetime(value)


class CollectionLegacy(BaseModel):
    """A snapshot of fleet and player data in PSS."""

    collection_id: int
    """An arbitrary ID for this Collection."""
    collected_at: datetime
    """Date and time of when this snapshot was created. Has timezone information, which is usually UTC."""
    duration: float = Field(ge=0.0)
    """The time it took to collection the data in this snapshot."""
    fleet_count: Optional[int] = Field(ge=0, le=101)  # Sometimes, 101 fleets participate.
    """The number of fleets collected in this snapshot."""
    user_count: Optional[int] = Field(ge=0, le=10200)  # Up to 100 members per fleet plus top 100 players, if they all aren't in a tournament fleet (unlikely, but still).
    """The number of players collected in this snapshot. Up to 100 members per fleet and an additional"""
    tournament_running: bool
    """Determines, if a monthly fleet tournament was active when collectin the data."""
    max_tournament_battle_attempts: Optional[int] = Field(ge=0, default=None)
    """The maximum Tournament battle attempts per day for any given player."""
    fleets: list[tuple[int, str, int, int, int, int, int]] = []
    """The fleets in this Collection. Can be empty."""
    players: list[
        tuple[
            int,
            str,
            int,
            int,
            int,
            int,
            datetime,
            datetime,
            Optional[datetime],
            Optional[int],
            Optional[int],
            Optional[int],
            Optional[int],
            Optional[int],
            Optional[int],
            Optional[int],
            Optional[int],
            Optional[int],
            Optional[int],
            Optional[int],
        ]
    ] = []
    """The players in this Collection. Can be empty."""


class AllianceLegacy(BaseModel):
    """A partial PSS Alliance (fleet)."""

    def __init__(self, **kwargs):
        # self.collection_id = kwargs.pop("collection_id", None)
        # self.alliance_id = kwargs.pop("alliance_id", None)
        self.data = (
            kwargs.pop("alliance_id", None),
            kwargs.pop("alliance_name", None),
            kwargs.pop("score", None),
            kwargs.pop("division_design_id", None),
            kwargs.pop("trophy", None),
            kwargs.pop("championship_score", None),
            kwargs.pop("number_of_members", None),
            kwargs.pop("number_of_approved_members", None),
        )

    collection_id: Optional[int] = Field(default=None, ge=0)
    """The `collection_id` of the Collection this User data is referencing."""
    alliance_id: int = Field(ge=0)
    """The PSS property `AllianceId` of the Alliance as returned by the PSS API."""
    data: tuple[int, str, int, int, int, int, int]

    # alliance_name: str = Field(min_length=1)
    # """The PSS property `AllianceName` of the Alliance as returned by the PSS API."""
    # score: int = Field(ge=0)
    # """The PSS property `Score` of the Alliance as returned by the PSS API."""
    # division_design_id: Optional[int] = Field(ge=0)
    # """The PSS property `DivisionDesignId` of the Alliance as returned by the PSS API."""
    # trophy: int = Field(ge=0)
    # """The PSS property `Trophy` of the Alliance as returned by the PSS API."""
    # championship_score: Optional[int] = Field(ge=0, default=None)
    # """The PSS property `ChampionshipScore` of the Alliance as returned by the PSS API."""
    # number_of_members: Optional[int] = Field(ge=0, le=100, default=None)
    # """The PSS property `NumberOfMembers` of the Alliance as returned by the PSS API."""
    # number_of_approved_members: Optional[int] = Field(ge=0, le=100, default=None)
    # """The PSS property `NumberOfApprovedMembers` of the Alliance as returned by the PSS API."""

    # collection: Optional[Collection] = Field(default=None)
    # """The Collection this Alliance data is referencing."""
    members: list["UserLegacy"] = []
    """The members of this fleet."""


class UserLegacy(BaseModel):
    """A partial PSS User (player)."""

    collection_id: Optional[int] = Field(default=None, ge=0)
    """The `collection_id` of the Collection this User data is referencing."""
    user_id: int = Field(primary_key=True, index=True, ge=0)
    """The PSS property `Id` of the User as returned by the PSS API."""
    alliance_id: int = Field(index=True, ge=0, default=0)
    """The PSS property `AllianceId` of the User as returned by the PSS API."""

    user_name: str = Field(min_length=1)
    """The PSS property `Name` of the User as returned by the PSS API."""
    trophy: int = Field(ge=0)
    """The PSS property `Trophy` of the User as returned by the PSS API."""
    alliance_score: int = Field(ge=0, default=0)
    """The PSS property `AllianceScore` (stars) of the User as returned by the PSS API."""
    alliance_membership: Optional[str] = Field(default=None)
    """The PSS property `AllianceMembership` (fleet rank) of the User as returned by the PSS API."""
    alliance_join_date: Optional[datetime] = Field(default=None)
    """The PSS property `AllianceJoinDate` of the User as returned by the PSS API."""
    last_login_date: datetime
    """The PSS property `LastLoginDate` of the User as returned by the PSS API."""
    last_heartbeat_date: Optional[datetime] = Field(default=None)
    """The PSS property `LastHeartBeatDate` of the User as returned by the PSS API."""
    crew_donated: Optional[int] = Field(ge=0)
    """The PSS property `CrewDonated` of the User as returned by the PSS API."""
    crew_received: Optional[int] = Field(ge=0)
    """The PSS property `CrewReceived` (crew borrowed) of the User as returned by the PSS API."""
    pvp_attack_wins: Optional[int] = Field(ge=0)
    """The PSS property `PvPAttackWins` of the User as returned by the PSS API."""
    pvp_attack_losses: Optional[int] = Field(ge=0)
    """The PSS property `PvPAttackLosses` of the User as returned by the PSS API."""
    pvp_attack_draws: Optional[int] = Field(ge=0)
    """The PSS property `PvPAttackDraws` of the User as returned by the PSS API."""
    pvp_defence_wins: Optional[int] = Field(ge=0)
    """The PSS property `PvPDefenceWins` of the User as returned by the PSS API."""
    pvp_defence_losses: Optional[int] = Field(ge=0)
    """The PSS property `PvPDefenceLosses` of the User as returned by the PSS API."""
    pvp_defence_draws: Optional[int] = Field(ge=0)
    """The PSS property `PvPDefenceDraws` of the User as returned by the PSS API."""
    championship_score: Optional[int] = Field(ge=0, default=None)
    """The PSS property `ChampionshipScore` of the User as returned by the PSS API."""
    highest_trophy: Optional[int] = Field(ge=0, default=None)
    """The PSS property `HighestTrophy` of the User as returned by the PSS API."""
    tournament_bonus_score: Optional[int] = Field(ge=0, default=None)
    """The PSS property `TournamentBonusScore` of the User as returned by the PSS API."""

    collection: Optional[CollectionLegacy] = Field(default=None)
    """The Collection this User data is referencing."""
    alliance: Optional[AllianceLegacy] = Field(default=None)
    """The fleet of this player."""


def add_utc_to_datetime(value: Union[datetime, int, str]) -> datetime:
    """Parses a string to datetime or takes the passed datetime and then adds `timezone.utc` to it."""
    if value:
        if isinstance(value, int):
            # If it's an integer value, then it's likely encoded as seconds from Jan 6th, 2016 00:00 UTC
            value = datetime(2016, 1, 6) + timedelta(seconds=value)
        elif isinstance(value, str):
            value = dateutil.parser.parse(value)
        if not value.tzinfo:
            value = value.replace(tzinfo=timezone.utc)
    return value
