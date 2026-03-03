# AGENTS.md

## Setup Commands

```bash
# Install dependencies
pip install -e ".[development,testing,linting,security]"

# Or use make
make install-all

# Run migrations
python manage.py migrate --settings=openclinic.settings.development

# Create superuser
python manage.py createsuperuser --settings=openclinic.settings.development

# Start development server
python manage.py runserver --settings=openclinic.settings.development
# Or: make dev
```

## Project Overview

OpenClinic is an open-source medical records system built with Django 5.2+. It manages patients, medical problems, history, and documents with a clean, secure interface.

### Tech Stack
- Python 3.10+
- Django 5.2
SQL (production- Postgre)
- SQLite (development)
- pytest for testing

### Key Directories
- `medical/` - Main Django application (models, views, forms, tests)
- `openclinic/` - Project configuration
- `templates/` - Base templates
- `docs/` - Documentation (Diátaxis structure)

## Code Style

- **Formatter**: Black with line-length 88
- **Linter**: Ruff (pycodestyle, isort, pydocstyle)
- **Type Checker**: MyPy
- **Quotes**: Single quotes for code, double quotes for docstrings
- **Indentation**: 4 spaces
- **Target Python**: 3.10+

Run formatting:
```bash
make format
# Or individually:
ruff format medical/ openclinic/
isort medical/ openclinic/
```

Run linting:
```bash
make lint
# Or: ruff check medical/ openclinic/
```

## Testing Instructions

```bash
# Run all tests with coverage
pytest --cov=medical --cov=openclinic --cov-report=term

# Run with make
make test

# Run unit tests only
make test-unit

# Run integration tests only
make test-integration

# Run with coverage report
make test-coverage
```

Test markers available:
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow running tests

## CI/CD Commands

```bash
# Run full CI locally (mirrors GitHub Actions)
make ci

# Or run individual checks
make ci-lint      # Linting and type checking
make ci-test      # Tests with coverage
make ci-security  # Security audits (bandit, pip-audit)
make ci-docs      # Documentation validation
make ci-docker    # Docker build verification
make ci-fast      # Fast CI (lint + test only)
```

## Security Considerations

- This is a medical records system - handle with care
- Never commit secrets or credentials
- Use environment variables for sensitive data
- Run security checks before merging:
  ```bash
  make security-check
  ```

## Database

```bash
# Create migrations
python manage.py makemigrations --settings=openclinic.settings.development

# Run migrations
python manage.py migrate --settings=openclinic.settings.development

# Check migrations status
python manage.py showmigrations
```

## Docker

```bash
# Start with Docker Compose
docker compose up -d

# Build development image
docker build --target development -t openclinic:dev .

# Build production image
docker build --target production -t openclinic:prod .
```

## Useful Commands

```bash
# Django shell
make shell

# Create superuser
make createsuperuser

# Collect static files
make collectstatic

# Clean temporary files
make clean
```

## PR Instructions

1. Run `make ci-fast` before committing
2. Ensure all tests pass
3. Run `make format` to format code
4. Update documentation if needed
5. Title format: `[<type>] <description>` (e.g., `[feature] Add patient export`)
