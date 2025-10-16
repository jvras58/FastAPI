"""Schemas for the Assignment entity."""
from pydantic import BaseModel

from app.utils.base_schemas import BaseAuditDTOSchema, BaseAuditModelSchema


class AssignmentDTOSchema(BaseAuditDTOSchema):
    """
    Represents an Assignment of a user to a role.
    """

    user_id: int
    role_id: int


class AssignmentSchema(AssignmentDTOSchema, BaseAuditModelSchema):
    """Schema representing an Assignment with audit fields."""

    id: int


class AssignmentListSchema(BaseModel):
    """Schema representing a list of Assignments."""

    assignments: list[AssignmentSchema]
