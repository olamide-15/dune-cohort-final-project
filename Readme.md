# SMARTSTUDY 

url: https://smartstudy-b6go.onrender.com
# SmartStudy 📚

A Django REST Framework backend for student tracking and grade management. SmartStudy enables educators and administrators to manage students, courses, grades, and academic performance through a clean, secure API.

---

## Features

- **Student Management** — Register, list, filter, search, and paginate student records
- **Grade Tracking** — Record and retrieve grades per student, course, and class
- **JWT Authentication** — Secure token-based auth via `djangorestframework-simplejwt`
- **Role-based Access** — Distinguish between student, teacher, and admin roles via a custom user model
- **Filtering & Search** — Filter students by course or class; search by name or username
- **Pagination** — Standardised paginated responses across all list endpoints
- **Admin Audit Logging** — Django admin log tracks all data changes

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Framework | Django 4.x + Django REST Framework |
| Auth | SimpleJWT |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Filtering | django-filter |

---

## Setup & Installation

### Prerequisites

- Python 3.11+
- `pip`
- `virtualenv` (recommended)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/smartstudy.git
cd smartstudy
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

Load it in `settings.py`:

```python
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-dev-key')
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## API Documentation

### Authentication

All protected endpoints require a JWT Bearer token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

#### Obtain tokens

```http
POST /api/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```

#### Refresh token

```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "<refresh_token>"
}
```

---

### Students

#### List students

```http
GET /api/students/
Authorization: Bearer <token>
```

**Query parameters:**

| Parameter | Type | Description |
|---|---|---|
| `course` | string | Filter by course |
| `student_class` | string | Filter by class |
| `search` | string | Search by name or username |
| `ordering` | string | Order by field (e.g. `created_at`) |
| `page` | integer | Page number for pagination |

**Response:**
```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/students/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "jdoe",
      "name": "John Doe",
      "course": "Mathematics",
      "student_class": "Year 10",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Retrieve a student

```http
GET /api/students/{id}/
Authorization: Bearer <token>
```

#### Create a student

```http
POST /api/students/
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "jdoe",
  "name": "John Doe",
  "course": "Mathematics",
  "student_class": "Year 10"
}
```

#### Update a student

```http
PUT /api/students/{id}/
PATCH /api/students/{id}/
Authorization: Bearer <token>
```

#### Delete a student

```http
DELETE /api/students/{id}/
Authorization: Bearer <token>
```

---

### Grades

#### List grades

```http
GET /api/grades/
Authorization: Bearer <token>
```

#### Record a grade

```http
POST /api/grades/
Authorization: Bearer <token>
Content-Type: application/json

{
  "student": 1,
  "course": "Mathematics",
  "score": 87.5,
  "grade": "A"
}
```

---

## Database Management

### Export data

```powershell
# Recommended — avoids encoding issues on Windows
python manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude admin.logentry -o data.json
```

### Import data

```bash
python manage.py loaddata data.json
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes and write tests where applicable
4. Ensure all tests pass: `python manage.py test`
5. Commit your changes: `git commit -m "feat: add your feature"`
6. Push to your branch: `git push origin feature/your-feature-name`
7. Open a Pull Request against `main`

### Code style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use descriptive variable and function names
- Add docstrings to all views and serializers
- Keep commits atomic and well-described

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.