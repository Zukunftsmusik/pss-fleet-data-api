import json
from typing import Annotated, Union

from fastapi import APIRouter, Body, Depends, File, UploadFile
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession

from ..database import crud, db
from ..database.models import CollectionDB
from ..models import (
    AllianceHistoryOut,
    CollectionCreate3,
    CollectionCreate4,
    CollectionCreate5,
    CollectionCreate6,
    CollectionCreate7,
    CollectionCreate8,
    CollectionCreate9,
    CollectionMetadataOut,
    CollectionOut,
    CollectionWithFleetsOut,
    CollectionWithUsersOut,
    UserHistoryOut,
)
from ..models.converters import FromDB, ToDB
from . import dependencies, endpoints, exceptions


router: APIRouter = APIRouter(tags=["collections"], prefix="/collections")


@router.get("/", **endpoints.collections_get)
async def get_collections(
    datetime_filter: Annotated[dependencies.DatetimeFilter, Depends(dependencies.from_to_date_parameters)],
    list_filter: Annotated[dependencies.ListFilter, Depends(dependencies.list_filter_parameters)],
    skip_take: Annotated[dependencies.SkipTakeFilter, Depends(dependencies.skip_take_parameters)],
    session: AsyncSession = Depends(db.get_session),
) -> list[CollectionMetadataOut]:
    collections = await crud.get_collections(
        session, datetime_filter.from_date, datetime_filter.to_date, list_filter.interval, list_filter.desc, skip_take.skip, skip_take.take
    )
    result = [FromDB.to_collection(collection, False, False).meta for collection in collections]
    return result


@router.post("/", **endpoints.collections_post, dependencies=dependencies.authorization_dependencies)
async def create_collection(
    collection: Annotated[CollectionCreate9, Body()], session: AsyncSession = Depends(db.get_session)
) -> CollectionMetadataOut:
    collection_with_same_timestamp = await crud.get_collection_by_timestamp(session, collection.meta.timestamp)
    if collection_with_same_timestamp is not None:
        raise exceptions.non_unique_timestamp(collection.meta.timestamp, collection_with_same_timestamp.collection_id)

    collection_db = ToDB.from_collection_9(collection)
    collection_db = await crud.save_collection(session, collection_db, True, True)
    result = FromDB.to_collection(collection_db, False, False)
    return result.meta


@router.delete("/{collectionId}", **endpoints.collections_collectionId_delete, dependencies=dependencies.authorization_dependencies)
async def delete_collection(
    collection_id: Annotated[int, Depends(dependencies.collection_id)], session: AsyncSession = Depends(db.get_session)
) -> None:
    collection_exists = await crud.has_collection(session, collection_id)
    if not collection_exists:
        raise exceptions.collection_not_found(collection_id)

    deleted = await crud.delete_collection(session, collection_id)

    if not deleted:
        raise exceptions.collection_not_deleted(collection_id)


@router.get("/{collectionId}", **endpoints.collections_collectionId_get)
async def get_collection(
    collection_id: Annotated[int, Depends(dependencies.collection_id)], session: AsyncSession = Depends(db.get_session)
) -> CollectionOut:
    collection = await crud.get_collection(session, collection_id, True, True)
    if not collection:
        raise exceptions.collection_not_found(collection_id)

    result = FromDB.to_collection(collection, True, True)
    return result


@router.get("/{collectionId}/alliances", **endpoints.collections_collectionId_alliances_get)
async def get_alliances_from_collection(
    collection_id: Annotated[int, Depends(dependencies.collection_id)], session: AsyncSession = Depends(db.get_session)
) -> CollectionWithFleetsOut:
    collection_exists = await crud.has_collection(session, collection_id)
    if not collection_exists:
        raise exceptions.collection_not_found(collection_id)

    collection = await crud.get_collection(session, collection_id, True, False)
    result = FromDB.to_collection_with_fleets(collection)
    return result


@router.get("/{collectionId}/alliances/{allianceId}", **endpoints.collections_collectionId_alliances_allianceId_get)
async def get_alliance_from_collection(
    collection_id: Annotated[int, Depends(dependencies.collection_id)],
    alliance_id: Annotated[int, Depends(dependencies.alliance_id)],
    session: AsyncSession = Depends(db.get_session),
) -> AllianceHistoryOut:
    collection_exists = await crud.has_collection(session, collection_id)
    if not collection_exists:
        raise exceptions.collection_not_found(collection_id)

    alliance_history = await crud.get_alliance_from_collection(session, collection_id, alliance_id)
    if not alliance_history:
        raise exceptions.alliance_not_found_in_collection(collection_id, alliance_id)

    result = FromDB.to_alliance_history(alliance_history)
    return result


@router.get("/{collectionId}/top100Users", **endpoints.collections_collectionId_top100Users_get)
async def get_top_100_from_collection(
    collection_id: Annotated[int, Depends(dependencies.collection_id)],
    skip_take: Annotated[dependencies.SkipTakeFilter, Depends(dependencies.skip_take_parameters)],
    session: AsyncSession = Depends(db.get_session),
) -> CollectionWithUsersOut:
    collection_exists = await crud.has_collection(session, collection_id)
    if not collection_exists:
        raise exceptions.collection_not_found(collection_id)

    collection = await crud.get_collection(session, collection_id, False, False)
    users = await crud.get_top_100_from_collection(session, collection_id, skip_take.skip, skip_take.take)
    collection.users = list(users)
    result = FromDB.to_collection_with_users(collection)
    return result


@router.get("/{collectionId}/users", **endpoints.collections_collectionId_users_get)
async def get_users_from_collection(
    collection_id: Annotated[int, Depends(dependencies.collection_id)], session: AsyncSession = Depends(db.get_session)
) -> CollectionWithUsersOut:
    collection_exists = await crud.has_collection(session, collection_id)
    if not collection_exists:
        raise exceptions.collection_not_found(collection_id)

    collection = await crud.get_collection(session, collection_id, False, True)
    result = FromDB.to_collection(collection, False, True)
    return result


@router.get("/{collectionId}/users/{userId}", **endpoints.collections_collectionId_users_userId_get)
async def get_user_from_collection(
    collection_id: Annotated[int, Depends(dependencies.collection_id)],
    user_id: Annotated[int, Depends(dependencies.user_id)],
    session: AsyncSession = Depends(db.get_session),
) -> UserHistoryOut:
    collection_exists = await crud.has_collection(session, collection_id)
    if not collection_exists:
        raise exceptions.collection_not_found(collection_id)

    user_history = await crud.get_user_from_collection(session, collection_id, user_id)
    if not user_history:
        raise exceptions.user_not_found_in_collection(collection_id, user_id)

    result = FromDB.to_user_history(user_history)
    return result


schema_version_to_create_class = {
    3: CollectionCreate3,
    4: CollectionCreate4,
    5: CollectionCreate5,
    6: CollectionCreate6,
    7: CollectionCreate7,
    8: CollectionCreate8,
    9: CollectionCreate9,
}

schema_version_to_converter = {
    3: ToDB.from_collection_3,
    4: ToDB.from_collection_4,
    5: ToDB.from_collection_5,
    6: ToDB.from_collection_6,
    7: ToDB.from_collection_7,
    8: ToDB.from_collection_8,
    9: ToDB.from_collection_9,
}


@router.post("/upload", **endpoints.collections_upload_post, dependencies=dependencies.authorization_dependencies)
async def upload_collection(
    collection_file: Annotated[UploadFile, File(media_type="application/json")], session: AsyncSession = Depends(db.get_session)
) -> CollectionMetadataOut:
    collection_db = await convert_uploaded_file(collection_file)

    collection_with_same_timestamp = await crud.get_collection_by_timestamp(session, collection_db.collected_at)
    if collection_with_same_timestamp is not None:
        raise exceptions.non_unique_timestamp(collection_db.collected_at, collection_with_same_timestamp.collection_id)

    collection_db = await crud.save_collection(session, collection_db, True, True)

    result = FromDB.to_collection(collection_db, False, False).meta
    return result


@router.put("/upload/{collectionId}", **endpoints.collections_update_put, dependencies=dependencies.authorization_dependencies)
async def update_collection(
    collection_id: Annotated[int, Depends(dependencies.collection_id)],
    collection_file: Annotated[UploadFile, File(media_type="application/json")],
    session: AsyncSession = Depends(db.get_session),
) -> CollectionMetadataOut:
    if not (await crud.has_collection(session, collection_id)):
        raise exceptions.collection_not_found(collection_id)

    collection_in = await convert_uploaded_file(collection_file)
    collection_db = await crud.get_collection(session, collection_id, True, True)

    if collection_db.collected_at != collection_in.collected_at:
        raise exceptions.collected_at_not_match(collection_in.collected_at, collection_db.collected_at, collection_id)

    collection_in = await crud.update_collection(session, collection_id, collection_in)

    result = FromDB.to_collection(collection_in, False, False).meta
    return result


async def convert_uploaded_file(uploaded_file: UploadFile) -> CollectionDB:
    file_contents = await uploaded_file.read()
    try:
        decoded_json: dict[str, Union[dict[str, Union[bool, float, int, str]], list[list]]] = json.loads(file_contents)
    except json.decoder.JSONDecodeError as json_decoder_error:
        raise exceptions.invalid_json_upload(json_decoder_error) from json_decoder_error

    metadata = decoded_json.get("meta")
    if metadata:
        expected_schema_version = int(metadata.get("schema_version", 3))
    else:
        raise exceptions.unsupported_schema()

    collection_create_class = schema_version_to_create_class[expected_schema_version]
    try:
        collection = collection_create_class(**decoded_json)
    except ValidationError as validation_error:
        raise exceptions.schema_version_mismatch(expected_schema_version, validation_error) from validation_error

    to_db_converter_func = schema_version_to_converter[expected_schema_version]
    collection_db = to_db_converter_func(collection)
    return collection_db


__all__ = [
    "router",
]
