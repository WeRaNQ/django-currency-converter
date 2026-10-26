Вот README в такой же стилистике — лаконично, по делу, без лишнего.

# Django Currency Exchange

A currency conversion web application built with Django, PostgreSQL, and Docker.

## Features

- User registration, login, and logout
- Custom user model (`AbstractBaseUser`) with roles: guest / staff / admin
- Currency conversion (EUR, RUB, USD, BYN) via [apilayer.com](https://apilayer.com) API
- Stores each user's last conversion request and displays it on their profile
- Fully containerized: Docker + docker-compose (Django + Postgres)
- CI/CD pipeline with GitHub Actions (tests + automated deploy)

## Tech Stack

- **Backend:** Python 3.13, Django 5.2
- **Database:** PostgreSQL 17
- **Infrastructure:** Docker, docker-compose, GitHub Actions (self-hosted runner)
- **External API:** apilayer.com (Currency Data API)
- **Testing:** 6 automated tests (pages, forms, registration → login flow)

## Project Structure

```
django-currency-converter/
├── .github/workflows/ci.yml    # CI/CD pipeline
├── mysite/
│   ├── manage.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   ├── .env.example
│   ├── mysite/                 # Django settings
│   └── sitex/                  # app: models, forms, views, templates, static, tests
└── README.md
```

## Quick Start

### Local

```bash
git clone https://github.com/WeRaNQ/django-currency-converter.git
cd django-currency-converter/mysite
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # fill in SECRET_KEY, DATABASE_*, API_KEY
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Docker

```bash
docker compose up --build
```

Site available at http://127.0.0.1:8000/

Create superuser inside the container:

```bash
docker compose exec django python manage.py createsuperuser
```

## Environment Variables

| Variable | Description |
| :--- | :--- |
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` / `False` |
| `DATABASE_NAME` | PostgreSQL database name |
| `DATABASE_USER` | PostgreSQL user |
| `DATABASE_PASSWORD` | PostgreSQL password |
| `DATABASE_HOST` | `localhost` (local) / `pgdb` (Docker) |
| `DATABASE_PORT` | `5432` |
| `API_KEY` | apilayer.com API key |

## Tests

```bash
python manage.py test
```

6 tests: pages (`/register/`, `/login/`), forms validation, registration → login flow.

## CI/CD

- **CI:** GitHub Actions runs tests on `ubuntu-latest` with a PostgreSQL 17 service container.
- **CD:** Deploys via `self-hosted` runner (`docker compose down && up --build`), triggered on push to `main`.

## Security

- Secrets stored in `.env` (not committed)
- `DEBUG=False` by default
- `has_perm` restricted to `admin`
- Open-redirect protection via `url_has_allowed_host_and_scheme`
- PostgreSQL bound to `127.0.0.1`
