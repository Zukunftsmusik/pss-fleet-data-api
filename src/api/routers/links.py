from ..models.enums import OperationId
from ..models.link import LinkDefinition


# /allianceHistory/{allianceId}


allianceHistory_getAllianceFromCollection = LinkDefinition(
    description="A `collection_id` value and the `alliance_id` value in the response can be used as the `collectionId` and `allianceId` parameters in `GET /collections/{collectionId}/alliances/{allianceId}`.",
    operationId=OperationId.GET_ALLIANCE_FROM_COLLECTION,
    parameters={
        "allianceId": "$response.body#/0/fleet/0",
        "collectionId": "$response.body#/0/metadata/collection_id",
    },
)


allianceHistory_getAllianceHistory = LinkDefinition(
    description="The `allianceId` value in the path can be used as the `allianceId` parameter in `GET /allianceHistory/{allianceId}`.",
    operationId=OperationId.GET_ALLIANCE_FROM_COLLECTION,
    parameters={
        "allianceId": "$request.path.allianceId",
    },
)


allianceHistory_getUserFromCollection = LinkDefinition(
    description="A `collection_id` value and a `user_id` value in the response can be used as the `collectionId` and `userId` parameters in `GET /collections/{collectionId}/users/{userId}`.",
    operationId=OperationId.GET_USER_FROM_COLLECTION,
    parameters={
        "collectionId": "$response.body#/0/metadata/collection_id",
        "userId": "$response.body#/0/users/0/0",
    },
)


allianceHistory_getUserHistory = LinkDefinition(
    description="A `user_id` value in the response can be used as the `userId` parameter in `GET /userHistory/{userId}`.",
    operationId=OperationId.GET_USER_HISTORY,
    parameters={
        "userId": "$response.body#/0/users/0/0",
    },
)


# /collections


collections_deleteCollection = LinkDefinition(
    description="A `collection_id` value in the response can be used as the `collectionId` parameter in `DELETE /collections/{collectionId}`.",
    operationId=OperationId.DELETE_COLLECTION,
    parameters={
        "collectionId": "$response.body#/0/metadata/collection_id",
    },
)


collections_deleteCollectionAfterInsert = LinkDefinition(
    description="The `collection_id` value in the response can be used as the `collectionId` parameter in `DELETE /collections/{collectionId}`.",
    operationId=OperationId.DELETE_COLLECTION,
    parameters={
        "collectionId": "$response.body#/collection_id",
    },
)


collections_getAlliancesFromCollection = LinkDefinition(
    description="A `collection_id` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/alliances`.",
    operationId=OperationId.GET_ALLIANCES_FROM_COLLECTION,
    parameters={
        "collectionId": "$response.body#/0/metadata/collection_id",
    },
)


collections_getAlliancesFromCollectionAfterInsert = LinkDefinition(
    description="The `collection_id` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/alliances`.",
    operationId=OperationId.GET_ALLIANCES_FROM_COLLECTION,
    parameters={
        "collectionId": "$response.body#/collection_id",
    },
)


collections_getCollection = LinkDefinition(
    description="A `collection_id` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}`.",
    operationId=OperationId.GET_COLLECTION,
    parameters={
        "collectionId": "$response.body#/0/metadata/collection_id",
    },
)


collections_getCollectionAfterInsert = LinkDefinition(
    description="The `collection_id` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}`.",
    operationId=OperationId.GET_COLLECTION,
    parameters={
        "collectionId": "$response.body#/collection_id",
    },
)


collections_getTop100UsersFromCollection = LinkDefinition(
    description="A `collection_id` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/top100Users`.",
    operationId=OperationId.GET_TOP_100_USERS_FROM_COLLECTION,
    parameters={
        "collectionId": "$response.body#/0/metadata/collection_id",
    },
)


collections_getUsersFromCollectionAfterInsert = LinkDefinition(
    description="The `collection_id` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/top100Users`.",
    operationId=OperationId.GET_TOP_100_USERS_FROM_COLLECTION,
    parameters={
        "collectionId": "$response.body#/collection_id",
    },
)


collections_getUsersFromCollection = LinkDefinition(
    description="A `collection_id` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/users`.",
    operationId=OperationId.GET_USERS_FROM_COLLECTION,
    parameters={
        "collectionId": "$response.body#/0/metadata/collection_id",
    },
)


collections_getUsersFromCollectionAfterInsert = LinkDefinition(
    description="The `collection_id` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/users`.",
    operationId=OperationId.GET_USERS_FROM_COLLECTION,
    parameters={
        "collectionId": "$response.body#/collection_id",
    },
)


# /collections/{collectionId}


collection_deleteCollection = LinkDefinition(
    description="The `collectionId` parameter in the path can be used as the `collectionId` parameter in `DELETE /collections/{collectionId}`.",
    operationId=OperationId.DELETE_COLLECTION,
    parameters={
        "collectionId": "$request.path.collectionId",
    },
)


collection_getAllianceFromCollection = LinkDefinition(
    description="The `collectionId` parameter in the path and an `alliance_id` value in the response can be used as the `collectionId` and `allianceId` parameters in `GET /collections/{collectionId}/alliances/{allianceId}`.",
    operationId=OperationId.GET_ALLIANCE_FROM_COLLECTION,
    parameters={
        "allianceId": "$response.body#/fleets/0/0",
        "collectionId": "$request.path.collectionId",
    },
)


collection_getAlliancesFromCollection = LinkDefinition(
    description="The `collectionId` parameter in the path can be used as the `collectionId` parameter in `GET /collections/{collectionId}/alliances`.",
    operationId=OperationId.GET_ALLIANCES_FROM_COLLECTION,
    parameters={
        "collectionId": "$request.path.collectionId",
    },
)


collection_getAllianceHistory = LinkDefinition(
    description="An `alliance_id` value in the response can be used as the `allianceId` parameter in `GET /allianceHistory/{allianceId}`.",
    operationId=OperationId.GET_ALLIANCE_HISTORY,
    parameters={
        "allianceId": "$response.body#/fleets/0/0",
    },
)


collection_getCollection = LinkDefinition(
    description="The `collectionId` parameter in the path can be used as the `collectionId` parameter in `GET /collections/{collectionId}`.",
    operationId=OperationId.GET_COLLECTION,
    parameters={
        "collectionId": "$request.path.collectionId",
    },
)


collection_getTop100UsersFromCollection = LinkDefinition(
    description="The `collectionId` parameter in the path can be used as the `collectionId` parameter in `GET /collections/{collectionId}/top100Users`.",
    operationId=OperationId.GET_TOP_100_USERS_FROM_COLLECTION,
    parameters={
        "collectionId": "$request.path.collectionId",
    },
)


collection_getUserFromCollection = LinkDefinition(
    description="The `collectionId` parameter in the path and a `user_id` value in the response can be used as the `collectionId` and `userId` parameters in `GET /collections/{collectionId}/users/{userId}`.",
    operationId=OperationId.GET_USER_FROM_COLLECTION,
    parameters={
        "collectionId": "$request.path.collectionId",
        "userId": "$response.body#/users/0/0",
    },
)


collection_getUsersFromCollection = LinkDefinition(
    description="The `collectionId` parameter in the path can be used as the `collectionId` parameter in `GET /collections/{collectionId}/users`.",
    operationId=OperationId.GET_USERS_FROM_COLLECTION,
    parameters={
        "collectionId": "$request.path.collectionId",
    },
)


collection_getUserHistory = LinkDefinition(
    description="A `user_id` value in the response can be used as the `userId` parameter in `GET /userHistory/{userId}`.",
    operationId=OperationId.GET_USER_HISTORY,
    parameters={
        "allianceId": "$response.body#/users/0/0",
    },
)


# /collections/{collectionId}/alliances


collection_alliances_getAllianceFromCollection = LinkDefinition(
    description="The `collectionId` parameter in the path and an `alliance_id` value in the response can be used as the `collectionId` and `allianceId` parameters in `GET /collections/{collectionId}/alliances/{allianceId}`.",
    operationId=OperationId.GET_USER_FROM_COLLECTION,
    parameters={
        "collectionId": "$request.path.collectionId",
        "allianceId": "$response.body#/fleets/0/0",
    },
)


collection_alliances_getAllianceHistory = LinkDefinition(
    description="An `alliance_id` value in the response can be used as the `allianceId` parameter in `GET /allianceHistory/{allianceId}`.",
    operationId=OperationId.GET_USER_HISTORY,
    parameters={
        "allianceId": "$response.body#/fleets/0/0",
    },
)


# /collections/{collectionId}/alliances/{allianceId}


collection_alliance_getAllianceHistory = LinkDefinition(
    description="The `alliance_id` value in the response can be used as the `allianceId` parameter in `GET /allianceHistory/{allianceId}`.",
    operationId=OperationId.GET_ALLIANCE_HISTORY,
    parameters={
        "allianceId": "$response.body#/fleet/0",
    },
)


collection_alliance_getUserFromCollection = LinkDefinition(
    description="The `collectionId` parameter in the path and a `user_id` value in the response can be used as the `collectionId` and `userId` parameters in `GET /collections/{collectionId}/users/{userId}`.",
    operationId=OperationId.GET_USER_FROM_COLLECTION,
    parameters={
        "collectionId": "$request.path.collectionId",
        "userId": "$response.body#/users/0/0",
    },
)


collection_alliance_getUserHistory = LinkDefinition(
    description="A `user_id` value in the response can be used as the `userId` parameter in `GET /userHistory/{userId}`.",
    operationId=OperationId.GET_USER_HISTORY,
    parameters={
        "userId": "$response.body#/users/0/0",
    },
)


# /collections/{collectionId}/users & /collections/{collectionId}/top100Users


collection_users_getUserFromCollection = LinkDefinition(
    description="The `collectionId` parameter in the path and a `user_id` value in the response can be used as the `collectionId` and `userId` parameters in `GET /collections/{collectionId}/users/{userId}`.",
    operationId=OperationId.GET_ALLIANCE_FROM_COLLECTION,
    parameters={
        "collectionId": "$request.path.collectionId",
        "userId": "$response.body#/users/0/2",
    },
)


collection_users_getUserHistory = LinkDefinition(
    description="A `user_id` value in the response can be used as the `userId` parameter in `GET /userHistory/{userId}`.",
    operationId=OperationId.GET_ALLIANCE_HISTORY,
    parameters={
        "userId": "$response.body#/users/0/2",
    },
)


# /collections/{collectionId}/users/{user_id}


collection_user_getAllianceFromCollection = LinkDefinition(
    description="The `collectionId` parameter in the path and the `alliance_id` value in the response can be used as the `collectionId` and `allianceId` parameters in `GET /collections/{collectionId}/alliances/{allianceId}`.",
    operationId=OperationId.GET_ALLIANCE_FROM_COLLECTION,
    parameters={
        "allianceId": "$response.body#/fleet/0",
        "collectionId": "$request.path.collectionId",
    },
)


collection_user_getAllianceHistory = LinkDefinition(
    description="The `alliance_id` value in the response can be used as the `allianceId` parameter in `GET /allianceHistory/{allianceId}`.",
    operationId=OperationId.GET_ALLIANCE_HISTORY,
    parameters={
        "allianceId": "$response.body#/fleet/0",
    },
)


collection_user_getUserHistory = LinkDefinition(
    description="The `user_id` value in the response can be used as the `userId` parameter in `GET /userHistory/{userId}`.",
    operationId=OperationId.GET_USER_HISTORY,
    parameters={
        "userId": "$response.body#/user/0",
    },
)


# /allianceHistory/{allianceId} & /userHistory/{userId}


history_deleteCollection = LinkDefinition(
    description="A `collection_id` value in the response can be used as the `collectionId` parameter in `DELETE /collections/{collectionId}`.",
    operationId=OperationId.DELETE_COLLECTION,
    parameters={
        "collectionId": "$response.body#/0/collection/collection_id",
    },
)


history_getAlliancesFromCollection = LinkDefinition(
    description="A `collection_id` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/alliances`.",
    operationId=OperationId.GET_ALLIANCES_FROM_COLLECTION,
    parameters={
        "collectionId": "$response.body#/0/collection/collection_id",
    },
)


history_getCollection = LinkDefinition(
    description="A `collection_id` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}`.",
    operationId=OperationId.GET_COLLECTION,
    parameters={
        "collectionId": "$response.body#/0/collection/collection_id",
    },
)


history_getTop100UsersFromCollection = LinkDefinition(
    description="A `collection_id` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/top100Users`.",
    operationId=OperationId.GET_TOP_100_USERS_FROM_COLLECTION,
    parameters={
        "collectionId": "$response.body#/0/collection/collection_id",
    },
)


history_getUsersFromCollection = LinkDefinition(
    description="A `collection_id` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/users`.",
    operationId=OperationId.GET_USERS_FROM_COLLECTION,
    parameters={
        "collectionId": "$response.body#/0/collection/collection_id",
    },
)


# /


homepage_getCollections = LinkDefinition(description="Get Collections.", operationId=OperationId.GET_COLLECTIONS, parameters={})


# /userHistory/{userId}


userHistory_getAllianceFromCollection = LinkDefinition(
    description="A `collectionId` value and an `alliance_id` value in the response can be used as the `collectionId` and `allianceId` parameters in `GET /collections/{collectionId}/alliances/{allianceId}`.",
    operationId=OperationId.GET_ALLIANCE_FROM_COLLECTION,
    parameters={
        "allianceId": "$response.body#/0/user/2",
        "collectionId": "$response.body#/0/collection/collection_id",
    },
)


userHistory_getAllianceHistory = LinkDefinition(
    description="An `alliance_id` value in the response can be used as the `allianceId` parameter in `GET /allianceHistory/{allianceId}`.",
    operationId=OperationId.GET_ALLIANCE_HISTORY,
    parameters={
        "allianceId": "$response.body#/0/user/2",
    },
)


userHistory_getUserFromCollection = LinkDefinition(
    description="A `collectionId` value and the `user_id` value in the response can be used as the `collectionId` and `userId` parameters in `GET /collections/{collectionId}/users/{userId}`.",
    operationId=OperationId.GET_USER_FROM_COLLECTION,
    parameters={
        "collectionId": "$response.body#/0/collection/collection_id",
        "userId": "$response.body#/0/user/0",
    },
)


# Link collections


default_entity_history_links = {
    OperationId.DELETE_COLLECTION: history_deleteCollection,
    OperationId.GET_ALLIANCES_FROM_COLLECTION: history_getAlliancesFromCollection,
    OperationId.GET_COLLECTION: history_getCollection,
    OperationId.GET_TOP_100_USERS_FROM_COLLECTION: history_getTop100UsersFromCollection,
    OperationId.GET_USERS_FROM_COLLECTION: history_getUsersFromCollection,
}


__all__ = [
    "allianceHistory_getAllianceFromCollection",
    "allianceHistory_getAllianceHistory",
    "allianceHistory_getUserFromCollection",
    "allianceHistory_getUserHistory",
    "collection_alliance_getAllianceHistory",
    "collection_alliance_getUserFromCollection",
    "collection_alliance_getUserHistory",
    "collection_alliances_getAllianceFromCollection",
    "collection_alliances_getAllianceHistory",
    "collection_deleteCollection",
    "collection_getAllianceFromCollection",
    "collection_getAllianceHistory",
    "collection_getAlliancesFromCollection",
    "collection_getCollection",
    "collection_getTop100UsersFromCollection",
    "collection_getUserFromCollection",
    "collection_getUserHistory",
    "collection_getUsersFromCollection",
    "collection_user_getAllianceFromCollection",
    "collection_user_getAllianceHistory",
    "collection_user_getUserHistory",
    "collection_users_getUserFromCollection",
    "collection_users_getUserHistory",
    "collections_deleteCollection",
    "collections_deleteCollectionAfterInsert",
    "collections_getAlliancesFromCollection",
    "collections_getAlliancesFromCollectionAfterInsert",
    "collections_getCollection",
    "collections_getCollectionAfterInsert",
    "collections_getTop100UsersFromCollection",
    "collections_getUsersFromCollection",
    "collections_getUsersFromCollectionAfterInsert",
    "collections_getUsersFromCollectionAfterInsert",
    "default_entity_history_links",
    "history_deleteCollection",
    "history_getAlliancesFromCollection",
    "history_getCollection",
    "history_getTop100UsersFromCollection",
    "history_getUsersFromCollection",
    "homepage_getCollections",
    "userHistory_getAllianceFromCollection",
    "userHistory_getAllianceHistory",
    "userHistory_getUserFromCollection",
]
