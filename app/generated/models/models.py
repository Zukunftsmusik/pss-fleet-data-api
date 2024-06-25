from typing import List, Optional, Tuple, Union

from pydantic import BaseModel, Field

from . import enums
from . import properties as properties


class AllianceCreate(BaseModel):
    allianceId: properties.PropAllianceAllianceId
    allianceName: properties.PropAllianceAllianceName
    score: properties.PropAllianceScore
    divisionDesignId: properties.PropAllianceDivisionDesignId
    trophy: properties.PropAllianceTrophy
    championshipScore: Optional[properties.PropAllianceChampionshipScore] = None
    numberOfMembers: Optional[properties.PropAllianceNumberOfMembers] = None
    numberOfApprovedMembers: Optional[properties.PropAllianceNumberOfApprovedMembers] = None


class AllianceUpload(BaseModel):
    """An array with 5, 6 or 8 elements (AllianceId, AllianceName, Score, DivisionDesignId, Trophy, optional: ChampionshipScore, optional: NumberOfMembers, optional: NumberOfApprovedMembers)."""

    __root__: Tuple[
        properties.PropAllianceAllianceId,
        properties.PropAllianceAllianceName,
        properties.PropAllianceScore,
        properties.PropAllianceDivisionDesignId,
        properties.PropAllianceTrophy,
        properties.PropAllianceChampionshipScore,
        properties.PropAllianceNumberOfMembers,
        properties.PropAllianceNumberOfApprovedMembers,
    ] = Field(
        ...,
        description="An array with 5, 6 or 8 elements (AllianceId, AllianceName, Score, DivisionDesignId, Trophy, optional: ChampionshipScore, optional: NumberOfMembers, optional: NumberOfApprovedMembers).",
        examples=['[43395, "Legion Basilea", 0, 0, 204370, 13, 94, 94]', '[44514, "Dynasty Savages", 0, 0, 178174, 25, 76, 74]'],
        max_items=8,
        min_items=5,
    )


class AllianceUploadArray(BaseModel):
    """An array of Alliance objects as denoted in a data Collection JSON file of schema version 4 or above."""

    __root__: List[AllianceUpload] = Field(
        ...,
        description="An array of Alliance objects as denoted in a data Collection JSON file of schema version 4 or above.",
        examples=['[[43395, "Legion Basilea", 0, 0, 204370, 13, 94, 94], [44514, "Dynasty Savages", 0, 0, 178174, 25, 76, 74]]'],
        max_items=101,
        min_items=0,
    )


class CollectionMetadataOut(BaseModel):
    collectionId: properties.PropCollectionCollectionId
    timestamp: properties.PropCollectionTimestampOut
    duration: properties.PropCollectionDuration
    fleetCount: properties.PropCollectionFleetCount
    userCount: properties.PropCollectionUserCount
    tournamentRunning: properties.PropCollectionTournamentRunningOut
    maxTournamentBattleAttempts: Optional[properties.PropCollectionMaxTournamentBattleAttempts] = None


class Error(BaseModel):
    code: enums.ErrorCode
    message: properties.PropErrorMessage
    details: properties.PropErrorDetails
    timestamp: properties.PropTimestamp
    path: properties.PropErrorPath
    suggestion: Optional[properties.PropErrorSuggestion] = None


class ErrorList(BaseModel):
    """A list of errors that occurred while processing the request."""

    __root__: List[Error] = Field(..., description="A list of errors that occurred while processing the request.", max_items=100, min_items=1)


class LegacyAllianceCreate(BaseModel):
    allianceId: properties.PropAllianceAllianceId
    allianceName: properties.PropAllianceAllianceName
    score: properties.PropAllianceScore
    divisionDesignId: Optional[properties.PropAllianceDivisionDesignId] = None


class LegacyAllianceUpload(BaseModel):
    """An array with 3 or 4 elements (AllianceId, AllianceName, Score, optional: DivisionDesignId)."""

    __root__: List[Union[properties.PropAllianceAllianceIdAsString, properties.PropAllianceAllianceName, properties.PropAllianceScoreAsString, properties.PropAllianceDivisionDesignIdAsString]] = (
        Field(
            ...,
            description="An array with 3 or 4 elements (AllianceId, AllianceName, Score, optional: DivisionDesignId).",
            examples=['["5938", "Nod Imperium", "234", "1"]', '["22864", "Triad", "0"]'],
            max_items=4,
            min_items=3,
        )
    )


class LegacyAllianceUploadArray(BaseModel):
    """An array of Alliance objects as denoted in a data Collection JSON file of schema version 3 or below."""

    __root__: List[LegacyAllianceUpload] = Field(
        ...,
        description="An array of Alliance objects as denoted in a data Collection JSON file of schema version 3 or below.",
        examples=['[["22864", "Triad", "12123"], ["5938", "Nod Imperium", "2252"]]', '[["22864", "Triad", "11723", "2"], ["5938", "Nod Imperium", "1149", "3"]]'],
        max_items=101,
        min_items=0,
    )


class LegacyCollectionMetadataCreate(BaseModel):
    timestamp: properties.PropCollectionTimestampCreateLegacy
    duration: properties.PropCollectionDuration
    fleet_count: properties.PropCollectionFleetCount
    user_count: properties.PropCollectionUserCount
    tourney_running: properties.PropCollectionTournamentRunningCreateLegacy


class LegacyDataCreate(BaseModel):
    user_id: properties.PropUserId
    allianceId: properties.PropUserAllianceId
    trophy: properties.PropUserTrophy
    alliance_score: properties.PropUserAllianceScore
    allianceMembership: properties.PropUserAllianceMembershipCreateLegacy
    alliance_join_date: properties.PropUserAllianceJoinDateCreateLegacy
    last_login_date: properties.PropUserLastLoginDateCreateLegacy


class LegacyDataUpload(BaseModel):
    """An array with 7 elements (UserId, AllianceId, Trophy, AllianceScore, AllianceMembership, AllianceJoinDate, LastLoginDate)."""

    __root__: List[
        Union[
            properties.PropUserIdAsString,
            properties.PropUserAllianceIdAsString,
            properties.PropUserTrophyAsString,
            properties.PropUserAllianceScoreAsString,
            properties.PropUserAllianceMembershipCreateLegacy,
            properties.PropUserAllianceJoinDateCreateLegacy,
            properties.PropUserLastLoginDateCreateLegacy,
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
    """An array of Data objects as denoted in a data Collection JSON file of schema version 3 or below."""

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
    user_id: properties.PropUserId
    user_name: properties.PropUserName


class LegacyUserUpload(BaseModel):
    """An array with 2 elements (Id, Name)."""

    __root__: Tuple[properties.PropUserIdAsString, properties.PropUserName] = Field(
        ..., description="An array with 2 elements (Id, Name).", examples=['["876543210", "Some username"]', '["987654321", "Some other name"]'], max_items=2, min_items=2
    )


class LegacyUserUploadArray(BaseModel):
    """An array of User objects as denoted in a data Collection JSON file of schema version 3 or below."""

    __root__: List[LegacyUserUpload] = Field(
        ...,
        description="An array of User objects as denoted in a data Collection JSON file of schema version 3 or below.",
        examples=['[["876543210", "Some username"], ["987654321", "Some other name"]]'],
        max_items=10100,
        min_items=0,
    )


class UserCreate(BaseModel):
    userId: properties.PropUserId
    userName: properties.PropUserName
    allianceId: properties.PropUserAllianceId
    trophy: properties.PropUserTrophy
    allianceScore: properties.PropUserAllianceScore
    allianceMembership: properties.PropUserAllianceMembershipCreate
    allianceJoinDate: properties.PropUserAllianceJoinDateCreate
    lastLoginDate: properties.PropUserLastLoginDateCreate
    lastHeartBeatDate: properties.PropUserLastHeartBeatDateCreate
    crewDonated: properties.PropUserCrewDonated
    crewReceived: properties.PropUserCrewReceived
    pvpAttackWins: properties.PropUserPvpAttackWins
    pvpAttackLosses: properties.PropUserPvpAttackLosses
    pvpAttackDraws: properties.PropUserPvpAttackDraws
    pvpDefenceWins: properties.PropUserPvpDefenceWins
    pvpDefenceLosses: properties.PropUserPvpDefenceLosses
    pvpDefenceDraws: properties.PropUserPvpDefenceDraws
    championshipScore: Optional[properties.PropUserChampionshipScore] = None
    highestTrophy: Optional[properties.PropUserHighestTrophy] = None
    tournamentBonusScore: Optional[properties.PropUserTournamentBonusScore] = None


class UserUpload(BaseModel):
    """An array with 17, 18, 19 or 20 elements (Id, Name, AllianceId, Trophy, AllianceScore, AllianceMembership, AllianceJoinDate, LastoginDate, LastHeartBeatDate, CrewDonated, CrewReceived, PVPAttackWins, PVPAttackLosses, PVPAttackDraws, PVPDefenceWins, PVPDefenceLosses, PVPDefenceDraws, optional: ChampionshipScore, optional: HighestTrophy, optional: TournamentBonusScore)."""

    __root__: Tuple[
        properties.PropUserIdAsString,
        properties.PropUserName,
        properties.PropUserAllianceId,
        properties.PropUserTrophy,
        properties.PropUserAllianceScore,
        properties.PropUserAllianceMembershipCreate,
        properties.PropUserAllianceJoinDateCreate,
        properties.PropUserLastLoginDateCreate,
        properties.PropUserLastHeartBeatDateCreate,
        properties.PropUserCrewDonated,
        properties.PropUserCrewReceived,
        properties.PropUserPvpAttackWins,
        properties.PropUserPvpAttackLosses,
        properties.PropUserPvpAttackDraws,
        properties.PropUserPvpDefenceWins,
        properties.PropUserPvpDefenceLosses,
        properties.PropUserPvpDefenceDraws,
        properties.PropUserChampionshipScore,
        properties.PropUserHighestTrophy,
        properties.PropUserTournamentBonusScore,
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
    """An array of User objects as denoted in a data Collection JSON file of schema version 4 or above."""

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
    __root__: properties.PropCollectionTimestampCreateLegacy


class CollectionMetadataCreate(BaseModel):
    timestamp: PropCollectionTimestampCreate
    duration: properties.PropCollectionDuration
    fleetCount: Optional[properties.PropCollectionFleetCount] = None
    userCount: Optional[properties.PropCollectionUserCount] = None
    tourneyRunning: Optional[PropCollectionTimestampCreate] = None
    maxTournamentBattleAttempts: Optional[properties.PropCollectionMaxTournamentBattleAttempts] = None
    schemaVersion: Optional[properties.PropCollectionSchemaVersion] = None


class CollectionMetadataUpload(BaseModel):
    timestamp: PropCollectionTimestampCreate
    duration: properties.PropCollectionDuration
    fleet_count: properties.PropCollectionFleetCount
    user_count: properties.PropCollectionUserCount
    tourney_running: PropCollectionTimestampCreate
    max_tournament_battle_attempts: Optional[properties.PropCollectionMaxTournamentBattleAttempts] = None
    schema_version: properties.PropCollectionSchemaVersion


class CollectionUpload(BaseModel):
    meta: Optional[CollectionMetadataUpload] = None
    fleets: AllianceUploadArray
    users: UserUploadArray


class LegacyCollectionCreate(BaseModel):
    metadata: LegacyCollectionMetadataCreate
    alliances: List[LegacyAllianceCreate] = Field(..., description="A list of partial PSS Alliances.", max_items=101, min_items=0)
    """A list of partial PSS Alliances."""
    users: List[LegacyUserCreate] = Field(..., description="A list of partial PSS Users.", max_items=10100, min_items=0)
    """A list of partial PSS Users."""
    data: List[LegacyDataCreate] = Field(..., description="A list of Users' data.", max_items=10100, min_items=0)
    """A list of Users' data."""


class LegacyCollectionMetadataUpload(BaseModel):
    timestamp: PropCollectionTimestampCreate
    duration: properties.PropCollectionDuration
    fleet_count: properties.PropCollectionFleetCount
    user_count: properties.PropCollectionUserCount
    tourney_running: PropCollectionTimestampCreate
    max_tournament_battle_attempts: Optional[properties.PropCollectionMaxTournamentBattleAttempts] = None
    schema_version: properties.PropCollectionSchemaVersion


class LegacyCollectionUpload(BaseModel):
    meta: LegacyCollectionMetadataUpload
    fleets: LegacyAllianceUploadArray
    users: LegacyUserUploadArray
    data: LegacyDataUploadArray


class CollectionCreate(BaseModel):
    metadata: CollectionMetadataCreate
    alliances: List[AllianceCreate] = Field(..., description="A list of partial PSS Alliances.", max_items=101, min_items=0)
    """A list of partial PSS Alliances."""
    users: List[UserCreate] = Field(..., description="A list of partial PSS Users.", max_items=10100, min_items=0)
    """A list of partial PSS Users."""


class AllianceHistoryOut(BaseModel):
    collection: CollectionMetadataOut
    alliance: "AllianceOut"


class AllianceOut(BaseModel):
    allianceId: properties.PropAllianceAllianceId
    allianceName: properties.PropAllianceAllianceName
    score: properties.PropAllianceScore
    divisionDesignId: properties.PropAllianceDivisionDesignId
    trophy: properties.PropAllianceTrophy
    championshipScore: Optional[properties.PropAllianceChampionshipScore] = None
    numberOfMembers: Optional[properties.PropAllianceNumberOfMembers] = None
    numberOfApprovedMembers: Optional[properties.PropAllianceNumberOfApprovedMembers] = None
    allianceMembers: List["UserOut"] = Field(..., description="A list of Users that were members of the Alliance at the time of the Collection.", max_items=100, min_items=0, unique_items=True)
    """A list of Users that were members of the Alliance at the time of the Collection."""


class CollectionOut(BaseModel):
    metadata: CollectionMetadataOut
    alliances: List[AllianceOut] = Field(..., description="A list of partial PSS Alliances.", max_items=101, min_items=0)
    """A list of partial PSS Alliances."""
    users: List["UserOut"] = Field(..., description="A list of partial PSS Users.", max_items=10100, min_items=0)
    """A list of partial PSS Users."""


class UserHistoryOut(BaseModel):
    collection: CollectionMetadataOut
    user: "UserOut"


class UserOut(BaseModel):
    userId: properties.PropUserId
    userName: properties.PropUserName
    allianceId: properties.PropUserAllianceId
    trophy: properties.PropUserTrophy
    allianceScore: properties.PropUserAllianceScore
    allianceMembership: properties.PropUserAllianceMembershipOut
    allianceJoinDate: properties.PropUserAllianceJoinDateOut
    lastLoginDate: properties.PropUserLastLoginDateOut
    lastHeartBeatDate: properties.PropUserLastHeartBeatDateOut
    crewDonated: properties.PropUserCrewDonated
    crewReceived: properties.PropUserCrewReceived
    pvpAttackWins: properties.PropUserPvpAttackWins
    pvpAttackLosses: properties.PropUserPvpAttackLosses
    pvpAttackDraws: properties.PropUserPvpAttackDraws
    pvpDefenceWins: properties.PropUserPvpDefenceWins
    pvpDefenceLosses: properties.PropUserPvpDefenceLosses
    pvpDefenceDraws: properties.PropUserPvpDefenceDraws
    championshipScore: Optional[properties.PropUserChampionshipScore] = None
    highestTrophy: Optional[properties.PropUserHighestTrophy] = None
    tournamentAttemptsLeft: Optional[properties.PropUserTournamentAttemptsLeftOut] = None
    alliance: Optional[AllianceOut] = None
