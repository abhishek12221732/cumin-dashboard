import pytest
from app import create_app
from models.db import db
from models.user import User
from models.permission import Permission
from models.role import Role
from werkzeug.security import generate_password_hash
import os
import time
import tempfile

@pytest.fixture
def test_client():
    # Create isolated app instance for each test
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key',
        'JWT_SECRET_KEY': 'test-jwt-key'
    })
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def init_database(test_client):
    # Setup basic permissions and roles
    permissions = [
        Permission(action='create_team'),
        Permission(action='create_project'),
        Permission(action='create_task'),
        Permission(action='edit_any_task'),
        Permission(action='edit_own_task'),
        Permission(action='manage_project'),
        Permission(action='add_team_member'),
        Permission(action='assign_team_role'),
        Permission(action='assign_project_role'),
        Permission(action='view_tasks'),
        Permission(action='view_project'),
        Permission(action='view_team_members')
    ]
    db.session.add_all(permissions)
    db.session.commit()
    
    roles = [
        Role(name='Firm Admin', scope='firm'),
        Role(name='Team Manager', scope='team'),
        Role(name='Team Member', scope='team'),
        Role(name='Project Owner', scope='project'),
        Role(name='Project Contributor', scope='project'),
        Role(name='Project Visitor', scope='project')
    ]
    db.session.add_all(roles)
    db.session.commit()
    
    # Assign perms to Firm Admin
    all_perms = Permission.query.all()
    roles[0].permissions = all_perms
    db.session.commit()

    # Create Admin User
    admin = User(username='admin', email='admin@example.com', password_hash=generate_password_hash('password'))
    db.session.add(admin)
    
    # Create Regular User
    user = User(username='user', email='user@example.com', password_hash=generate_password_hash('password'))
    db.session.add(user)
    
    db.session.commit()
    return db

@pytest.fixture
def auth_headers(test_client, init_database):
    # Login as admin to get token
    response = test_client.post('/login', json={
        'email': 'admin@example.com',
        'password': 'password'
    })
    token = response.json['token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def user_auth_headers(test_client, init_database):
    # Login as regular user
    response = test_client.post('/login', json={
        'email': 'user@example.com',
        'password': 'password'
    })
    token = response.json['token']
    return {'Authorization': f'Bearer {token}'}
