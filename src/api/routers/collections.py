from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query
from sqlmodel import Session

from ..database import crud, db
from ..models import AllianceOut, CollectionCreate9, CollectionOut, UserOut
from ..models.converters import FromDB, ToDB
from ..models.enums import ParameterInterval

router: APIRouter = APIRouter(tags=["collections"], prefix="/collections")


@router.get("/")
async def get_collections(
    from_date: Annotated[Optional[datetime], Query(alias="fromDate")] = None,
    to_date: Annotated[Optional[datetime], Query(alias="toDate")] = None,
    interval: Annotated[Optional[ParameterInterval], Query()] = ParameterInterval.MONTHLY,
    desc: Annotated[Optional[bool], Query()] = False,
    skip: Annotated[Optional[int], Query(ge=0)] = 0,
    take: Annotated[Optional[int], Query(ge=1, le=100)] = 100,
    session: Session = Depends(db.get_session),
) -> list[CollectionOut]:
    collections = crud.get_collections(session, from_date, to_date, interval, desc, skip, take)
    result = [FromDB.to_collection(collection, False, False) for collection in collections]
    return result


@router.post("/")
async def create_collection(collection: Annotated[CollectionCreate9, Body()], session: Session = Depends(db.get_session)) -> CollectionOut:
    collection_db = ToDB.from_collection_9(collection)
    collection_db = crud.save_collection(session, collection_db)
    result = FromDB.to_collection(collection_db, False, False)
    return result


@router.delete("/{collection_id}")
async def delete_collection(collection_id: Annotated[int, Path(ge=0)], session: Session = Depends(db.get_session)) -> None:
    crud.delete_collection_by_id(session, collection_id)


@router.get("/{collection_id}")
async def get_collection(collection_id: Annotated[int, Path(ge=0)], session: Session = Depends(db.get_session)) -> CollectionOut:
    collection = crud.get_collection(session, collection_id, True, True)
    if not collection:
        raise HTTPException(404, f"A collection with the ID `{collection_id}` was not found.")

    result = FromDB.to_collection(collection, True, True)
    return result


@router.get("/{collection_id}/alliances")
async def get_alliances_from_collection(collection_id: Annotated[int, Path(ge=0)], session: Session = Depends(db.get_session)) -> list[AllianceOut]:
    collection = crud.get_collection(session, collection_id, True, False)
    if not collection:
        raise HTTPException(404, f"A collection with the ID `{collection_id}` was not found.")

    result = FromDB.to_collection(collection, True, False)
    return result


@router.get("/{collection_id}/alliances/{alliance_id}")
async def get_alliance_from_collection(collection_id: Annotated[int, Path(ge=0)], alliance_id: Annotated[int, Path(ge=0)], session: Session = Depends(db.get_session)) -> AllianceOut:
    if not crud.has_collection(session, collection_id):
        raise HTTPException(404, f"A collection with the ID `{collection_id}` was not found.")

    alliance = crud.get_alliance_from_collection(session, collection_id, alliance_id, True)
    if not alliance:
        raise HTTPException(404, f"An alliance with the ID `{alliance_id}` was not found in the collection with the ID `{collection_id}`.")

    result = FromDB.to_alliance(alliance)
    return result


@router.get("/{collection_id}/top100Users")
async def get_top_100_from_collection(
    collection_id: Annotated[int, Path(ge=0)], skip: Annotated[Optional[int], Query(ge=0)] = 0, take: Annotated[Optional[int], Query(ge=1, le=100)] = 100, session: Session = Depends(db.get_session)
) -> list[UserOut]:
    if not crud.has_collection(session, collection_id):
        raise HTTPException(404, f"A collection with the ID `{collection_id}` was not found.")

    users = crud.get_top_100_from_collection(session, collection_id, skip, take)
    result = [FromDB.to_user(user) for user in users]
    return result


@router.get("/{collection_id}/users")
async def get_users_from_collection(collection_id: Annotated[int, Path(ge=0)], session: Session = Depends(db.get_session)) -> list[UserOut]:
    if not crud.has_collection(session, collection_id):
        raise HTTPException(404, f"A collection with the ID `{collection_id}` was not found.")

    collection = crud.get_collection(session, collection_id, False, True)
    result = FromDB.to_collection(collection, False, True)
    return result


@router.get("/{collection_id}/users/{user_id}")
async def get_user_from_collection(collection_id: Annotated[int, Path(ge=0)], user_id: Annotated[int, Path(ge=0)], session: Session = Depends(db.get_session)) -> UserOut:
    if not crud.has_collection(session, collection_id):
        raise HTTPException(404, f"A collection with the ID `{collection_id}` was not found.")

    user = crud.get_user_from_collection(session, collection_id, user_id, True)
    if not user:
        raise HTTPException(404, f"A user with the ID `{user_id}` was not found in the collection with the ID `{collection_id}`.")

    result = FromDB.to_user(user)
    return result
