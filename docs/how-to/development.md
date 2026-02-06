
---
category: how-to
audience: Developers setting up development environment
---

# Development Guide

## Setting Up Development Environment

This guide covers setting up and working with OpenClinic development environment.

## Prerequisites

- Python 3.10+
- Git
- Visual Studio Code (recommended) or IDE of choice

## Quick Start

```bash
# Clone and setup
git clone https://github.com/jact/openclinic-in-django.git
cd openclinic-in-django

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e ".[development]"

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

## Development Tools

### Code Formatting

```bash
# Format code
ruff check --fix .
# or
make format
```

### Type Checking

```bash
# Run type checker
mypy medical/
# or
make typecheck
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=medical --cov-report=term

# Run specific test file
pytest medical/tests/models/test_models.py
```

### Linting

```bash
# Check code quality
ruff check .

# Security audit
bandit -r medical/
```

## Project Structure

```
openclinic-in-django/
├── medical/              # Main Django app
│   ├── models/           # Data models
│   ├── views/            # View classes
│   ├── forms/            # Form classes
│   ├── tests/            # Test suite
│   ├── templatetags/    # Custom template tags
│   └── urls.py           # URL routing
├── openclinic/           # Project settings
│   └── settings/         # Configuration files
├── templates/            # Base templates
├── static/              # Static files
└── docs/                # Documentation
```

## Database Management

### Create Migrations

```bash
python manage.py makemigrations
```

### Apply Migrations

```bash
python manage.py migrate
```

### Reset Database

```bash
# Warning: Deletes all data!
rm openclinic.db
python manage.py migrate
python manage.py createsuperuser
```

## Code Conventions

### Python Style

- Follow PEP 8
- Use type hints
- Add docstrings to public functions

### Commit Messages

Follow Conventional Commits:

```
<type>(<scope>): <subject>

feat(auth): add OAuth2 login support
fix(views): resolve 404 handling issue
docs(readme): update installation guide
```

### Pull Request Process

1. Create feature branch
2. Write tests for changes
3. Ensure all tests pass
4. Update documentation
5. Request review

## Debugging

### Enable Django Debug Toolbar

```python
# In development.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

### Logging

```python
# Configure logging in settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```
