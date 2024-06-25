from datetime import datetime
from typing import List, Optional, Union

from fastapi import Path, Query
from pydantic import conint

from .generated_models import (
    AllianceHistoryOut,
    CollectionCreate,
    CollectionOut,
    CollectionUpload,
    EnumParamAllianceProperties,
    EnumParamInterval,
    EnumParamMetadataProperties,
    EnumParamUserProperties,
    ErrorList,
    LegacyCollectionCreate,
    LegacyCollectionUpload,
    UserHistoryOut,
)

all = [
    datetime.__name__,
    List.__name__,
    Optional.__name__,
    Union.__name__,
    Path.__name__,
    Query.__name__,
    conint.__name__,
    AllianceHistoryOut.__name__,
    CollectionCreate.__name__,
    CollectionOut.__name__,
    CollectionUpload.__name__,
    EnumParamAllianceProperties.__name__,
    EnumParamInterval.__name__,
    EnumParamMetadataProperties.__name__,
    EnumParamUserProperties.__name__,
    ErrorList.__name__,
    LegacyCollectionCreate.__name__,
    LegacyCollectionUpload.__name__,
    UserHistoryOut.__name__,
]
