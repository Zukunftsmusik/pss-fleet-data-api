import pytest
from src.database.crud import get_collections
from src.models.enums import ParameterInterval
from sqlmodel import Session


@pytest.mark.usefixtures("session")
def test_get_collections(session: Session):
    collections = get_collections(session, None, None, ParameterInterval.MONTHLY, False, 0, 100)
    assert len(collections) == 3
