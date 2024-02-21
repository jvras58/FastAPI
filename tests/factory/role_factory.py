import factory

from app.models.role import Role


class RoleFactory(factory.Factory):
    class Meta:
        model = Role

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda obj: f'Role TEST{obj.id}')
    description = factory.LazyAttribute(lambda obj: f'Description TEST{obj.id}')
    audit_user_ip = factory.Faker('ipv4')
    audit_user_login = factory.Faker('user_name')
