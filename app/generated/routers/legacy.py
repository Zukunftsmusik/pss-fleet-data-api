from fastapi import APIRouter

from ..dependencies import *

router = APIRouter(tags=["legacy"])


@router.post(
    "/legacy/collections",
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
    tags=["legacy"],
)
def create_legacy_collection(body: LegacyCollectionCreate = None) -> Optional[Union[CollectionOut, ErrorList]]:
    """
    Create a new Collection from data schema version 3 or lower.
    """


@router.post(
    "/legacy/collections/uploadJson",
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
    tags=["legacy"],
)
def upload_legacy_collection(body: LegacyCollectionUpload = None) -> Optional[Union[CollectionOut, ErrorList]]:
    """
    Upload a collection file of schema version 3 or below.
    """
