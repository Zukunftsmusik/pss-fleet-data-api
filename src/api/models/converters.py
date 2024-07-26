from .. import utils
from ..config import CONSTANTS
from ..database.models import AllianceDB, AllianceHistoryDB, CollectionDB, UserDB, UserHistoryDB
from .api_models import (
    AllianceCreate2,
    AllianceCreate3,
    AllianceCreate4,
    AllianceCreate6,
    AllianceCreate7,
    AllianceHistoryOut,
    AllianceOut,
    CollectionCreate3,
    CollectionCreate4,
    CollectionCreate5,
    CollectionCreate6,
    CollectionCreate7,
    CollectionCreate8,
    CollectionCreate9,
    CollectionMetadataOut,
    CollectionOut,
    CollectionWithFleetsOut,
    CollectionWithUsersOut,
    UserCreate3,
    UserCreate4,
    UserCreate5,
    UserCreate6,
    UserCreate8,
    UserCreate9,
    UserDataCreate3,
    UserHistoryOut,
    UserOut,
)
from .enums import UserAllianceMembership


class FromDB:
    """
    Offers functions to convert database objects to objects to be returned by the API.
    """

    @staticmethod
    def to_alliance(source: AllianceDB) -> AllianceOut:
        """Takes an Alliance from the database and converts it to an Alliance to be returned by the API.

        Args:
            source (AllianceDB): The Alliance to be converted.

        Returns:
            AllianceOut: The converted Alliance.
        """
        return (
            source.alliance_id,
            source.alliance_name,
            source.score,
            source.division_design_id,
            source.trophy,
            source.championship_score,
            source.number_of_members,
            source.number_of_approved_members,
        )

    @staticmethod
    def to_alliance_history(source: AllianceHistoryDB) -> AllianceHistoryOut:
        """Takes a tuple of a Collection and an Alliance from the database and converts it to an Alliance History to be returned by the API.

        Args:
            source (AllianceHistoryDB): The tuple of a Collection and an Alliance to be converted.

        Returns:
            AllianceHistoryOut: The converted Alliance History.
        """
        collection = FromDB.to_collection_metadata(source[0])
        alliance = FromDB.to_alliance(source[1])
        users = [FromDB.to_user(user) for user in source[1].users if user] if source[1].users else []
        return AllianceHistoryOut(collection=collection, fleet=alliance, users=users)

    @staticmethod
    def to_collection(source: CollectionDB, include_alliances: bool, include_users: bool) -> CollectionOut:
        """Takes a Collection from the database and converts it to a Collection to be returned by the API.

        Args:
            source (CollectionDB): The Collection to be converted.

        Returns:
            CollectionOut: The converted Collection.
        """
        return CollectionOut(
            meta=FromDB.to_collection_metadata(source),
            fleets=[FromDB.to_alliance(alliance) for alliance in source.alliances if alliance] if include_alliances and source.alliances else [],
            users=[FromDB.to_user(user) for user in source.users if user] if include_users and source.users else [],
        )

    @staticmethod
    def to_collection_metadata(source: CollectionDB) -> CollectionMetadataOut:
        """Takes a Collection from the database and converts it to a CollectionMetadata to be returned by the API.

        Args:
            source (CollectionDB): The Collection to be converted.

        Returns:
            CollectionMetadataOut: The converted Collection.
        """
        return CollectionMetadataOut(
            collection_id=source.collection_id,
            data_version=source.data_version,
            timestamp=utils.localize_to_utc(source.collected_at),
            duration=source.duration,
            fleet_count=source.fleet_count,
            user_count=source.user_count,
            tourney_running=source.tournament_running,
            max_tournament_battle_attempts=source.max_tournament_battle_attempts,
            schema_version=CONSTANTS.latest_schema_version,
        )

    @staticmethod
    def to_collection_with_fleets(source: CollectionDB) -> CollectionWithFleetsOut:
        """Takes a Collection with Alliances from the database and converts it to a Collection with Fleets to be returned by the API.

        Args:
            source (CollectionDB): The Collection to be converted.

        Returns:
            CollectionWithFleetsOut: The converted Collection.
        """
        return CollectionWithFleetsOut(
            meta=FromDB.to_collection_metadata(source),
            fleets=[FromDB.to_alliance(alliance) for alliance in source.alliances if alliance] if source.alliances else [],
        )

    @staticmethod
    def to_collection_with_users(source: CollectionDB) -> CollectionWithUsersOut:
        """Takes a Collection with Users from the database and converts it to a Collection with Fleets to be returned by the API.

        Args:
            source (CollectionDB): The Collection to be converted.

        Returns:
            CollectionWithUsersOut: The converted Collection.
        """
        return CollectionWithUsersOut(
            meta=FromDB.to_collection_metadata(source),
            users=[FromDB.to_user(user) for user in source.users if user] if source.users else [],
        )

    @staticmethod
    def to_user(source: UserDB) -> UserOut:
        """Takes a User from the database and converts it to a User to be returned by the API.

        Args:
            source (UserDB): The User to be converted.

        Returns:
            UserOut: The converted User.
        """
        return (
            source.user_id,
            source.user_name,
            source.alliance_id,
            source.trophy,
            source.alliance_score,
            utils.encode_alliance_membership(source.alliance_membership),
            utils.convert_datetime_to_seconds(source.alliance_join_date),
            utils.convert_datetime_to_seconds(source.last_login_date),
            utils.convert_datetime_to_seconds(source.last_heartbeat_date),
            source.crew_donated,
            source.crew_received,
            source.pvp_attack_wins,
            source.pvp_attack_losses,
            source.pvp_attack_draws,
            source.pvp_defence_wins,
            source.pvp_defence_losses,
            source.pvp_defence_draws,
            source.championship_score,
            source.highest_trophy,
            source.tournament_bonus_score,
        )

    @staticmethod
    def to_user_history(source: UserHistoryDB) -> UserHistoryOut:
        """Takes a tuple of a Collection and a User from the database and converts it to a User History to be returned by the API.

        Args:
            source (UserHistoryDB): The tuple of a Collection and a User to be converted.

        Returns:
            UserHistoryOut: The converted User History.
        """
        collection = FromDB.to_collection_metadata(source[0])
        user = FromDB.to_user(source[1])
        alliance = FromDB.to_alliance(source[1].alliance) if source[1].alliance else None
        return UserHistoryOut(collection=collection, user=user, fleet=alliance)


class ToDB:
    """
    Offers functions to convert objects received by the API to database objects.
    """

    @staticmethod
    def from_alliance_2(source: AllianceCreate2) -> AllianceDB:
        """Takes a tuple of values denoting an Alliance of schema version 3 without a DivisionDesignId and converts it to an Alliance for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (AllianceCreate2): The Alliance to be converted.

        Returns:
            AllianceDB: The converted Alliance.
        """
        return AllianceDB(alliance_id=int(source[0]), alliance_name=source[1], score=int(source[2]))

    @staticmethod
    def from_alliance_3(source: AllianceCreate3) -> AllianceDB:
        """Takes a tuple of values denoting an Alliance of schema version 3 with a DivisionDesignId and converts it to an Alliance for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (AllianceCreate3): The Alliance to be converted.

        Returns:
            AllianceDB: The converted Alliance.
        """
        result = ToDB.from_alliance_2(source)
        result.division_design_id = int(source[3])
        return result

    @staticmethod
    def from_alliance_4(source: AllianceCreate4) -> AllianceDB:
        """Takes a tuple of values denoting an Alliance of schema version 4 and converts it to an Alliance for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (AllianceCreate4): The Alliance to be converted.

        Returns:
            AllianceDB: The converted Alliance.
        """
        result = ToDB.from_alliance_3(source)
        result.trophy = source[4]
        return result

    @staticmethod
    def from_alliance_6(source: AllianceCreate6) -> AllianceDB:
        """Takes a tuple of values denoting an Alliance of schema version 6 and converts it to an Alliance for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (AllianceCreate6): The Alliance to be converted.

        Returns:
            AllianceDB: The converted Alliance.
        """
        result = ToDB.from_alliance_4(source)
        result.championship_score = source[5]
        return result

    @staticmethod
    def from_alliance_7(source: AllianceCreate7) -> AllianceDB:
        """Takes a tuple of values denoting an Alliance of schema version 7 and converts it to an Alliance for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (AllianceCreate7): The Alliance to be converted.

        Returns:
            AllianceDB: The converted Alliance.
        """
        result = ToDB.from_alliance_6(source)
        result.number_of_members = source[6]
        result.number_of_approved_members = source[7]
        return result

    @staticmethod
    def from_collection_3(source: CollectionCreate3) -> CollectionDB:
        """Takes a dictionary denoting a Collection of schema version 3 and converts it to a Collection for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (CollectionCreate3): The Collection to be converted.

        Returns:
            CollectionDB: The converted Collection.
        """
        for rank, fleet in enumerate(source.fleets):
            if len(fleet) == 3:
                if source.meta.tourney_running:
                    if rank < 8:
                        division_design_id = "1"
                    elif rank < 20:
                        division_design_id = "2"
                    elif rank < 50:
                        division_design_id = "3"
                    else:
                        division_design_id = "4"
                else:
                    division_design_id = "0"
                source.fleets[rank] = (*fleet, division_design_id)
        fleets = [ToDB.from_alliance_3(alliance) for alliance in source.fleets]

        user_dict = {user[0]: user for user in source.users}
        user_data_dict = {user_data[0]: user_data for user_data in source.data}
        users = [ToDB.from_user_3(user, user_data_dict[user_id]) for user_id, user in user_dict.items()]

        return CollectionDB(
            data_version=3,
            collected_at=utils.remove_timezone(source.meta.timestamp),
            duration=source.meta.duration,
            fleet_count=source.meta.fleet_count,
            user_count=source.meta.user_count,
            tournament_running=source.meta.tourney_running,
            alliances=fleets,
            users=users,
        )

    @staticmethod
    def from_collection_4(source: CollectionCreate4) -> CollectionDB:
        """Takes a dictionary denoting a Collection of schema version 4 and converts it to a Collection for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (CollectionCreate4): The Collection to be converted.

        Returns:
            CollectionDB: The converted Collection.
        """
        fleets = [ToDB.from_alliance_4(alliance) for alliance in source.fleets]
        users = [ToDB.from_user_4(user) for user in source.users]

        return CollectionDB(
            data_version=source.meta.schema_version,
            collected_at=utils.remove_timezone(source.meta.timestamp),
            duration=source.meta.duration,
            fleet_count=source.meta.fleet_count,
            user_count=source.meta.user_count,
            tournament_running=source.meta.tourney_running,
            alliances=fleets,
            users=users,
        )

    @staticmethod
    def from_collection_5(source: CollectionCreate5) -> CollectionDB:
        """Takes a dictionary denoting a Collection of schema version 5 and converts it to a Collection for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (CollectionCreate5): The Collection to be converted.

        Returns:
            CollectionDB: The converted Collection.
        """
        fleets = [ToDB.from_alliance_4(alliance) for alliance in source.fleets]
        users = [ToDB.from_user_5(user) for user in source.users]

        return CollectionDB(
            data_version=source.meta.schema_version,
            collected_at=utils.remove_timezone(source.meta.timestamp),
            duration=source.meta.duration,
            fleet_count=source.meta.fleet_count,
            user_count=source.meta.user_count,
            tournament_running=source.meta.tourney_running,
            alliances=fleets,
            users=users,
        )

    @staticmethod
    def from_collection_6(source: CollectionCreate6) -> CollectionDB:
        """Takes a dictionary denoting a Collection of schema version 6 and converts it to a Collection for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (CollectionCreate6): The Collection to be converted.

        Returns:
            CollectionDB: The converted Collection.
        """
        fleets = [ToDB.from_alliance_6(alliance) for alliance in source.fleets]
        users = [ToDB.from_user_6(user) for user in source.users]

        return CollectionDB(
            data_version=source.meta.schema_version,
            collected_at=utils.remove_timezone(source.meta.timestamp),
            duration=source.meta.duration,
            fleet_count=source.meta.fleet_count,
            user_count=source.meta.user_count,
            tournament_running=source.meta.tourney_running,
            alliances=fleets,
            users=users,
        )

    @staticmethod
    def from_collection_7(source: CollectionCreate7) -> CollectionDB:
        """Takes a dictionary denoting a Collection of schema version 7 and converts it to a Collection for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (CollectionCreate7): The Collection to be converted.

        Returns:
            CollectionDB: The converted Collection.
        """
        fleets = [ToDB.from_alliance_7(alliance) for alliance in source.fleets]
        users = [ToDB.from_user_6(user) for user in source.users]

        return CollectionDB(
            data_version=source.meta.schema_version,
            collected_at=utils.remove_timezone(source.meta.timestamp),
            duration=source.meta.duration,
            fleet_count=source.meta.fleet_count,
            user_count=source.meta.user_count,
            tournament_running=source.meta.tourney_running,
            alliances=fleets,
            users=users,
        )

    @staticmethod
    def from_collection_8(source: CollectionCreate8) -> CollectionDB:
        """Takes a dictionary denoting a Collection of schema version 8 and converts it to a Collection for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (CollectionCreate8): The Collection to be converted.

        Returns:
            CollectionDB: The converted Collection.
        """
        fleets = [ToDB.from_alliance_7(alliance) for alliance in source.fleets]
        users = [ToDB.from_user_8(user) for user in source.users]

        return CollectionDB(
            data_version=source.meta.schema_version,
            collected_at=utils.remove_timezone(source.meta.timestamp),
            duration=source.meta.duration,
            fleet_count=source.meta.fleet_count,
            user_count=source.meta.user_count,
            tournament_running=source.meta.tourney_running,
            alliances=fleets,
            users=users,
        )

    @staticmethod
    def from_collection_9(source: CollectionCreate9) -> CollectionDB:
        """Takes a dictionary denoting a Collection of schema version 9 and converts it to a Collection for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (CollectionCreate9): The Collection to be converted.

        Returns:
            CollectionDB: The converted Collection.
        """
        fleets = [ToDB.from_alliance_7(alliance) for alliance in source.fleets]
        users = [ToDB.from_user_9(user) for user in source.users]

        return CollectionDB(
            data_version=source.meta.schema_version,
            collected_at=utils.remove_timezone(source.meta.timestamp),
            duration=source.meta.duration,
            fleet_count=source.meta.fleet_count,
            user_count=source.meta.user_count,
            tournament_running=source.meta.tourney_running,
            max_tournament_battle_attempts=source.meta.max_tournament_battle_attempts,
            alliances=fleets,
            users=users,
        )

    @staticmethod
    def from_user_3(user: UserCreate3, data: UserDataCreate3) -> UserDB:
        """Takes 2 tuples of values denoting a User of schema version 3 and converts them to a User for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            user (UserCreate3): The User to be converted.
            data (UserDataCreate3): The User data to be converted.

        Returns:
            UserDB: The converted User.
        """
        alliance_membership = UserAllianceMembership(data[4])
        alliance_join_date = utils.remove_timezone(utils.localize_to_utc(utils.parse_datetime(data[5])))
        last_login_date = utils.remove_timezone(utils.localize_to_utc(utils.parse_datetime(data[6])))

        return UserDB(
            user_id=int(user[0]),
            user_name=user[1],
            alliance_id=int(data[1]),
            trophy=int(data[2]),
            alliance_score=int(data[3]),
            alliance_membership=alliance_membership,
            alliance_join_date=alliance_join_date,
            last_login_date=last_login_date,
        )

    @staticmethod
    def from_user_4(source: UserCreate4) -> UserDB:
        """Takes a tuple of values denoting a User of schema version 4 and converts them to a User for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (UserCreate4): The User to be converted.

        Returns:
            UserDB: The converted User.
        """
        user_id = source[0]
        user_name = source[1]
        alliance_membership = utils.decode_alliance_membership(source[5])
        alliance_join_date = utils.localize_to_utc(utils.parse_datetime(source[5]))
        last_login_date = utils.localize_to_utc(utils.parse_datetime(source[6]))
        last_heartbeat_date = utils.localize_to_utc(utils.parse_datetime(source[8]))

        if last_login_date < CONSTANTS.pss_start_date:
            raise ValueError(
                f"The `LastLoginDate` of User `{user_name}` with ID `{user_id}` received an invalid value: {last_login_date} (original value: {int(source[6])})"
            )

        if last_heartbeat_date < CONSTANTS.pss_start_date:
            raise ValueError(
                f"The `LastHeartBeatDate` of User `{user_name}` with ID `{user_id}` received an invalid value: {last_login_date} (original value: {int(source[6])})"
            )

        return UserDB(
            user_id=user_id,
            user_name=user_name,
            alliance_id=source[2],
            trophy=source[3],
            alliance_score=source[4],
            alliance_membership=alliance_membership,
            alliance_join_date=utils.remove_timezone(alliance_join_date),
            last_login_date=utils.remove_timezone(last_login_date),
            last_heartbeat_date=utils.remove_timezone(last_heartbeat_date),
            crew_donated=source[9],
            crew_received=source[10],
            pvp_attack_wins=source[11],
            pvp_attack_losses=source[12],
            pvp_attack_draws=source[13],
            pvp_defence_wins=source[14],
            pvp_defence_losses=source[15],
            pvp_defence_draws=source[16],
        )

    @staticmethod
    def from_user_5(source: UserCreate5) -> UserDB:
        """Takes a tuple of values denoting a User of schema version 5 and converts them to a User for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (UserCreate5): The User to be converted.

        Returns:
            UserDB: The converted User.
        """
        user_db = ToDB.from_user_4(source)
        return user_db

    @staticmethod
    def from_user_6(source: UserCreate6) -> UserDB:
        """Takes a tuple of values denoting a User of schema version 6 and converts them to a User for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (UserCreate6): The User to be converted.

        Returns:
            UserDB: The converted User.
        """
        user_db = ToDB.from_user_5(source)
        user_db.championship_score = source[17]
        return user_db

    @staticmethod
    def from_user_8(source: UserCreate8) -> UserDB:
        """Takes a tuple of values denoting a User of schema version 8 and converts them to a User for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (UserCreate8): The User to be converted.

        Returns:
            UserDB: The converted User.
        """
        user_db = ToDB.from_user_6(source)
        user_db.highest_trophy = source[18]
        return user_db

    @staticmethod
    def from_user_9(source: UserCreate9) -> UserDB:
        """Takes a tuple of values denoting a User of schema version 9 and converts them to a User for the database.
        For more information on the schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions

        Args:
            source (UserCreate9): The User to be converted.

        Returns:
            UserDB: The converted User.
        """
        user_db = ToDB.from_user_8(source)
        user_db.tournament_bonus_score = source[19]
        return user_db


__all__ = [
    FromDB.__name__,
    ToDB.__name__,
]
