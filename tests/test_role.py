from unittest.mock import patch

from sqlalchemy import select

from app.models.role import Role


def test_db_structure_role_entity(session):
    """Test db structure role entity."""
    new_role: Role = Role(
        name='Role de teste',
        description='Descrição da role de teste',
        audit_user_ip='localhost',
        audit_user_login='tester',
    )

    session.add(new_role)
    session.commit()

    role = session.scalar(select(Role).where(Role.name == 'Role de teste'))

    assert role.name == 'Role de teste'
    assert role.id == 1
    assert role.audit_created_at
    assert role.audit_updated_on


def test_get_role_by_id(client, token, role_10):
    """Test get role."""
    with patch(
        'app.api.role.router.validate_transaction_access'
    ) as mocked_access_validation:

        response = client.get('/role/2', headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 200
        assert response.json()['id'] == 2
        assert response.json()['name'] == 'Role TEST2'
        assert response.json()['description'] == 'Description TEST2'
        assert mocked_access_validation.assert_called_once


def test_get_all_roles(client, token, role_10):
    with patch(
        'app.api.role.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.get('/role/', headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 200
        assert 'roles' in response.json()
        assert len(response.json()['roles']) == 10
        assert mocked_access_validation.assert_called_once


def test_create_role(client, token):
    with patch(
        'app.api.role.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.post(
            '/role/',
            json={'name': 'role test', 'description': 'description test'},
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 201
        assert response.json()['id'] == 1
        assert response.json()['name'] == 'role test'
        assert response.json()['description'] == 'description test'
        assert response.json()['audit_created_at']
        assert response.json()['audit_updated_on']
        assert response.json()['audit_user_ip']
        assert response.json()['audit_user_login']
        assert mocked_access_validation.assert_called_once


def test_create_role_with_name_already_exist(client, token):
    role_data = {'name': 'Role TEST2', 'description': 'description test'}
    with patch(
        'app.api.role.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.post(
            '/role/',
            json=role_data,
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 201
    with patch(
        'app.api.role.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.post(
            '/role/',
            json=role_data,
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 400
        assert response.json()['detail'] == 'Object ROLE was not accepted'
        assert mocked_access_validation.assert_called_once


def test_update_role(client, token):
    role_data = {'name': 'Role TEST2', 'description': 'description test'}
    with patch(
        'app.api.role.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.post(
            '/role/',
            json=role_data,
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 201
    with patch(
        'app.api.role.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.put(
            '/role/1',
            json={'name': 'Role TEST2', 'description': 'description test updated'},
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 200
        assert response.json()['name'] == 'Role TEST2'
        assert response.json()['description'] == 'description test updated'
        assert mocked_access_validation.assert_called_once


def test_update_none_existent_role(client, token):
    """Test update a none existent role."""
    with patch(
        'app.api.role.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.put(
            '/role/1000000',
            json={'name': 'Role TEST2', 'description': 'description test updated'},
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 404
        assert 'not found' in response.json()['detail'].lower()
        assert mocked_access_validation.assert_called_once


def test_delete_role(client, token):
    role_data = {'name': 'Role TEST2', 'description': 'description test'}
    with patch(
        'app.api.role.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.post(
            '/role/',
            json=role_data,
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 201
        assert mocked_access_validation.assert_called_once
    with patch(
        'app.api.role.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.delete(
            '/role/1',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 200
        assert 'detail' in response.json()
        assert response.json()['detail'] == 'Role deleted successfully'
        assert mocked_access_validation.assert_called_once


def test_delete_role_not_found(client, token):
    with patch(
        'app.api.role.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.delete(
            '/role/1',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 404
        assert 'detail' in response.json()
        assert response.json()['detail'] == 'Role with ID [1] not found'
        assert mocked_access_validation.assert_called_once
