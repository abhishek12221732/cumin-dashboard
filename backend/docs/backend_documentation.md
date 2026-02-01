# Cumin Dashboard Backend Documentation

## 1. Architecture Overview
This backend acts as the RESTful API for the Cumin Dashboard, facilitating project management, team collaboration, and issue tracking.

**Tech Stack:**
- **Language:** Python 3
- **Framework:** Flask
- **Database:** SQLite (dev) / PostgreSQL (prod ready via SQLAlchemy)
- **ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Tokens) via `flask-jwt-extended`
- **Migrations:** Flask-Migrate (Alembic wrapper)

## 2. Business Logic & Controllers

The core business logic is encapsulated in the `controllers/` directory, keeping `routes/` focused on request handling.

### Authentication Controller (`auth_controller.py`)
- **Registration**: Accepts `username`, `email`, `password`. Hashes password using `werkzeug.security`.
- **Login**: Verifies credentials and issues a JWT access token. Identity is the `user.id`.

### Project Controller (`project_controller.py`)
- **Creation**:
    - Creates a new `Project` linked to an `Owner Team`.
    - Automatically creates default Kanban columns: "To Do", "In Progress", "In Review", "Done".
    - **Role Management**: Automatically assigns the Team Manager as `Project Owner` and all other team members as `Project Contributor`.
- **Dashboard Stats**: Aggregates counts of Projects, Tasks (assigned/reported), and Teams for the user.
- **Progress**: Calculates completion percentage based on item status (`done` vs total).

### Item Controller (`item_controller.py`)
Handles logic for Tasks (Items), Subtasks, and Comments.
- **Activity Logging**: Most actions (create, update, delete) trigger an `ActivityLog` entry.
- **Notifications**:
    - **Assignment**: Notifies the new assignee when a task/subtask is assigned.
    - **Comments**: Notifies the Assignee (if not the commenter) and Reporter (if not the commenter) of new comments.
- **Hierarchical Deletion**: Deleting a task cascades to delete its Subtasks and Activity Logs.
- **Validation**: Enforces strict constraints on `status` (todo, inprogress/done/inreview), `priority`, and `type`.

### Project Member Controller (`project_member_controller.py`)
Manages the complex RBAC and membership flows.
- **Invitations**:
    - Users can be invited by email. Creates a `ProjectJoinRequest` (type='invite').
    - Pending invitations can be Accepted (adds user to project) or Rejected.
- **Join Requests**:
    - Users can request to join a project. Creates a `ProjectJoinRequest` (type='request').
    - Project Owners/Managers are notified of new requests.
- **Role Limits**: Prevents removing or demoting the *last* `Project Owner` to ensure project accessibility.

### Teams Controller (`teams.py` route file contains logic)
*Note: Currently, some team logic resides directly in the route handler `routes/teams.py` rather than a dedicated controller file, which is a noted architectural inconsistency.*
- **Manager Requests**: Users can request to become the Team Manager.
- **Role Assignment**: Team Admins/Managers can assign `Team Member` or `Team Manager` roles. Promoting a new manager automatically demotes the previous one.

### Board Column Controller (`board_column_controller.py`)
- **Management**: Allows creating, updating (renaming/reordering), and deleting columns for the Kanban board.
- **Ordering**: Columns have an explicit `order` integer index.

### Report Controller (`report_controller.py`)
- **Project Report**: Generates a comprehensive status report including:
    - Member list with roles.
    - Task status distribution (counts of done, todo, etc.).
    - List of detailed tasks.

### Notification Controller (`notification_controller.py`)
- **Storage**: Persists notifications to the database.
- **Retrieval**: Fetches unread notifications for a user.
- **Status**: Supports marking individual notifications as read.

## 3. Database Schema
The database is normalized and relational. Below are the key entities and relationships.

### User & Authorization
- **User**
    - `id`: Integer, PK
    - `username`: String(80), Unique
    - `email`: String(120), Unique
    - `password_hash`: String(512)
- **Role**
    - `id`: Integer, PK
    - `name`: String(50) (e.g., "Firm Admin", "Team Manager")
    - `scope`: String(20) (Values: `firm`, `team`, `project`)
    - `permissions`: Many-to-Many with `Permission`
- **Permission**
    - `action`: String(50) (e.g., `create_project`)

### Team Structure
- **Team**
    - `id`: Integer, PK
    - `manager_id`: FK -> `User.id`
    - `members`: One-to-Many -> `TeamMember`
- **TeamDetails**: `TeamMember` links User to Team with a specific Role.
- **TeamManagerRequest**: Tracks status (`pending`/`accepted`) of leadership transfer requests.

### Project Management
- **Project**
    - `id`: Integer, PK
    - `owner_team_id`: FK -> `Team.id` (Projects are owned by teams)
    - `members`: One-to-Many -> `ProjectMember`
- **ProjectMember**: Links User to Project with a specific Role.
- **ProjectJoinRequest**: Handles both *Invitations* (outbound) and *access requests* (inbound).

### Work Items (Issues/Tasks)
- **BoardColumn**: Ordered columns logic for Kanban.
- **Item**:
    - `type`: task, bug, epic, feature.
    - `status`: todo, inprogress, inreview, done.
    - `parent_id`: For Subtasks.
- **Comment**: Simple text comments on Items.
- **ActivityLog**: History of changes for audit trails.

## 4. Authorization System (RBAC)
Permissions are checked hierarchically via `controllers/rbac.py`.

1.  **Global Level (Hardcoded Admin)**: `admin@example.com` has bypass authority.
2.  **Firm Level**: Checks `TeamMember` roles with `scope='firm'`.
3.  **Team Level**: Checks `TeamMember` roles for the specific team.
4.  **Project Level**: Checks `ProjectMember` roles.
    - Support for "Own" vs "Any" permissions (e.g., `edit_own_task` vs `edit_any_task`).

## 5. API Reference Summary

### Authentication (`/auth`)
- `POST /register`: Sign up
- `POST /login`: Get JWT
- `GET /me`: Profile

### Projects (`/projects`)
- `POST /`: Create project (requires Team ID).
- `GET /`: List my projects.
- `GET /{id}`: Details + Settings.
- `POST /{id}/transfer-ownership`: Change owner.

### Project Members (`/projects/{id}/members`)
- `POST /`: Invite user (by email).
- `POST /index`: Join request.
- `PATCH /{uid}`: Change role.

### Teams (`/teams`)
- `POST /{id}/manager-request`: Claim leadership.
- `POST /{id}/members`: Add member.

### Work Items (`/items`, `/projects/{pid}/items`)
- `POST /projects/{pid}/items`: Create Task.
- `POST /{id}/subtasks`: Create Subtask.
- `PATCH /{id}`: Update status/assignee.
- `POST /{id}/comments`: Add comment.

## 6. Configuration & Environment (`app.py`)
The application is configured via environment variables managed by `python-dotenv`.

- **CORS**: Configured via `flask-cors`. Allowed origins are set by `CORS_ORIGINS` env var (default `*`).
- **JWT**:
    - Location: Headers only.
    - Header Name: `Authorization` (configurable via `JWT_HEADER_NAME`).
    - Header Type: `Bearer` (configurable via `JWT_HEADER_TYPE`).
- **Database**:
    - `SQLALCHEMY_DATABASE_URI`: Connection string.
    - `SQLALCHEMY_TRACK_MODIFICATIONS`: Disabled for performance.

## 7. Development Utilities
### Demo Data Seeding (`generate_demo_data.py`)
A utility script to populate the database with initial data for testing.
- **Command**: `python generate_demo_data.py` (Resets DB and seeds)
- **Seeded Data**:
    - **Permissions**: Complete list of 23 permissions (e.g., `create_task`, `view_reports`).
    - **Roles**:
        - `Firm Admin`: All permissions.
        - `Team Manager`: Team management permissions.
        - `Team Member`: View only.
        - `Project Owner`: Full project control.
        - `Project Contributor`: Edit own tasks, view project.
        - `Project Visitor`: Read-only access.
    - **Users**:
        - `admin@example.com` (Firm Admin)
        - `alice@example.com` (Manager Team Alpha)
        - `bob@example.com` (Member Team Alpha)
        - `carol@example.com` (Manager Team Beta)
    - **Teams**: Alpha, Beta.
    - **Projects**: Project X (Alpha), Project Y (Beta).

