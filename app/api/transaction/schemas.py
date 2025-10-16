"""Schemas for transaction API endpoints."""
from pydantic import BaseModel

from app.utils.base_schemas import BaseAuditDTOSchema, BaseAuditModelSchema


class TransactionDTOSchema(BaseAuditDTOSchema):
    """Represents a Transaction for the system."""

    name: str
    description: str
    operation_code: str


class TransactionSchema(TransactionDTOSchema, BaseAuditModelSchema):
    """Represents a Transaction for the system."""

    id: int


class TransactionListSchema(BaseModel):
    """Represents a list of Transactions for the system."""

    transactions: list[TransactionSchema]
