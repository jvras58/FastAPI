from unittest.mock import patch

from sqlalchemy import select

from app.models.assignment import Assignment


def test_db_structure_assignment_entity(session, user, role):
    """Test db structure assignment entity."""
    new_assignment: Assignment = Assignment(
        role_id=1,
        user_id=1,
        audit_user_ip='localhost',
        audit_user_login='tester',
    )

    session.add(new_assignment)
    session.commit()

    assignment = session.scalar(select(Assignment).where(Assignment.role_id == 1))

    assert assignment.role_id == 1
    assert assignment.user_id == 1
    assert assignment.audit_created_at
    assert assignment.audit_updated_on

    assert assignment.role.name == role.name
    assert assignment.user.username == user.username


def test_get_assignment_by_id(client, token, assignment_10):
    """Test get assignment by id."""
    with patch(
        'app.api.assignment.router.validate_transaction_access'
    ) as mocked_access_validation:

        mocked_access_validation.return_value = None
        response = client.get(
            '/assignment/4',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 200
        assert response.json()['id'] == 4
        assert response.json()['role_id']
        assert response.json()['user_id']
        assert response.json()['audit_created_at']
        assert response.json()['audit_updated_on']
        assert response.json()['audit_user_ip']
        assert response.json()['audit_user_login']
        assert mocked_access_validation.assert_called_once


def test_get_assignment_by_id_unauthorized(client, assignment_10):
    """Test get assignment by id without authorization."""
    response = client.get(
        '/assignment/4',
    )

    assert response.status_code == 401
    # assert response.json()['detail'] == 'Unauthorized'
    assert response.json()['detail'] == 'Not authenticated'


def test_get_all_assignments(client, token, assignment_10):
    with patch(
        'app.api.assignment.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.get(
            '/assignment/', headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        assert 'assignments' in response.json()
        assert len(response.json()['assignments']) == 10
        assert mocked_access_validation.assert_called_once


def test_create_assignment(client, token, role, user):
    with patch(
        'app.api.assignment.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.post(
            '/assignment/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'role_id': role.id,
                'user_id': user.id,
            },
        )

        assert response.status_code == 201
        assert response.json()['id']
        assert response.json()['role_id'] == role.id
        assert response.json()['user_id'] == user.id
        assert response.json()['audit_created_at']
        assert response.json()['audit_updated_on']
        assert response.json()['audit_user_ip']
        assert response.json()['audit_user_login']
        assert mocked_access_validation.assert_called_once


def test_create_two_equals_assignment_to_a_user(client, token, user, role):
    with patch(
        'app.api.assignment.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.post(
            '/assignment/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'role_id': role.id,
                'user_id': user.id,
            },
        )

        assert response.status_code == 201
        assert mocked_access_validation.assert_called

        response = client.post(
            '/assignment/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'role_id': role.id,
                'user_id': user.id,
            },
        )

        assert response.status_code == 400
        assert response.json()['detail'] == 'Object ASSIGNMENT was not accepted'
        assert mocked_access_validation.assert_called


def test_update_assignment(client, token, assignment_10, role_10):
    with patch(
        'app.api.role.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.post(
            '/role/',
            json={'name': 'role test', 'description': 'description test'},
            headers={'Authorization': f'Bearer {token}'},
        )

        new_role_id = response.json()['id']
    with patch(
        'app.api.assignment.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.get(
            '/assignment/3', headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        assert response.json()['role_id'] == 3
        assert mocked_access_validation.assert_called
    with patch(
        'app.api.assignment.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.put(
            '/assignment/3',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'role_id': new_role_id,
                'user_id': 1,
            },
        )
    with patch(
        'app.api.assignment.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.get(
            '/assignment/3', headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 200
        assert response.json()['role_id'] == new_role_id
        assert response.json()['user_id'] == 1
        assert response.json()['audit_created_at']
        assert response.json()['audit_updated_on']
        assert response.json()['audit_user_ip']
        assert response.json()['audit_user_login']
        assert mocked_access_validation.assert_called


def test_update_assignment_integrity_error(client, token, assignment_10, role_10):
    with patch(
        'app.api.assignment.router.validate_transaction_access'
    ) as mocked_access_validation:

        response = client.get(
            '/assignment/1', headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        original_assignment = response.json()

        response = client.put(
            '/assignment/1',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'role_id': 9999,
                'user_id': original_assignment['user_id'],
            },
        )

        assert response.status_code == 400
        assert response.json()['detail'] == 'Object ASSIGNMENT was not accepted'
        assert mocked_access_validation.assert_called


def test_delete_assingnment(client, token, assignment_10):
    with patch(
        'app.api.assignment.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.delete(
            '/assignment/3',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 200
        assert 'detail' in response.json()
        assert response.json()['detail'] == 'Assignment deleted successfully'
        assert mocked_access_validation.assert_called_once


def test_delete_assingnment_not_found(client, token):
    with patch(
        'app.api.assignment.router.validate_transaction_access'
    ) as mocked_access_validation:
        response = client.delete(
            '/assignment/3',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == 404
        assert 'detail' in response.json()
        assert 'Assignment with ID' in response.json()['detail']
        assert mocked_access_validation.assert_called_once
