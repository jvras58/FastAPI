"""bigbang

Revision ID: 00292430c7bd
Revises: 
Create Date: 2024-02-21 17:20:35.437247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00292430c7bd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('str_name', sa.String(), nullable=False),
    sa.Column('str_description', sa.String(), nullable=False),
    sa.Column('audit_user_ip', sa.String(length=16), nullable=False),
    sa.Column('audit_created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('audit_updated_on', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('audit_user_login', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_role_name', 'role', ['str_name'], unique=True)
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('str_name', sa.String(), nullable=False),
    sa.Column('str_description', sa.String(), nullable=False),
    sa.Column('str_operation_code', sa.String(length=7), nullable=False),
    sa.Column('audit_user_ip', sa.String(length=16), nullable=False),
    sa.Column('audit_created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('audit_updated_on', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('audit_user_login', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_transaction_op_code', 'transaction', ['str_operation_code'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('str_display_name', sa.String(), nullable=False),
    sa.Column('str_username', sa.String(), nullable=False),
    sa.Column('str_password', sa.String(), nullable=False),
    sa.Column('str_email', sa.String(), nullable=False),
    sa.Column('audit_user_ip', sa.String(length=16), nullable=False),
    sa.Column('audit_created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('audit_updated_on', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('audit_user_login', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_user_email', 'user', ['str_email'], unique=True)
    op.create_index('idx_user_username', 'user', ['str_username'], unique=True)
    op.create_table('assignment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('audit_user_ip', sa.String(length=16), nullable=False),
    sa.Column('audit_created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('audit_updated_on', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('audit_user_login', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_user_role', 'assignment', ['user_id', 'role_id'], unique=True)
    op.create_table('authorization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.Column('audit_user_ip', sa.String(length=16), nullable=False),
    sa.Column('audit_created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('audit_updated_on', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('audit_user_login', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['transaction_id'], ['transaction.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_role_transaction', 'authorization', ['role_id', 'transaction_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_role_transaction', table_name='authorization')
    op.drop_table('authorization')
    op.drop_index('idx_user_role', table_name='assignment')
    op.drop_table('assignment')
    op.drop_index('idx_user_username', table_name='user')
    op.drop_index('idx_user_email', table_name='user')
    op.drop_table('user')
    op.drop_index('idx_transaction_op_code', table_name='transaction')
    op.drop_table('transaction')
    op.drop_index('idx_role_name', table_name='role')
    op.drop_table('role')
    # ### end Alembic commands ###