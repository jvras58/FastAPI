from unittest.mock import patch

from sqlalchemy import select

from app.models.transaction import Transaction


def test_db_structure_trasaction_entity(session):
    new_transaction: Transaction = Transaction(
        name='Trasação de teste',
        description='Descrição da transação de teste',
        operation_code='TST0001',
        audit_user_ip='localhost',
        audit_user_login='tester',
    )

    session.add(new_transaction)
    session.commit()

    transaction = session.scalar(
        select(Transaction).where(Transaction.name == 'Trasação de teste')
    )

    assert transaction.name == 'Trasação de teste'
    assert transaction.id == 1
    assert transaction.audit_created_at
    assert transaction.audit_updated_on


def test_create_transaction_success(client, token):
    with patch(
        'app.api.transaction.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.post(
            '/transaction/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'name': 'Trasação de teste',
                'description': 'Descrição da transação de teste',
                'operation_code': 'TST0001',
            },
        )

        transaction_created = response.json()

        assert response.status_code == 201
        assert transaction_created['name'] == 'Trasação de teste'
        assert transaction_created['description'] == 'Descrição da transação de teste'
        assert transaction_created['id'] == 1
        assert transaction_created['operation_code'] == 'TST0001'
        assert transaction_created['audit_created_at']
        assert transaction_created['audit_updated_on']
        assert transaction_created['audit_user_ip']
        assert transaction_created['audit_user_login']
        assert mocked_access_validation.assert_called_once


def test_create_transaction_IntegrityValidationException(
    client, token, transaction_10_plus_one
):
    with patch(
        'app.api.transaction.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.post(
            '/transaction/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'name': 'Transação TEST666',
                'description': 'Descrição TEST666',
                'operation_code': 'TEST666',
            },
        )

    transaction_created = response.json()
    assert response.status_code == 400
    assert transaction_created['detail'] == 'Object TRANSACTION was not accepted'
    assert mocked_access_validation.assert_called_once


def test_update_transaction_sucess(client, token, transaction_10_plus_one):
    with patch(
        'app.api.transaction.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.get(
            '/transaction/?op_code=TEST666',
            headers={'Authorization': f'Bearer {token}'},
        )
        trans_id = response.json()['transactions'][0]['id']
        assert mocked_access_validation.assert_called_once
    with patch(
        'app.api.transaction.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.put(
            f'/transaction/{trans_id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'name': 'Transação ALTERADA',
                'description': 'Descrição ALTERADA',
                'operation_code': 'TST0010',
            },
        )

        transaction_updated = response.json()

        assert response.status_code == 200
        assert transaction_updated['name'] == 'Transação ALTERADA'
        assert transaction_updated['description'] == 'Descrição ALTERADA'
        assert transaction_updated['id'] == 10
        assert transaction_updated['operation_code'] == 'TST0010'
        assert transaction_updated['audit_created_at']
        assert transaction_updated['audit_updated_on']
        assert transaction_updated['audit_user_ip']
        assert transaction_updated['audit_user_login']


def test_update_transaction_not_found(client, token):
    with patch(
        'app.api.transaction.router.validate_transaction_access'
    ) as mocked_access_validation:
        non_existent_transaction_id = 9999
        response = client.put(
            f'/transaction/{non_existent_transaction_id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'name': 'Transação ALTERADA',
                'description': 'Descrição ALTERADA',
                'operation_code': 'TST0010',
            },
        )

        assert response.status_code == 404
        assert 'not found' in response.json()['detail'].lower()
        assert mocked_access_validation.assert_called_once


def test_get_transaction_by_op_code(client, transaction_10_plus_one, token):
    with patch(
        'app.api.transaction.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.get(
            '/transaction/?op_code=TEST666',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 200
        assert 'transactions' in response.json()
        assert len(response.json()['transactions']) == 1
        assert response.json()['transactions'][0]['operation_code'] == 'TEST666'
        assert mocked_access_validation.assert_called_once


def test_list_transactions(client, transaction_200, token):
    with patch(
        'app.api.transaction.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.get(
            '/transaction/?limit=300',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 200
        assert 'transactions' in response.json()
        transaction_list = response.json()['transactions']
        assert len(transaction_list) == 200
        assert mocked_access_validation.assert_called_once


def test_get_transaction_by_id(client, transaction_10_plus_one, token):
    with patch(
        'app.api.transaction.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.get(
            '/transaction/10',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 200
        assert 'id' in response.json()
        assert response.json()['id'] == 10
        assert response.json()['operation_code'] == 'TEST666'
        assert response.json()['name'] == 'Transação TEST666'
        assert response.json()['description'] == 'Descrição TEST666'
        assert mocked_access_validation.assert_called_once


def test_delete_transection_success(client, token, transaction_10_plus_one):
    with patch(
        'app.api.transaction.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.get(
            '/transaction/?op_code=TEST666',
            headers={'Authorization': f'Bearer {token}'},
        )
        trans_id = response.json()['transactions'][0]['id']
        assert mocked_access_validation.assert_called_once
    with patch(
        'app.api.transaction.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.delete(
            f'/transaction/{trans_id}',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 200
        assert response.json()['detail'] == 'Transaction deleted'
        assert mocked_access_validation.assert_called_once


def test_delete_none_existent_transaction(client, token):
    with patch(
        'app.api.transaction.router.validate_transaction_access'
    ) as mocked_access_validation:
        non_existent_transaction_id = 9999
        response = client.delete(
            f'/transaction/{non_existent_transaction_id}',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 404
        assert 'not found' in response.json()['detail'].lower()
        assert mocked_access_validation.assert_called_once
