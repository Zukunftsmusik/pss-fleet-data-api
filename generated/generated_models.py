from datetime import datetime
from typing import Annotated, Any, List, Optional, Union

from pydantic import BaseModel, Field, confloat, conint, constr


class EnumErrorCode(BaseModel):
    __root__: str = Field(..., description="A custom error code, more detailed than the HTTP status code.", examples=["INVALID_PARAMETER_VALUE"])


class EnumParamAllianceProperties(BaseModel):
    __root__: str = Field(..., description="Choose, which properties should be included in the Alliance object(s) in the response. Specify no value to have all properties returned.")


class EnumParamInterval(BaseModel):
    __root__: str = Field(..., description="Specify the interval of the data returned.", example="day")


class EnumParamMetadataProperties(BaseModel):
    __root__: str = Field(..., description="Choose, which properties should be included in the CollectionMetadata object(s) in the response. Specify no value to have all properties returned.")


class EnumParamUserProperties(BaseModel):
    __root__: str = Field(..., description="Choose, which properties should be included in the User object(s) in the response. Specify no value to have all properties returned.")


class EnumUserAllianceMembershipCreate(BaseModel):
    __root__: int = Field(..., description="A mapping of the PSS property `AllianceMembership` of the User to integer values.")


class EnumUserAllianceMembershipCreateLegacy(BaseModel):
    __root__: str = Field(..., description="The PSS property `AllianceMembership` (fleet rank) of the User as returned by the PSS API.")


class EnumUserAllianceMembershipOut(BaseModel):
    __root__: EnumUserAllianceMembershipCreateLegacy


class LinkAllianceHistoryGetAllianceById(BaseModel):
    __root__: Any = Field(
        ...,
        description="A `collectionId` value and the `allianceId` value in the response can be used as the `collectionId` and `allianceId` parameters in `GET /collections/{collectionId}/alliances/{allianceId}`.",
    )


class LinkAllianceHistoryGetUserById(BaseModel):
    __root__: Any = Field(
        ..., description="A `collectionId` value and a `userId` value in the response can be used as the `collectionId` and `userId` parameters in `GET /collections/{collectionId}/users/{userId}`."
    )


class LinkAllianceHistoryGetUserHistoryById(BaseModel):
    __root__: Any = Field(..., description="A `userId` value in the response can be used as the `userId` parameter in `GET /users/{userId}`.")


class LinkCollectionAllianceGetAllianceHistoryById(BaseModel):
    __root__: Any = Field(..., description="The `allianceId` value in the response can be used as the `allianceId` parameter in `GET /alliances/{allianceId}`.")


class LinkCollectionAllianceGetUserById(BaseModel):
    __root__: Any = Field(
        ...,
        description="The `collectionId` parameter in the path and a `userId` value in the response can be used as the `collectionId` and `userId` parameters in `GET /collections/{collectionId}/users/{userId}`.",
    )


class LinkCollectionAllianceGetUserHistoryById(BaseModel):
    __root__: Any = Field(..., description="A `userId` value in the response can be used as the `userId` parameter in `GET /users/{userId}`.")


class LinkCollectionAlliancesGetUserById(BaseModel):
    __root__: Any = Field(
        ...,
        description="The `collectionId` parameter in the path and a `userId` value in the response can be used as the `collectionId` and `userId` parameters in `GET /collections/{collectionId}/users/{userId}`.",
    )


class LinkCollectionAlliancesGetUserHistoryById(BaseModel):
    __root__: Any = Field(..., description="A `userId` value in the response can be used as the `userId` parameter in `GET /users/{userId}`.")


class LinkCollectionDeleteCollectionById(BaseModel):
    __root__: Any = Field(..., description="The `collectionId` parameter in the path can be used as the `collectionId` parameter in `DELETE /collections/{collectionId}`.")


class LinkCollectionGetAllianceById(BaseModel):
    __root__: Any = Field(
        ...,
        description="The `collectionId` parameter in the path and an `allianceId` value in the response can be used as the `collectionId` and `allianceId` parameters in `GET /collections/{collectionId}/alliances/{allianceId}`.",
    )


class LinkCollectionGetCollectionAlliances(BaseModel):
    __root__: Any = Field(..., description="The `collectionId` parameter in the path can be used as the `collectionId` parameter in `GET /collections/{collectionId}/alliances`.")


class LinkCollectionGetCollectionById(BaseModel):
    __root__: Any = Field(..., description="The `collectionId` parameter in the path can be used as the `collectionId` parameter in `GET /collections/{collectionId}`.")


class LinkCollectionGetUserById(BaseModel):
    __root__: Any = Field(
        ...,
        description="The `collectionId` parameter in the path and a `userId` value in the response can be used as the `collectionId` and `userId` parameters in `GET /collections/{collectionId}/users/{userId}`.",
    )


class LinkCollectionGetAllianceHistoryById(BaseModel):
    __root__: Any = Field(..., description="An `allianceId` value in the response can be used as the `allianceId` parameter in `GET /alliances/{allianceId}`.")


class LinkCollectionGetCollectionTop100(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/top100Users`.")


class LinkCollectionGetCollectionUsers(BaseModel):
    __root__: Any = Field(..., description="The `collectionId` parameter in the path can be used as the `collectionId` parameter in `GET /collections/{collectionId}/users`.")


class LinkCollectionGetUserHistoryById(BaseModel):
    __root__: Any = Field(..., description="A `userId` value in the response can be used as the `userId` parameter in `GET /users/{userId}`.")


class LinkCollectionUpdateCollectionById(BaseModel):
    __root__: Any = Field(..., description="The `collectionId` parameter in the path can be used as the `collectionId` parameter in `PUT /collections/{collectionId}`.")


class LinkCollectionsDeleteCollectionById(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `DELETE /collections/{collectionId}`.")


class LinkCollectionsGetCollectionAlliances(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/alliances`.")


class LinkCollectionsGetCollectionById(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}`.")


class LinkCollectionsGetCollectionTop100(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/top100Users`.")


class LinkCollectionsGetCollectionUsers(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/users`.")


class LinkCollectionsUpdateCollectionById(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `PUT /collections/{collectionId}`.")


class LinkHistoryDeleteCollectionById(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `DELETE /collections/{collectionId}`.")


class LinkHistoryGetCollectionAlliances(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/alliances`.")


class LinkHistoryGetCollectionById(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}`.")


class LinkHistoryGetCollectionTop100(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/top100Users`.")


class LinkHistoryGetCollectionUsers(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/users`.")


class LinkHistoryUpdateCollectionById(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `PUT /collections/{collectionId}`.")


class LinkCollectionUserGetAllianceById(BaseModel):
    __root__: Any = Field(
        ...,
        description="The `collectionId` parameter in the path and the `allianceId` value in the response can be used as the `collectionId` and `allianceId` parameters in `GET /collections/{collectionId}/alliances/{allianceId}`.",
    )


class LinkCollectionUserGetAllianceHistoryById(BaseModel):
    __root__: Any = Field(..., description="The `allianceId` value in the response can be used as the `allianceId` parameter in `GET /alliances/{allianceId}`.")


class LinkCollectionUsersGetAllianceById(BaseModel):
    __root__: Any = Field(
        ...,
        description="The `collectionId` parameter in the path and an `allianceId` value in the response can be used as the `collectionId` and `allianceId` parameters in `GET /collections/{collectionId}/alliances/{allianceId}`.",
    )


class LinkCollectionUsersGetAllianceHistoryById(BaseModel):
    __root__: Any = Field(..., description="An `allianceId` value in the response can be used as the `allianceId` parameter in `GET /alliances/{allianceId}`.")


class LinkCollectionUserGetUserHistoryById(BaseModel):
    __root__: Any = Field(..., description="The `userId` value in the response can be used as the `userId` parameter in `GET /users/{userId}`.")


class LinkUserHistoryGetAllianceById(BaseModel):
    __root__: Any = Field(
        ...,
        description="A `collectionId` value and an `allianceId` value in the response can be used as the `collectionId` and `allianceId` parameters in `GET /collections/{collectionId}/alliances/{allianceId}`.",
    )


class LinkUserHistoryGetAllianceHistoryById(BaseModel):
    __root__: Any = Field(..., description="An `allianceId` value in the response can be used as the `allianceId` parameter in `GET /alliances/{allianceId}`.")


class LinkUserHistoryGetUserById(BaseModel):
    __root__: Any = Field(
        ..., description="A `collectionId` value and the `userId` value in the response can be used as the `collectionId` and `userId` parameters in `GET /collections/{collectionId}/users/{userId}`."
    )


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
    __root__: EnumUserAllianceMembershipCreate


class PropUserAllianceMembershipCreateLegacy(BaseModel):
    __root__: EnumUserAllianceMembershipCreateLegacy


class PropUserAllianceMembershipOut(BaseModel):
    __root__: EnumUserAllianceMembershipOut


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


class AllianceCreate(BaseModel):
    allianceId: PropAllianceAllianceId
    allianceName: PropAllianceAllianceName
    score: PropAllianceScore
    divisionDesignId: PropAllianceDivisionDesignId
    trophy: PropAllianceTrophy
    championshipScore: Optional[PropAllianceChampionshipScore] = None
    numberOfMembers: Optional[PropAllianceNumberOfMembers] = None
    numberOfApprovedMembers: Optional[PropAllianceNumberOfApprovedMembers] = None


class AllianceUpload(BaseModel):
    __root__: List[
        Union[
            PropAllianceAllianceId,
            PropAllianceAllianceName,
            PropAllianceScore,
            PropAllianceDivisionDesignId,
            PropAllianceTrophy,
            PropAllianceChampionshipScore,
            PropAllianceNumberOfMembers,
            PropAllianceNumberOfApprovedMembers,
        ]
    ] = Field(
        ...,
        description="An array with 5, 6 or 8 elements (AllianceId, AllianceName, Score, DivisionDesignId, Trophy, optional: ChampionshipScore, optional: NumberOfMembers, optional: NumberOfApprovedMembers).",
        examples=['[43395, "Legion Basilea", 0, 0, 204370, 13, 94, 94]', '[44514, "Dynasty Savages", 0, 0, 178174, 25, 76, 74]'],
        max_items=8,
        min_items=5,
    )


class AllianceUploadArray(BaseModel):
    __root__: List[AllianceUpload] = Field(
        ...,
        description="An array of Alliance objects as denoted in a data Collection JSON file of schema version 4 or above.",
        examples=['[[43395, "Legion Basilea", 0, 0, 204370, 13, 94, 94], [44514, "Dynasty Savages", 0, 0, 178174, 25, 76, 74]]'],
        max_items=101,
        min_items=0,
    )


class CollectionMetadataOut(BaseModel):
    collectionId: PropCollectionCollectionId
    timestamp: PropCollectionTimestampOut
    duration: PropCollectionDuration
    fleetCount: PropCollectionFleetCount
    userCount: PropCollectionUserCount
    tournamentRunning: PropCollectionTournamentRunningOut
    maxTournamentBattleAttempts: Optional[PropCollectionMaxTournamentBattleAttempts] = None


class Error(BaseModel):
    code: EnumErrorCode
    message: PropErrorMessage
    details: PropErrorDetails
    timestamp: PropTimestamp
    path: PropErrorPath
    suggestion: Optional[PropErrorSuggestion] = None


class ErrorList(BaseModel):
    __root__: List[Error] = Field(..., description="A list of errors that occurred while processing the request.", max_items=100, min_items=1)


class LegacyAllianceCreate(BaseModel):
    allianceId: PropAllianceAllianceId
    allianceName: PropAllianceAllianceName
    score: PropAllianceScore
    divisionDesignId: Optional[PropAllianceDivisionDesignId] = None


class LegacyAllianceUpload(BaseModel):
    __root__: List[Union[PropAllianceAllianceIdAsString, PropAllianceAllianceName, PropAllianceScoreAsString, PropAllianceDivisionDesignIdAsString]] = Field(
        ...,
        description="An array with 3 or 4 elements (AllianceId, AllianceName, Score, optional: DivisionDesignId).",
        examples=['["5938", "Nod Imperium", "234", "1"]', '["22864", "Triad", "0"]'],
        max_items=4,
        min_items=3,
    )


class LegacyAllianceUploadArray(BaseModel):
    __root__: List[LegacyAllianceUpload] = Field(
        ...,
        description="An array of Alliance objects as denoted in a data Collection JSON file of schema version 3 or below.",
        examples=['[["22864", "Triad", "12123"], ["5938", "Nod Imperium", "2252"]]', '[["22864", "Triad", "11723", "2"], ["5938", "Nod Imperium", "1149", "3"]]'],
        max_items=101,
        min_items=0,
    )


class LegacyCollectionMetadataCreate(BaseModel):
    timestamp: PropCollectionTimestampCreateLegacy
    duration: PropCollectionDuration
    fleet_count: PropCollectionFleetCount
    user_count: PropCollectionUserCount
    tourney_running: PropCollectionTournamentRunningCreateLegacy


class LegacyDataCreate(BaseModel):
    user_id: PropUserId
    allianceId: PropUserAllianceId
    trophy: PropUserTrophy
    alliance_score: PropUserAllianceScore
    allianceMembership: PropUserAllianceMembershipCreateLegacy
    alliance_join_date: PropUserAllianceJoinDateCreateLegacy
    last_login_date: PropUserLastLoginDateCreateLegacy


class LegacyDataUpload(BaseModel):
    __root__: List[
        Union[
            PropUserIdAsString,
            PropUserAllianceIdAsString,
            PropUserTrophyAsString,
            PropUserAllianceScoreAsString,
            PropUserAllianceMembershipCreateLegacy,
            PropUserAllianceJoinDateCreateLegacy,
            PropUserLastLoginDateCreateLegacy,
        ]
    ] = Field(
        ...,
        description="An array with 7 elements (UserId, AllianceId, Trophy, AllianceScore, AllianceMembership, AllianceJoinDate, LastLoginDate).",
        examples=[
            '["876543210", "22864", "5800", "604", "Ensign", "2019-05-01T04:11:45", "2019-11-30T22:07:50"]',
            '["987654321", "13019", "5315", "1014", "Lieutenant", "1900-01-01T00:00:00", "2019-11-30T17:06:13"]',
        ],
        max_items=7,
        min_items=7,
    )


class LegacyDataUploadArray(BaseModel):
    __root__: List[LegacyDataUpload] = Field(
        ...,
        description="An array of Data objects as denoted in a data Collection JSON file of schema version 3 or below.",
        examples=[
            '[["876543210", "22864", "5800", "604", "Commander", "2019-05-01T04:11:45", "2019-11-30T22:07:50"], ["987654321", "13019", "5315", "1014", "ViceAdmiral", "1900-01-01T00:00:00", "2019-11-30T17:06:13"]]'
        ],
        max_items=10100,
        min_items=0,
    )


class LegacyUserCreate(BaseModel):
    user_id: PropUserId
    user_name: PropUserName


class LegacyUserUpload(BaseModel):
    __root__: List[Union[PropUserIdAsString, PropUserName]] = Field(
        ..., description="An array with 2 elements (Id, Name).", examples=['["876543210", "Some username"]', '["987654321", "Some other name"]'], max_items=2, min_items=2
    )


class LegacyUserUploadArray(BaseModel):
    __root__: List[LegacyUserUpload] = Field(
        ...,
        description="An array of User objects as denoted in a data Collection JSON file of schema version 3 or below.",
        examples=['[["876543210", "Some username"], ["987654321", "Some other name"]]'],
        max_items=10100,
        min_items=0,
    )


class UserCreate(BaseModel):
    userId: PropUserId
    userName: PropUserName
    allianceId: PropUserAllianceId
    trophy: PropUserTrophy
    allianceScore: PropUserAllianceScore
    allianceMembership: PropUserAllianceMembershipCreate
    allianceJoinDate: PropUserAllianceJoinDateCreate
    lastLoginDate: PropUserLastLoginDateCreate
    lastHeartBeatDate: PropUserLastHeartBeatDateCreate
    crewDonated: PropUserCrewDonated
    crewReceived: PropUserCrewReceived
    pvpAttackWins: PropUserPvpAttackWins
    pvpAttackLosses: PropUserPvpAttackLosses
    pvpAttackDraws: PropUserPvpAttackDraws
    pvpDefenceWins: PropUserPvpDefenceWins
    pvpDefenceLosses: PropUserPvpDefenceLosses
    pvpDefenceDraws: PropUserPvpDefenceDraws
    championshipScore: Optional[PropUserChampionshipScore] = None
    highestTrophy: Optional[PropUserHighestTrophy] = None
    tournamentBonusScore: Optional[PropUserTournamentBonusScore] = None


class UserUpload(BaseModel):
    __root__: List[
        Union[
            PropUserIdAsString,
            PropUserName,
            PropUserAllianceId,
            PropUserTrophy,
            PropUserAllianceScore,
            PropUserAllianceMembershipCreate,
            PropUserAllianceJoinDateCreate,
            PropUserLastLoginDateCreate,
            PropUserLastHeartBeatDateCreate,
            PropUserCrewDonated,
            PropUserCrewReceived,
            PropUserPvpAttackWins,
            PropUserPvpAttackLosses,
            PropUserPvpAttackDraws,
            PropUserPvpDefenceWins,
            PropUserPvpDefenceLosses,
            PropUserPvpDefenceDraws,
            PropUserChampionshipScore,
            PropUserHighestTrophy,
            PropUserTournamentBonusScore,
        ]
    ] = Field(
        ...,
        description="An array with 17, 18, 19 or 20 elements (Id, Name, AllianceId, Trophy, AllianceScore, AllianceMembership, AllianceJoinDate, LastoginDate, LastHeartBeatDate, CrewDonated, CrewReceived, PVPAttackWins, PVPAttackLosses, PVPAttackDraws, PVPDefenceWins, PVPDefenceLosses, PVPDefenceDraws, optional: ChampionshipScore, optional: HighestTrophy, optional: TournamentBonusScore).",
        examples=[
            '[876543210, "Some username", 43801, 4847, 0, 4, 191925293, 265343984, 265344565, 3339, 3178, 4764, 447, 61, 241, 729, 9, 0, 5000, 0]',
            '[987654321, "Some other name", 43801, 4836, 0, 5, 210719841, 264613066, 264614336, 498, 1096, 5165, 235, 4, 500, 3323, 11, 0, 4885, 0]',
        ],
        max_items=20,
        min_items=17,
    )


class UserUploadArray(BaseModel):
    __root__: List[UserUpload] = Field(
        ...,
        description="An array of User objects as denoted in a data Collection JSON file of schema version 4 or above.",
        examples=[
            '[[876543210, "Some username", 43801, 4847, 0, 4, 191925293, 265343984, 265344565, 3339, 3178, 4764, 447, 61, 241, 729, 9, 0, 5000, 0], [987654321, "Some other name", 43801, 4836, 0, 5, 210719841, 264613066, 264614336, 498, 1096, 5165, 235, 4, 500, 3323, 11, 0, 4885, 0]]'
        ],
        max_items=10100,
        min_items=0,
    )


class PropCollectionTimestampCreate(BaseModel):
    __root__: PropCollectionTimestampCreateLegacy


class CollectionMetadataCreate(BaseModel):
    timestamp: PropCollectionTimestampCreate
    duration: PropCollectionDuration
    fleetCount: Optional[PropCollectionFleetCount] = None
    userCount: Optional[PropCollectionUserCount] = None
    tourneyRunning: Optional[PropCollectionTimestampCreate] = None
    maxTournamentBattleAttempts: Optional[PropCollectionMaxTournamentBattleAttempts] = None
    schemaVersion: Optional[PropCollectionSchemaVersion] = None


class CollectionMetadataUpload(BaseModel):
    timestamp: PropCollectionTimestampCreate
    duration: PropCollectionDuration
    fleet_count: PropCollectionFleetCount
    user_count: PropCollectionUserCount
    tourney_running: PropCollectionTimestampCreate
    max_tournament_battle_attempts: Optional[PropCollectionMaxTournamentBattleAttempts] = None
    schema_version: PropCollectionSchemaVersion


class CollectionUpload(BaseModel):
    meta: Optional[CollectionMetadataUpload] = None
    fleets: AllianceUploadArray
    users: UserUploadArray


class LegacyCollectionCreate(BaseModel):
    metadata: LegacyCollectionMetadataCreate
    alliances: List[LegacyAllianceCreate] = Field(..., description="A list of partial PSS Alliances.", max_items=101, min_items=0)
    users: List[LegacyUserCreate] = Field(..., description="A list of partial PSS Users.", max_items=10100, min_items=0)
    data: List[LegacyDataCreate] = Field(..., description="A list of Users' data.", max_items=10100, min_items=0)


class LegacyCollectionMetadataUpload(BaseModel):
    timestamp: PropCollectionTimestampCreate
    duration: PropCollectionDuration
    fleet_count: PropCollectionFleetCount
    user_count: PropCollectionUserCount
    tourney_running: PropCollectionTimestampCreate
    max_tournament_battle_attempts: Optional[PropCollectionMaxTournamentBattleAttempts] = None
    schema_version: PropCollectionSchemaVersion


class LegacyCollectionUpload(BaseModel):
    meta: LegacyCollectionMetadataUpload
    fleets: LegacyAllianceUploadArray
    users: LegacyUserUploadArray
    data: LegacyDataUploadArray


class CollectionCreate(BaseModel):
    metadata: CollectionMetadataCreate
    alliances: List[AllianceCreate] = Field(..., description="A list of partial PSS Alliances.", max_items=101, min_items=0)
    users: List[UserCreate] = Field(..., description="A list of partial PSS Users.", max_items=10100, min_items=0)


class AllianceHistoryOut(BaseModel):
    collection: CollectionMetadataOut
    alliance: "AllianceOut"


class AllianceOut(BaseModel):
    allianceId: PropAllianceAllianceId
    allianceName: PropAllianceAllianceName
    score: PropAllianceScore
    divisionDesignId: PropAllianceDivisionDesignId
    trophy: PropAllianceTrophy
    championshipScore: Optional[PropAllianceChampionshipScore] = None
    numberOfMembers: Optional[PropAllianceNumberOfMembers] = None
    numberOfApprovedMembers: Optional[PropAllianceNumberOfApprovedMembers] = None
    allianceMembers: List["UserOut"] = Field(..., description="A list of Users that were members of the Alliance at the time of the Collection.", max_items=100, min_items=0, unique_items=True)


class CollectionOut(BaseModel):
    metadata: CollectionMetadataOut
    alliances: List[AllianceOut] = Field(..., description="A list of partial PSS Alliances.", max_items=101, min_items=0)
    users: List["UserOut"] = Field(..., description="A list of partial PSS Users.", max_items=10100, min_items=0)


class UserHistoryOut(BaseModel):
    collection: CollectionMetadataOut
    user: "UserOut"


class UserOut(BaseModel):
    userId: PropUserId
    userName: PropUserName
    allianceId: PropUserAllianceId
    trophy: PropUserTrophy
    allianceScore: PropUserAllianceScore
    allianceMembership: PropUserAllianceMembershipOut
    allianceJoinDate: PropUserAllianceJoinDateOut
    lastLoginDate: PropUserLastLoginDateOut
    lastHeartBeatDate: PropUserLastHeartBeatDateOut
    crewDonated: PropUserCrewDonated
    crewReceived: PropUserCrewReceived
    pvpAttackWins: PropUserPvpAttackWins
    pvpAttackLosses: PropUserPvpAttackLosses
    pvpAttackDraws: PropUserPvpAttackDraws
    pvpDefenceWins: PropUserPvpDefenceWins
    pvpDefenceLosses: PropUserPvpDefenceLosses
    pvpDefenceDraws: PropUserPvpDefenceDraws
    championshipScore: Optional[PropUserChampionshipScore] = None
    highestTrophy: Optional[PropUserHighestTrophy] = None
    tournamentAttemptsLeft: Optional[PropUserTournamentAttemptsLeftOut] = None
    alliance: Optional[AllianceOut] = None
