from datetime import datetime
from typing import Any, Optional, Union

from pydantic import field_validator
from sqlalchemy.orm import foreign, relationship
from sqlmodel import Field, Relationship, SQLModel, and_

from .. import utils
from ..config import CONSTANTS


class CollectionBaseDB(SQLModel):
    collected_at: datetime = Field(index=True, unique=True)
    """Date and time of when this snapshot was created."""

    @field_validator("collected_at", mode="before")
    @staticmethod
    def transform_collected_at(value: Any) -> Union[datetime, Any]:
        """Takes the value provided to set the property `collected_at`, parses it, localizes it to UTC and then removes the timezone information.

        Args:
            value (Any): The value to set. Will be transformed, if it's of type `datetime`, `int` or `str`.

        Raises:
            ValueError: Raised, if the parsed datetime is lower than the PSS start date.

        Returns:
            Union[datetime, Any]: The transformed datetime or the original value, if it's not been transformed.
        """
        if isinstance(value, (datetime, int, str)):
            result = utils.remove_timezone(utils.localize_to_utc(utils.parse_datetime(value)))
            if result < CONSTANTS.pss_start_date:
                raise ValueError
            return utils.remove_timezone(result)
        else:
            return value


class CollectionDB(CollectionBaseDB, table=True):
    """A snapshot of fleet and player data in PSS."""

    __tablename__ = "collection"

    collection_id: int | None = Field(primary_key=True, index=True, default=None, ge=0)
    """An arbitrary ID for this Collection."""
    data_version: int = Field(ge=3)
    """The schema version with which this data was first collected and stored."""
    collected_at: datetime = Field(index=True, unique=True)
    """Date and time of when this snapshot was created."""
    duration: float = Field(ge=0.0)
    """The time it took to collection the data in this snapshot."""
    fleet_count: Optional[int] = Field(ge=0, le=101)  # Sometimes, 101 fleets participate.
    """The number of fleets collected in this snapshot."""
    user_count: Optional[int] = Field(
        ge=0, le=10200
    )  # Up to 100 members per fleet plus top 100 players, if they all aren't in a tournament fleet (unlikely, but still).
    """The number of players collected in this snapshot. Up to 100 members per fleet and an additional"""
    tournament_running: bool
    """Determines, if a monthly fleet tournament was active when collectin the data."""
    max_tournament_battle_attempts: Optional[int] = Field(ge=0, default=None, nullable=True)
    """The maximum Tournament battle attempts per day for any given player."""

    alliances: list["AllianceDB"] = Relationship(
        back_populates="collection", sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "noload"}
    )
    """The fleets in this Collection."""
    users: list["UserDB"] = Relationship(back_populates="collection", sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "noload"})
    """The players in this Collection."""


class AllianceBaseDB(SQLModel):
    pass


class AllianceDB(AllianceBaseDB, table=True):
    """A partial PSS Alliance (fleet)."""

    __tablename__ = "pss_alliance"

    collection_id: int = Field(primary_key=True, index=True, foreign_key="collection.collection_id", ge=0)
    """The `collection_id` of the Collection this User data is referencing."""
    alliance_id: int = Field(primary_key=True, index=True, ge=0)
    """The PSS property `AllianceId` of the Alliance as returned by the PSS API."""

    alliance_name: str = Field(min_length=1)
    """The PSS property `AllianceName` of the Alliance as returned by the PSS API."""
    score: int = Field(ge=0)
    """The PSS property `Score` of the Alliance as returned by the PSS API."""
    division_design_id: int = Field(ge=0)
    """The PSS property `DivisionDesignId` of the Alliance as returned by the PSS API."""
    trophy: Optional[int] = Field(ge=0, default=None, nullable=True)
    """The PSS property `Trophy` of the Alliance as returned by the PSS API."""
    championship_score: Optional[int] = Field(ge=0, default=None, nullable=True)
    """The PSS property `ChampionshipScore` of the Alliance as returned by the PSS API."""
    number_of_members: Optional[int] = Field(ge=0, le=100, default=None, nullable=True)
    """The PSS property `NumberOfMembers` of the Alliance as returned by the PSS API."""
    number_of_approved_members: Optional[int] = Field(ge=0, le=100, default=None, nullable=True)
    """The PSS property `NumberOfApprovedMembers` of the Alliance as returned by the PSS API."""

    collection: CollectionDB = Relationship(back_populates="alliances", sa_relationship_kwargs={"lazy": "noload"})
    """The Collection this Alliance data is referencing."""
    users: list["UserDB"] = Relationship()
    """The members of this fleet."""


class UserBaseDB(SQLModel):
    alliance_join_date: Optional[datetime] = Field(default=None, nullable=True)
    """The PSS property `AllianceJoinDate` of the User as returned by the PSS API."""
    last_login_date: Optional[datetime] = Field(default=None, nullable=True)
    """The PSS property `LastLoginDate` of the User as returned by the PSS API."""
    last_heartbeat_date: Optional[datetime] = Field(default=None, nullable=True)
    """The PSS property `LastHeartBeatDate` of the User as returned by the PSS API."""

    @field_validator("alliance_join_date", mode="before")
    @staticmethod
    def transform_alliance_join_date(value: Any) -> datetime:
        """Takes the value provided to set the property `alliance_join_datemake`, parses it, localizes it to UTC and then removes the timezone information.

        Args:
            value (Any): The value to set. Will be transformed, if it's of type `datetime`, `int` or `str`.

        Raises:
            ValueError: Raised, if the parsed datetime is lower than the PSS start date.

        Returns:
            Union[datetime, Any]: The transformed datetime or the original value, if it's not been transformed.
        """
        if isinstance(value, (datetime, int, str)):
            result = utils.remove_timezone(utils.localize_to_utc(utils.parse_datetime(value)))
            if result < CONSTANTS.pss_start_date:
                raise ValueError
            return utils.remove_timezone(result)
        else:
            return value

    @field_validator("last_login_date", mode="before")
    @staticmethod
    def transform_last_login_date(value: Any) -> datetime:
        """Takes the value provided to set the property `last_login_date`, parses it, localizes it to UTC and then removes the timezone information.

        Args:
            value (Any): The value to set. Will be transformed, if it's of type `datetime`, `int` or `str`.

        Raises:
            ValueError: Raised, if the parsed datetime is lower than the PSS start date.

        Returns:
            Union[datetime, Any]: The transformed datetime or the original value, if it's not been transformed.
        """
        if isinstance(value, (datetime, int, str)):
            result = utils.remove_timezone(utils.localize_to_utc(utils.parse_datetime(value)))
            if result < CONSTANTS.pss_start_date:
                raise ValueError
            return utils.remove_timezone(result)
        else:
            return value

    @field_validator("last_heartbeat_date", mode="before")
    @staticmethod
    def transform_last_heartbeat_date(value: Any) -> datetime:
        """Takes the value provided to set the property `last_heartbeat_date`, parses it, localizes it to UTC and then removes the timezone information.

        Args:
            value (Any): The value to set. Will be transformed, if it's of type `datetime`, `int` or `str`.

        Raises:
            ValueError: Raised, if the parsed datetime is lower than the PSS start date.

        Returns:
            Union[datetime, Any]: The transformed datetime or the original value, if it's not been transformed.
        """
        if isinstance(value, (datetime, int, str)):
            result = utils.remove_timezone(utils.localize_to_utc(utils.parse_datetime(value)))
            if result < CONSTANTS.pss_start_date:
                raise ValueError
            return utils.remove_timezone(result)
        else:
            return value


class UserDB(UserBaseDB, table=True):
    """A dipartial PSS User (player)."""

    __tablename__ = "pss_user"

    collection_id: int = Field(primary_key=True, index=True, foreign_key="collection.collection_id", ge=0)
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
    alliance_membership: Optional[str] = Field(default=None, nullable=True)
    """The PSS property `AllianceMembership` (fleet rank) of the User as returned by the PSS API."""
    alliance_join_date: Optional[datetime] = Field(default=None, nullable=True)
    """The PSS property `AllianceJoinDate` of the User as returned by the PSS API."""
    last_login_date: Optional[datetime] = Field(default=None, nullable=True)
    """The PSS property `LastLoginDate` of the User as returned by the PSS API."""
    last_heartbeat_date: Optional[datetime] = Field(default=None, nullable=True)
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
    championship_score: Optional[int] = Field(ge=0, default=None, nullable=True)
    """The PSS property `ChampionshipScore` of the User as returned by the PSS API."""
    highest_trophy: Optional[int] = Field(ge=0, default=None, nullable=True)
    """The PSS property `HighestTrophy` of the User as returned by the PSS API."""
    tournament_bonus_score: Optional[int] = Field(ge=0, default=None, nullable=True)
    """The PSS property `TournamentBonusScore` of the User as returned by the PSS API."""

    collection: CollectionDB = Relationship(back_populates="users", sa_relationship_kwargs={"lazy": "noload"})
    """The Collection this User data is referencing."""
    alliance: Optional[AllianceDB] = Relationship()
    """The fleet of this player."""


AllianceDB.__mapper__.add_property(
    "users",
    relationship(
        "UserDB",
        primaryjoin=and_(foreign(AllianceDB.collection_id) == UserDB.collection_id, foreign(AllianceDB.alliance_id) == UserDB.alliance_id),
        uselist=True,
        lazy="noload",
        back_populates="alliance",
        viewonly=True,
    ),
)
UserDB.__mapper__.add_property(
    "alliance",
    relationship(
        "AllianceDB",
        primaryjoin=and_(foreign(AllianceDB.collection_id) == UserDB.collection_id, foreign(AllianceDB.alliance_id) == UserDB.alliance_id),
        uselist=False,
        lazy="noload",
        back_populates="users",
        viewonly=True,
    ),
)


AllianceHistoryDB = tuple[CollectionDB, AllianceDB]
UserHistoryDB = tuple[CollectionDB, UserDB]


__all__ = [
    AllianceDB.__name__,
    AllianceHistoryDB.__name__,
    CollectionDB.__name__,
    UserDB.__name__,
    UserHistoryDB.__name__,
]
