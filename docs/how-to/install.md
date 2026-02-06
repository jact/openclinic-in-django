
---
category: how-to
audience: System administrators installing OpenClinic
---

# Installation Guide

## How to Install OpenClinic

This guide covers installing OpenClinic on a fresh system.

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.10 | 3.12+ |
| Django | 5.0 | 5.2 |
| Database | SQLite | PostgreSQL 14+ |
| OS | Linux/macOS | Ubuntu 22.04 LTS |

## Step 1: Clone the Repository

```bash
git clone https://github.com/jact/openclinic-in-django.git
cd openclinic-in-django
```

## Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate   # Windows
```

## Step 3: Install Dependencies

```bash
# Install package and development dependencies
pip install -e ".[development]"

# Or using Makefile
make install-all
```

## Step 4: Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```bash
# Required
export DJANGO_SECRET_KEY='your-secure-secret-key'

# Optional - for production
export ALLOWED_HOSTS='your-domain.com'
export DATABASE_URL='postgres://user:pass@localhost/openclinic'
```

## Step 5: Run Migrations

```bash
# Development
python manage.py migrate --settings=openclinic.settings.development

# Production
python manage.py migrate --settings=openclinic.settings.production
```

## Step 6: Create Superuser

```bash
python manage.py createsuperuser
```

## Step 7: Start the Server

```bash
# Development
python manage.py runserver --settings=openclinic.settings.development

# Production (requires WSGI server)
gunicorn openclinic.wsgi:application
```

## Verification

1. Navigate to `http://localhost:8000/`
2. Log in with your superuser credentials
3. Verify patient creation works

## Next Steps

- [Configure settings](configure.md)
- [Set up development environment](development.md)
