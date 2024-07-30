from fastapi import APIRouter
from starlette.responses import HTMLResponse

from . import endpoints


router: APIRouter = APIRouter(tags=["root"], prefix="")


@router.get("/", **endpoints.homepage_get)
async def get_home() -> HTMLResponse:
    with open("src/api/html/home.html", "r") as fp:
        return HTMLResponse(content=fp.read())


@router.get("/ping", **endpoints.ping_get)
async def get_ping() -> dict[str, str]:
    return {"ping": "Pong!"}


__all__ = [
    "router",
]
