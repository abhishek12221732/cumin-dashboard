from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import team_controller

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/teams/<int:team_id>/manager-request', methods=['POST'])
@jwt_required()
def request_manager(team_id):
    return team_controller.request_manager(team_id)

@teams_bp.route('/teams/<int:team_id>/manager-requests', methods=['GET'])
@jwt_required()
def list_manager_requests(team_id):
    return team_controller.list_manager_requests(team_id)

@teams_bp.route('/teams/<int:team_id>/manager-requests/<int:request_id>/accept', methods=['POST'])
@jwt_required()
def accept_manager_request(team_id, request_id):
    return team_controller.accept_manager_request(team_id, request_id)

@teams_bp.route('/teams/<int:team_id>/manager-requests/<int:request_id>/reject', methods=['POST'])
@jwt_required()
def reject_manager_request(team_id, request_id):
    return team_controller.reject_manager_request(team_id, request_id)

@teams_bp.route('/teams', methods=['GET'])
def get_teams():
    return team_controller.get_teams()

@teams_bp.route('/teams', methods=['POST'])
@jwt_required()
def create_team():
    return team_controller.create_team()

@teams_bp.route('/teams/<int:team_id>', methods=['GET'])
@jwt_required()
def get_team(team_id):
    return team_controller.get_team(team_id)

@teams_bp.route('/teams/<int:team_id>/projects', methods=['POST'])
@jwt_required()
def add_team_project(team_id):
    return team_controller.add_team_project(team_id)

@teams_bp.route('/teams/<int:team_id>/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def remove_team_project(team_id, project_id):
    return team_controller.remove_team_project(team_id, project_id)

@teams_bp.route('/teams/<int:team_id>/members', methods=['POST'])
@jwt_required()
def add_team_member(team_id):
    return team_controller.add_team_member(team_id)

@teams_bp.route('/teams/<int:team_id>/members/<int:user_id>', methods=['DELETE'])
@jwt_required()
def remove_team_member(team_id, user_id):
    return team_controller.remove_team_member(team_id, user_id)

@teams_bp.route('/teams/<int:team_id>/my-role', methods=['GET'])
@jwt_required()
def get_my_team_permissions(team_id):
    return team_controller.get_my_team_permissions(team_id)

@teams_bp.route('/teams/<int:team_id>/members/<int:user_id>/role', methods=['PATCH'])
@jwt_required()
def change_team_member_role(team_id, user_id):
    return team_controller.change_team_member_role(team_id, user_id)

@teams_bp.route('/teams/<int:team_id>', methods=['DELETE'])
@jwt_required()
def delete_team(team_id):
    return team_controller.delete_team(team_id)

@teams_bp.route('/teams/my-teams', methods=['GET'])
@jwt_required()
def get_my_teams():
    return team_controller.get_my_teams()

@teams_bp.route('/teams/all', methods=['GET'])
@jwt_required()
def get_all_teams():
    return team_controller.get_all_teams()

@teams_bp.route('/roles/team', methods=['GET'])
def get_team_roles():
    return team_controller.get_team_roles()