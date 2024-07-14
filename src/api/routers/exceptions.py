from datetime import datetime
from json.decoder import JSONDecodeError

from pydantic import ValidationError

from ..models.exceptions import (
    AllianceNotFoundError,
    CollectionNotDeletedError,
    CollectionNotFoundError,
    InvalidJsonUpload,
    NonUniqueTimestampError,
    SchemaVersionMismatch,
    UnsupportedSchemaError,
    UserNotFoundError,
)


def alliance_not_found_in_collection(collection_id: int, alliance_id: int) -> AllianceNotFoundError:
    f"""Creates an `{AllianceNotFoundError.__name__}` based on the given parameters.

    Args:
        collection_id (int): The ID of the Collection the requested Alliance wasn't found in.
        alliance_id (int): The ID of the Alliance that wasn't found.

    Returns:
        {AllianceNotFoundError.__name__}: An exception to be raised.
    """
    return AllianceNotFoundError(
        details=f"There is no Alliance with the ID '{alliance_id}' in the Collection with the ID '{collection_id}'.",
        suggestion="Check the provided `collectionId` and `allianceId` parameters in the path.",
    )


def collection_not_deleted(collection_id: int) -> CollectionNotDeletedError:
    f"""Creates a `{CollectionNotDeletedError.__name__}` based on the given parameters.

    Args:
        collection_id (int): The ID of the Collection that wasn't deleted.

    Returns:
        {CollectionNotDeletedError.__name__}: An exception to be raised.
    """
    return CollectionNotDeletedError(
        details=f"The Collection with the ID '{collection_id}' exists, but an error occured while trying to delete it.",
        suggestion="Check, if the Collection with the provided `collectionId` still exists and try again later, if it does.",
    )


def collection_not_found(collection_id: int) -> CollectionNotFoundError:
    f"""Creates an `{CollectionNotFoundError.__name__}` based on the given parameters.

    Args:
        collection_id (int): The ID of the Collection that wasn't found.

    Returns:
        {CollectionNotFoundError.__name__}: An exception to be raised.
    """
    return CollectionNotFoundError(
        details=f"There is no Collection with the ID '{collection_id}'.",
        suggestion="Check the provided `collectionId` parameter in the path.",
    )


def invalid_json_upload(error: JSONDecodeError) -> InvalidJsonUpload:
    f"""Creates an `{InvalidJsonUpload.__name__}` based on the given parameters.

    Args:
        error (json.decoder.JSONDecodeError): The error that was raised by the JSON Decoder.

    Returns:
        {InvalidJsonUpload.__name__}: An exception to be raised.
    """
    return InvalidJsonUpload(
        details=str(error),
        suggestion="Fix the JSON.",
    )


def non_unique_timestamp(timestamp: datetime, collection_id: int) -> NonUniqueTimestampError:
    f"""Creates a `{NonUniqueTimestampError.__name__}` based on the given parameters.

    Args:
        timestamp (datetime): The timestamp for which a Collection already exists in the database.
        collection_id (int): The ID of the Collection with this timestamp.

    Returns:
        {NonUniqueTimestampError.__name__}: An exception to be raised.
    """
    return NonUniqueTimestampError(
        details=f"Can't insert collection: A collection with this timestamp ({timestamp.strftime("%Y-%m-%d %H:%M:%S")}) already exists in the database with the ID '{collection_id}'.",
        suggestion="If you want to update the Collection in question, delete and re-insert it.",
    )


def schema_version_mismatch(expected_schema_version: int, error: ValidationError) -> SchemaVersionMismatch:
    f"""Creates a `{SchemaVersionMismatch.__name__}` based on the given parameters.

    Args:
        expected_schema_version (int): The expected schema version.
        error (pydantic.ValidationError): The validation error that was raised by pydantic.

    Returns:
        {SchemaVersionMismatch.__name__}: An exception to be raised.
    """
    return SchemaVersionMismatch(
        details=f"The file contents don't match the declared schema version (expected schema version: {expected_schema_version}):\n{error}"
    )


def unsupported_schema() -> UnsupportedSchemaError:
    f"""Creates an `{UnsupportedSchemaError.__name__}` based on the given parameters.

    Returns:
        {UnsupportedSchemaError.__name__}: An exception to be raised.
    """
    return UnsupportedSchemaError(
        details="The uploaded file is not a valid Fleet Data Collection file.",
        suggestion="For the supported schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions",
    )


def user_not_found_in_collection(collection_id: int, user_id: int) -> UserNotFoundError:
    f"""Creates an `{UserNotFoundError.__name__}` based on the given parameters.

    Args:
        collection_id (int): The ID of the Collection the requested User wasn't found in.
        user_id (int): The ID of the User that wasn't found.

    Returns:
        {UserNotFoundError.__name__}: An exception to be raised.
    """
    return UserNotFoundError(
        details=f"There is no User with the ID '{user_id}' in the Collection with the ID '{collection_id}'.",
        suggestion="Check the provided `collectionId` and `userId` parameters in the path.",
    )


__all__ = [
    alliance_not_found_in_collection.__name__,
    collection_not_deleted.__name__,
    collection_not_found.__name__,
    invalid_json_upload.__name__,
    non_unique_timestamp.__name__,
    schema_version_mismatch.__name__,
    unsupported_schema.__name__,
    user_not_found_in_collection.__name__,
]
