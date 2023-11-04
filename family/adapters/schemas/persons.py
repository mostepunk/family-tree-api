from enum import Enum

from pydantic import Field

from family.adapters.schemas.base import BaseSchema


class SexEnum(str, Enum):
    f: str = "F"
    m: str = "M"


class PersonName(BaseSchema):
    name: str | None
    given_surn: str | None
    marriage_surn: str | None


class PersonDate(BaseSchema):
    date: str | None
    plac: str | None
    addr: str | None


class PersonDBSchema(BaseSchema):
    i_id: str
    i_sex: str
    i_file: int
    i_rin: str
    i_gedcom: str


class PersonAnswer(BaseSchema):
    id_: str = Field(alias="id")
    sex: SexEnum
    name: PersonName
    born: PersonDate
    media: list[str]
    family_partners: list[str]
    family_child: list[str]
