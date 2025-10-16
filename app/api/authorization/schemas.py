"""Authorization Schemas"""
from pydantic import BaseModel

from app.utils.base_schemas import BaseAuditDTOSchema, BaseAuditModelSchema


class AuthorizationDTOSchema(BaseAuditDTOSchema):
    """
    Authorization Schema
    """

    role_id: int
    transaction_id: int


class AuthorizationSchema(AuthorizationDTOSchema, BaseAuditModelSchema):
    """
    Authorization Schema
    """

    id: int


class AuthorizationListSchema(BaseModel):
    """
    Authorization List Schema
    """

    authorizations: list[AuthorizationSchema]
