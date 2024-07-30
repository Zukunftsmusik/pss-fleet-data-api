import pytest

from src.api.database.models import UserDB
from src.api.models.api_models import UserCreate3, UserCreate4, UserCreate5, UserCreate6, UserCreate8, UserCreate9, UserDataCreate3
from src.api.models.converters import ToDB


@pytest.mark.usefixtures("user_create_3", "user_data_create_3")
def test_from_user_create_3(user_create_3: UserCreate3, user_data_create_3: UserDataCreate3):
    user_db = ToDB.from_user_3(user_create_3, user_data_create_3)
    _check_user_db_from_3(user_db)


@pytest.mark.usefixtures("user_create_3", "user_data_create_3_without_timestamps")
def test_from_user_create_3_without_timestamps(user_create_3: UserCreate3, user_data_create_3_without_timestamps: UserDataCreate3):
    user_db = ToDB.from_user_3(user_create_3, user_data_create_3_without_timestamps)
    _check_user_db_from_3_without_timestamps(user_db)


@pytest.mark.usefixtures("user_create_4")
def test_from_user_create_4(user_create_4: UserCreate4):
    user_db = ToDB.from_user_4(user_create_4)
    _check_user_db_from_4(user_db)


@pytest.mark.usefixtures("user_create_5")
def test_from_user_create_5(user_create_5: UserCreate5):
    user_db = ToDB.from_user_5(user_create_5)
    _check_user_db_from_5(user_db)


@pytest.mark.usefixtures("user_create_6")
def test_from_user_create_6(user_create_6: UserCreate6):
    user_db = ToDB.from_user_6(user_create_6)
    _check_user_db_from_6(user_db)


@pytest.mark.usefixtures("user_create_8")
def test_from_user_create_8(user_create_8: UserCreate8):
    user_db = ToDB.from_user_8(user_create_8)
    _check_user_db_from_8(user_db)


@pytest.mark.usefixtures("user_create_9")
def test_from_user_create_9(user_create_9: UserCreate9):
    user_db = ToDB.from_user_9(user_create_9)
    _check_user_db_from_9(user_db)


# Helpers


def _check_user_db_from_3(user_db: UserDB):
    assert user_db
    assert isinstance(user_db, UserDB)

    assert user_db.user_id is not None
    assert user_db.user_name is not None
    assert user_db.alliance_id is not None
    assert user_db.trophy is not None
    assert user_db.alliance_score is not None
    assert user_db.alliance_membership is not None
    assert user_db.alliance_join_date is not None
    assert user_db.last_login_date is not None


def _check_user_db_from_3_without_timestamps(user_db: UserDB):
    assert user_db
    assert isinstance(user_db, UserDB)

    assert user_db.user_id is not None
    assert user_db.user_name is not None
    assert user_db.alliance_id is not None
    assert user_db.trophy is not None
    assert user_db.alliance_score is not None
    assert user_db.alliance_membership is not None
    assert user_db.alliance_join_date is None
    assert user_db.last_login_date is None


def _check_user_db_from_4(user_db: UserDB):
    _check_user_db_from_3(user_db)
    assert user_db.crew_donated is not None
    assert user_db.crew_received is not None
    assert user_db.pvp_attack_wins is not None
    assert user_db.pvp_attack_losses is not None
    assert user_db.pvp_attack_draws is not None
    assert user_db.pvp_defence_wins is not None
    assert user_db.pvp_defence_losses is not None
    assert user_db.pvp_defence_draws is not None


def _check_user_db_from_5(user_db: UserDB):
    _check_user_db_from_4(user_db)


def _check_user_db_from_6(user_db: UserDB):
    _check_user_db_from_5(user_db)
    assert user_db.championship_score is not None


def _check_user_db_from_8(user_db: UserDB):
    _check_user_db_from_6(user_db)
    assert user_db.highest_trophy is not None


def _check_user_db_from_9(user_db: UserDB):
    _check_user_db_from_8(user_db)
    assert user_db.tournament_bonus_score is not None
