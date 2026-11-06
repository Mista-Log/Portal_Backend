# Portal Project

## Project Overview

The Bitly University Admission and Course Registration Portal is a web-based application developed to manage postgraduate admissions, student accounts, school-fee payments, and course registration at Bitly University, Osogbo, Nigeria.

The system provides role-based access for applicants, returning students, Admission Officers, the Registrar, ICT Administrators, and PG School Staff.

## Core Functionalities

- **Admission Management:** Applicants can create accounts, submit applications, pay admission form fees, and check admission status.
- **Admission Decisions:** Admission Officers and the Registrar can review applications, grant or revoke admission, and notify applicants via email.
- **Student Account Management:** Admitted students can activate their accounts and log in.
- **School-Fee Payment:** Students can pay school fees and view their payment status.
- **Course Registration:** Students who have paid at least 70% of applicable fees can register for first-semester courses.
- **Returning Student Registration:** Old students can register for an academic session using their matriculation/application number and personal details.
- **Course Management:** ICT Officers can upload course lists using Excel or CSV files.
- **Role-Based Access Control:** Users access functionalities based on their assigned roles.

## Technology Stack

- Python
- Django
- UV (Package Manager)
- Postgresql

## Project Structure

```text
portal_backend/
├── config/
├── manage.py
├── pyproject.toml
├── uv.lock
├── .env.example
└── README.md
```

## Installation Guide

### Prerequisites

Install Python, UV, and Git

### 1. Clone the Repository

```bash
git clone <REPOSITORY_URL>
cd portal_backend
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file using `.env.example`.

Configure your Django secret key, database credentials, and email settings.

### 4. Apply Migrations

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

### 5. Start the Development Server

```bash
uv run python manage.py runserver
```

Visit:

- Portal: http://127.0.0.1:8000/

## Common Commands

| Command | Description |
|---|---|
| `uv sync` | Install dependencies |
| `uv add package_name` | Add a package |
| `uv run python manage.py runserver` | Start server |
| `uv run python manage.py migrate` | Apply migrations |
| `uv run python manage.py makemigrations` | Create migrations |
| `uv run python manage.py startapp app_name` | Create an app |
| `uv run python manage.py test` | Run tests |

## Team Collaboration

- Pull the latest changes before starting work.
- Create feature branches for development.
- Never commit `.env` or `.venv`.
- Commit `uv.lock` when dependencies change.
- Use descriptive commit messages.
- Submit Pull Requests before merging into the main branch.

## Security

- Implement role-based access control.
- Validate user inputs on the backend.
- Secure payment verification.
- Protect sensitive credentials using environment variables.
- Enforce the 70% fee-payment requirement server-side.
- Use Django authentication and CSRF protection.

## Project Objective

To develop a secure and efficient admission and course registration platform that automates admission processing, school-fee payments, and academic course registration at Bitly University.