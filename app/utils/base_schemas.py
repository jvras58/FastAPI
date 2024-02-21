from datetime import datetime

from pydantic import BaseModel


class SimpleMessageSchema(BaseModel):
    """
    Representação de uma mensagem no sistama
    """

    detail: str


class BaseAuditDTOSchema(BaseModel):
    audit_user_ip: str | None = None
    audit_user_login: str | None = None


class BaseAuditModelSchema(BaseModel):
    audit_created_at: datetime
    audit_updated_on: datetime
