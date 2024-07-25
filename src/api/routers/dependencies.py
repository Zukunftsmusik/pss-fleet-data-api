from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Any, Optional

from fastapi import Depends, Header, Path, Query, Request

from .. import utils
from ..config import CONSTANTS, SETTINGS
from ..models.enums import ParameterInterval
from ..models.exceptions import FromDateAfterToDateError, MissingAccessError, NotAuthenticatedError


@dataclass(frozen=True)
class ListFilter:
    interval: ParameterInterval = ParameterInterval.MONTHLY
    desc: bool = False


@dataclass(frozen=True)
class DatetimeFilter:
    from_date: datetime = None
    to_date: datetime = None


@dataclass(frozen=True)
class SkipTakeFilter:
    skip: int = 0
    take: int = 100


async def alliance_id(alliance_id: Annotated[int, Path(alias="allianceId", ge=1, description="The ID of a PSS Alliance.", examples=[21])]) -> int:
    """
    Adds path parameter `allianceId` to a path.

    Returns:
        int: The AllianceId.
    """
    return alliance_id


async def collection_id(
    collection_id: Annotated[int, Path(alias="collectionId", ge=1, description="The ID of a PSS fleet data Collection.", examples=[1])]
) -> int:
    """
    Adds path parameter `collectionId` to a path.

    Returns:
        int: The CollectionId.
    """
    return collection_id


async def user_id(user_id: Annotated[int, Path(alias="userId", ge=1, description="The ID of a PSS User.", examples=[4510693])]) -> int:
    """
    Adds path parameter `userId` to a path.

    Returns:
        int: The UserId.
    """
    return user_id


async def division_design_id(
    division_design_id: Annotated[
        int, Query(alias="divisionDesignId", ge=0, description="The ID of the PSS Monthly Fleet Tournament Division.", examples=[1])
    ]
) -> int:
    """
    Adds query parameter `divisionDesignId` to a path.

    Returns:
        int: The DivisionDesignId.
    """
    return division_design_id


async def from_to_date_parameters(
    from_date: Annotated[
        Optional[datetime],
        Query(
            alias="fromDate",
            ge=CONSTANTS.pss_start_date,
            description="The earliest data for which data shall be returned. Must be Jan 6th, 2016 or later. Must be earlier than parameter `toDate`, if that's specified. If no timezone information is given, UTC is assumed.",
            examples=[datetime(2019, 11, 30, 23, 59, 0)],
        ),
    ] = None,
    to_date: Annotated[
        Optional[datetime],
        Query(
            alias="toDate",
            ge=CONSTANTS.pss_start_date,
            description="The latest data for which data shall be returned. Must be Jan 6th, 2016 or later. Must be later than parameter `fromDate`, if that's specified. If no timezone information is given, UTC is assumed.",
            examples=[datetime.now().replace(microsecond=0)],
        ),
    ] = None,
) -> DatetimeFilter:
    """
    Adds query parameters `fromDate` and `toDate` to a path and also validates that `toDate` is equal to or after `fromDate`.

    Returns:
        DatetimeFilter: An object encapsulating the added parameters.
    """
    from_date: datetime = utils.remove_timezone(utils.localize_to_utc(from_date)).replace(microsecond=0) if from_date else None
    to_date: datetime = utils.remove_timezone(utils.localize_to_utc(to_date)).replace(microsecond=0) if to_date else None
    if from_date and to_date and to_date < from_date:
        raise FromDateAfterToDateError("Parameter `toDate` must not be earlier than parameter `fromDate`.")

    return DatetimeFilter(from_date=from_date, to_date=to_date)


async def list_filter_parameters(
    interval: Annotated[
        Optional[ParameterInterval],
        Query(
            description="Return the data from the specified time frame in hourly, daily (last Collection of a day) or monthly (last Collection of a month) interval.",
            examples=[ParameterInterval.MONTHLY],
        ),
    ] = ParameterInterval.MONTHLY,
    desc: Annotated[Optional[bool], Query(description="Return the results in descending order by timestamp.", examples=[False])] = False,
) -> ListFilter:
    """
    Adds query parameters `interval` and `desc` to a path.

    Returns:
        ListFilter: An object encapsulating the added parameters.
    """
    return ListFilter(interval=interval, desc=desc)


async def skip_take_parameters(
    skip: Annotated[Optional[int], Query(ge=0, description="Skip this number of results from the result set.", examples=[0])] = 0,
    take: Annotated[Optional[int], Query(ge=1, le=100, description="Limit the number of results returned.", examples=[100])] = 100,
) -> SkipTakeFilter:
    """
    Adds query parameters `skip` and `take` to a path.

    Returns:
        SkipTakeFilter: An object encapsulating the added parameters.
    """
    return SkipTakeFilter(skip=skip, take=take)


def root_api_key() -> str:
    return SETTINGS.root_api_key


async def verify_api_key(
    request: Request,
    api_key: Annotated[str, Header(alias="Authorization", description="Your API key.")],
    root_api_key: str = Depends(root_api_key),
):
    """Verifies, if an api key has been provided in the 'Authorization' header and if it's authorized to access the endpoint.

    Args:
        request (Request): The request from the client.
        api_key (str): The contents of the header 'Authorization'.

    Raises:
        NotAuthenticatedError: Raised, if there's no 'Authorization' header or if the value is empty.
        MissingAccessError: Raise, if the provided 'Authorization' api key is not allowed to access the requested endpoint with the requested method.
    """
    if root_api_key:
        if not _check_is_authenticated(api_key):
            raise NotAuthenticatedError(
                "'Authorization' header not found in request.", suggestion="Add an 'Authorization' header to the request with an authorized api key."
            )

        if not _check_is_authorized(request, api_key, root_api_key):
            raise MissingAccessError(f"You're not allowed to use the method '{request.method}' on the endpoint '{request.url.path}'.")


def _check_is_authenticated(api_key: str) -> bool:
    """Checks, if the client is authenticated.

    Args:
        api_key (str): The api key provided by the client.

    Returns:
        bool: The result of the check.
    """
    return bool(api_key)


def _check_is_authorized(request: Request, api_key: str, root_api_key: str) -> bool:
    """Checks, if the client is authorized.

    Args:
        request (Request): The request from the client.
        api_key (str): The api key provided by the client.

    Returns:
        bool: The result of the check.
    """
    return api_key == root_api_key


authorization_dependencies: list[Any] = [Depends(verify_api_key)] if root_api_key() else []


__all__ = [
    # classes
    DatetimeFilter.__name__,
    ListFilter.__name__,
    SkipTakeFilter.__name__,
    # functions
    alliance_id.__name__,
    collection_id.__name__,
    division_design_id.__name__,
    from_to_date_parameters.__name__,
    list_filter_parameters.__name__,
    skip_take_parameters.__name__,
    user_id.__name__,
    verify_api_key.__name__,
    # conditional dependencies
    "authorization_dependencies",
]
