from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator


class BaseSchema(BaseModel):
    # class Config:
    #     allow_population_by_field_name = True
    #     populate_by_name = True
    #     str_strip_whitespace = True
    #     use_enum_values = True
    #     from_attributes = True
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        use_enum_values=True,
        from_attributes=True,
    )

    # @model_validator("*", mode="before")
    @model_validator(mode="before")
    @classmethod
    def empty_str_to_none(cls, v) -> str | None:
        if v == "":
            return None
        return v


class BaseDBSchema(BaseSchema):
    uuid: UUID
    created_at: datetime
    updated_at: datetime

    # class Config:
    #     orm_mode = True
