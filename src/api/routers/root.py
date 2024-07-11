from fastapi import APIRouter
from starlette.responses import HTMLResponse

from . import endpoints


router: APIRouter = APIRouter(tags=["root"], prefix="")


@router.get("/", **endpoints.homepage_get)
async def get_home() -> HTMLResponse:
    with open("src/api/routers/home.html", "r") as fp:
        return HTMLResponse(content=fp.read())


__all__ = ["router"]
