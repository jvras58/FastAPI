from app.database.session import get_session
from app.models.assignment import Assignment
from app.models.authorization import Authorization
from app.models.role import Role
from app.models.transaction import Transaction
from app.models.user import User
from app.utils.security import get_password_hash


def seed_super_user():
    with next(get_session()) as db_session:
        # 1. Inserir usuário administrador
        if not db_session.query(User).filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                display_name='Administrador',
                email='admin@teste.com.br',
                password=get_password_hash('admin123'),
                audit_user_ip='0.0.0.0',
                audit_user_login='system',
            )
            db_session.add(admin_user)
            db_session.commit()
            db_session.refresh(admin_user)
        else:
            admin_user = db_session.query(User).filter_by(username='admin').first()

        # 2. Inserir papel SUPER ADMIN
        if not db_session.query(Role).filter_by(name='SUPER ADMIN').first():
            super_admin_role = Role(
                name='SUPER ADMIN',
                description='Role for system Administrator',
                audit_user_ip='0.0.0.0',
                audit_user_login='system',
            )
            db_session.add(super_admin_role)
            db_session.commit()
            db_session.refresh(super_admin_role)
        else:
            super_admin_role = (
                db_session.query(Role).filter_by(name='SUPER ADMIN').first()
            )

        # 3. Inserir atribuição (assignment) vinculando usuário ao papel
        if (
            not db_session.query(Assignment)
            .filter_by(user_id=admin_user.id, role_id=super_admin_role.id)
            .first()
        ):
            assignment = Assignment(
                user_id=admin_user.id,
                role_id=super_admin_role.id,
                audit_user_ip='0.0.0.0',
                audit_user_login='system',
            )
            db_session.add(assignment)
            db_session.commit()

        # 4. Inserir autorizações para todas as transações
        existing_transactions = db_session.query(Transaction).all()
        for transaction in existing_transactions:
            if (
                not db_session.query(Authorization)
                .filter_by(role_id=super_admin_role.id, transaction_id=transaction.id)
                .first()
            ):
                authorization = Authorization(
                    role_id=super_admin_role.id,
                    transaction_id=transaction.id,
                    audit_user_ip='0.0.0.0',
                    audit_user_login='system',
                )
                db_session.add(authorization)
        db_session.commit()


if __name__ == '__main__':
    seed_super_user()
