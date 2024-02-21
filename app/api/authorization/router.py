from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi import status as HTTP_STATUS
from sqlalchemy.orm import Session

from app.api.authentication.controller import get_current_user
from app.api.authorization.controller import validate_transaction_access
from app.api.authorization.schemas import (
    AuthorizationDTOSchema,
    AuthorizationListSchema,
    AuthorizationSchema,
)
from app.api.transaction.enum_operation_code import EnumOperationCode as op
from app.database.session import get_session
from app.models.authorization import Authorization
from app.models.user import User
from app.utils.base_schemas import SimpleMessageSchema
from app.utils.exceptions import IntegrityValidationException, ObjectNotFoundException
from app.utils.generic_controller import GenericController

router = APIRouter()
controller = GenericController(Authorization)

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/',
    status_code=HTTP_STATUS.HTTP_201_CREATED,
    response_model=AuthorizationSchema,
)
def create_authorization(
    authorization: AuthorizationDTOSchema,
    db_session: Session,
    current_user: CurrentUser,
    request: Request,
):
    validate_transaction_access(db_session, current_user, op.OP_1020001.value)
    new_authorization = Authorization(**authorization.model_dump())

    new_authorization.audit_user_ip = request.client.host
    new_authorization.audit_user_login = current_user.username

    try:
        new_authorization = controller.save(db_session, new_authorization)
    except IntegrityValidationException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_400_BAD_REQUEST,
            detail='Object AUTHORIZATION was not accepted',
        ) from ex

    return new_authorization


@router.get(
    '/', status_code=HTTP_STATUS.HTTP_200_OK, response_model=AuthorizationListSchema
)
def get_all_authorizations(
    db_session: Session, current_user: CurrentUser, skip: int = 0, limit: int = 100
):
    validate_transaction_access(db_session, current_user, op.OP_1020003.value)
    authorizations = controller.get_all(db_session, skip, limit)
    return {'authorizations': authorizations}


@router.get(
    '/{autorization_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=AuthorizationSchema,
)
def get_authorization_by_id(
    autorization_id: int, db_session: Session, current_user: CurrentUser
):

    validate_transaction_access(db_session, current_user, op.OP_1020005.value)

    try:
        authorization = controller.get(db_session, autorization_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_404_NOT_FOUND,
            detail='Object AUTHORIZATION was not found',
        ) from ex

    return authorization


@router.delete(
    '/{autorization_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=SimpleMessageSchema,
)
def delete_authorization(
    autorization_id: int, db_session: Session, current_user: CurrentUser
):
    validate_transaction_access(db_session, current_user, op.OP_1020004.value)

    try:
        controller.delete(db_session, autorization_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_404_NOT_FOUND,
            detail='Object AUTHORIZATION was not found',
        ) from ex

    return {'detail': 'Object AUTHORIZATION was deleted'}


@router.put(
    '/{autorization_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=AuthorizationSchema,
)
def update_authorization(
    autorization_id: int,
    authorization: AuthorizationDTOSchema,
    db_session: Session,
    request: Request,
    current_user: CurrentUser,
):

    validate_transaction_access(db_session, current_user, op.OP_1020002.value)

    new_authorization: Authorization = Authorization(**authorization.model_dump())
    new_authorization.id = autorization_id
    new_authorization.audit_user_ip = request.client.host
    new_authorization.audit_user_login = current_user.username

    try:
        return controller.update(db_session, new_authorization)
    except ObjectNotFoundException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_404_NOT_FOUND, detail=ex.args[0]
        ) from ex
