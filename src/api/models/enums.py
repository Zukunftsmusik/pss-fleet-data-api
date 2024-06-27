from enum import IntEnum, StrEnum


class ErrorCode(StrEnum):
    DUPLICATE_COLLECTION = "DUPLICATE_COLLECTION"
    """A collection with this timestamp already exists."""
    INVALID_PARAMETER_FORMAT = "INVALID_PARAMETER_FORMAT"
    """A parameter is not of the expected type representation. Check the error message and description for more details."""
    PARAMETER_OUT_OF_BOUNDS = "PARAMETER_OUT_OF_BOUNDS"
    """A parameter value is not within the expected range. Check the error message and description for more details."""
    INVALID_PARAMETER_VALUE = "INVALID_PARAMETER_VALUE"
    """A parameter received an invalid value. Check the error message and description for more details."""
    INVALID_PARAMETER_VALUES = "INVALID_PARAMETER_VALUES"
    """Two or more parameters received an invalid value. Check the error message and description for more details."""


class ParameterAllianceProperties(StrEnum):
    ALLIANCE_ID = "allianceId"
    """Include the fleet's ID in the response."""
    ALLIANCE_NAME = "allianceName"
    """Include the fleet's name in the response."""
    CHAMPIONSHIP_SCORE = "championshipScore"
    """Include the fleet's championship score in the response."""
    DIVISION_DESIGN_ID = "divisionDesignId"
    """Include the fleet's division design ID in the response."""
    NUMBER_OF_APPROVED_MEMBERS = "numberOfApprovedMembers"
    """Include the number of the fleet's approved members in the response."""
    NUMBER_OF_MEMBERS = "numberOfMembers"
    """Include the number of the fleet's members in the response."""
    SCORE = "score"
    """Include the fleet's star count in the response."""
    TROPHY = "trophy"
    """Include the fleet's trophy count in the response."""
    MEMBERS = "allianceMembers"
    """Include the fleet's members in the response."""


class ParameterInterval(StrEnum):
    HOURLY = "hour"
    """Return hourly data recorded 1 minute before a given full hour, if possible. Hourly data may not be available."""
    DAILY = "day"
    """Return daily data recorded 1 minute before daily reset, if possible. Daily data may not be available."""
    MONTHLY = "month"
    """Return monthly data recorded 1 minute before monthly reset, if possible. Monthly data may not be available."""


class ParameterMetadataProperties(StrEnum):
    COLLECTION_ID = "collectionId"
    """Include the collection's ID in the response."""
    TIMESTAMP = "timestamp"
    """Include the collection's timestamp in the response."""
    DURATION = "duration"
    """Include the collection's duration in the response."""
    FLEET_COUNT = "fleetCount"
    """Include the collection's fleet count in the response."""
    USER_COUNT = "userCount"
    """Include the collection's user count in the response."""
    TOURNAMENT_RUNNING = "tournamentRunning"
    """Include, whether a tournament was active during the collection in the response."""
    MAX_TOURNAMENT_BATTLE_ATTEMPTS = "maxTournamentBattleAttempts"
    """Include the collection's maximum tournament battle attempts in the response."""


class ParameterUserProperties(StrEnum):
    USER_ID = "userId"
    """Include the user's ID in the response."""
    USER_NAME = "userName"
    """Include the user's name in the response."""
    ALLIANCE_ID = "allianceId"
    """Include the user's fleet ID in the response."""
    TROPHY = "trophy"
    """Include the user's trophy count in the response."""
    ALLIANCE_SCORE = "allianceScore"
    """Include the user's star count in the response."""
    ALLIANCE_MEMBERSHIP = "allianceMembership"
    """Include the user's fleet rank in the response."""
    ALLIANCE_JOIN_DATE = "allianceJoinDate"
    """Include the user's fleet join date in the response."""
    LAST_LOGIN_DATE = "lastLoginDate"
    """Include the user's last login date in the response."""
    LAST_HEART_BEAT_DATE = "lastHeartBeatDate"
    """Include the user's last heartbeat date in the response."""
    CREW_DONATED = "crewDonated"
    """Include the user's donated crews count in the response."""
    CREW_RECEIVED = "crewReceived"
    """Include the user's borrowed crews count in the response."""
    PVP_ATTACK_WINS = "pvpAttackWins"
    """Include the user's PvP attack wins in the response."""
    PVP_ATTACK_LOSSES = "pvpAttackLosses"
    """Include the user's PvP attack losses in the response."""
    PVP_ATTACK_DRAWS = "pvpAttackDraws"
    """Include the user's PvP attack draws in the response."""
    PVP_DEFENSE_WINS = "pvpDefenseWins"
    """Include the user's PvP defense wins in the response."""
    PVP_DEFENSE_LOSSES = "pvpDefenseLosses"
    """Include the user's PvP defense losses in the response."""
    PVP_DEFENSE_DRAWS = "pvpDefenseDraws"
    """Include the user's PvP defense draws in the response."""
    CHAMPIONSHIP_SCORE = "championshipScore"
    """Include the user's championship score in the response."""
    HIGHEST_TROPHY = "highestTrophy"
    """Include the user's highest trophy count in the response."""
    TOURNAMENT_ATTEMPTS_LEFT = "tournamentAttemptsLeft"
    """Include the user's remaining tournament battle attemtps in the response."""
    ALLIANCE = "alliance"
    """Include the user's alliance in the response."""


class UserAllianceMembership(StrEnum):
    NONE = "None"
    """This User is not member of an Alliance."""
    FLEET_ADMIRAL = "FleetAdmiral"
    """This User is of rank Fleet Admiral."""
    VICE_ADMIRAL = "ViceAdmiral"
    """This User is of rank Vice Admiral."""
    COMMANDER = "Commander"
    """This User is of rank Commander."""
    MAJOR = "Major"
    """This User is of rank Major."""
    LIEUTENANT = "Lieutenant"
    """This User is of rank Lieutenant."""
    ENSIGN = "Ensign"
    """This User is of rank Ensign."""
    CANDIDATE = "Candidate"
    """This User is of rank Candidate."""


class UserCreateAllianceMembership(IntEnum):
    NONE = -1
    """This User is not member of an Alliance."""
    FLEET_ADMIRAL = 0
    """This User is of rank Fleet Admiral."""
    VICE_ADMIRAL = 1
    """This User is of rank Vice Admiral."""
    COMMANDER = 2
    """This User is of rank Commander."""
    MAJOR = 3
    """This User is of rank Major."""
    LIEUTENANT = 4
    """This User is of rank Lieutenant."""
    ENSIGN = 5
    """This User is of rank Ensign."""
    CANDIDATE = 6
    """This User is of rank Candidate."""
