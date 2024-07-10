from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from ..database import crud, db
from ..models import AllianceHistoryOut, exceptions
from ..models.converters import FromDB
from . import dependencies, endpoints


router: APIRouter = APIRouter(tags=["allianceHistory"], prefix="/allianceHistory")


@router.get("/{allianceId}", **endpoints.allianceHistory_allianceId_get)
async def get_alliance_history(
    alliance_id: Annotated[int, Depends(dependencies.alliance_id)],
    datetime_filter: Annotated[dependencies.DatetimeFilter, Depends(dependencies.from_to_date_parameters)],
    list_filter: Annotated[dependencies.ListFilter, Depends(dependencies.list_filter_parameters)],
    skip_take: Annotated[dependencies.SkipTakeFilter, Depends(dependencies.skip_take_parameters)],
    session: AsyncSession = Depends(db.get_session),
) -> list[AllianceHistoryOut]:
    has_alliance_history = await crud.has_alliance_history(session, alliance_id)
    if not has_alliance_history:
        raise exceptions.AllianceNotFoundError(
            details=f"There is no historic data for an Alliance with the ID '{alliance_id}' in any of the collections.",
            suggestion="Check the provided `allianceId` in the path.",
        )

    history = await crud.get_alliance_history(
        session,
        alliance_id,
        datetime_filter.from_date,
        datetime_filter.to_date,
        list_filter.interval,
        list_filter.desc,
        skip_take.skip,
        skip_take.take,
    )
    result = [FromDB.to_alliance_history(entry) for entry in history]
    return result


__all__ = [
    "router",
]
