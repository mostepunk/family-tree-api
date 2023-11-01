from family.adapters.schemas.base import BaseSchema


class PersonBase(BaseSchema):
    i_id: str
    i_sex: str


class PersonDBSchema(PersonBase):
    i_file: int
    i_rin: str
    i_gedcom: str


class PersonGET(PersonBase):
    ...
