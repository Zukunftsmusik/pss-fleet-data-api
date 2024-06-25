from typing import Annotated

from fastapi import APIRouter

from ..dependencies import *

router = APIRouter(tags=["alliances"])


@router.get(
    "/alliances/{alliance_id}",
    response_model=List[AllianceHistoryOut],
    responses={"400": {"model": ErrorList}, "404": {"model": ErrorList}, "429": {"model": ErrorList}, "500": {"model": ErrorList}},
    tags=["alliances"],
)
def get_alliance_history(
    alliance_id: Annotated[int, conint(ge=0, le=2147483647)] = Path(..., alias="allianceId"),
    from_date: Optional[datetime] = Query("2016-01-06T00:00:00Z", alias="fromDate"),
    to_date: Optional[datetime] = Query(None, alias="toDate"),
    interval: Optional[EnumParamInterval] = None,
    desc: Optional[bool] = False,
    skip: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = 0,
    take: Optional[Annotated[int, conint(ge=0, le=100)]] = 100,
    alliance_properties: Optional[EnumParamAllianceProperties] = Query(None, alias="allianceProperties"),
) -> Union[List[AllianceHistoryOut], ErrorList]:
    """
    Get an Alliance's history.
    """
