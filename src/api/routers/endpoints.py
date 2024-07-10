from fastapi import status

from ..models.endpoint import EndpointDefinition
from ..models.enums import OperationId
from . import links, responses


_collections_post_response_201 = {
    "description": "A Collection has been created. Returns inserted Collection metadata including new Collection ID. Doesn't include inserted Alliances or Users.",
    "links": {
        OperationId.DELETE_COLLECTION: links.collections_deleteCollectionAfterInsert,
        OperationId.GET_ALLIANCES_FROM_COLLECTION: links.collections_getAlliancesFromCollectionAfterInsert,
        OperationId.GET_COLLECTION: links.collections_getCollectionAfterInsert,
        OperationId.GET_TOP_100_USERS_FROM_COLLECTION: links.collections_getUsersFromCollectionAfterInsert,
        OperationId.GET_USERS_FROM_COLLECTION: links.collections_getUsersFromCollectionAfterInsert,
    },
}


allianceHistory_allianceId_get = EndpointDefinition(
    summary="Get an Alliance's history.",
    description="Get the complete history or a subset of the history of a specific Alliance. You can use the parameters to limit the result set.",
    operation_id=OperationId.GET_ALLIANCE_HISTORY,
    status_code=status.HTTP_200_OK,
    response_description="A list of objects denoting the requested Alliance at a specific point in time.",
    responses={
        **responses.get_default_responses_for_get(
            include_204=True,
            include_404=True,
            description_404="The requested Alliance could not be found.",
        ),
        status.HTTP_200_OK: {
            "description": "A list of objects denoting the requested Alliance at a specific point in time.",
            "links": {
                OperationId.GET_ALLIANCE_FROM_COLLECTION: links.allianceHistory_getAllianceFromCollection,
                OperationId.GET_USER_FROM_COLLECTION: links.allianceHistory_getUserFromCollection,
                OperationId.GET_USER_HISTORY: links.allianceHistory_getUserHistory,
                **links.default_entity_history_links,
            },
        },
    },
)


collections_get = EndpointDefinition(
    summary="Get metadata of all Collections or a subset of Collections.",
    description="Get the metadata of a subset of all Collections. You can use the parameters to limit the result set.",
    operation_id=OperationId.GET_COLLECTION,
    status_code=status.HTTP_200_OK,
    response_description="A list of Collection Metadata objects.",
    responses={
        **responses.get_default_responses_for_get(
            include_204=True,
        ),
        status.HTTP_200_OK: {
            "description": "A list of Collection Metadata objects.",
            "links": {
                OperationId.DELETE_COLLECTION: links.collections_deleteCollection,
                OperationId.GET_ALLIANCES_FROM_COLLECTION: links.collections_getAlliancesFromCollection,
                OperationId.GET_COLLECTION: links.collections_getCollection,
                OperationId.GET_TOP_100_USERS_FROM_COLLECTION: links.collections_getTop100UsersFromCollection,
                OperationId.GET_USERS_FROM_COLLECTION: links.collections_getUsersFromCollection,
            },
        },
    },
)


collections_post = EndpointDefinition(
    summary="Create a new Collection from data schema version 9.",
    description="Insert Collection data into the database that was created with data schema version 9. See https://github.com/Zukunftsmusik/pss-fleet-data/blob/master/readme.md for a description of the expected schema.",
    operation_id=OperationId.CREATE_COLLECTION,
    status_code=status.HTTP_201_CREATED,
    response_description="A Collection has been created. Returns inserted Collection metadata including new Collection ID. Doesn't include inserted Alliances or Users.",
    responses={
        **responses.get_default_responses_for_get(),
        **responses.get_default_responses(
            status.HTTP_409_CONFLICT,
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        ),
        status.HTTP_201_CREATED: _collections_post_response_201,
    },
)


collections_collectionId_delete = EndpointDefinition(
    summary="Delete a specific Collection.",
    description="Delete a specific data Collection.",
    operation_id=OperationId.DELETE_COLLECTION,
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="The Collection with the specified ID got deleted.",
    responses={
        **responses.get_default_responses_for_get(
            include_204=True,
            description_204="The Collection with the specified ID got deleted.",
            include_404=True,
            description_404="The requested Collection could not be found.",
        ),
    },
)


collections_collectionId_get = EndpointDefinition(
    summary="Get all data of a specific Collection.",
    description="Get all data from a specific data Collection.",
    operation_id=OperationId.GET_COLLECTION,
    status_code=status.HTTP_200_OK,
    response_description="The requested Collection's metadata, Alliances and Users with the specified metadata, Alliance and User properties.",
    responses={
        **responses.get_default_responses_for_get(
            include_404=True,
            description_404="The requested Collection could not be found.",
        ),
        status.HTTP_200_OK: {
            "description": "The requested Collection's metadata, Alliances and Users with the specified metadata, Alliance and User properties.",
            "links": {
                OperationId.DELETE_COLLECTION: links.collection_deleteCollection,
                OperationId.GET_ALLIANCE_HISTORY: links.collection_getAllianceHistory,
                OperationId.GET_ALLIANCE_FROM_COLLECTION: links.collection_getAllianceFromCollection,
                OperationId.GET_ALLIANCES_FROM_COLLECTION: links.collection_getAlliancesFromCollection,
                OperationId.GET_TOP_100_USERS_FROM_COLLECTION: links.collection_getTop100UsersFromCollection,
                OperationId.GET_USER_FROM_COLLECTION: links.collection_getUserFromCollection,
                OperationId.GET_USERS_FROM_COLLECTION: links.collection_getUsersFromCollection,
                OperationId.GET_USER_HISTORY: links.collection_getUserHistory,
            },
        },
    },
)


collections_collectionId_alliances_get = EndpointDefinition(
    summary="Get a list of Alliances from a specific Collection.",
    description="Get all Alliance data of a specific Collections or of a subset of the Alliance data. You can use the parameters to limit the result set.",
    operation_id=OperationId.GET_ALLIANCES_FROM_COLLECTION,
    status_code=status.HTTP_200_OK,
    response_description="Returns the Collection with a list of Alliances. Does not include Users.",
    responses={
        **responses.get_default_responses_for_get(
            include_204=True,
            description_204="The requested Collection doesn't contain any Alliance data.",
            include_404=True,
            description_404="The requested Collection could not be found.",
        ),
        status.HTTP_200_OK: {
            "description": "Returns the Collection with a list of Alliances. Does not include Users.",
            "links": {
                OperationId.DELETE_COLLECTION: links.collection_deleteCollection,
                OperationId.GET_ALLIANCE_HISTORY: links.collection_alliance_getAllianceHistory,
                OperationId.GET_ALLIANCE_FROM_COLLECTION: links.collection_alliances_getAllianceFromCollection,
                OperationId.GET_COLLECTION: links.collection_getCollection,
                OperationId.GET_TOP_100_USERS_FROM_COLLECTION: links.collection_getTop100UsersFromCollection,
                OperationId.GET_USERS_FROM_COLLECTION: links.collection_getUsersFromCollection,
            },
        },
    },
)


collections_collectionId_alliances_allianceId_get = EndpointDefinition(
    summary="Get a specific Alliance from a specific Collection.",
    description="Get the data for a specific Alliances from a specific data Collection. Includes its members.",
    operation_id=OperationId.GET_ALLIANCE_FROM_COLLECTION,
    status_code=status.HTTP_200_OK,
    response_description="Returns the requested Alliance and related Users with the specified Alliance and User properties.",
    responses={
        **responses.get_default_responses_for_get(
            include_404=True,
            description_404="The requested Collection could not be found or the requested Alliance could not be found in the requested Collection.",
        ),
        status.HTTP_200_OK: {
            "description": "Returns the requested Alliance and related Users with the specified Alliance and User properties.",
            "links": {
                OperationId.DELETE_COLLECTION: links.collection_deleteCollection,
                OperationId.GET_ALLIANCE_HISTORY: links.collection_alliance_getAllianceHistory,
                OperationId.GET_ALLIANCES_FROM_COLLECTION: links.collection_getAllianceFromCollection,
                OperationId.GET_COLLECTION: links.collection_getCollection,
                OperationId.GET_TOP_100_USERS_FROM_COLLECTION: links.collection_getTop100UsersFromCollection,
                OperationId.GET_USERS_FROM_COLLECTION: links.collection_getUsersFromCollection,
                OperationId.GET_USER_FROM_COLLECTION: links.collection_alliance_getUserFromCollection,
                OperationId.GET_USER_HISTORY: links.collection_alliance_getUserHistory,
            },
        },
    },
)


collections_collectionId_top100Users_get = EndpointDefinition(
    summary="Get top 100 Users from a specific Collection.",
    description="Get top 100 Users or a subset of top 100 Users from a specific Collection. You can use the parameters to limit the result set.",
    operation_id=OperationId.GET_TOP_100_USERS_FROM_COLLECTION,
    status_code=status.HTTP_200_OK,
    response_description="Returns the Collection with a list of top 100 Users. Doesn't includes the Alliances.",
    responses={
        **responses.get_default_responses_for_get(
            include_204=True,
            description_204="The requested Collection doesn't contain any User data.",
            include_404=True,
            description_404="The requested Collection could not be found.",
        ),
        status.HTTP_200_OK: {
            "description": "Returns the Collection with a list of top 100 Users. Doesn't includes the Alliances.",
            "links": {
                OperationId.DELETE_COLLECTION: links.collection_deleteCollection,
                OperationId.GET_ALLIANCES_FROM_COLLECTION: links.collection_getAlliancesFromCollection,
                OperationId.GET_USER_FROM_COLLECTION: links.collection_getUserFromCollection,
                OperationId.GET_USERS_FROM_COLLECTION: links.collection_getUsersFromCollection,
                OperationId.GET_USER_HISTORY: links.collection_getUserHistory,
            },
        },
    },
)


collections_collectionId_users_get = EndpointDefinition(
    summary="Get a list of Users from a specific Collection.",
    description="Get all User data of a specific Collections or of a subset of the User data. You can use the parameters to limit the result set.",
    operation_id=OperationId.GET_USERS_FROM_COLLECTION,
    status_code=status.HTTP_200_OK,
    response_description="Returns the Collection with a list of Users. Does not include Alliances.",
    responses={
        **responses.get_default_responses_for_get(
            include_204=True,
            description_204="The requested Collection doesn't contain any User data.",
            include_404=True,
            description_404="The requested Collection could not be found.",
        ),
        status.HTTP_200_OK: {
            "description": "Returns the Collection with a list of Users. Does not include Alliances.",
            "links": {
                OperationId.DELETE_COLLECTION: links.collection_deleteCollection,
                OperationId.GET_ALLIANCE_HISTORY: links.collection_getAllianceHistory,
                OperationId.GET_ALLIANCE_FROM_COLLECTION: links.collection_getAllianceFromCollection,
                OperationId.GET_ALLIANCES_FROM_COLLECTION: links.collection_getAlliancesFromCollection,
                OperationId.GET_TOP_100_USERS_FROM_COLLECTION: links.collection_getTop100UsersFromCollection,
                OperationId.GET_USER_FROM_COLLECTION: links.collection_users_getUserFromCollection,
                OperationId.GET_USER_HISTORY: links.collection_users_getUserHistory,
            },
        },
    },
)


collections_collectionId_users_userId_get = EndpointDefinition(
    summary="Get a specific User from a specific Collection.",
    description="Get the data for a specific User from a specific data Collection.",
    operation_id=OperationId.GET_USER_FROM_COLLECTION,
    status_code=status.HTTP_200_OK,
    response_description="Returns the requested User, its Alliance and the corresponding Collection metadata.",
    responses={
        **responses.get_default_responses_for_get(
            include_404=True,
            description_404="The requested Collection could not be found or the requested User could not be found in the requested Collection.",
        ),
        status.HTTP_200_OK: {
            "description": "Returns the requested User, its Alliance and the corresponding Collection metadata.",
            "links": {
                OperationId.DELETE_COLLECTION: links.collection_deleteCollection,
                OperationId.GET_ALLIANCE_HISTORY: links.collection_user_getAllianceHistory,
                OperationId.GET_ALLIANCE_FROM_COLLECTION: links.collection_user_getAllianceFromCollection,
                OperationId.GET_ALLIANCES_FROM_COLLECTION: links.collection_getAlliancesFromCollection,
                OperationId.GET_COLLECTION: links.collection_getCollection,
                OperationId.GET_TOP_100_USERS_FROM_COLLECTION: links.collection_getTop100UsersFromCollection,
                OperationId.GET_USERS_FROM_COLLECTION: links.collection_getUsersFromCollection,
                OperationId.GET_USER_HISTORY: links.collection_user_getUserHistory,
            },
        },
    },
)


collections_upload_post = EndpointDefinition(
    summary="Upload a collection file.",
    description="Upload a JSON file containing a complete data Collection that was created with the schema version 3 or higher.",
    operation_id=OperationId.UPLOAD_COLLECTION,
    status_code=status.HTTP_201_CREATED,
    response_description="A Collection has been created. Returns inserted Collection metadata including new Collection ID. Does not include inserted Alliances or Users.",
    responses={
        **responses.get_default_responses_for_get(),
        **responses.get_default_responses(
            status.HTTP_409_CONFLICT,
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        ),
        status.HTTP_201_CREATED: _collections_post_response_201,
    },
)


userHistory_userId_get = EndpointDefinition(
    summary="Get an User's history.",
    description="Get the complete history or a subset of the history of a specific User. You can use the parameters to limit the result set.",
    operation_id=OperationId.GET_USER_HISTORY,
    status_code=status.HTTP_200_OK,
    response_description="A list of objects denoting the requested User at a specific point in time.",
    responses={
        **responses.get_default_responses_for_get(
            include_204=True,
            include_404=True,
            description_404="The requested User could not be found.",
        ),
        status.HTTP_200_OK: {
            "description": "A list of objects denoting the requested User at a specific point in time.",
            "links": {
                OperationId.GET_ALLIANCE_HISTORY: links.userHistory_getAllianceHistory,
                OperationId.GET_ALLIANCE_FROM_COLLECTION: links.userHistory_getAllianceFromCollection,
                OperationId.GET_USER_FROM_COLLECTION: links.userHistory_getUserFromCollection,
                **links.default_entity_history_links,
            },
        },
    },
)


__all__ = [
    "allianceHistory_allianceId_get",
    "collections_collectionId_alliances_allianceId_get",
    "collections_collectionId_alliances_get",
    "collections_collectionId_delete",
    "collections_collectionId_get",
    "collections_collectionId_top100Users_get",
    "collections_collectionId_users_get",
    "collections_collectionId_users_userId_get",
    "collections_get",
    "collections_post",
    "collections_upload_post",
    "userHistory_userId_get",
]
