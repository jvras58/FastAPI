from unittest.mock import patch

from sqlalchemy import select

from app.models.authorization import Authorization


def test_authorization_db_structure(session, role, trasaction):
    new_authorization = Authorization(
        role=role,
        transaction=trasaction,
        audit_user_ip='localhost',
        audit_user_login='tester',
    )

    session.add(new_authorization)
    session.commit()

    auth_db = session.scalar(
        select(Authorization).where(
            Authorization.role_id == role.id,
            Authorization.transaction_id == trasaction.id,
        )
    )

    assert auth_db.id == 1
    assert auth_db.role_id == role.id
    assert auth_db.transaction_id == trasaction.id
    assert auth_db.audit_created_at
    assert auth_db.audit_updated_on
    assert auth_db.audit_user_ip == 'localhost'
    assert auth_db.audit_user_login == 'tester'


def test_create_athorization(client, token, role, trasaction):
    with patch(
        'app.api.authorization.router.validate_transaction_access'
    ) as mocked_access_validation:

        response = client.post(
            '/authorization/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'role_id': role.id,
                'transaction_id': trasaction.id,
            },
        )

        assert response.status_code == 201
        assert response.json()['id'] == 1
        assert response.json()['role_id'] == role.id
        assert response.json()['transaction_id'] == trasaction.id
        assert response.json()['audit_created_at']
        assert response.json()['audit_updated_on']
        assert response.json()['audit_user_ip']
        assert response.json()['audit_user_login']
        assert mocked_access_validation.assert_called_once


def test_create_two_equals_athorization(client, token, role, trasaction):
    with patch(
        'app.api.authorization.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.post(
            '/authorization/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'role_id': role.id,
                'transaction_id': trasaction.id,
            },
        )

        assert response.status_code == 201
        assert response.json()['id'] == 1
        assert mocked_access_validation.assert_called_once
    with patch(
        'app.api.authorization.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.post(
            '/authorization/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'role_id': role.id,
                'transaction_id': trasaction.id,
            },
        )

        assert response.status_code == 400
        assert response.json()['detail'] == 'Object AUTHORIZATION was not accepted'
        assert mocked_access_validation.assert_called_once


def test_get_all_authorizations(client, token, authorization_10_plus_one):
    with patch(
        'app.api.authorization.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.get(
            '/authorization/', headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        assert 'authorizations' in response.json()
        assert len(response.json()['authorizations']) == 11
        assert mocked_access_validation.assert_called_once


def test_get_authorization_by_id(client, token, authorization_10_plus_one):
    with patch(
        'app.api.authorization.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.get(
            '/authorization/1', headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        assert 'id' in response.json()
        assert response.json()['id'] == 1
        assert response.json()['role_id'] == 1
        assert response.json()['transaction_id'] == 1
        assert response.json()['audit_created_at']
        assert response.json()['audit_updated_on']
        assert response.json()['audit_user_ip']
        assert response.json()['audit_user_login']
        assert mocked_access_validation.assert_called_once


def test_get_authorization_by_id_not_found(client, token):
    with patch(
        'app.api.authorization.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.get(
            '/authorization/1',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 404
        assert response.json()['detail'] == 'Object AUTHORIZATION was not found'
        assert mocked_access_validation.assert_called_once


def test_delete_authorization(client, token, authorization_10_plus_one):
    with patch(
        'app.api.authorization.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.delete(
            '/authorization/1', headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        assert 'detail' in response.json()
        assert response.json()['detail'] == 'Object AUTHORIZATION was deleted'
        assert mocked_access_validation.assert_called_once


def test_delete_authorization_not_found(client, token):
    with patch(
        'app.api.authorization.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.delete(
            '/authorization/1', headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 404
        assert response.json()['detail'] == 'Object AUTHORIZATION was not found'
        assert mocked_access_validation.assert_called_once


def test_update_authorization(client, token, authorization_10_plus_one):
    with patch(
        'app.api.role.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.post(
            '/role',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'name': 'role test com auth',
                'description': 'description test com authorization',
            },
        )
        assert response.status_code == 201
        assert 'id' in response.json()
        new_role_id = response.json()['id']
        assert mocked_access_validation.assert_called_once
    with patch(
        'app.api.authorization.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.get(
            '/authorization/1', headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        assert 'id' in response.json()
        old_role_id = response.json()['role_id']
        assert mocked_access_validation.assert_called_once
    with patch(
        'app.api.authorization.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.put(
            '/authorization/1',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'role_id': new_role_id,
                'transaction_id': 10,
            },
        )
        assert response.status_code == 200
        assert 'id' in response.json()
        assert response.json()['id'] == 1
        assert response.json()['role_id'] != old_role_id
        assert response.json()['role_id'] == new_role_id
        assert response.json()['transaction_id'] == 10
        assert response.json()['audit_created_at']
        assert response.json()['audit_updated_on']
        assert response.json()['audit_user_ip']
        assert response.json()['audit_user_login']
        assert mocked_access_validation.assert_called_once


def test_update_authorization_not_found(client, token):
    with patch(
        'app.api.authorization.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.put(
            '/authorization/1',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'role_id': 1,
                'transaction_id': 1,
            },
        )

        assert response.status_code == 404
        assert 'Authorization with ID' in response.json()['detail']
        assert mocked_access_validation.assert_called_once
