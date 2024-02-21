import factory

from app.models.authorization import Authorization
from tests.factory.role_factory import RoleFactory
from tests.factory.trasaction_factory import TransactonFactory


class AuthorizationFactory(factory.Factory):
    class Meta:
        model = Authorization

    id = factory.Sequence(lambda n: n)
    audit_user_ip = factory.Faker('ipv4')
    audit_user_login = factory.Faker('user_name')

    role = factory.SubFactory(RoleFactory)
    transaction = factory.SubFactory(TransactonFactory)

    role_id = factory.LazyAttribute(lambda obj: obj.role.id)
    transaction_id = factory.LazyAttribute(lambda obj: obj.transaction.id)


def create_authorization(role, transaction):
    """
    Cria um AUTHORIZATION no banco de dados.
    """
    return AuthorizationFactory.create(role=role, transaction=transaction)
