from pydantic import BaseModel

from app.utils.base_schemas import BaseAuditDTOSchema, BaseAuditModelSchema


class AssignmentDTOSchema(BaseAuditDTOSchema):
    """
    Representa uma Designação de um usuário para um papel.
    """

    user_id: int
    role_id: int


class AssignmentSchema(AssignmentDTOSchema, BaseAuditModelSchema):
    id: int


class AssignmentListSchema(BaseModel):
    assignments: list[AssignmentSchema]
