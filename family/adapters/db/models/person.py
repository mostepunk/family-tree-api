"""
CREATE TABLE public.individuals (
    i_id varchar(20) NOT NULL,
    i_file int4 NOT NULL,
    i_rin varchar(20) NOT NULL,
    i_sex varchar(255) NOT NULL,
    i_gedcom text NOT NULL,


    CONSTRAINT individuals_i_sex_check CHECK (
    (
      (i_sex)::text = ANY
      (
       (ARRAY['U'::character varying, 'M'::character varying, 'F'::character varying])::text[]
      )
    )
    ),

    CONSTRAINT individuals_pkey PRIMARY KEY (i_id, i_file)
    CONSTRAINT individuals_i_file_i_id_unique UNIQUE (i_file, i_id),
);
"""

from sqlalchemy import PrimaryKeyConstraint, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from family.adapters.db.models.base import Base
from family.utils.gedcom import GedcomParser, Individual
from family.utils.gedcom.standart import GEDCOM_TAG_FAMILY_CHILD


class PersonModel(Base):
    """Странная конструкция у individuals_i_sex_check"""

    __tablename__ = "individuals"
    __table_args__ = (
        PrimaryKeyConstraint("i_id", "i_file"),
        UniqueConstraint("i_file", "i_id"),
        {},
    )

    i_id: Mapped[str] = mapped_column(String(20))
    i_file: Mapped[int] = mapped_column()
    i_rin: Mapped[str] = mapped_column(String(20))
    i_sex: Mapped[str] = mapped_column(String(255))
    i_gedcom: Mapped[str] = mapped_column(Text)

    families: Mapped[list["FamilyModel"]] = relationship(
        primaryjoin="or_(PersonModel.i_id == FamilyModel.f_husb, PersonModel.i_id == FamilyModel.f_wife)",
        foreign_keys=i_id,
        uselist=True,
    )
    parents: Mapped[list["FamilyModel"]] = relationship(
        secondary="link",
        primaryjoin=f"and_(PersonModel.i_id == LinkModel.l_from, LinkModel.l_type == '{GEDCOM_TAG_FAMILY_CHILD}')",
        secondaryjoin="LinkModel.l_to == FamilyModel.f_id",
        uselist=True,
        lazy="selectin",
        foreign_keys="LinkModel.l_from, LinkModel.l_to",
    )

    @property
    def individual(self) -> Individual:
        return GedcomParser.parse_individual(self.i_gedcom)

    def __repr__(self):
        return f"Individual: {self.i_id}, {self.individual.name.get('name')}"
