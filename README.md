# COAST TAF (Technical Assistance Facility) Records Database

## Overview

The COAST TAF Records Database is a full-stack web application designed to manage Technical Assistance Facility (TAF) records. It provides distinct functionalities for regular users (viewing, searching, downloading) and administrators (full CRUD operations on records, user management, backups, etc.).

This application is built with Python/Django for the backend and a dynamic HTML/CSS/JavaScript frontend (manipulated by JavaScript, resembling a Single Page Application). It uses PostgreSQL as its database and is designed to be deployed as a set of Docker containers.

## Key Features

*   **User Roles:** Administrator and Regular User roles with different permissions.
*   **TAF Record Management:** Admins can create, read, update, and delete TAF records, including detailed information and categorized file attachments. Regular users can view, search, and download records and attachments.
*   **Expert & Consortium Information:** Backend models to store information about experts and their associated consortium members (though full frontend CRUD for these is not yet implemented beyond basic listing for Experts).
*   **Document Templates:** Admins can upload and manage document templates (e.g., for TORs, Concept Notes), which can be downloaded by users.
*   **File Handling:** Secure upload and download of attachments related to TAF records and templates.
*   **Dynamic Dashboard:** Overview statistics and charts (TAs by Country, TAs by Theme) generated from TAF record data.
*   **Filtering & Search:** Comprehensive filtering and search capabilities for TAF records.
*   **Backup System:** Admins can trigger database and application (code + media files) backups via API.
*   **Containerized Deployment:** Dockerized setup for easy deployment and scalability.

## Technology Stack

*   **Backend:** Python 3.11, Django 4.2, Django REST Framework
*   **Database:** PostgreSQL 15
*   **WSGI Server:** Gunicorn
*   **Reverse Proxy & Static Files:** Nginx (in Docker setup)
*   **Frontend:** HTML, Tailwind CSS, Font Awesome, Vanilla JavaScript (dynamically manipulating a single `index.html`)
*   **Containerization:** Docker, Docker Compose

## Prerequisites

*   Docker Engine and Docker Compose (for containerized deployment)
*   Python 3.11 (if running locally without Docker for development)
*   PostgreSQL Client (psql, pg_dump) - `pg_dump` is required on the server/container running the Django app for database backups.
*   Access to a PostgreSQL server (if not using the Dockerized one for local development)

## Local Development Setup (Without Docker)

1.  **Clone the repository:**
    \`\`\`bash
    git clone <repository_url>
    cd <repository_name>
    \`\`\`

2.  **Create and activate a virtual environment:**
    \`\`\`bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    \`\`\`

3.  **Install dependencies:**
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`

4.  **Set up PostgreSQL Database:**
    *   Ensure PostgreSQL is installed and running.
    *   Create a database (e.g., `taf_db_local`).
    *   Create a database user (e.g., `taf_user_local`) with a password.
    *   Grant the user privileges on the database.

5.  **Configure Environment Variables:**
    *   Create a `.env` file in the project root (where `manage.py` is).
    *   Copy content from `.env_example` and fill in your local settings:
        \`\`\`env
        DEBUG=1
        SECRET_KEY=your_local_secret_key_make_it_strong
        ALLOWED_HOSTS=localhost 127.0.0.1

        DB_HOST=localhost # Or your DB server address
        DB_NAME=taf_db_local
        DB_USER=taf_user_local
        DB_PASSWORD=your_local_db_password
        DB_PORT=5432
        \`\`\`
    *   **Important:** Ensure `taf_project/settings.py` is configured to read these environment variables (especially `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and `DATABASES`).

6.  **Run database migrations:**
    \`\`\`bash
    python manage.py migrate
    \`\`\`

7.  **Create a superuser (admin account):**
    \`\`\`bash
    python manage.py createsuperuser
    \`\`\`
    Follow the prompts. After creation, you might need to manually set this user's `UserProfile.user_type` to 'admin' via the Django admin interface or a shell command if the registration API was not used.
    Alternatively, use the script from the Docker setup to set an existing user to admin:
    \`\`\`bash
    echo "from django.contrib.auth.models import User; from users.models import UserProfile; admin_user = User.objects.get(username='your_superuser_name'); admin_user.profile.user_type = 'admin'; admin_user.profile.save(); print('Profile updated')" | python manage.py shell
    \`\`\`


8.  **Run the development server:**
    \`\`\`bash
    python manage.py runserver
    \`\`\`
    The application will be accessible at `http://127.0.0.1:8000/`. The main interface is `index.html`.

## Docker Deployment

1.  **Clone the repository (if not already done).**
2.  **Create `.env` file:**
    *   Copy `.env_example` to `.env` in the project root.
    *   Modify the variables as needed for your deployment environment. **Especially `SECRET_KEY` and `ALLOWED_HOSTS`**.
    *   For `ALLOWED_HOSTS`, include any domain names or IP addresses that will be used to access the application. Example: `ALLOWED_HOSTS=yourdomain.com www.yourdomain.com localhost 127.0.0.1`
3.  **Build and run the containers:**
    \`\`\`bash
    docker-compose up --build -d
    \`\`\`
    The `-d` flag runs containers in detached mode.
4.  **Accessing the application:**
    *   The application should be accessible via Nginx on port 80: `http://localhost` or `http://your_server_ip_or_domain`.
5.  **Initial Superuser (if not created via entrypoint):**
    *   If the superuser creation in `entrypoint.sh` was disabled or failed, you can create one by running:
        \`\`\`bash
        docker-compose exec web python manage.py createsuperuser
        \`\`\`
    *   Then, set the user profile type to 'admin' (see step 7 in local development).
6.  **Viewing logs:**
    \`\`\`bash
    docker-compose logs -f web
    docker-compose logs -f nginx
    docker-compose logs -f db
    \`\`\`
7.  **Stopping the application:**
    \`\`\`bash
    docker-compose down
    \`\`\`
    To remove volumes (WARNING: this deletes database data, media files, backups if stored in named volumes):
    \`\`\`bash
    docker-compose down -v
    \`\`\`

## Static and Media Files (Docker)

*   **Static files** are collected by `entrypoint.sh` into the `static_volume` and served by Nginx.
*   **Media files** (user uploads) are stored in `media_volume` and served by Nginx.
*   Ensure these volumes are properly managed and backed up if necessary in a production environment.

## Backup System

The application includes management commands and API endpoints for backups.

*   **Prerequisite:** `pg_dump` (PostgreSQL client utility) must be available in the environment where `manage.py backup_database` is run (it's included in the `web` Docker image).

*   **Management Commands (run inside the 'web' container):**
    *   `docker-compose exec web python manage.py backup_database`
    *   `docker-compose exec web python manage.py backup_application`
    Backup files are stored in the `backups_volume` (mounted to `backups/` in the project root on the host if you mounted `./app:/app` and `backups_volume:/app/backups`).

*   **API Endpoints (Admin access required):**
    *   `POST /api/backups/trigger/database/`: Initiates a database backup.
    *   `POST /api/backups/trigger/application/`: Initiates an application backup.
    *   `GET /api/backups/list/`: Lists available backup files.
    *   `GET /api/backups/download/<type>/<filename>/`: Downloads a specific backup file (type is 'database' or 'application').

## Key API Endpoints (Brief)

*   `/api/auth/login/`, `/api/auth/logout/`, `/api/auth/register/`, `/api/auth/me/`
*   `/api/taf-records/` (CRUD for TAF Records)
*   `/api/attachments/` (File uploads/management for TAF Records)
*   `/api/templates/` (CRUD for Document Templates)
*   `/api/experts/` (CRUD for Experts - admin; List/Retrieve for users)
*   `/api/consortium-members/` (CRUD for Consortium Members - admin)
*   Backup endpoints listed above.

## Frontend (`index.html`)

The frontend is a single `index.html` file that uses JavaScript to dynamically render views and interact with the backend API. It simulates a Single Page Application (SPA) experience. All core user interactions are managed through this file.

---

*Further development could include a dedicated admin interface beyond the Django admin, more detailed user guides, and frontend UI for backup management.*
