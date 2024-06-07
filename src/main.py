from typing import Union

import fastapi

app = fastapi.FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/collections/{id}")
async def read_item(id: int, p: int, q: Union[str, None] = None):
    return {"id": id, "p": p, "q": q}
