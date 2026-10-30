
from __future__ import annotations

from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class ProductBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of the product.",
    )
    category_id: int = Field(
        ...,
        gt=0,
        description="ID of the category to which the product belongs.",
    )
    description: str | None = Field(
        default=None,
        description="Optional description of the product.",
    )
    is_active: bool = Field(
        default=True,
        description="Whether the product is available in the store.",
    )

    @field_validator("name")
    @classmethod
    def validate_and_sanitize_name(cls, value: str) -> str:
        trimmed_value = value.strip()

        if not trimmed_value:
            raise ValueError("Product name cannot consist only of whitespace.")

        return trimmed_value

    @field_validator("description")
    @classmethod
    def sanitize_description(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return value.strip()


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Updated name of the product.",
    )
    category_id: int | None = Field(
        default=None,
        gt=0,
        description="Updated category ID of the product.",
    )
    description: str | None = Field(
        default=None,
        description="Updated product description. Null clears the description.",
    )
    is_active: bool | None = Field(
        default=None,
        description="Updated activation status of the product.",
    )

    @field_validator("name")
    @classmethod
    def validate_and_sanitize_name(cls, value: str | None) -> str | None:
        if value is None:
            return None

        trimmed_value = value.strip()

        if not trimmed_value:
            raise ValueError("Product name cannot consist only of whitespace.")

        return trimmed_value

    @field_validator("description")
    @classmethod
    def sanitize_description(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return value.strip()

    @model_validator(mode="after")
    def validate_at_least_one_field(self):
        if not self.model_fields_set:
            raise ValueError("Update payload cannot be empty.")

        return self


class ProductResponse(ProductBase):
    id: int = Field(
        description="Unique identifier of the product.",
    )
    created_at: datetime = Field(
        description="Date and time the product was created.",
    )
    updated_at: datetime = Field(
        description="Date and time the product was last updated.",
    )

    model_config = ConfigDict(from_attributes=True)
