"""
CREATE TABLE public.families (
	f_id varchar(20) NOT NULL,
	f_file int4 NOT NULL,
	f_husb varchar(20) NULL,
	f_wife varchar(20) NULL,
	f_gedcom text NOT NULL,
	f_numchil int4 NOT NULL,

	CONSTRAINT families_f_file_f_id_unique UNIQUE (f_file, f_id),
	CONSTRAINT families_pkey PRIMARY KEY (f_id, f_file)
);
CREATE INDEX families_f_husb_index ON public.families USING btree (f_husb);
CREATE INDEX families_f_wife_index ON public.families USING btree (f_wife);
"""

from sqlalchemy import Integer, PrimaryKeyConstraint, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from family.adapters.db.models.base import Base
from family.utils.gedcom.standart import GEDCOM_TAG_CHILD


class FamilyModel(Base):
    __tablename__ = "families"
    __table_args__ = (
        PrimaryKeyConstraint("f_id", "f_file"),
        UniqueConstraint("f_id", "f_file"),
        {},
    )

    f_id: Mapped[str] = mapped_column(String(20))
    f_file: Mapped[int] = mapped_column()
    f_husb: Mapped[str] = mapped_column(String(20), index=True)
    f_wife: Mapped[str] = mapped_column(String(20), index=True)
    f_gedcom: Mapped[str] = mapped_column(Text)
    f_numchil: Mapped[int] = mapped_column(Integer)

    husband: Mapped["PersonModel"] = relationship(  # noqa:F821
        primaryjoin="FamilyModel.f_husb == PersonModel.i_id",
        lazy="selectin",
        foreign_keys=f_husb,
    )
    wife: Mapped["PersonModel"] = relationship(  # noqa:F821
        primaryjoin="FamilyModel.f_wife == PersonModel.i_id",
        lazy="selectin",
        foreign_keys=f_wife,
    )

    # father: Mapped[list["FamilyModel"]] = relationship(
    #     secondary="link",
    #     primaryjoin=f"and_(FamilyModel.f_id == LinkModel.l_from, LinkModel.l_type == '{GEDCOM_TAG_CHILD}')",
    #     secondaryjoin="LinkModel.l_to == PersonModel.i_id",
    #     uselist=False,
    #     lazy="selectin",
    #     foreign_keys=f_id,
    # )

    # mother: Mapped[list["FamilyModel"]] = relationship(
    #     secondary="link",
    #     primaryjoin=f"and_(FamilyModel.f_id == LinkModel.l_from, LinkModel.l_type == '{GEDCOM_TAG_CHILD}')",
    #     secondaryjoin="LinkModel.l_to == PersonModel.i_id",
    #     uselist=False,
    #     lazy="selectin",
    #     foreign_keys=f_id,
    # )


    def __repr__(self):
        return f"<Family Husb: {self.f_husb} Wife: {self.f_wife}>"
