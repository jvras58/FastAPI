"""Seed Transactions Module."""
from app.api.transaction.enum_operation_code import EnumOperationCode
from app.database.session import get_session
from app.models.transaction import Transaction


def seed_transactions():
    """Seed initial transactions into the database."""
    with next(get_session()) as db_session:
        # List of transactions to be entered
        transactions_data = [
            {
                "operation_code": EnumOperationCode.OP_1010001.value,
                "name": "Assignment - Create",
                "description": "Create a new assignment",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1010002.value,
                "name": "Assignment - Update",
                "description": "Update a existent assignment",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1010003.value,
                "name": "Assignment - List",
                "description": "List and search for a assignment",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1010004.value,
                "name": "Assignment - Delete",
                "description": "Delete a existent assignment",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1010005.value,
                "name": "Assignment - View",
                "description": "Get a existent assignment",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1020001.value,
                "name": "Authorization - Create",
                "description": "Create a new authorization",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1020002.value,
                "name": "Authorization - Update",
                "description": "Update a existent authorization",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1020003.value,
                "name": "Authorization - List",
                "description": "List and search for a Authorization",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1020004.value,
                "name": "Authorization - Delete",
                "description": "Delete a existent Authorization",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1020005.value,
                "name": "Authorization - View",
                "description": "Get a existent Authorization",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1030001.value,
                "name": "Transaction - Create",
                "description": "Create a new Transaction",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1030002.value,
                "name": "Transaction - Update",
                "description": "Update a existent Transaction",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1030003.value,
                "name": "Transaction - List",
                "description": "List and search for a Transaction",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1030004.value,
                "name": "Transaction - Delete",
                "description": "Delete a existent Transaction",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1030005.value,
                "name": "Transaction - View",
                "description": "Get a existent Transaction",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1040001.value,
                "name": "User - Create",
                "description": "Create a new User",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1040002.value,
                "name": "User - Update",
                "description": "Update a existent User",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1040003.value,
                "name": "User - List",
                "description": "List and search for a User",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1040004.value,
                "name": "User - Delete",
                "description": "Delete a existent User",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1040005.value,
                "name": "User - View",
                "description": "Get a existent User",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1040006.value,
                "name": "User - Transactions granted",
                "description": "List all transactions granted to a user",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1050001.value,
                "name": "Role - Create",
                "description": "Create a new Role",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1050002.value,
                "name": "Role - Update",
                "description": "Update a existent Role",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1050003.value,
                "name": "Role - List",
                "description": "List and search for a Role",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1050004.value,
                "name": "Role - Delete",
                "description": "Delete a existent Role",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_1050005.value,
                "name": "Role - View",
                "description": "Get a existent Role",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
            {
                "operation_code": EnumOperationCode.OP_2000001.value,
                "name": "Data Processing - Execute",
                "description": "Perform data processing with AI",
                "audit_user_ip": "0.0.0.0",
                "audit_user_login": "system",
            },
        ]

        # Inserir cada transação, verificando se já existe
        for transaction_data in transactions_data:
            if (
                not db_session.query(Transaction)
                .filter_by(operation_code=transaction_data['operation_code'])
                .first()
            ):
                transaction = Transaction(
                    operation_code=transaction_data['operation_code'],
                    name=transaction_data['name'],
                    description=transaction_data['description'],
                    audit_user_ip=transaction_data['audit_user_ip'],
                    audit_user_login=transaction_data['audit_user_login'],
                )
                db_session.add(transaction)
        db_session.commit()


if __name__ == '__main__':
    seed_transactions()
