"""Schemas for the system Role."""
from pydantic import BaseModel

from app.utils.base_schemas import BaseAuditDTOSchema, BaseAuditModelSchema


class RoleDTOSchema(BaseAuditDTOSchema):
    """
    Represents a Role for the system.
    """

    name: str
    description: str


class RoleSchema(RoleDTOSchema, BaseAuditModelSchema):
    """Represents a Role for the system."""

    id: int


class RoleListSchema(BaseModel):
    """Represents a list of Roles for the system."""

    roles: list[RoleSchema]
