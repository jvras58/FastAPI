"""Base model definitions for SQLAlchemy ORM."""

from datetime import datetime

from sqlalchemy import DateTime, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Class that represents any entity in the system.
    """

    pass


class AbstractBaseModel(Base):
    """
    Abstract class that represents any entity that will have the base properties
    to be audited.
    """

    __abstract__ = True

    audit_user_ip: Mapped[str] = mapped_column(
        String(16), name='audit_user_ip'
    )
    audit_created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text('CURRENT_TIMESTAMP'),
        name='audit_created_at',
    )
    audit_updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=text('CURRENT_TIMESTAMP'),
        name='audit_updated_on',
    )
    audit_user_login: Mapped[str] = mapped_column(name='audit_user_login')

    def as_dict(self):
        """Convert the model instance to a dictionary, excluding audit fields."""
        return {
            attr.key: getattr(self, attr.key)
            for attr in self.__mapper__.column_attrs
            if not attr.key.startswith('audit_')
        }
