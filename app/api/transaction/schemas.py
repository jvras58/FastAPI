from pydantic import BaseModel

from app.utils.base_schemas import BaseAuditDTOSchema, BaseAuditModelSchema


class TransactionDTOSchema(BaseAuditDTOSchema):
    name: str
    description: str
    operation_code: str


class TransactionSchema(TransactionDTOSchema, BaseAuditModelSchema):
    id: int


class TransactionListSchema(BaseModel):
    transactions: list[TransactionSchema]
