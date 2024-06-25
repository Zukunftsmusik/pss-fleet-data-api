from typing import Annotated

from fastapi import APIRouter

from ..dependencies import *

router = APIRouter(tags=["users"])


@router.get(
    "/users/{user_id}",
    response_model=List[UserHistoryOut],
    responses={"400": {"model": ErrorList}, "404": {"model": ErrorList}, "429": {"model": ErrorList}, "500": {"model": ErrorList}},
    tags=["users"],
)
def get_user_history(
    user_id: Annotated[int, conint(ge=0, le=2147483647)] = Path(..., alias="userId"),
    from_date: Optional[datetime] = Query("2016-01-06T00:00:00Z", alias="fromDate"),
    to_date: Optional[datetime] = Query(None, alias="toDate"),
    interval: Optional[EnumParamInterval] = None,
    desc: Optional[bool] = False,
    skip: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = 0,
    take: Optional[Annotated[int, conint(ge=0, le=100)]] = 100,
    user_properties: Optional[EnumParamUserProperties] = Query(None, alias="userProperties"),
) -> Union[List[UserHistoryOut], ErrorList]:
    """
    Get a User's history.
    """
