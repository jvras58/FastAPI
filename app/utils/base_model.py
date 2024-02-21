from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """
    Classe que representa qualque entidade no sistema.
    """

    pass


class AbstractBaseModel(Base):
    """
    Classe abstrata que representa qualquer entidade que cinterá as propriedades base
    para se auditada.
    """

    __abstract__ = True

    audit_user_ip: Mapped[str] = mapped_column(String(16), name='audit_user_ip')
    audit_created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), name='audit_created_at'
    )
    audit_updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        name='audit_updated_on',
    )
    audit_user_login: Mapped[str] = mapped_column(name='audit_user_login')

    def as_dict(self):
        return {
            attr.key: getattr(self, attr.key)
            for attr in self.__mapper__.column_attrs
            if not attr.key.startswith('audit_')
        }
