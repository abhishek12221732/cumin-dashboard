import pytest
from models.project import Project
from models.team import Team

def test_create_project_success(test_client, auth_headers, init_database):
    # Create valid team first
    test_client.post('/teams', headers=auth_headers, json={'name': 'P Team', 'description': 'Test'})
    team = Team.query.filter_by(name='P Team').first()
    
    response = test_client.post('/projects', headers=auth_headers, json={
        'name': 'New Project',
        'description': 'Desc',
        'owner_team_id': team.id
    })
    assert response.status_code == 201, f"Failed: {response.json}"
    assert 'project_id' in response.json
    
def test_create_project_missing_team(test_client, auth_headers, init_database):
    response = test_client.post('/projects', headers=auth_headers, json={
        'name': 'Orphan Project',
        'description': 'Desc'
        # No team_id
    })
    assert response.status_code == 400

def test_get_projects(test_client, auth_headers, init_database):
    # Create project 
    test_client.post('/teams', headers=auth_headers, json={'name': 'Get P Team', 'description': 'Test'})
    team = Team.query.filter_by(name='Get P Team').first()
    test_client.post('/projects', headers=auth_headers, json={'name': 'My Project', 'description': 'desc', 'owner_team_id': team.id})
    
    response = test_client.get('/projects', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json['projects']) > 0

def test_update_project(test_client, auth_headers, init_database):
    # Create
    test_client.post('/teams', headers=auth_headers, json={'name': 'Upd Team', 'description': 'Test'})
    team = Team.query.filter_by(name='Upd Team').first()
    test_client.post('/projects', headers=auth_headers, json={'name': 'Old Name', 'description': 'desc', 'owner_team_id': team.id})
    project = Project.query.filter_by(name='Old Name').first()
    
    # Update
    response = test_client.patch(f'/projects/{project.id}', headers=auth_headers, json={
        'name': 'New Name'
    })
    assert response.status_code == 200
    assert Project.query.get(project.id).name == 'New Name'
