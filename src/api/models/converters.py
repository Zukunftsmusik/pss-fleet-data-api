from .. import utils
from ..database.models import AllianceDB, CollectionDB, UserDB
from .api_models import (
    AllianceCreate2,
    AllianceCreate3,
    AllianceCreate4,
    AllianceCreate6,
    AllianceCreate7,
    AllianceHistoryOut,
    AllianceOut,
    CollectionCreate2,
    CollectionCreate3,
    CollectionCreate4,
    CollectionCreate5,
    CollectionCreate6,
    CollectionCreate7,
    CollectionCreate8,
    CollectionCreate9,
    CollectionMetadataOut,
    CollectionOut,
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

LATEST_SCHEMA_VERSION: int = 9


class FromDB:
    @staticmethod
    def to_alliance(source: AllianceDB) -> AllianceOut:
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
    def to_alliance_history(source: tuple[CollectionDB, AllianceDB]) -> AllianceHistoryOut:
        collection = FromDB.to_collection(source[0], False, False)
        alliance = FromDB.to_alliance(source[1])
        users = [FromDB.to_user(user)[0] for user in source[1].users if user] if source[1].users else []
        return AllianceHistoryOut(collection=collection, fleet=alliance, users=users)

    @staticmethod
    def to_collection(source: CollectionDB, include_alliances: bool, include_users: bool) -> CollectionOut:
        return CollectionOut(
            metadata=CollectionMetadataOut(
                collection_id=source.collection_id,
                timestamp=utils.add_timezone_utc(source.collected_at),
                duration=source.duration,
                fleet_count=source.fleet_count,
                user_count=source.user_count,
                tourney_running=source.tournament_running,
                max_tournament_battle_attempts=source.max_tournament_battle_attempts,
                schema_version=LATEST_SCHEMA_VERSION,
            ),
            fleets=[FromDB.to_alliance(alliance) for alliance in source.alliances if alliance] if include_alliances and source.alliances else [],
            users=[FromDB.to_user(user) for user in source.users if user] if include_users and source.users else [],
        )

    @staticmethod
    def to_user(source: UserDB) -> UserOut:
        return (
            source.user_id,
            source.user_name,
            source.alliance_id,
            source.trophy,
            source.alliance_score,
            utils.convert_alliance_membership_to_int(source.alliance_membership),
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
    def to_user_history(source: tuple[CollectionDB, UserDB]) -> UserHistoryOut:
        collection = FromDB.to_collection(source[0], False, False)
        user = FromDB.to_user(source[1])
        alliance = FromDB.to_alliance(source[1].alliance) if source[1].alliance else None
        return UserHistoryOut(collection=collection, user=user, fleet=alliance)


class ToDB:
    @staticmethod
    def from_alliance_2(source: AllianceCreate2) -> AllianceDB:
        return AllianceDB(alliance_id=source[0], alliance_name=source[1], score=source[2])

    @staticmethod
    def from_alliance_3(source: AllianceCreate3) -> AllianceDB:
        result = ToDB.from_alliance_2(source)
        result.division_design_id = source[3]
        return result

    @staticmethod
    def from_alliance_4(source: AllianceCreate4) -> AllianceDB:
        result = ToDB.from_alliance_3(source)
        result.trophy = source[4]
        return result

    @staticmethod
    def from_alliance_6(source: AllianceCreate6) -> AllianceDB:
        result = ToDB.from_alliance_4(source)
        result.championship_score = source[5]
        return result

    @staticmethod
    def from_alliance_7(source: AllianceCreate7) -> AllianceDB:
        result = ToDB.from_alliance_6(source)
        result.number_of_members = source[6]
        result.number_of_approved_members = source[7]
        return result

    @staticmethod
    def from_collection_2(source: CollectionCreate2) -> CollectionDB:
        fleets = [ToDB.from_alliance_2(alliance) for alliance in source.fleets]
        for rank, fleet in enumerate(fleets):
            if fleet.division_design_id is None:
                if rank <= 8:
                    fleet.division_design_id = 1
                elif rank <= 20:
                    fleet.division_design_id = 2
                elif rank <= 50:
                    fleet.division_design_id = 3
                else:
                    fleet.division_design_id = 4

        user_dict = {user[0]: user for user in source.users}
        user_data_dict = {user_data[0]: user_data for user_data in source.data}
        users = [ToDB.from_user_3(user, user_data_dict[user_id]) for user_id, user in user_dict.items()]

        return CollectionDB(
            collected_at=source.metadata.timestamp,
            duration=source.metadata.duration,
            fleet_count=source.metadata.fleet_count,
            user_count=source.metadata.user_count,
            tournament_running=source.metadata.tourney_running,
            alliances=fleets,
            users=users,
        )

    @staticmethod
    def from_collection_3(source: CollectionCreate3) -> CollectionDB:
        return ToDB.from_collection_2(source)

    @staticmethod
    def from_collection_4(source: CollectionCreate4) -> CollectionDB:
        fleets = [ToDB.from_alliance_4(alliance) for alliance in source.fleets]
        users = [ToDB.from_user_4(user) for user in source.users]

        return CollectionDB(
            collected_at=source.metadata.timestamp,
            duration=source.metadata.duration,
            fleet_count=source.metadata.fleet_count,
            user_count=source.metadata.user_count,
            tournament_running=source.metadata.tourney_running,
            alliances=fleets,
            users=users,
        )

    @staticmethod
    def from_collection_5(source: CollectionCreate5) -> CollectionDB:
        fleets = [ToDB.from_alliance_4(alliance) for alliance in source.fleets]
        users = [ToDB.from_user_5(user) for user in source.users]

        return CollectionDB(
            collected_at=source.metadata.timestamp,
            duration=source.metadata.duration,
            fleet_count=source.metadata.fleet_count,
            user_count=source.metadata.user_count,
            tournament_running=source.metadata.tourney_running,
            alliances=fleets,
            users=users,
        )

    @staticmethod
    def from_collection_6(source: CollectionCreate6) -> CollectionDB:
        fleets = [ToDB.from_alliance_6(alliance) for alliance in source.fleets]
        users = [ToDB.from_user_6(user) for user in source.users]

        return CollectionDB(
            collected_at=source.metadata.timestamp,
            duration=source.metadata.duration,
            fleet_count=source.metadata.fleet_count,
            user_count=source.metadata.user_count,
            tournament_running=source.metadata.tourney_running,
            alliances=fleets,
            users=users,
        )

    @staticmethod
    def from_collection_7(source: CollectionCreate7) -> CollectionDB:
        fleets = [ToDB.from_alliance_7(alliance) for alliance in source.fleets]
        users = [ToDB.from_user_6(user) for user in source.users]

        return CollectionDB(
            collected_at=source.metadata.timestamp,
            duration=source.metadata.duration,
            fleet_count=source.metadata.fleet_count,
            user_count=source.metadata.user_count,
            tournament_running=source.metadata.tourney_running,
            alliances=fleets,
            users=users,
        )

    @staticmethod
    def from_collection_8(source: CollectionCreate8) -> CollectionDB:
        fleets = [ToDB.from_alliance_7(alliance) for alliance in source.fleets]
        users = [ToDB.from_user_8(user) for user in source.users]

        return CollectionDB(
            collected_at=source.metadata.timestamp,
            duration=source.metadata.duration,
            fleet_count=source.metadata.fleet_count,
            user_count=source.metadata.user_count,
            tournament_running=source.metadata.tourney_running,
            alliances=fleets,
            users=users,
        )

    @staticmethod
    def from_collection_9(source: CollectionCreate9) -> CollectionDB:
        fleets = [ToDB.from_alliance_7(alliance) for alliance in source.fleets]
        users = [ToDB.from_user_9(user) for user in source.users]

        return CollectionDB(
            collected_at=source.metadata.timestamp,
            duration=source.metadata.duration,
            fleet_count=source.metadata.fleet_count,
            user_count=source.metadata.user_count,
            tournament_running=source.metadata.tourney_running,
            max_tournament_battle_attempts=source.metadata.max_tournament_battle_attempts,
            alliances=fleets,
            users=users,
        )

    @staticmethod
    def from_user_3(user: UserCreate3, data: UserDataCreate3) -> UserDB:
        return UserDB(user_id=user[0], user_name=user[1], alliance_id=data[1], trophy=data[2], alliance_score=data[3], alliance_membership=data[4], alliance_join_date=data[5], last_login_date=data[6])

    @staticmethod
    def from_user_4(source: UserCreate4) -> UserDB:
        return UserDB(
            user_id=source[0],
            user_name=source[1],
            alliance_id=source[2],
            trophy=source[3],
            alliance_score=source[4],
            alliance_membership=source[5],
            alliance_join_date=utils.parse_datetime(source[6]),
            last_login_date=utils.parse_datetime(source[7]),
            last_heartbeat_date=utils.parse_datetime(source[8]),
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
        user_db = ToDB.from_user_4(source)
        user_db.alliance_join_date = utils.parse_datetime(source[6])
        user_db.last_login_date = utils.parse_datetime(source[7])
        user_db.last_heartbeat_date = utils.parse_datetime(source[8])
        return user_db

    @staticmethod
    def from_user_6(source: UserCreate6) -> UserDB:
        user_db = ToDB.from_user_5(source)
        user_db.championship_score = source[17]
        return user_db

    @staticmethod
    def from_user_8(source: UserCreate8) -> UserDB:
        user_db = ToDB.from_user_6(source)
        user_db.highest_trophy = source[18]
        return user_db

    @staticmethod
    def from_user_9(source: UserCreate9) -> UserDB:
        user_db = ToDB.from_user_8(source)
        user_db.tournament_bonus_score = source[19]
        return user_db
