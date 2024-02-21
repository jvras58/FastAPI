import factory

from app.models.user import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    username = factory.Faker('user_name')
    display_name = factory.Faker('name')
    email = factory.Faker('email')
    password = factory.Faker('password')
    audit_user_ip = factory.Faker('ipv4')
    audit_user_login = factory.Faker('user_name')
