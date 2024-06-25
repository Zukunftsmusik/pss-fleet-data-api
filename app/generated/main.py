from fastapi import FastAPI

from .routers import alliances, collections, healthcheck, legacy, users

app = FastAPI(
    version="1.0",
    title="PSS Fleet Data API",
    description="An API server for Pixel Starships Fleet Data.",
    contact={"email": "theworstpss@gmail.com", "name": "The worst.", "url": "https://dolores2.xyz"},
    license={"name": "MIT", "url": "https://github.com/Zukunftsmusik/pss-fleet-data-api/blob/main/LICENSE"},
    servers=[{"url": "https://fleetdata.dolores2.xyz", "description": "The PSS Fleet Data API.", "variables": {}}],
)

app.include_router(alliances.router)
app.include_router(collections.router)
app.include_router(healthcheck.router)
app.include_router(legacy.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Gateway of the App"}
