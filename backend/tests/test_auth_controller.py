import pytest
from models.user import User

def test_register_user(test_client, init_database):
    response = test_client.post('/register', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'
    assert User.query.filter_by(email='new@example.com').first() is not None

def test_register_duplicate_email(test_client, init_database):
    test_client.post('/register', json={
        'username': 'user1',
        'email': 'duplicate@example.com',
        'password': 'password123'
    })
    response = test_client.post('/register', json={
        'username': 'user2',
        'email': 'duplicate@example.com',
        'password': 'password123'
    })
    assert response.status_code == 409
    assert response.json['error'] == 'User already exists'

def test_login_success(test_client, init_database):
    response = test_client.post('/login', json={
        'email': 'admin@example.com',
        'password': 'password'
    })
    assert response.status_code == 200
    assert 'token' in response.json
    assert response.json['user']['email'] == 'admin@example.com'

def test_login_invalid_credentials(test_client, init_database):
    response = test_client.post('/login', json={
        'email': 'admin@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.json['error'] == 'Invalid credentials'

def test_get_me(test_client, auth_headers):
    response = test_client.get('/me', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['username'] == 'admin'
