from fastapi import APIRouter

from ..dependencies import *

router = APIRouter(tags=["healthcheck"])


@router.get("/ping", response_model=str, responses={"429": {"model": ErrorList}, "500": {"model": ErrorList}}, tags=["healthcheck"])
def ping() -> Union[str, ErrorList]:
    """
    Ping. Pong.
    """
