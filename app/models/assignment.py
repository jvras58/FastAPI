from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.base_model import AbstractBaseModel

if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.user import User


class Assignment(AbstractBaseModel):
    """
    Representa a tabela de Assignment (Designações) de usuários.
    Essas designações determinam qual o papel (Role) o usuário assume para o sistema.
    """

    __tablename__ = 'assignment'

    id: Mapped[int] = mapped_column(primary_key=True, name='id')
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), name='user_id', nullable=False
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey('role.id'), name='role_id', nullable=False
    )

    user: Mapped['User'] = relationship(back_populates='assignments', lazy='subquery')
    role: Mapped['Role'] = relationship(back_populates='assignments', lazy='subquery')

    __table_args__ = (Index('idx_user_role', user_id, role_id, unique=True),)
