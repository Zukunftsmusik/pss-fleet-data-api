from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass(frozen=True)
class Link(BaseModel):
    """
    A simple dataclass to denote a hyperlink with a description in an API response.
    """

    path: str = Field(min_length=0)
    description: str


class LinkDefinition(BaseModel):
    """
    Defines an OpenAPI link used in responses.
    """

    description: str
    operationId: str
    parameters: dict[str, str]


__all__ = [
    Link.__name__,
    LinkDefinition.__name__,
]
