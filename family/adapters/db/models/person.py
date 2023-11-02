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
from sqlalchemy.orm import Mapped, mapped_column

from family.adapters.db.models.base import Base
from family.utils.gedcom import GedcomParser, Individual


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

    @property
    def individual(self) -> Individual:
        return GedcomParser.parse_individual(self.i_gedcom)
