from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi import status as HTTP_STATUS
from sqlalchemy.orm import Session

from app.api.assignment.schemas import (
    AssignmentDTOSchema,
    AssignmentListSchema,
    AssignmentSchema,
)
from app.api.authentication.controller import get_current_user
from app.api.authorization.controller import validate_transaction_access
from app.api.transaction.enum_operation_code import EnumOperationCode as op
from app.database.session import get_session
from app.models.assignment import Assignment
from app.models.user import User
from app.utils.base_schemas import SimpleMessageSchema
from app.utils.exceptions import IntegrityValidationException, ObjectNotFoundException
from app.utils.generic_controller import GenericController

router = APIRouter()
controller = GenericController(Assignment)

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get(
    '/{assignment_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=AssignmentSchema,
)
def get_assignment_by_id(
    assignment_id: int, db_session: Session, current_user: CurrentUser
):
    validate_transaction_access(db_session, current_user, op.OP_1010005.value)

    return controller.get(db_session, assignment_id)


@router.get(
    '/', status_code=HTTP_STATUS.HTTP_200_OK, response_model=AssignmentListSchema
)
def get_all_assignments(
    db_session: Session, current_user: CurrentUser, skip: int = 0, limit: int = 100
):
    validate_transaction_access(db_session, current_user, op.OP_1010003.value)
    assignments = controller.get_all(db_session, skip, limit)
    return {'assignments': assignments}


@router.post(
    '/', status_code=HTTP_STATUS.HTTP_201_CREATED, response_model=AssignmentSchema
)
def create_assignment(
    assignment: AssignmentDTOSchema,
    db_session: Session,
    current_user: CurrentUser,
    request: Request,
):
    validate_transaction_access(db_session, current_user, op.OP_1010001.value)

    new_assignment = Assignment(**assignment.model_dump())
    new_assignment.audit_user_ip = request.client.host
    new_assignment.audit_user_login = current_user.username

    try:
        new_assignment = controller.save(db_session, new_assignment)
    except IntegrityValidationException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_400_BAD_REQUEST,
            detail='Object ASSIGNMENT was not accepted',
        ) from ex

    return new_assignment


@router.put(
    '/{assignment_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=AssignmentSchema,
)
def update_assignment(
    assignment_id: int,
    assignment: AssignmentDTOSchema,
    db_session: Session,
    current_user: CurrentUser,
    request: Request,
):
    validate_transaction_access(db_session, current_user, op.OP_1010002.value)

    new_assignment: Assignment = Assignment(**assignment.model_dump())
    new_assignment.id = assignment_id
    new_assignment.audit_user_ip = request.client.host
    new_assignment.audit_user_login = current_user.username

    try:
        new_assignment = controller.update(db_session, new_assignment)
    except IntegrityValidationException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_400_BAD_REQUEST,
            detail='Object ASSIGNMENT was not accepted',
        ) from ex

    return new_assignment


@router.delete(
    '/{assignment_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=SimpleMessageSchema,
)
def delete_assignment(
    assignment_id: int, db_session: Session, current_user: CurrentUser
):
    validate_transaction_access(db_session, current_user, op.OP_1010004.value)

    try:
        controller.delete(db_session, assignment_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_404_NOT_FOUND, detail=ex.args[0]
        ) from ex

    return {'detail': 'Assignment deleted successfully'}
