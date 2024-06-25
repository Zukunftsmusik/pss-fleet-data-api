from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field, confloat, conint, constr

from .enums import *


class PropAllianceAllianceId(BaseModel):
    __root__: Annotated[int, conint(ge=0, le=2147483647)] = Field(..., description="The PSS property `AllianceId` of the Alliance as returned by the PSS API.", examples=[9343])


class PropAllianceAllianceIdAsString(BaseModel):
    __root__: Annotated[str, constr(regex=r"^\d{1,10}$", min_length=1, max_length=10)] = Field(
        ..., description="The PSS property `AllianceId` of the Alliance as returned by the PSS API. Must represent a non-negative 32 bit integer value.", examples=["9343"]
    )


class PropAllianceAllianceName(BaseModel):
    __root__: Annotated[str, constr(min_length=1, max_length=16)] = Field(..., description="The PSS property `AllianceName` of the Alliance as returned by the PSS API.", examples=["Trek Federation"])


class PropAllianceChampionshipScore(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="The PSS property `ChampionshipScore` of the Alliance as returned by the PSS API.", examples=[280])


class PropAllianceDivisionDesignId(BaseModel):
    __root__: Annotated[int, conint(ge=0, le=2147483647)] = Field(..., description="The PSS property `DivisionDesignId` of the Alliance as returned by the PSS API.", examples=[1])


class PropAllianceDivisionDesignIdAsString(BaseModel):
    __root__: Annotated[str, constr(regex=r"^\d{1,10}$", min_length=1, max_length=10)] = Field(
        ...,
        description="The PSS property `DivisionDesignId` of the Alliance as returned by the PSS API.  Must represent a non-negative 32 bit integer value. Might not be present at all in any of the Alliances.",
        examples=["1"],
    )


class PropAllianceNumberOfMembers(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=100)]] = Field(None, description="The PSS property `NumberOfMembers` of the Alliance as returned by the PSS API.", examples=[95])


class PropAllianceNumberOfApprovedMembers(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=100)]] = Field(None, description="The PSS property `NumberOfApprovedMembers` of the Alliance as returned by the PSS API.", examples=[94])


class PropAllianceScore(BaseModel):
    __root__: Annotated[int, conint(ge=0, le=2147483647)] = Field(..., description="The PSS property `Score` (stars) of the Alliance as returned by the PSS API.", examples=[21242])


class PropAllianceScoreAsString(BaseModel):
    __root__: Annotated[str, constr(regex=r"^\d{1,10}$", min_length=1, max_length=10)] = Field(
        ..., description="The PSS property `Score` (stars) of the Alliance as returned by the PSS API. Must represent a non-negative 32 bit integer value.", examples=["21242"]
    )


class PropAllianceTrophy(BaseModel):
    __root__: Annotated[int, conint(ge=0, le=2147483647)] = Field(..., description="The PSS property `Trophy` of the Alliance as returned by the PSS API.", examples=[506276])


class PropCollectionCollectionId(BaseModel):
    __root__: Annotated[int, conint(ge=0, le=9223372036854776000)] = Field(..., description="The ID of the Collection.", examples=[1])


class PropCollectionDuration(BaseModel):
    __root__: Annotated[float, confloat(ge=0.0, le=3600.0)] = Field(..., description="The duration of the Collection run in seconds.", examples=[1.2])


class PropCollectionFleetCount(BaseModel):
    __root__: Annotated[int, conint(ge=0, le=101)] = Field(..., description="The number of Alliances (fleets) in this Collection.", examples=[100])


class PropCollectionMaxTournamentBattleAttempts(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(
        None, description="The maximum number of daily tournament battle attempts at the time of retrieving the data.", examples=[6]
    )


class PropCollectionSchemaVersion(BaseModel):
    __root__: Annotated[int, conint(ge=4, le=9)] = Field(..., description="The schema version of the data in this Collection.", examples=[9])


class PropCollectionTimestampCreateLegacy(BaseModel):
    __root__: datetime = Field(
        ..., description="The date and time when the data was retrieved from the PSS API. If no timezone information is given, UTC is assumed.", examples=["2024-02-29 23:59:00"]
    )


class PropCollectionTimestampOut(BaseModel):
    __root__: PropCollectionTimestampCreateLegacy


class PropCollectionTournamentRunningCreate(BaseModel):
    __root__: bool = Field(..., description="Determines, if the monthly tournament was running at the time of retrieving the data.", examples=[True])


class PropCollectionTournamentRunningCreateLegacy(BaseModel):
    __root__: PropCollectionTournamentRunningCreate


class PropCollectionTournamentRunningOut(BaseModel):
    __root__: bool = Field(..., description="Determines, if the monthly tournament was running at the time of retrieving the data.", examples=[True])


class PropCollectionUserCount(BaseModel):
    __root__: Annotated[int, conint(ge=0, le=10100)] = Field(..., description="The number of Users (players) in this Collection.", examples=[8123])


class PropErrorMessage(BaseModel):
    __root__: Annotated[str, constr(min_length=1, max_length=512)] = Field(..., description="An error message matching the code.", examples=["The parameter 'from' has received an invalid value."])


class PropErrorDetails(BaseModel):
    __root__: Annotated[str, constr(min_length=1, max_length=10000)] = Field(..., description="A detailed error message.", examples=["The parameter 'from' must not be in the future."])


class PropErrorPath(BaseModel):
    __root__: Annotated[str, constr(min_length=1, max_length=512)] = Field(..., description="The API path that returned the error.", examples=["/alliances/{allianceId}"])


class PropErrorSuggestion(BaseModel):
    __root__: Optional[Annotated[str, constr(min_length=1, max_length=10000)]] = Field(
        None, description="A suggestion for the client on how to fix the error.", examples=["Specify a date and time in the past."]
    )


class PropUserAllianceId(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="The PSS property `AllianceId` of the User as returned by the PSS API.", examples=[21])


class PropUserAllianceIdAsString(BaseModel):
    __root__: Optional[Annotated[str, constr(regex=r"^\d{1,10}$", min_length=1, max_length=10)]] = Field(
        None, description="The PSS property `AllianceId` of the User as returned by the PSS API. Must represent a non-negative 32 bit integer value.", examples=["21"]
    )


class PropUserAllianceJoinDateCreate(BaseModel):
    __root__: Annotated[int, conint(ge=0, le=9223372036854776000)] = Field(
        ..., description="The PSS property `AllianceJoinDate` of the User converted to the number of seconds since Jan 6th, 2016 (start date of PSS).", examples=[252885827]
    )


class PropUserAllianceJoinDateCreateLegacy(BaseModel):
    __root__: Optional[datetime] = Field(
        None, description="The PSS property `AllianceJoinDate` of the User as returned by the PSS API. If no timezone information is given, UTC is assumed.", examples=["2019-09-28T02:19:46"]
    )


class PropUserAllianceJoinDateOut(BaseModel):
    __root__: Optional[datetime] = Field(
        None, description="The PSS property `AllianceJoinDate` of the User as returned by the PSS API. If no timezone information is given, UTC is assumed.", examples=["2019-09-28T02:19:46Z"]
    )


class PropUserAllianceMembershipCreate(BaseModel):
    __root__: UserCreateAllianceMembership


class PropUserAllianceMembershipCreateLegacy(BaseModel):
    __root__: UserAllianceMembership


class PropUserAllianceMembershipOut(BaseModel):
    __root__: UserAllianceMembership


class PropUserAllianceScore(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="The PSS property `AllianceScore` (stars) of the User as returned by the PSS API.", examples=[270])


class PropUserAllianceScoreAsString(BaseModel):
    __root__: Optional[Annotated[str, constr(regex=r"^\d{1,10}$", min_length=1, max_length=10)]] = Field(
        None, description="The PSS property `AllianceScore` (stars) of the User as returned by the PSS API.", examples=["270"]
    )


class PropUserChampionshipScore(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="The PSS property `ChampionshipScore` of the User as returned by the PSS API.", examples=[240])


class PropUserCrewDonated(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="The PSS property `CrewDonated` of the User as returned by the PSS API.", examples=[456])


class PropUserCrewReceived(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="The PSS property `CrewReceived` of the User as returned by the PSS API.", examples=[183])


class PropUserHighestTrophy(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="The PSS property `HighestTrophy` of the User as returned by the PSS API.", examples=[5000])


class PropUserId(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="The PSS property `Id` of the User as returned by the PSS API.", examples=[876543210])


class PropUserIdAsString(BaseModel):
    __root__: Optional[Annotated[str, constr(regex=r"^\d{1,10}$", min_length=1, max_length=10)]] = Field(
        None, description="The PSS property `Id` of the User as returned by the PSS API. Must represent a non-negative 32 bit integer value.", examples=["876543210"]
    )


class PropUserLastHeartBeatDateCreate(BaseModel):
    __root__: Annotated[int, conint(ge=0, le=9223372036854776000)] = Field(
        ..., description="The PSS property `LastHeartBeatDate` of the User converted to the number of seconds since Jan 6th, 2016 (start date of PSS).", examples=[252885827]
    )


class PropUserLastHeartBeatDateOut(BaseModel):
    __root__: Optional[datetime] = Field(
        None, description="The PSS property `LastHeartBeatDate` of the User as returned by the PSS API. If no timezone information is given, UTC is assumed.", examples=["2019-09-28T02:19:46Z"]
    )


class PropUserLastLoginDateCreate(BaseModel):
    __root__: Annotated[int, conint(ge=0, le=9223372036854776000)] = Field(
        ..., description="The PSS property `LastLoginDate` of the User converted to the number of seconds since Jan 6th, 2016 (start date of PSS).", examples=[252885827]
    )


class PropUserLastLoginDateCreateLegacy(BaseModel):
    __root__: Optional[datetime] = Field(
        None, description="The PSS property `LastLoginDate` of the User as returned by the PSS API. If no timezone information is given, UTC is assumed.", examples=["2019-09-28T02:19:46"]
    )


class PropUserLastLoginDateOut(BaseModel):
    __root__: PropUserLastLoginDateCreateLegacy


class PropUserName(BaseModel):
    __root__: Optional[Annotated[str, constr(min_length=1, max_length=16)]] = Field(None, description="The PSS property `Name` of the User as returned by the PSS API.", examples=["The worst."])


class PropUserPvpAttackDraws(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="The PSS property `PVPAttackWins` of the User as returned by the PSS API.", examples=[4])


class PropUserPvpAttackLosses(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="The PSS property `PVPAttackLosses` of the User as returned by the PSS API.", examples=[583])


class PropUserPvpAttackWins(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="The PSS property `PVPAttackWins` of the User as returned by the PSS API.", examples=[7114])


class PropUserPvpDefenceDraws(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="The PSS property `PVPDefenceDrawss` of the User as returned by the PSS API.", examples=[18])


class PropUserPvpDefenceLosses(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="The PSS property `PVPDefenceLosses` of the User as returned by the PSS API.", examples=[4125])


class PropUserPvpDefenceWins(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="The PSS property `PVPDefenceWins` of the User as returned by the PSS API.", examples=[848])


class PropUserTournamentAttemptsLeftOut(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="A calculated property based on the PSS property `TournamentBonusScore` of the User.", examples=[1])


class PropUserTournamentBonusScore(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="The PSS property `TournamentBonusScore` of the User as returned by the PSS API.", examples=[1])


class PropUserTrophy(BaseModel):
    __root__: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Field(None, description="The PSS property `Trophy` of the User as returned by the PSS API.", examples=[1000])


class PropUserTrophyAsString(BaseModel):
    __root__: Optional[Annotated[str, constr(regex=r"^\d{1,10}$", min_length=1, max_length=10)]] = Field(
        None, description="The PSS property `Trophy` of the User as returned by the PSS API.", examples=["1000"]
    )


class PropTimestamp(BaseModel):
    __root__: Optional[datetime] = Field(None, description="An ISO 8601 timestamp with timezone information.", examples=["2019-09-28T02:19:46Z"])
