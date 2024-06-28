from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Path, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from ..database import crud, db
from ..models import AllianceHistoryOut
from ..models.converters import FromDB
from ..models.enums import ParameterInterval

router: APIRouter = APIRouter(tags=["alliances"], prefix="/alliances")


@router.get("/{alliance_id}")
async def get_alliance_history(
    alliance_id: Annotated[int, Path()],
    from_date: Annotated[Optional[datetime], Query()] = None,
    to_date: Annotated[Optional[datetime], Query()] = None,
    interval: Annotated[Optional[ParameterInterval], Query()] = ParameterInterval.MONTHLY,
    desc: Annotated[Optional[bool], Query()] = False,
    skip: Annotated[Optional[int], Query(ge=0)] = 0,
    take: Annotated[Optional[int], Query(ge=0)] = 100,
    session: AsyncSession = Depends(db.get_session),
) -> AllianceHistoryOut:
    history = await crud.get_alliance_history(session, alliance_id, True, from_date, to_date, interval, desc, skip, take)
    result = [FromDB.to_alliance_history(entry) for entry in history]
    return result
