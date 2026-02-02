import pytest
from models.project import Project
from models.team import Team
from models.board_column import BoardColumn

def test_get_columns(test_client, auth_headers, init_database):
    # Setup
    test_client.post('/teams', headers=auth_headers, json={'name': 'Col Team', 'description': 'desc'})
    team = Team.query.filter_by(name='Col Team').first()
    test_client.post('/projects', headers=auth_headers, json={'name': 'Col Project', 'description': 'desc', 'owner_team_id': team.id})
    project = Project.query.filter_by(name='Col Project').first()
    
    # Should be empty initially or default columns if logic added? Assuming empty for new project if no defaults logic
    response = test_client.get(f'/projects/{project.id}/columns', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json['columns'], list)

def test_create_column(test_client, auth_headers, init_database):
    # Setup
    test_client.post('/teams', headers=auth_headers, json={'name': 'New Col Team', 'description': 'desc'})
    team = Team.query.filter_by(name='New Col Team').first()
    test_client.post('/projects', headers=auth_headers, json={'name': 'New Col P', 'description': 'desc', 'owner_team_id': team.id})
    project = Project.query.filter_by(name='New Col P').first()
    
    response = test_client.post(f'/projects/{project.id}/columns', headers=auth_headers, json={
        'name': 'To Do',
        'order': 1
    })
    assert response.status_code == 201
    assert BoardColumn.query.filter_by(name='To Do', project_id=project.id).first() is not None
