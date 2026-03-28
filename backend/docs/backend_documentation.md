# Cumin Dashboard Backend Documentation

## 1. Architecture Overview
This backend provides the RESTful API for the Cumin Dashboard, supporting project and team management, issue tracking, notifications, and role-based access control.

**Tech Stack:**
- **Language:** Python 3
- **Framework:** Flask
- **Database ORM:** SQLAlchemy
- **Authentication:** JWT via `flask-jwt-extended`
- **Migrations:** Flask-Migrate (Alembic)
- **CORS:** `flask-cors`

## 2. Backend Structure

### Entry Point
- `app.py`
  - Creates the Flask application
  - Loads environment variables with `dotenv`
  - Configures database URI, JWT, and CORS
  - Registers route blueprints
  - Initializes `db` and migrations
  - Creates database tables automatically in app context

### Route Layer
- `routes/` contains HTTP endpoint definitions and handles request authentication.
- Each route file registers a `Blueprint` and delegates business logic to controller functions.
- Common route files:
  - `auth.py`
  - `projects.py`
  - `project_member.py`
  - `item.py`
  - `board_column.py`
  - `teams.py`
  - `user.py`
  - `notification.py`
  - `reports.py`
  - `admin.py`

### Controller Layer
- `controllers/` contains application logic and database operations.
- It isolates validation, permission checks, creation/update flows, notifications, and activity logging from the HTTP layer.
- Key controllers:
  - `auth_controller.py`
  - `project_controller.py`
  - `item_controller.py`
  - `project_member_controller.py`
  - `team_controller.py`
  - `board_column_controller.py`
  - `report_controller.py`
  - `notification_controller.py`
  - `admin_controller.py`
  - `rbac.py`

### Data Layer
- `models/` defines SQLAlchemy models for database tables.
- `models/db.py` creates the shared `SQLAlchemy` instance.

## 3. Database Schema

### User and Auth
- `User`
  - `id`, `username`, `email`, `password_hash`
  - timestamps: `created_at`, `updated_at`

### Permissions and Roles
- `Role`
  - `name` and `scope` (`firm`, `team`, `project`)
  - many-to-many relationship to `Permission`
- `Permission`
  - `action` and optional `description`

### Teams
- `Team`
  - `manager_id` references `User`
- `TeamMember`
  - composite PK (`team_id`, `user_id`)
  - stores user role in team
- `TeamManagerRequest`
  - requests to become a team manager

### Projects
- `Project`
  - `owner_id` references `User`
  - `owner_team_id` references `Team`
  - relationships to board columns, items, and members
- `ProjectMember`
  - composite PK (`project_id`, `user_id`)
  - stores user role in project
- `ProjectJoinRequest`
  - handles invitations and join requests

### Work Items
- `BoardColumn`
  - ordered Kanban columns for a project
- `Item`
  - tasks/issues with type, status, priority, and optional parent for subtasks
- `Comment`
  - comments on items
- `ActivityLog`
  - audit trail of actions on items

### Notifications
- `Notification`
  - per-user notifications with `is_read` status

## 4. Authorization (RBAC)
- `controllers/rbac.py` implements permission checks.
- Uses team/project roles and permissions to determine authorization.
- Global admin bypass is applied for a hardcoded admin user.
- Supports permissions like:
  - `edit_own_task` vs `edit_any_task`
  - `delete_own_task` vs `delete_any_task`

## 5. API Reference

### Authentication (`/auth`)
- `POST /register`: Register new user
- `POST /login`: Authenticate and return JWT
- `GET /me`: Get current user profile

### Projects (`/projects`)
- `POST /projects`: Create project (admin-only)
- `GET /projects`: List authenticated user's projects
- `GET /projects/<project_id>`: Get project details
- `GET /projects/<project_id>/progress`: Get completion metrics
- `GET /dashboard/stats`: Get dashboard summary
- `PATCH /projects/<project_id>`: Update project
- `DELETE /projects/<project_id>`: Delete project (admin-only)
- `POST /projects/<project_id>/transfer-ownership`: Transfer owner
- `POST /projects/<project_id>/owner_team`: Set owning team (admin-only)
- `GET /projects/<project_id>/my-role`: Get current user's project role and permissions
- `GET /all-projects`: Admin-only project listing

### Project Membership (`/projects/<project_id>/members`)
- `POST /projects/<project_id>/members`: Add project member
- `GET /projects/<project_id>/members`: List project members
- `POST /projects/<project_id>/join-request`: Request project access
- `GET /projects/<project_id>/join-requests`: List join requests
- `POST /projects/<project_id>/join-request/<request_id>/accept`: Accept join request
- `POST /projects/<project_id>/join-request/<request_id>/reject`: Reject join request
- `GET /my-invitations`: List invitations for current user
- `POST /projects/<project_id>/invitation/<invite_id>/accept`: Accept invitation
- `POST /projects/<project_id>/invitation/<invite_id>/reject`: Reject invitation
- `DELETE /projects/<project_id>/members/<user_id>`: Remove user from project
- `PATCH /projects/<project_id>/members/<user_id>`: Update member role

### Teams (`/teams`)
- `GET /teams`: List teams
- `POST /teams`: Create team
- `GET /teams/<team_id>`: Get team details
- `POST /teams/<team_id>/manager-request`: Request manager role
- `GET /teams/<team_id>/manager-requests`: List manager requests
- `POST /teams/<team_id>/manager-requests/<request_id>/accept`: Accept request
- `POST /teams/<team_id>/manager-requests/<request_id>/reject`: Reject request
- `POST /teams/<team_id>/projects`: Assign a project to team
- `DELETE /teams/<team_id>/projects/<project_id>`: Remove project from team
- `POST /teams/<team_id>/members`: Add team member
- `DELETE /teams/<team_id>/members/<user_id>`: Remove team member
- `GET /teams/<team_id>/my-role`: Get current user's team role and permissions
- `PATCH /teams/<team_id>/members/<user_id>/role`: Change team member role
- `DELETE /teams/<team_id>`: Delete team
- `GET /teams/my-teams`: List teams current user belongs to
- `GET /teams/all`: List all teams
- `GET /roles/team`: Get team-role definitions

### Items (`/items`)
- `POST /projects/<project_id>/items`: Create item/task
- `GET /projects/<project_id>/items`: List project items
- `GET /items/<item_id>`: Get item details
- `PATCH /items/<item_id>`: Update item
- `DELETE /items/<item_id>`: Delete item
- `GET /items/<item_id>/subtasks`: List subtasks
- `POST /items/<item_id>/subtasks`: Create subtask
- `PATCH /items/subtasks/<subtask_id>`: Update subtask
- `DELETE /items/subtasks/<subtask_id>`: Delete subtask
- `GET /items/<item_id>/activity`: Get item activity logs
- `GET /items/activity`: Get recent activity across items
- `GET /items/my-tasks`: Get tasks assigned to current user
- `POST /items/<item_id>/comments`: Add comment
- `PATCH /items/comments/<comment_id>`: Edit comment

### Notifications (`/notifications`)
- `GET /notifications`: Fetch notifications for current user
- `POST /notifications/<notif_id>/read`: Mark notification as read

### Reports (`/reports`)
- `GET /reports/project/<project_id>`: Get project report data

### Admin (`/admin`)
- `POST /admin/users/<user_id>/teams/<team_id>`: Add user to team
- `DELETE /admin/users/<user_id>/teams/<team_id>`: Remove user from team
- `POST /admin/users/<user_id>/projects/<project_id>`: Add user to project
- `DELETE /admin/users/<user_id>/projects/<project_id>`: Remove user from project
- `PATCH /admin/users/<user_id>/teams/<team_id>/role`: Change team role
- `PATCH /admin/users/<user_id>/projects/<project_id>/role`: Change project role
- `GET /admin/teams/<team_id>/members`: List team members
- `GET /admin/projects/<project_id>/members`: List project members
- `POST /admin/projects/<project_id>/visitor-team`: Add visitors from a team to a project
- `POST /admin/projects/<project_id>/remove-visitors`: Remove visitor members from project

## 6. Demo Data Utility
- `generate_demo_data.py` resets and seeds the database
- Includes seeded users, teams, roles, permissions, projects, board columns, items, and memberships
- Sample users:
  - `admin@example.com` / `adminpass`
  - `alice@example.com` / `password123`
  - `bob@example.com` / `password123`
  - `carol@example.com` / `password123`
  - `dave@example.com` / `password123`

## 7. Notes and Suggestions
- Most application logic is in `controllers/`; routes remain thin HTTP adapters.
- Some team-related flows are handled directly by `routes/teams.py` instead of a dedicated controller.
- There is an opportunity to add stronger model relationships and more explicit permissions checks.
- Expanding API docs with example request/response payloads would improve developer usability.
