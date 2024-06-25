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
    skip: Annotated[Optional[int], Query(ge=0)] = 0,
    take: Annotated[Optional[int], Query(ge=1, le=100)] = 100,
    interval: Annotated[Optional[ParameterInterval], Query()] = ParameterInterval.MONTHLY,
    session: Session = Depends(db.get_session),
) -> list[CollectionOut]:
    collections = crud.get_collections(session, None, None, interval, None, skip, take)
    result = [FromDB.to_collection(collection, include_alliances=False, include_users=False) for collection in collections]
    return result


@router.post("/")
async def create_collection(collection: Annotated[CollectionCreate9, Body()], session: Session = Depends(db.get_session)) -> CollectionOut:
    collection_db = ToDB.from_collection_9(collection)
    collection_db = crud.save_collection(session, collection_db)
    result = FromDB.to_collection(collection_db, include_alliances=False, include_users=False)
    return result


@router.delete("/{collection_id}")
async def delete_collection(collection_id: Annotated[int, Path(ge=0)], session: Session = Depends(db.get_session)) -> None:
    crud.delete_collection_by_id(session, collection_id)


@router.get("/{collection_id}")
async def get_collection(collection_id: Annotated[int, Path(ge=0)], session: Session = Depends(db.get_session)) -> CollectionOut:
    collection = crud.get_collection(session, collection_id)
    if not collection:
        raise HTTPException(404, f"A collection with the ID `{collection_id}` was not found.")

    result = FromDB.to_collection(collection)
    return result


@router.get("/{collection_id}/alliances")
async def get_alliances_from_collection(collection_id: Annotated[int, Path(ge=0)], session: Session = Depends(db.get_session)) -> list[AllianceOut]:
    if not crud.has_collection(session, collection_id):
        raise HTTPException(404, f"A collection with the ID `{collection_id}` was not found.")

    collection = crud.get_collection(session, collection_id, include_users=False)
    result = FromDB.to_collection(collection)
    return result


@router.get("/{collection_id}/alliances/{alliance_id}")
async def get_alliance_from_collection(collection_id: Annotated[int, Path(ge=0)], alliance_id: Annotated[int, Path(ge=0)], session: Session = Depends(db.get_session)) -> AllianceOut:
    if not crud.has_collection(session, collection_id):
        raise HTTPException(404, f"A collection with the ID `{collection_id}` was not found.")

    alliance = crud.get_alliance_from_collection(collection_id, alliance_id)
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

    users = crud.get_top_100_from_collection(collection_id, skip, take)
    result = [FromDB.to_user(user) for user in users]
    return result


@router.get("/{collection_id}/users")
async def get_users_from_collection(collection_id: Annotated[int, Path(ge=0)], session: Session = Depends(db.get_session)) -> list[UserOut]:
    if not crud.has_collection(session, collection_id):
        raise HTTPException(404, f"A collection with the ID `{collection_id}` was not found.")

    collection = crud.get_collection(session, collection_id, include_alliances=False)
    result = FromDB.to_collection(collection)
    return result


@router.get("/{collection_id}/users/{user_id}")
async def get_user_from_collection(collection_id: Annotated[int, Path(ge=0)], user_id: Annotated[int, Path(ge=0)], session: Session = Depends(db.get_session)) -> UserOut:
    if not crud.has_collection(session, collection_id):
        raise HTTPException(404, f"A collection with the ID `{collection_id}` was not found.")

    user = crud.get_user_from_collection(collection_id, user_id)
    if not user:
        raise HTTPException(404, f"A user with the ID `{user_id}` was not found in the collection with the ID `{collection_id}`.")

    result = FromDB.to_alliance(user)
    return result
