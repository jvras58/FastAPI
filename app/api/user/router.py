from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi import status as HTTP_STATUS
from sqlalchemy.orm import Session

from app.api.authentication.controller import get_current_user
from app.api.authorization.controller import (
    get_user_authorized_transactions,
    validate_transaction_access,
)
from app.api.transaction.enum_operation_code import EnumOperationCode as op
from app.api.transaction.schemas import TransactionListSchema
from app.api.user.controller import UserController
from app.api.user.schemas import UserList, UserPublic, UserSchema
from app.database.session import get_session
from app.models.user import User
from app.utils.base_schemas import SimpleMessageSchema
from app.utils.exceptions import IntegrityValidationException, ObjectNotFoundException

router = APIRouter()
user_controller = UserController()

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=201, response_model=UserPublic)
async def create_new_user(user: UserSchema, request: Request, session: Session):

    new_user: User = User(**user.model_dump())
    new_user.audit_user_ip = request.client.host
    new_user.audit_user_login = 'adm'  # FIXME: Ajustar para pegar o login do usuário

    try:
        return user_controller.save(session, new_user)
    except IntegrityValidationException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_400_BAD_REQUEST,
            detail='Object USER was not accepted',
        ) from ex


@router.get(
    '/{user_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=UserPublic,
)
def get_user_by_id(user_id: int, db_session: Session, current_user: CurrentUser):
    validate_transaction_access(db_session, current_user, op.OP_1040005.value)

    return user_controller.get(db_session, user_id)


@router.get('/', response_model=UserList)
def read_users(
    db_session: Session, current_user: CurrentUser, skip: int = 0, limit: int = 100
):
    validate_transaction_access(db_session, current_user, op.OP_1040003.value)
    users: list[User] = user_controller.get_all(db_session, skip, limit)
    return {'users': users}


@router.put('/{user_id}', response_model=UserPublic)
def update_existing_user(
    user_id: int,
    user: UserSchema,
    request: Request,
    db_session: Session,
    current_user: CurrentUser,
):
    validate_transaction_access(db_session, current_user, op.OP_1040002.value)

    try:
        new_user: User = User(**user.model_dump())
        new_user.id = user_id

        new_user.audit_user_ip = request.client.host
        new_user.audit_user_login = (
            'adm'  # FIXME: Ajustar para pegar o login do usuário
        )

        return user_controller.update(db_session, new_user)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.args[0]) from ex


@router.delete('/{user_id}', response_model=SimpleMessageSchema)
def delete_existing_user(
    user_id: int,
    db_session: Session,
    current_user: CurrentUser,
):
    validate_transaction_access(db_session, current_user, op.OP_1040004.value)

    try:
        user_controller.delete(db_session, user_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.args[0]) from ex

    return {'detail': 'User deleted'}


@router.get('/{user_id}/transactions', response_model=TransactionListSchema)
def get_user_transactions(user_id: int, db_session: Session, current_user: CurrentUser):
    validate_transaction_access(db_session, current_user, op.OP_1040006.value)
    return {'transactions': get_user_authorized_transactions(db_session, user_id)}
