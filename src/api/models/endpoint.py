from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel


class EndpointDefinition(BaseModel, Mapping):
    """
    Defines an API endpoint. The values can be used as keyword parameters using the `**` operator (`**EndpointDefinition`).
    """

    description: str
    operation_id: str
    response_description: str
    responses: dict[int, dict[str, Any]]
    status_code: int
    summary: str

    def keys(self) -> list[str]:
        return self.model_dump().keys()

    def __iter__(self):
        for item in self.model_dump().items():
            yield item

    def __len__(self) -> int:
        return len(self.model_dump())

    def __getitem__(self, key) -> Any:
        return self.model_dump()[key]


__all__ = [
    EndpointDefinition.__name__,
]
