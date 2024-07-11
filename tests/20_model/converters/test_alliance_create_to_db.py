import pytest

from src.api.database.models import AllianceDB
from src.api.models.api_models import AllianceCreate2, AllianceCreate3, AllianceCreate4, AllianceCreate6, AllianceCreate7
from src.api.models.converters import ToDB


@pytest.mark.usefixtures("alliance_create_2")
def test_from_alliance_create_2(alliance_create_2: AllianceCreate2):
    alliance_db = ToDB.from_alliance_2(alliance_create_2)
    _check_alliance_db_from_2(alliance_db)


@pytest.mark.usefixtures("alliance_create_3")
def test_from_alliance_create_3(alliance_create_3: AllianceCreate3):
    alliance_db = ToDB.from_alliance_3(alliance_create_3)
    _check_alliance_db_from_3(alliance_db)


@pytest.mark.usefixtures("alliance_create_4")
def test_from_alliance_create_4(alliance_create_4: AllianceCreate4):
    alliance_db = ToDB.from_alliance_4(alliance_create_4)
    _check_alliance_db_from_4(alliance_db)


@pytest.mark.usefixtures("alliance_create_6")
def test_from_alliance_create_6(alliance_create_6: AllianceCreate6):
    alliance_db = ToDB.from_alliance_6(alliance_create_6)
    _check_alliance_db_from_6(alliance_db)


@pytest.mark.usefixtures("alliance_create_7")
def test_from_alliance_create_7(alliance_create_7: AllianceCreate7):
    alliance_db = ToDB.from_alliance_7(alliance_create_7)
    _check_alliance_db_from_7(alliance_db)


# Helpers


def _check_alliance_db_from_2(alliance_db: AllianceDB):
    assert alliance_db
    assert isinstance(alliance_db, AllianceDB)

    assert alliance_db.alliance_id is not None
    assert alliance_db.alliance_name is not None
    assert alliance_db.score is not None


def _check_alliance_db_from_3(alliance_db: AllianceDB):
    _check_alliance_db_from_2(alliance_db)
    assert alliance_db.division_design_id is not None


def _check_alliance_db_from_4(alliance_db: AllianceDB):
    _check_alliance_db_from_3(alliance_db)
    assert alliance_db.trophy is not None


def _check_alliance_db_from_6(alliance_db: AllianceDB):
    _check_alliance_db_from_4(alliance_db)
    assert alliance_db.championship_score is not None


def _check_alliance_db_from_7(alliance_db: AllianceDB):
    _check_alliance_db_from_6(alliance_db)
    assert alliance_db.number_of_members is not None
    assert alliance_db.number_of_approved_members is not None
