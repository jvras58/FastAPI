"""Assignment router module."""
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
from app.utils.client_ip import get_client_ip
from app.utils.exceptions import (
    IntegrityValidationException,
    ObjectNotFoundException,
)
from app.utils.generic_controller import GenericController
from app.utils.logging import get_logger

router = APIRouter()
controller = GenericController(Assignment)
logger = get_logger(__name__)

SessionDep = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get(
    '/{assignment_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=AssignmentSchema,
)
def get_assignment_by_id(
    assignment_id: int, db_session: SessionDep, current_user: CurrentUser
):
    """Get assignment by ID."""
    validate_transaction_access(db_session, current_user, op.OP_1010005.value)

    logger.info(
        "Fetch assignment id=%s by user=%s",
        assignment_id,
        current_user.username,
    )

    return controller.get(db_session, assignment_id)


@router.get(
    '/',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=AssignmentListSchema,
)
def get_all_assignments(
    db_session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
):
    """Get all assignments with pagination."""
    validate_transaction_access(db_session, current_user, op.OP_1010003.value)
    logger.info(
        "List assignments skip=%s limit=%s by user=%s",
        skip,
        limit,
        current_user.username,
    )
    assignments = controller.get_all(db_session, skip, limit)
    return {'assignments': assignments}


@router.post(
    '/',
    status_code=HTTP_STATUS.HTTP_201_CREATED,
    response_model=AssignmentSchema,
)
def create_assignment(
    assignment: AssignmentDTOSchema,
    db_session: SessionDep,
    current_user: CurrentUser,
    request: Request,
):
    """Create a new assignment."""
    validate_transaction_access(db_session, current_user, op.OP_1010001.value)

    logger.info(
        "Create assignment for user_id=%s role_id=%s by user=%s ip=%s",
        assignment.user_id,
        assignment.role_id,
        current_user.username,
        get_client_ip(request),
    )

    new_assignment = Assignment(**assignment.model_dump())
    new_assignment.audit_user_ip = get_client_ip(request)
    new_assignment.audit_user_login = current_user.username

    try:
        new_assignment = controller.save(db_session, new_assignment)
        logger.info("Assignment created id=%s", new_assignment.id)
    except IntegrityValidationException as ex:
        logger.warning("Assignment create failed: %s", ex.args[0])
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
    db_session: SessionDep,
    current_user: CurrentUser,
    request: Request,
):
    """Update an existing assignment."""
    validate_transaction_access(db_session, current_user, op.OP_1010002.value)

    logger.info(
        "Update assignment id=%s user_id=%s role_id=%s by user=%s ip=%s",
        assignment_id,
        assignment.user_id,
        assignment.role_id,
        current_user.username,
        get_client_ip(request),
    )

    new_assignment: Assignment = Assignment(**assignment.model_dump())
    new_assignment.id = assignment_id
    new_assignment.audit_user_ip = get_client_ip(request)
    new_assignment.audit_user_login = current_user.username

    try:
        new_assignment = controller.update(db_session, new_assignment)
        logger.info("Assignment updated id=%s", assignment_id)
    except IntegrityValidationException as ex:
        logger.warning("Assignment update failed id=%s: %s", assignment_id, ex.args[0])
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
    assignment_id: int, db_session: SessionDep, current_user: CurrentUser
):
    """Delete an assignment."""
    validate_transaction_access(db_session, current_user, op.OP_1010004.value)

    logger.info(
        "Delete assignment id=%s by user=%s",
        assignment_id,
        current_user.username,
    )

    try:
        controller.delete(db_session, assignment_id)
    except ObjectNotFoundException as ex:
        logger.warning("Assignment delete failed id=%s: %s", assignment_id, ex.args[0])
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_404_NOT_FOUND, detail=ex.args[0]
        ) from ex

    return {'detail': 'Assignment deleted successfully'}
