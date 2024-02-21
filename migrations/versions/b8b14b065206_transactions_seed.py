"""transactions_seed

Revision ID: b8b14b065206
Revises: 00292430c7bd
Create Date: 2024-02-21 17:28:00.168725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8b14b065206'
down_revision: Union[str, None] = '00292430c7bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --------------------- Assignment ---------------------
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1010001\', \'Assignment - Create\', \'Create a new assignment\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1010002\', \'Assignment - Update\', \'Update a existent assignment\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1010003\', \'Assignment - List\', \'List and search for a assignment\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1010004\', \'Assignment - Delete\', \'Delete a existent assignment\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1010005\', \'Assignment - View\', \'Get a existent assignment\', \'0.0.0.0\', \'system\')')
    # --------------------- Authorization ---------------------
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1020001\', \'Authorization - Create\', \'Create a new authorization\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1020002\', \'Authorization - Update\', \'Update a existent authorization\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1020003\', \'Authorization - List\', \'List and search for a Authorization\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1020004\', \'Authorization - Delete\', \'Delete a existent Authorization\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1020005\', \'Authorization - View\', \'Get a existent Authorization\', \'0.0.0.0\', \'system\')')
    # --------------------- Transaction ---------------------
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1030001\', \'Transaction - Create\', \'Create a new Transaction\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1030002\', \'Transaction - Update\', \'Update a existent Transaction\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1030003\', \'Transaction - List\', \'List and search for a Transaction\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1030004\', \'Transaction - Delete\', \'Delete a existent Transaction\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1030005\', \'Transaction - View\', \'Get a existent Transaction\', \'0.0.0.0\', \'system\')')
        # --------------------- User ---------------------
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1040001\', \'User - Create\', \'Create a new User\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1040002\', \'User - Update\', \'Update a existent User\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1040003\', \'User - List\', \'List and search for a User\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1040004\', \'User - Delete\', \'Delete a existent User\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1040005\', \'User - View\', \'Get a existent User\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1040006\', \'User - Transactions granted\', \'List all transactions granted to a user\', \'0.0.0.0\', \'system\')')
    # --------------------- Role ---------------------
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1050001\', \'Role - Create\', \'Create a new Role\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1050002\', \'Role - Update\', \'Update a existent Role\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1050003\', \'Role - List\', \'List and search for a Role\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1050004\', \'Role - Delete\', \'Delete a existent Role\', \'0.0.0.0\', \'system\')')
    op.execute('INSERT INTO "transaction" (str_operation_code, str_name, str_description,audit_user_ip, audit_user_login) VALUES(\'1050005\', \'Role - View\', \'Get a existent Role\', \'0.0.0.0\', \'system\')')


def downgrade() -> None:
    # --------------------- Assignment ---------------------
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1010001\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1010002\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1010003\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1010004\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1010005\'')
    # --------------------- Authorization ---------------------
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1020001\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1020002\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1020003\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1020004\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1020005\'')
    # --------------------- Transaction ---------------------
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1030001\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1030002\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1030003\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1030004\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1030005\'')
    # --------------------- User ---------------------
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1040001\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1040002\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1040003\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1040004\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1040005\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1040006\'')
    # --------------------- Role ---------------------
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1050001\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1050002\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1050003\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1050004\'')
    op.execute('DELETE FROM "transaction" WHERE str_operation_code=\'1050005\'')
