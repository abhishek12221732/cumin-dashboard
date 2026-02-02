from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import admin_controller

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users/<int:user_id>/teams/<int:team_id>', methods=['POST'])
@jwt_required()
def add_user_to_team(user_id, team_id):
    return admin_controller.add_user_to_team(user_id, team_id)

@admin_bp.route('/admin/users/<int:user_id>/teams/<int:team_id>', methods=['DELETE'])
@jwt_required()
def remove_user_from_team(user_id, team_id):
    return admin_controller.remove_user_from_team(user_id, team_id)

@admin_bp.route('/admin/users/<int:user_id>/projects/<int:project_id>', methods=['POST'])
@jwt_required()
def add_user_to_project(user_id, project_id):
    return admin_controller.add_user_to_project(user_id, project_id)

@admin_bp.route('/admin/users/<int:user_id>/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def remove_user_from_project(user_id, project_id):
    return admin_controller.remove_user_from_project(user_id, project_id)

@admin_bp.route('/admin/users/<int:user_id>/teams/<int:team_id>/role', methods=['PATCH'])
@jwt_required()
def change_user_team_role(user_id, team_id):
    return admin_controller.change_user_team_role(user_id, team_id)

@admin_bp.route('/admin/users/<int:user_id>/projects/<int:project_id>/role', methods=['PATCH'])
@jwt_required()
def change_user_project_role(user_id, project_id):
    return admin_controller.change_user_project_role(user_id, project_id)

@admin_bp.route('/admin/teams/<int:team_id>/members', methods=['GET'])
@jwt_required()
def list_team_members(team_id):
    return admin_controller.list_team_members(team_id)

@admin_bp.route('/admin/projects/<int:project_id>/members', methods=['GET'])
@jwt_required()
def list_project_members(project_id):
    return admin_controller.list_project_members(project_id)

@admin_bp.route('/admin/projects/<int:project_id>/visitor-team', methods=['POST'])
@jwt_required()
def add_visitor_team(project_id):
    return admin_controller.add_visitor_team(project_id)

@admin_bp.route('/admin/projects/<int:project_id>/remove-visitors', methods=['POST'])
@jwt_required()
def remove_visitors_from_project(project_id):
    return admin_controller.remove_visitors_from_project(project_id)
 