"""Base schemas for the system."""
from datetime import datetime

from pydantic import BaseModel


class SimpleMessageSchema(BaseModel):
    """
    Representation of a message in the system
    """

    detail: str


class BaseAuditDTOSchema(BaseModel):
    """Base schema for audit fields in DTOs."""

    audit_user_ip: str | None = None
    audit_user_login: str | None = None


class BaseAuditModelSchema(BaseModel):
    """Base schema for audit fields in models."""

    audit_created_at: datetime
    audit_updated_on: datetime
