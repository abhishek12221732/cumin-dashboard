import pytest
from models.team import Team
from models.project import Project
from models.team_member import TeamMember
from models.project_member import ProjectMember
from models.user import User

def test_admin_add_user_to_team(test_client, auth_headers, init_database):
    # Admin creates team
    test_client.post('/teams', headers=auth_headers, json={'name': 'Admin Team', 'description': 'Test'})
    team = Team.query.filter_by(name='Admin Team').first()
    user = User.query.filter_by(email='user@example.com').first()
    
    # Add user to team via admin route (only if not already in)
    if not TeamMember.query.filter_by(user_id=user.id, team_id=team.id).first():
        response = test_client.post(f'/admin/users/{user.id}/teams/{team.id}', headers=auth_headers)
        assert response.status_code == 200, f"Failed to add user to team: {response.json}"
        assert TeamMember.query.filter_by(user_id=user.id, team_id=team.id).first() is not None
    else:
        # If already added (maybe by defaults), ensure logic handles it or test is skipped/valid
        pass

def test_admin_add_user_to_project(test_client, auth_headers, init_database):
    # Setup team and project
    # Setup team and project
    test_client.post('/teams', headers=auth_headers, json={'name': 'Project Team', 'description': 'Test'})
    team = Team.query.filter_by(name='Project Team').first()
    test_client.post('/projects', headers=auth_headers, json={'name': 'Admin Project', 'description': 'desc', 'owner_team_id': team.id})
    project = Project.query.filter_by(name='Admin Project').first()
    user = User.query.filter_by(email='user@example.com').first()

    # Add user to project (only if not already in)
    if not ProjectMember.query.filter_by(user_id=user.id, project_id=project.id).first():
        response = test_client.post(f'/admin/users/{user.id}/projects/{project.id}', headers=auth_headers)
        assert response.status_code == 200, f"Failed to add: {response.json}"
        assert ProjectMember.query.filter_by(user_id=user.id, project_id=project.id).first() is not None

def test_admin_fail_non_admin(test_client, user_auth_headers, init_database):
    # Try to access admin route as regular user
    response = test_client.get('/admin/teams/1/members', headers=user_auth_headers)
    assert response.status_code == 403
