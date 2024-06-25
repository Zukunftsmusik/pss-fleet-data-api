from typing import Annotated

from fastapi import APIRouter

from ..dependencies import *

router = APIRouter(tags=["collections"])


@router.delete(
    "/collections", response_model=None, responses={"401": {"model": ErrorList}, "403": {"model": ErrorList}, "429": {"model": ErrorList}, "500": {"model": ErrorList}}, tags=["collections"]
)
def delete_all_collections() -> Optional[ErrorList]:
    """
    Delete all Collections.
    """


@router.get("/collections", response_model=List[CollectionOut], responses={"400": {"model": ErrorList}, "429": {"model": ErrorList}, "500": {"model": ErrorList}}, tags=["collections"])
def get_collections_metadata(
    from_date: Optional[datetime] = Query("2016-01-06T00:00:00Z", alias="fromDate"),
    to_date: Optional[datetime] = Query(None, alias="toDate"),
    interval: Optional[EnumParamInterval] = None,
    desc: Optional[bool] = False,
    skip: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = 0,
    take: Optional[Annotated[int, conint(ge=0, le=100)]] = 100,
    metadata_properties: Optional[EnumParamMetadataProperties] = Query(None, alias="metadataProperties"),
) -> Union[List[CollectionOut], ErrorList]:
    """
    Get metadata of all Collections or a subset of Collections.
    """


@router.post(
    "/collections",
    response_model=None,
    responses={
        "201": {"model": CollectionOut},
        "400": {"model": ErrorList},
        "401": {"model": ErrorList},
        "403": {"model": ErrorList},
        "409": {"model": ErrorList},
        "415": {"model": ErrorList},
        "429": {"model": ErrorList},
        "500": {"model": ErrorList},
    },
    tags=["collections"],
)
def import_collection(body: CollectionCreate = None) -> Optional[Union[CollectionOut, ErrorList]]:
    """
    Create a new Collection from data schema version 4 or higher.
    """


@router.post(
    "/collections/uploadJson",
    response_model=None,
    responses={
        "201": {"model": CollectionOut},
        "400": {"model": ErrorList},
        "401": {"model": ErrorList},
        "403": {"model": ErrorList},
        "409": {"model": ErrorList},
        "415": {"model": ErrorList},
        "429": {"model": ErrorList},
        "500": {"model": ErrorList},
    },
    tags=["collections"],
)
def upload_collection(body: CollectionUpload = None) -> Optional[Union[CollectionOut, ErrorList]]:
    """
    Upload a collection file of schema version 4 or above.
    """


@router.delete(
    "/collections/{collection_id}",
    response_model=None,
    responses={"400": {"model": ErrorList}, "401": {"model": ErrorList}, "403": {"model": ErrorList}, "404": {"model": ErrorList}, "429": {"model": ErrorList}, "500": {"model": ErrorList}},
    tags=["collections"],
)
def delete_collection(collection_id: Annotated[int, conint(ge=0, le=9223372036854776000)] = Path(..., alias="collectionId")) -> Optional[ErrorList]:
    """
    Delete a specific Collection.
    """


@router.get(
    "/collections/{collection_id}",
    response_model=CollectionOut,
    responses={"400": {"model": ErrorList}, "404": {"model": ErrorList}, "429": {"model": ErrorList}, "500": {"model": ErrorList}},
    tags=["collections"],
)
def get_collection(
    collection_id: Annotated[int, conint(ge=0, le=9223372036854776000)] = Path(..., alias="collectionId"),
    metadata_properties: Optional[EnumParamMetadataProperties] = Query(None, alias="metadataProperties"),
    alliance_properties: Optional[EnumParamAllianceProperties] = Query(None, alias="allianceProperties"),
    user_properties: Optional[EnumParamUserProperties] = Query(None, alias="userProperties"),
) -> Union[CollectionOut, ErrorList]:
    """
    Get all data of a specific Collection.
    """


@router.put(
    "/collections/{collection_id}",
    response_model=CollectionOut,
    responses={
        "201": {"model": CollectionOut},
        "400": {"model": ErrorList},
        "401": {"model": ErrorList},
        "403": {"model": ErrorList},
        "409": {"model": ErrorList},
        "415": {"model": ErrorList},
        "429": {"model": ErrorList},
        "500": {"model": ErrorList},
    },
    tags=["collections"],
)
def update_collection(collection_id: Annotated[int, conint(ge=0, le=9223372036854776000)] = Path(..., alias="collectionId"), body: CollectionOut = None) -> Union[CollectionOut, ErrorList]:
    """
    Update or insert a specific Collection.
    """


@router.get(
    "/collections/{collection_id}/alliances",
    response_model=List[CollectionOut],
    responses={"400": {"model": ErrorList}, "404": {"model": ErrorList}, "429": {"model": ErrorList}, "500": {"model": ErrorList}},
    tags=["collections"],
)
def get_alliances(
    collection_id: Annotated[int, conint(ge=0, le=9223372036854776000)] = Path(..., alias="collectionId"),
    division_design_id: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Query(None, alias="divisionDesignId"),
    skip: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = 0,
    take: Optional[Annotated[int, conint(ge=0, le=100)]] = 100,
    alliance_properties: Optional[EnumParamAllianceProperties] = Query(None, alias="allianceProperties"),
    metadata_properties: Optional[EnumParamMetadataProperties] = Query(None, alias="metadataProperties"),
    user_properties: Optional[EnumParamUserProperties] = Query(None, alias="userProperties"),
) -> Union[List[CollectionOut], ErrorList]:
    """
    Get a list of Alliances from a specific Collection.
    """


@router.get(
    "/collections/{collection_id}/alliances/{alliance_id}",
    response_model=AllianceHistoryOut,
    responses={"400": {"model": ErrorList}, "404": {"model": ErrorList}, "429": {"model": ErrorList}, "500": {"model": ErrorList}},
    tags=["collections"],
)
def get_alliance(
    collection_id: Annotated[int, conint(ge=0, le=9223372036854776000)] = Path(..., alias="collectionId"),
    alliance_id: Annotated[int, conint(ge=0, le=2147483647)] = Path(..., alias="allianceId"),
    alliance_properties: Optional[EnumParamAllianceProperties] = Query(None, alias="allianceProperties"),
    metadata_properties: Optional[EnumParamMetadataProperties] = Query(None, alias="metadataProperties"),
    user_properties: Optional[EnumParamUserProperties] = Query(None, alias="userProperties"),
) -> Union[AllianceHistoryOut, ErrorList]:
    """
    Get a specific Alliance from a specific Collection.
    """


@router.get(
    "/collections/{collection_id}/top100Users",
    response_model=List[CollectionOut],
    responses={"400": {"model": ErrorList}, "404": {"model": ErrorList}, "429": {"model": ErrorList}, "500": {"model": ErrorList}},
    tags=["collections"],
)
def get_top100_users(
    collection_id: Annotated[int, conint(ge=0, le=9223372036854776000)] = Path(..., alias="collectionId"),
    desc: Optional[bool] = False,
    skip: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = 0,
    take: Optional[Annotated[int, conint(ge=0, le=100)]] = 100,
    alliance_properties: Optional[EnumParamAllianceProperties] = Query(None, alias="allianceProperties"),
    metadata_properties: Optional[EnumParamMetadataProperties] = Query(None, alias="metadataProperties"),
    user_properties: Optional[EnumParamUserProperties] = Query(None, alias="userProperties"),
) -> Union[List[CollectionOut], ErrorList]:
    """
    Get top 100 Users from a specific Collection.
    """


@router.get(
    "/collections/{collection_id}/users",
    response_model=List[CollectionOut],
    responses={"400": {"model": ErrorList}, "404": {"model": ErrorList}, "429": {"model": ErrorList}, "500": {"model": ErrorList}},
    tags=["collections"],
)
def get_users(
    collection_id: Annotated[int, conint(ge=0, le=9223372036854776000)] = Path(..., alias="collectionId"),
    division_design_id: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = Query(None, alias="divisionDesignId"),
    skip: Optional[Annotated[int, conint(ge=0, le=2147483647)]] = 0,
    take: Optional[Annotated[int, conint(ge=0, le=100)]] = 100,
    alliance_properties: Optional[EnumParamAllianceProperties] = Query(None, alias="allianceProperties"),
    metadata_properties: Optional[EnumParamMetadataProperties] = Query(None, alias="metadataProperties"),
    user_properties: Optional[EnumParamUserProperties] = Query(None, alias="userProperties"),
) -> Union[List[CollectionOut], ErrorList]:
    """
    Get a list of Users from a specific Collection.
    """


@router.get(
    "/collections/{collection_id}/users/{user_id}",
    response_model=UserHistoryOut,
    responses={"400": {"model": ErrorList}, "404": {"model": ErrorList}, "429": {"model": ErrorList}, "500": {"model": ErrorList}},
    tags=["collections"],
)
def get_user(
    collection_id: Annotated[int, conint(ge=0, le=9223372036854776000)] = Path(..., alias="collectionId"),
    user_id: Annotated[int, conint(ge=0, le=2147483647)] = Path(..., alias="userId"),
    alliance_properties: Optional[EnumParamAllianceProperties] = Query(None, alias="allianceProperties"),
    user_properties: Optional[EnumParamUserProperties] = Query(None, alias="userProperties"),
) -> Union[UserHistoryOut, ErrorList]:
    """
    Get a specific User from a specific Collection.
    """
