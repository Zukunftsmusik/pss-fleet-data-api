from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import db
from .routers import alliances, collections, upload, users

from .config import SETTINGS


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.set_up_db_engine(SETTINGS.database_connection_str)
    if SETTINGS.initialize_database_on_startup:
        db.initialize_db()
    yield


app = FastAPI(
    version=SETTINGS.version,
    title=SETTINGS.project_name,
    description=SETTINGS.description,
    contact={"email": "theworstpss@gmail.com", "name": "The worst.", "url": "https://dolores2.xyz"},
    license={"name": "MIT", "url": "https://github.com/Zukunftsmusik/pss-fleet-data-api/blob/main/LICENSE"},
    # servers=[{"url": "https://fleetdata.dolores2.xyz", "description": "The PSS Fleet Data API.", "variables": {}}],
    lifespan=lifespan,
)
app.include_router(alliances.router)
app.include_router(collections.router)
app.include_router(upload.router)
app.include_router(users.router)
