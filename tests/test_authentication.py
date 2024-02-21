from jose import jwt

from app.utils.security import create_access_token


def test_jwt_token():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = jwt.decode(token, 'TESTE_SECRET', algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert decoded['exp']   # Testa se o valor de exp foi adicionado ao token


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.clear_password},
    )

    token = response.json()

    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token
    assert token['token_type'] == 'bearer'


def test_execute_user_login_valid_credentials(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.clear_password},
    )
    token = response.json()
    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token
    assert token['token_type'] == 'bearer'


def test_execute_user_login_invalid_credentials(client, user):
    response = client.post(
        '/auth/token',
        data={'username': 'invalid_login', 'password': user.clear_password},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Incorrect email or password'}

    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': 'invalid_password'},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_current_user_invalid_token(client, user):
    token = 'invalid_token'

    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_with_empty_username(client, user):
    token_data = {'sub': ''}
    token = create_access_token(data=token_data)

    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}
