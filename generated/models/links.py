from typing import Any

from pydantic import BaseModel, Field


class LinkAllianceHistoryGetAllianceById(BaseModel):
    __root__: Any = Field(
        ...,
        description="A `collectionId` value and the `allianceId` value in the response can be used as the `collectionId` and `allianceId` parameters in `GET /collections/{collectionId}/alliances/{allianceId}`.",
    )


class LinkAllianceHistoryGetUserById(BaseModel):
    __root__: Any = Field(
        ..., description="A `collectionId` value and a `userId` value in the response can be used as the `collectionId` and `userId` parameters in `GET /collections/{collectionId}/users/{userId}`."
    )


class LinkAllianceHistoryGetUserHistoryById(BaseModel):
    __root__: Any = Field(..., description="A `userId` value in the response can be used as the `userId` parameter in `GET /users/{userId}`.")


class LinkCollectionAllianceGetAllianceHistoryById(BaseModel):
    __root__: Any = Field(..., description="The `allianceId` value in the response can be used as the `allianceId` parameter in `GET /alliances/{allianceId}`.")


class LinkCollectionAllianceGetUserById(BaseModel):
    __root__: Any = Field(
        ...,
        description="The `collectionId` parameter in the path and a `userId` value in the response can be used as the `collectionId` and `userId` parameters in `GET /collections/{collectionId}/users/{userId}`.",
    )


class LinkCollectionAllianceGetUserHistoryById(BaseModel):
    __root__: Any = Field(..., description="A `userId` value in the response can be used as the `userId` parameter in `GET /users/{userId}`.")


class LinkCollectionAlliancesGetUserById(BaseModel):
    __root__: Any = Field(
        ...,
        description="The `collectionId` parameter in the path and a `userId` value in the response can be used as the `collectionId` and `userId` parameters in `GET /collections/{collectionId}/users/{userId}`.",
    )


class LinkCollectionAlliancesGetUserHistoryById(BaseModel):
    __root__: Any = Field(..., description="A `userId` value in the response can be used as the `userId` parameter in `GET /users/{userId}`.")


class LinkCollectionDeleteCollectionById(BaseModel):
    __root__: Any = Field(..., description="The `collectionId` parameter in the path can be used as the `collectionId` parameter in `DELETE /collections/{collectionId}`.")


class LinkCollectionGetAllianceById(BaseModel):
    __root__: Any = Field(
        ...,
        description="The `collectionId` parameter in the path and an `allianceId` value in the response can be used as the `collectionId` and `allianceId` parameters in `GET /collections/{collectionId}/alliances/{allianceId}`.",
    )


class LinkCollectionGetCollectionAlliances(BaseModel):
    __root__: Any = Field(..., description="The `collectionId` parameter in the path can be used as the `collectionId` parameter in `GET /collections/{collectionId}/alliances`.")


class LinkCollectionGetCollectionById(BaseModel):
    __root__: Any = Field(..., description="The `collectionId` parameter in the path can be used as the `collectionId` parameter in `GET /collections/{collectionId}`.")


class LinkCollectionGetUserById(BaseModel):
    __root__: Any = Field(
        ...,
        description="The `collectionId` parameter in the path and a `userId` value in the response can be used as the `collectionId` and `userId` parameters in `GET /collections/{collectionId}/users/{userId}`.",
    )


class LinkCollectionGetAllianceHistoryById(BaseModel):
    __root__: Any = Field(..., description="An `allianceId` value in the response can be used as the `allianceId` parameter in `GET /alliances/{allianceId}`.")


class LinkCollectionGetCollectionTop100(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/top100Users`.")


class LinkCollectionGetCollectionUsers(BaseModel):
    __root__: Any = Field(..., description="The `collectionId` parameter in the path can be used as the `collectionId` parameter in `GET /collections/{collectionId}/users`.")


class LinkCollectionGetUserHistoryById(BaseModel):
    __root__: Any = Field(..., description="A `userId` value in the response can be used as the `userId` parameter in `GET /users/{userId}`.")


class LinkCollectionUpdateCollectionById(BaseModel):
    __root__: Any = Field(..., description="The `collectionId` parameter in the path can be used as the `collectionId` parameter in `PUT /collections/{collectionId}`.")


class LinkCollectionsDeleteCollectionById(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `DELETE /collections/{collectionId}`.")


class LinkCollectionsGetCollectionAlliances(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/alliances`.")


class LinkCollectionsGetCollectionById(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}`.")


class LinkCollectionsGetCollectionTop100(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/top100Users`.")


class LinkCollectionsGetCollectionUsers(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/users`.")


class LinkCollectionsUpdateCollectionById(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `PUT /collections/{collectionId}`.")


class LinkHistoryDeleteCollectionById(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `DELETE /collections/{collectionId}`.")


class LinkHistoryGetCollectionAlliances(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/alliances`.")


class LinkHistoryGetCollectionById(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}`.")


class LinkHistoryGetCollectionTop100(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/top100Users`.")


class LinkHistoryGetCollectionUsers(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `GET /collections/{collectionId}/users`.")


class LinkHistoryUpdateCollectionById(BaseModel):
    __root__: Any = Field(..., description="A `collectionId` value in the response can be used as the `collectionId` parameter in `PUT /collections/{collectionId}`.")


class LinkCollectionUserGetAllianceById(BaseModel):
    __root__: Any = Field(
        ...,
        description="The `collectionId` parameter in the path and the `allianceId` value in the response can be used as the `collectionId` and `allianceId` parameters in `GET /collections/{collectionId}/alliances/{allianceId}`.",
    )


class LinkCollectionUserGetAllianceHistoryById(BaseModel):
    __root__: Any = Field(..., description="The `allianceId` value in the response can be used as the `allianceId` parameter in `GET /alliances/{allianceId}`.")


class LinkCollectionUsersGetAllianceById(BaseModel):
    __root__: Any = Field(
        ...,
        description="The `collectionId` parameter in the path and an `allianceId` value in the response can be used as the `collectionId` and `allianceId` parameters in `GET /collections/{collectionId}/alliances/{allianceId}`.",
    )


class LinkCollectionUsersGetAllianceHistoryById(BaseModel):
    __root__: Any = Field(..., description="An `allianceId` value in the response can be used as the `allianceId` parameter in `GET /alliances/{allianceId}`.")


class LinkCollectionUserGetUserHistoryById(BaseModel):
    __root__: Any = Field(..., description="The `userId` value in the response can be used as the `userId` parameter in `GET /users/{userId}`.")


class LinkUserHistoryGetAllianceById(BaseModel):
    __root__: Any = Field(
        ...,
        description="A `collectionId` value and an `allianceId` value in the response can be used as the `collectionId` and `allianceId` parameters in `GET /collections/{collectionId}/alliances/{allianceId}`.",
    )


class LinkUserHistoryGetAllianceHistoryById(BaseModel):
    __root__: Any = Field(..., description="An `allianceId` value in the response can be used as the `allianceId` parameter in `GET /alliances/{allianceId}`.")


class LinkUserHistoryGetUserById(BaseModel):
    __root__: Any = Field(
        ..., description="A `collectionId` value and the `userId` value in the response can be used as the `collectionId` and `userId` parameters in `GET /collections/{collectionId}/users/{userId}`."
    )
