from typing import TYPE_CHECKING, List

from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.base_model import AbstractBaseModel

if TYPE_CHECKING:
    from app.models.authorization import Authorization


class Transaction(AbstractBaseModel):
    """
    Represetna a tabela de Trasações do sistema.
    """

    __tablename__ = 'transaction'

    id: Mapped[int] = mapped_column(primary_key=True, name='id')
    name: Mapped[str] = mapped_column(name='str_name')
    description: Mapped[str] = mapped_column(name='str_description')
    operation_code: Mapped[str] = mapped_column(String(7), name='str_operation_code')

    authorizations: Mapped[List['Authorization']] = relationship(
        back_populates='transaction', lazy='subquery'
    )

    __table_args__ = (Index('idx_transaction_op_code', operation_code, unique=True),)
