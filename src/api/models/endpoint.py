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
        return self.__dict__.keys()

    def __iter__(self):
        for item in self.__dict__.items():
            yield item

    def __len__(self) -> int:
        return len(self.__dict__)

    def __getitem__(self, key) -> Any:
        return self.__dict__[key]

    def __dict__(self) -> dict[str, Any]:
        result = {
            "description": self.description,
            "operation_id": self.operation_id,
            "response_description": self.response_description,
            "responses": self.responses,
            "status_code": self.status_code,
            "summary": self.summary,
        }
        return result


__all__ = [
    EndpointDefinition.__name__,
]
