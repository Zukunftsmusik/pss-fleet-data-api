from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from ..database import crud, db
from ..models import UserHistoryOut, exceptions
from ..models.converters import FromDB
from . import dependencies, endpoints


router: APIRouter = APIRouter(tags=["userHistory"], prefix="/userHistory")


@router.get("/{userId}", **endpoints.userHistory_userId_get)
async def get_user_history(
    user_id: Annotated[int, Depends(dependencies.user_id)],
    datetime_filter: Annotated[dependencies.DatetimeFilter, Depends(dependencies.from_to_date_parameters)],
    list_filter: Annotated[dependencies.ListFilter, Depends(dependencies.list_filter_parameters)],
    skip_take: Annotated[dependencies.SkipTakeFilter, Depends(dependencies.skip_take_parameters)],
    session: AsyncSession = Depends(db.get_session),
) -> list[UserHistoryOut]:
    has_user_history = await crud.has_user_history(session, user_id)
    if not has_user_history:
        raise exceptions.UserNotFoundError(
            details=f"There is no historic data for a User with the ID '{user_id}' in any of the collections.",
            suggestion="Check the provided `userId` in the path.",
        )

    history = await crud.get_user_history(
        session,
        user_id,
        True,
        datetime_filter.from_date,
        datetime_filter.to_date,
        list_filter.interval,
        list_filter.desc,
        skip_take.skip,
        skip_take.take,
    )
    result = [FromDB.to_user_history(entry) for entry in history]
    return result


__all__ = [
    "router",
]
