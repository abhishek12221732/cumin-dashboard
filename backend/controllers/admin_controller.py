from flask import request, jsonify
from models.user import User
from models.team import Team
from models.team_member import TeamMember
from models.project import Project
from models.project_member import ProjectMember
from models.role import Role
from models.db import db
from models.project_member import add_team_as_project_visitors, remove_all_project_visitors
from controllers.rbac import is_admin
from flask_jwt_extended import get_jwt_identity

def check_admin():
    user_id = get_jwt_identity()
    if not is_admin(user_id):
        return False
    return True

def add_user_to_team(user_id, team_id):
    if not check_admin():
        return jsonify({'error': 'Forbidden: Admins only'}), 403
    if not User.query.get(user_id) or not Team.query.get(team_id):
        return jsonify({'error': 'User or Team not found'}), 404
    if TeamMember.query.filter_by(user_id=user_id, team_id=team_id).first():
        return jsonify({'error': 'User already in team'}), 409
    # Assign default team role if not provided
    team_role = Role.query.filter_by(name='Team Member', scope='team').first()
    if not team_role:
        return jsonify({'error': 'Default team role not found'}), 400
    tm = TeamMember(user_id=user_id, team_id=team_id, role_id=team_role.id)
    db.session.add(tm)
    db.session.commit()
    return jsonify({'message': 'User added to team'}), 200

def remove_user_from_team(user_id, team_id):
    if not check_admin():
        return jsonify({'error': 'Forbidden: Admins only'}), 403
    tm = TeamMember.query.filter_by(user_id=user_id, team_id=team_id).first()
    if not tm:
        return jsonify({'error': 'Membership not found'}), 404
    db.session.delete(tm)
    db.session.commit()
    return jsonify({'message': 'User removed from team'}), 200

def add_user_to_project(user_id, project_id):
    if not check_admin():
        return jsonify({'error': 'Forbidden: Admins only'}), 403
    if not User.query.get(user_id) or not Project.query.get(project_id):
        return jsonify({'error': 'User or Project not found'}), 404
    if ProjectMember.query.filter_by(user_id=user_id, project_id=project_id).first():
        return jsonify({'error': 'User already in project'}), 409
    # Assign default project role if not provided
    project_role = Role.query.filter_by(name='Project Contributor', scope='project').first()
    if not project_role:
        return jsonify({'error': 'Default project role not found'}), 400
    pm = ProjectMember(user_id=user_id, project_id=project_id, role_id=project_role.id)
    db.session.add(pm)
    db.session.commit()
    return jsonify({'message': 'User added to project'}), 200

def remove_user_from_project(user_id, project_id):
    if not check_admin():
        return jsonify({'error': 'Forbidden: Admins only'}), 403
    pm = ProjectMember.query.filter_by(user_id=user_id, project_id=project_id).first()
    if not pm:
        return jsonify({'error': 'Membership not found'}), 404
    db.session.delete(pm)
    db.session.commit()
    return jsonify({'message': 'User removed from project'}), 200

def change_user_team_role(user_id, team_id):
    if not check_admin():
        return jsonify({'error': 'Forbidden: Admins only'}), 403
    data = request.get_json()
    role_id = data.get('role_id')
    tm = TeamMember.query.filter_by(user_id=user_id, team_id=team_id).first()
    role = Role.query.get(role_id)
    if not tm or not role or role.scope != 'team':
        return jsonify({'error': 'Invalid membership or role'}), 400
    tm.role_id = role_id
    db.session.commit()
    return jsonify({'message': 'Team role updated'}), 200

def change_user_project_role(user_id, project_id):
    if not check_admin():
        return jsonify({'error': 'Forbidden: Admins only'}), 403
    data = request.get_json()
    role_id = data.get('role_id')
    pm = ProjectMember.query.filter_by(user_id=user_id, project_id=project_id).first()
    role = Role.query.get(role_id)
    if not pm or not role or role.scope != 'project':
        return jsonify({'error': 'Invalid membership or role'}), 400
    pm.role_id = role_id
    db.session.commit()
    return jsonify({'message': 'Project role updated'}), 200

def list_team_members(team_id):
    if not check_admin():
        return jsonify({'error': 'Forbidden: Admins only'}), 403
    members = TeamMember.query.filter_by(team_id=team_id).all()
    result = []
    for m in members:
        user = User.query.get(m.user_id)
        role = Role.query.get(m.role_id) if m.role_id else None
        result.append({
            'user_id': m.user_id,
            'username': user.username if user else None,
            'email': user.email if user else None,
            'role': role.name if role else None
        })
    return jsonify({'members': result}), 200

def list_project_members(project_id):
    if not check_admin():
        return jsonify({'error': 'Forbidden: Admins only'}), 403
    members = ProjectMember.query.filter_by(project_id=project_id).all()
    result = []
    for m in members:
        user = User.query.get(m.user_id)
        role = Role.query.get(m.role_id) if m.role_id else None
        result.append({
            'user_id': m.user_id,
            'username': user.username if user else None,
            'email': user.email if user else None,
            'role': role.name if role else None
        })
    return jsonify({'members': result}), 200

def add_visitor_team(project_id):
    if not check_admin():
        return jsonify({'error': 'Forbidden: Admins only'}), 403
    data = request.get_json()
    team_id = data.get('team_id')
    if not team_id:
        return jsonify({'error': 'team_id required'}), 400
    team = Team.query.get(team_id)
    project = Project.query.get(project_id)
    if not team or not project:
        return jsonify({'error': 'Team or Project not found'}), 404
    try:
        added = add_team_as_project_visitors(project_id, team_id)
        return jsonify({'message': f'Team added as visitors', 'members_added': added}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def remove_visitors_from_project(project_id):
    if not check_admin():
        return jsonify({'error': 'Forbidden: Admins only'}), 403
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    try:
        removed = remove_all_project_visitors(project_id)
        return jsonify({'message': f'All visitors removed', 'visitors_removed': removed}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
