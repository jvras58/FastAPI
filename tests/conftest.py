import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.session import get_session
from app.models.assignment import Assignment
from app.models.authorization import Authorization
from app.models.role import Role
from app.models.transaction import Transaction
from app.models.user import User
from app.startup import app
from app.utils.base_model import Base
from app.utils.security import get_password_hash
from tests.factory.assignment_factory import AssignmentFactory, create_assignment
from tests.factory.authorization_factory import (
    AuthorizationFactory,
    create_authorization,
)
from tests.factory.role_factory import RoleFactory
from tests.factory.trasaction_factory import TransactonFactory
from tests.factory.user_factory import UserFactory


@pytest.fixture
def client(session):
    """
    Contexto de webclient para teste de APIRest

    Returns:
        TestClient: Uma instancia de TestClient do FastAPI.
    """

    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()

    return TestClient(app)


@pytest.fixture
def session():
    """
    Contexto de Session para teste de estrutura de banco de dados.

    Yields:
        Session: Uma instancia de Session do SQLAlchemy
    """
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
        # echo=True,
    )

    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    yield Session()
    Base.metadata.drop_all(engine)


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Define o pragma de chaves estrangeiras para conexões de banco de dados SQLite.

    Args:
        dbapi_connection: O objeto de conexão com o banco de dados.
        connection_record: O objeto de registro de conexão.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()


@pytest.fixture
def user(session):
    """
    Cria uma ingessão de User para os testes.

    Args:
        session (Session): Uma instância de Session do SQLAlchemy.

    Returns:
        User: Uma instância de User do sistema.
    """
    clr_password = 'testtest'
    user = User(
        username='Teste',
        display_name='User Teste',
        email='teste@test.com',
        password=get_password_hash(clr_password),
        audit_user_ip='0.0.0.0',
        audit_user_login='tester',
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clear_password = clr_password
    return user


@pytest.fixture
def other_user(session):
    """
    Cria uma ingessão de User para os testes.

    Args:
        session (Session): Uma instância de Session do SQLAlchemy.

    Returns:
        User: Uma instância de User do sistema.
    """
    clr_password = 'Qwert123'
    user = User(
        username='TesteOutro',
        email='teste_outro@test.com',
        display_name='User Teste Outro',
        password=get_password_hash(clr_password),
        audit_user_ip='0.0.0.0',
        audit_user_login='tester',
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clear_password = clr_password
    return user


@pytest.fixture
def user_10(session):
    """
    Cria uma lista de 10 objetos Users para os testes.
    """
    UserFactory.reset_sequence()
    user: list[User] = UserFactory.build_batch(10)
    session.add_all(user)
    session.commit()

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.clear_password},
    )
    return response.json()['access_token']


@pytest.fixture
def trasaction(session) -> Transaction:
    trasaction = TransactonFactory.build()
    session.add(trasaction)
    session.commit()
    session.refresh(trasaction)
    return trasaction


@pytest.fixture
def transaction_200(session):
    TransactonFactory.reset_sequence()
    trasactions: list[Transaction] = TransactonFactory.build_batch(200)
    session.add_all(trasactions)
    session.commit()

    return trasactions


@pytest.fixture
def transaction_10_plus_one(session):
    TransactonFactory.reset_sequence()
    trasactions: list[Transaction] = TransactonFactory.build_batch(10)
    session.add_all(trasactions)
    session.commit()

    trans_test666 = Transaction(
        name='Transação TEST666',
        description='Descrição TEST666',
        operation_code='TEST666',
        audit_user_ip='localhost',
        audit_user_login='tester',
    )

    session.add(trans_test666)
    session.commit()
    trasactions.append(trans_test666)

    return trasactions


@pytest.fixture
def role_10(session):
    RoleFactory.reset_sequence()
    roles: list[Role] = RoleFactory.build_batch(10)
    session.add_all(roles)
    session.commit()

    return roles


@pytest.fixture
def role(session):
    """
    Cria um ROLE no banco de dados.
    """
    new_role = Role(
        name='ROLE_TEST',
        description='ROLE_TEST',
        audit_user_ip='localhost',
        audit_user_login='tester',
    )
    session.add(new_role)
    session.commit()
    session.refresh(new_role)
    return new_role


@pytest.fixture
def assignment_10(session, user, role_10):
    """
    Cria um ROLE no banco de dados.
    """
    AssignmentFactory.reset_sequence()
    assignments: list[Assignment] = []
    db_user = session.get(User, user.id)

    for role in role_10:
        db_role = session.get(Role, role.id)
        new_assignment = create_assignment(db_role, db_user)
        assignments.append(new_assignment)

    session.add_all(assignments)
    session.commit()
    return assignments


@pytest.fixture
def authorization_10_plus_one(session, role, transaction_10_plus_one):
    """
    Cria 10 Autorizações no banco de dados.
    """
    AuthorizationFactory.reset_sequence()
    authorizations: list[Authorization] = []
    db_role = session.get(Role, role.id)

    for transaction in transaction_10_plus_one:
        db_transaction = session.get(Transaction, transaction.id)
        new_authorization = create_authorization(db_role, db_transaction)
        authorizations.append(new_authorization)

    session.add_all(authorizations)
    session.commit()
    return authorizations
