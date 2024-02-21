from pydantic import BaseModel

from app.utils.base_schemas import BaseAuditDTOSchema, BaseAuditModelSchema


class RoleDTOSchema(BaseAuditDTOSchema):
    """
    Representa um Role (Papel) para o sistema.
    """

    name: str
    description: str


class RoleSchema(RoleDTOSchema, BaseAuditModelSchema):
    id: int


class RoleListSchema(BaseModel):
    roles: list[RoleSchema]
