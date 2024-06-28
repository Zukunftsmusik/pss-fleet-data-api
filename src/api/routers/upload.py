from typing import Annotated

from fastapi import APIRouter, Depends, File
from sqlmodel.ext.asyncio.session import AsyncSession

from ..database import crud, db
from ..models import CollectionCreate3, CollectionCreate4, CollectionCreate5, CollectionCreate6, CollectionCreate7, CollectionCreate8, CollectionCreate9, CollectionOut
from ..models.converters import FromDB, ToDB

router: APIRouter = APIRouter(tags=["upload"], prefix="/upload")


@router.post("3")
async def schema_version_3(collection: Annotated[CollectionCreate3, File()], session: AsyncSession = Depends(db.get_session)) -> CollectionOut:
    """Use this endpoint to upload JSON files of schema versions 3 or below."""
    collection_db = ToDB.from_collection_3(collection)
    collection_db = await crud.save_collection(session, collection_db)
    result = FromDB.to_collection(collection_db, False, False)
    return result


@router.post("4")
async def schema_version_4(collection: Annotated[CollectionCreate4, File()], session: AsyncSession = Depends(db.get_session)) -> CollectionOut:
    """Use this endpoint to upload JSON files of schema version 4."""
    collection_db = ToDB.from_collection_4(collection)
    collection_db = await crud.save_collection(session, collection_db)
    result = FromDB.to_collection(collection_db, False, False)
    return result


@router.post("5")
async def schema_version_5(collection: Annotated[CollectionCreate5, File()], session: AsyncSession = Depends(db.get_session)) -> CollectionOut:
    """Use this endpoint to upload JSON files of schema version 5."""
    collection_db = ToDB.from_collection_5(collection)
    collection_db = await crud.save_collection(session, collection_db)
    result = FromDB.to_collection(collection_db, False, False)
    return result


@router.post("6")
async def schema_version_6(collection: Annotated[CollectionCreate6, File()], session: AsyncSession = Depends(db.get_session)) -> CollectionOut:
    """Use this endpoint to upload JSON files of schema version 6."""
    collection_db = ToDB.from_collection_6(collection)
    collection_db = await crud.save_collection(session, collection_db)
    result = FromDB.to_collection(collection_db, False, False)
    return result


@router.post("7")
async def schema_version_7(collection: Annotated[CollectionCreate7, File()], session: AsyncSession = Depends(db.get_session)) -> CollectionOut:
    """Use this endpoint to upload JSON files of schema version 7."""
    collection_db = ToDB.from_collection_7(collection)
    collection_db = await crud.save_collection(session, collection_db)
    result = FromDB.to_collection(collection_db, False, False)
    return result


@router.post("8")
async def schema_version_8(collection: Annotated[CollectionCreate8, File()], session: AsyncSession = Depends(db.get_session)) -> CollectionOut:
    """Use this endpoint to upload JSON files of schema version 8."""
    collection_db = ToDB.from_collection_8(collection)
    collection_db = await crud.save_collection(session, collection_db)
    result = FromDB.to_collection(collection_db, False, False)
    return result


@router.post("9")
async def schema_version_9(collection: Annotated[CollectionCreate9, File()], session: AsyncSession = Depends(db.get_session)) -> CollectionOut:
    """Use this endpoint to upload JSON files of schema version 9."""
    collection_db = ToDB.from_collection_9(collection)
    collection_db = await crud.save_collection(session, collection_db)
    result = FromDB.to_collection(collection_db, False, False)
    return result
