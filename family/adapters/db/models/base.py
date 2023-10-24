from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


'''
class _BaseTableOLD(Base):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    uuid = Column(
        UUID(as_uuid=True),
        nullable=False,
        primary_key=True,
        server_default=func.uuid_generate_v4(),
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        server_onupdate=func.now(),
    )

    def __repr__(self):
        """Форматированный вывод данных из таблицы.

        Returns:
            форматированное представление строки
        """
        return f"<{self.__class__.__name__}(uuid={self.uuid})>"

'''


class BaseTable(Base):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        server_onupdate=func.now(),
    )

    def __repr__(self):
        """Форматированный вывод данных из таблицы.

        Returns:
            форматированное представление строки
        """
        return f"<{self.__class__.__name__}(uuid={self.uuid})>"
