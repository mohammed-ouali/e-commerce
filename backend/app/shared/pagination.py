from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T] = Field(
        description="Items on the current page."
    )
    total: int = Field(
        ge=0,
        description="Total number of matching items across all pages.",
    )
    page: int = Field(
        ge=1,
        description="Current page number, starting from 1.",
    )
    limit: int = Field(
        ge=1,
        description="Maximum number of items requested per page.",
    )