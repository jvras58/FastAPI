import factory

from app.models.transaction import Transaction


class TransactonFactory(factory.Factory):
    class Meta:
        model = Transaction

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda obj: f'Transaction TEST{obj.id}')
    description = factory.LazyAttribute(lambda obj: f'Description TEST{obj.id}')
    operation_code = factory.LazyAttribute(lambda obj: f'TEST{obj.id}')
    audit_user_ip = factory.Faker('ipv4')
    audit_user_login = factory.Faker('user_name')
