# Django REST API Project

## Overview

This project is a Django REST API for managing projects, issues, and comments. It supports user authentication and authorization, allowing users to create and manage projects, assign contributors, report issues, and add comments.

## Features

- **User Management:** Create, authenticate, and manage users.
- **Project Management:** Create, update, delete, and list projects.
- **Issue Tracking:** Create, update, delete, and list issues within projects.
- **Commenting System:** Add comments to issues.
- **Authentication:** JSON Web Token (JWT) based authentication for secure access.
- **Permissions:** Role-based access control for users and contributors.

## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Euvad/softdesk.git
   cd softdesk_api
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   Ensure you have a database configured in `settings.py`. For development, you can use SQLite.

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://localhost:8000/`.

## API Endpoints

Here are some of the main API endpoints:

### Authentication:

- `POST /api/token/`: Obtain JWT token.

### Users:

- `GET /api/users/`: List users.
- `POST /api/users/`: Create a new user.

### Projects:

- `GET /api/projects/`: List all projects.
- `POST /api/projects/`: Create a new project.
- `PUT /api/projects/<id>/`: Update a project.
- `DELETE /api/projects/<id>/`: Delete a project.

### Issues:

- `GET /api/issues/`: List all issues.
- `POST /api/issues/`: Create a new issue.
- `PUT /api/issues/<id>/`: Update an issue.
- `DELETE /api/issues/<id>/`: Delete an issue.

### Comments:

- `GET /api/comments/`: List all comments.
- `POST /api/comments/`: Create a new comment.
- `PUT /api/comments/<id>/`: Update a comment.
- `DELETE /api/comments/<id>/`: Delete a comment.

## Testing

### Unit and Integration Tests

To run tests, use the following command:

```bash
python3 tester.py
```
