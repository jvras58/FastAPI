"""Controller for handling authorization logic."""
from sqlalchemy import Select, and_, select

from app.api.user.controller import UserController
from app.database.session import Session
from app.models.assignment import Assignment
from app.models.authorization import Authorization
from app.models.role import Role
from app.models.transaction import Transaction
from app.models.user import User
from app.utils.exceptions import (
    AmbiguousAuthorizationException,
    CredentialsValidationException,
    IllegalAccessException,
)

user_controller = UserController()


def validate_transaction_access(
    db_session: Session, current_user: User, op_code: str
) -> None:
    """Validate if the current user has access to the specified operation code."""
    if not current_user:
        raise CredentialsValidationException()

    transactions = get_user_authorized_transactions(
        db_session, current_user.id, op_code
    )
    if not transactions:
        raise IllegalAccessException(current_user.id, op_code)

    if len(transactions) > 1:
        raise AmbiguousAuthorizationException(current_user.id, op_code)

    if transactions[0].operation_code != op_code:
        raise IllegalAccessException(
            current_user.id, transactions[0].operation_code
        )


def get_user_authorized_transactions(
    db_session: Session, user_id: int, op_code: str | None = None
) -> list[Transaction]:
    """
    Retrieve transactions authorized for a specific user,
    optionally filtered by operation code.
    """
    query: Select = (
        select(Transaction)
        .join(Authorization)
        .join(Role)
        .join(Assignment)
        .join(User)
    )

    criteria_and = []
    criteria_and.append(User.id == user_id)

    if op_code:
        criteria_and.append(Transaction.operation_code == op_code)

    query = query.filter(and_(*criteria_and))

    transactions: list[Transaction] = list(db_session.scalars(query).all())
    return transactions
