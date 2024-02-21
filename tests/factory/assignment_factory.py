import factory

from app.models.assignment import Assignment
from tests.factory.role_factory import RoleFactory
from tests.factory.user_factory import UserFactory


class AssignmentFactory(factory.Factory):
    class Meta:
        model = Assignment

    id = factory.Sequence(lambda n: n)
    audit_user_ip = factory.Faker('ipv4')
    audit_user_login = factory.Faker('user_name')

    user = factory.SubFactory(UserFactory)
    role = factory.SubFactory(RoleFactory)

    role_id = factory.LazyAttribute(lambda obj: obj.role.id)
    user_id = factory.LazyAttribute(lambda obj: obj.user.id)


def create_assignment(role, user):
    """
    Cria um ASSIGNMENT no banco de dados.
    """
    return AssignmentFactory.create(role=role, user=user)
