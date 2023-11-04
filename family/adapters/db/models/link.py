"""Развязочная таблица, которая связывает персону с любым объектом в БД.

Надо подумать где она может пригоодится, и пригодится ли. Связь с семьей я сделал через relationship.
Возможно пригодится для связи с другими данными.

```sql
    CREATE TABLE public.link (
        l_file int4 NOT NULL,
        l_from varchar(20) NOT NULL,
        l_type varchar(15) NOT NULL,
        l_to varchar(20) NOT NULL,
        CONSTRAINT link_l_to_l_file_l_type_l_from_unique UNIQUE (l_to, l_file, l_type, l_from),
        CONSTRAINT link_pkey PRIMARY KEY (l_from, l_file, l_type, l_to)
    );
```
"""

from sqlalchemy import PrimaryKeyConstraint, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from family.adapters.db.models.base import Base


class LinkModel(Base):
    __tablename__ = "link"
    __table_args__ = (
        PrimaryKeyConstraint("l_from", "l_file", "l_type", "l_to"),
        UniqueConstraint("l_from", "l_file", "l_type", "l_to"),
        {},
    )

    l_file: Mapped[int] = mapped_column()
    l_from: Mapped[str] = mapped_column(String(20))
    l_type: Mapped[str] = mapped_column(String(15))
    l_to: Mapped[str] = mapped_column(String(20))

    # family: Mapped["PersonModel"] = mapped_column()

    def __repr__(self):
        return f"<Link From: {self.l_from} {self.l_type} TO: {self.l_to}>"
