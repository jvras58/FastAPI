"""Router for transaction-related operations."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi import status as HTTP_STATUS
from sqlalchemy.orm import Session

from app.api.authentication.controller import get_current_user
from app.api.authorization.controller import validate_transaction_access
from app.api.transaction.enum_operation_code import EnumOperationCode as op
from app.api.transaction.schemas import (
    TransactionDTOSchema,
    TransactionListSchema,
    TransactionSchema,
)
from app.database.session import get_session
from app.models.transaction import Transaction
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
transaction_controller = GenericController(Transaction)
logger = get_logger(__name__)

SessionDep = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/',
    status_code=HTTP_STATUS.HTTP_201_CREATED,
    response_model=TransactionSchema,
)
async def create_transaction(
    transaction: TransactionDTOSchema,
    request: Request,
    current_user: CurrentUser,
    db_session: SessionDep,
):
    """Create a new transaction."""
    validate_transaction_access(db_session, current_user, op.OP_1030001.value)
    logger.info(
        "Create transaction op_code=%s by user=%s ip=%s",
        transaction.operation_code,
        current_user.username,
        get_client_ip(request),
    )
    new_transaction: Transaction = Transaction(**transaction.model_dump())

    new_transaction.audit_user_login = current_user.username
    new_transaction.audit_user_ip = get_client_ip(request)

    try:
        new_transaction = transaction_controller.save(
            db_session, new_transaction
        )
        logger.info("Transaction created id=%s", new_transaction.id)
    except IntegrityValidationException as ex:
        logger.warning("Transaction create failed: %s", ex.args[0])
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_400_BAD_REQUEST,
            detail='Object TRANSACTION was not accepted',
        ) from ex
    return new_transaction


@router.get(
    '/',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=TransactionListSchema,
)
async def get_all_transactions(
    db_session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    op_code: str | None = None,
):
    """Get all transactions with optional filtering by operation code."""
    validate_transaction_access(db_session, current_user, op.OP_1030003.value)
    logger.info(
        "List transactions skip=%s limit=%s op_code=%s by user=%s",
        skip,
        limit,
        op_code,
        current_user.username,
    )
    criterias = {}
    if op_code:
        criterias['operation_code'] = op_code

    transactions: list[Transaction] = transaction_controller.get_all(
        db_session, skip, limit, **criterias
    )
    return {'transactions': transactions}


@router.get(
    '/{transaction_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=TransactionSchema,
)
def get_transaction_by_id(
    transaction_id: int, db_session: SessionDep, current_user: CurrentUser
):
    """Get transaction by ID."""
    validate_transaction_access(db_session, current_user, op.OP_1030005.value)

    logger.info(
        "Fetch transaction id=%s by user=%s",
        transaction_id,
        current_user.username,
    )

    return transaction_controller.get(db_session, transaction_id)


@router.put(
    '/{transaction_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=TransactionSchema,
)
async def update_transaction(
    db_session: SessionDep,
    transaction_id: int,
    transaction: TransactionDTOSchema,
    request: Request,
    current_user: CurrentUser,
):
    """Update an existing transaction."""
    validate_transaction_access(db_session, current_user, op.OP_1030002.value)

    logger.info(
        "Update transaction id=%s op_code=%s by user=%s ip=%s",
        transaction_id,
        transaction.operation_code,
        current_user.username,
        get_client_ip(request),
    )

    new_transaction: Transaction = Transaction(**transaction.model_dump())
    new_transaction.id = transaction_id
    new_transaction.audit_user_login = current_user.username
    new_transaction.audit_user_ip = get_client_ip(request)

    try:
        updated = transaction_controller.update(db_session, new_transaction)
        logger.info("Transaction updated id=%s", transaction_id)
        return updated
    except ObjectNotFoundException as ex:
        logger.warning(
            "Transaction update failed id=%s: %s",
            transaction_id,
            ex.args[0],
        )
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_404_NOT_FOUND, detail=ex.args[0]
        ) from ex


@router.delete('/{transaction_id}', response_model=SimpleMessageSchema)
def delete_existing_transaction(
    transaction_id: int,
    db_session: SessionDep,
    current_user: CurrentUser,
):
    """Delete a transaction by ID."""
    validate_transaction_access(db_session, current_user, op.OP_1030004.value)

    logger.info(
        "Delete transaction id=%s by user=%s",
        transaction_id,
        current_user.username,
    )

    try:
        transaction_controller.delete(db_session, transaction_id)
    except ObjectNotFoundException as ex:
        logger.warning(
            "Transaction delete failed id=%s: %s",
            transaction_id,
            ex.args[0],
        )
        raise HTTPException(status_code=404, detail=ex.args[0]) from ex

    return {'detail': 'Transaction deleted'}
