from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Path, Query

from ..database import crud, db
from ..models import UserHistoryOut
from ..models.converters import FromDB
from ..models.enums import ParameterInterval

router: APIRouter = APIRouter(tags=["users"], prefix="/users")


@router.get("/{user_id}")
def get_user_history(
    user_id: Annotated[int, Path()],
    from_date: Annotated[Optional[datetime], Query()] = None,
    to_date: Annotated[Optional[datetime], Query()] = None,
    interval: Annotated[Optional[ParameterInterval], Query()] = ParameterInterval.MONTHLY,
    desc: Annotated[Optional[bool], Query()] = False,
    skip: Annotated[Optional[int], Query(ge=0)] = 0,
    take: Annotated[Optional[int], Query(ge=0)] = 100,
) -> UserHistoryOut:
    history = crud.get_user_history(db.ENGINE, user_id, True, from_date, to_date, interval, desc, skip, take)
    result = [FromDB.to_user_history(entry) for entry in history]
    return result
