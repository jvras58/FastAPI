"""Model for Role (Perfil de usuário)."""
from typing import TYPE_CHECKING

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.base_model import AbstractBaseModel

if TYPE_CHECKING:
    from app.models.assignment import Assignment
    from app.models.authorization import Authorization


class Role(AbstractBaseModel):
    """
    Represents the Role (Perfil de usuário) table.
    """

    __tablename__ = 'role'

    id: Mapped[int] = mapped_column(primary_key=True, name='id')
    name: Mapped[str] = mapped_column(name='str_name')
    description: Mapped[str] = mapped_column(name='str_description')

    assignments: Mapped[list['Assignment']] = relationship(
        back_populates='role', lazy='subquery'
    )
    authorizations: Mapped[list['Authorization']] = relationship(
        back_populates='role', lazy='subquery'
    )

    __table_args__ = (Index('idx_role_name', name, unique=True),)
