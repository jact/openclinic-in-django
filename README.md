# OpenClinic

![License](https://img.shields.io/badge/License-GPLv3-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10+-green.svg)
![Django](https://img.shields.io/badge/Django-5.2-brightgreen.svg)
![Tests](https://img.shields.io/badge/Tests-81.65%25-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

![CI/CD](https://img.shields.io/github/actions/workflow/status/jact/openclinic-in-django/openclinic-ci.yml?branch=main&label=CI/CD)

OpenClinic is an open-source medical records system built with Django. Manage patients, medical problems, history, and documents with a clean, secure interface.

## Features

- **Patient Management**: Complete demographic and administrative data
- **Medical Problems**: Track active and closed medical issues
- **Medical History**: Record personal and family antecedents
- **Document Management**: Attach medical tests and documents
- **Multi-Doctor Support**: Assign patients to healthcare staff
- **Security-First**: Built with Django security best practices

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
python manage.py migrate --settings=openclinic.settings.development

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver --settings=openclinic.settings.development
```

Visit `http://localhost:8000/` and log in with your superuser account.

## Docker Quick Start

```bash
# Clone and navigate
git clone https://github.com/jact/openclinic-in-django.git
cd openclinic-in-django

# Configure environment
cp .env.example .env

# Start with Docker Compose
docker compose up -d

# Access the application
http://localhost:8000

# Create superuser
docker exec -it openclinic-dev python manage.py createsuperuser
```

See [docs/how-to/docker.md](docs/how-to/docker.md) for detailed Docker deployment documentation.

## Documentation

Comprehensive documentation following the [Diátaxis Framework](https://diataxis.frameworks.io/):

| Documentation Type | Description | Link |
|-------------------|-------------|------|
| **Tutorials** | Learning-oriented guides | [docs/tutorials/](docs/tutorials/getting-started.md) |
| **How-To Guides** | Problem-solving steps | [docs/how-to/](docs/how-to/install.md) |
| **Reference** | Technical documentation | [docs/reference/](docs/reference/architecture.md) |
| **Explanations** | Conceptual guides | [docs/explanation/](docs/explanation/security.md) |

### Quick Links

- **Getting Started**: [docs/tutorials/getting-started.md](docs/tutorials/getting-started.md)
- **Installation**: [docs/how-to/install.md](docs/how-to/install.md)
- **Docker Deployment**: [docs/how-to/docker.md](docs/how-to/docker.md)
- **Development Setup**: [docs/how-to/development.md](docs/how-to/development.md)
- **Security Audit**: [role_audit_report.md](role_audit_report.md)

## CI/CD Pipeline

OpenClinic uses GitHub Actions for continuous integration and deployment:

```bash
# Run CI locally (mirrors GitHub Actions)
make ci

# Or run individual checks
make ci-lint      # Linting and type checking
make ci-test      # Tests with coverage
make ci-security  # Security audits
make ci-docs      # Documentation validation
make ci-docker    # Docker build verification
make ci-fast      # Fast CI (lint + test only)
```

### GitHub Actions Jobs

| Job | Purpose | Status |
|-----|---------|--------|
| **quality-gates** | Ruff, Black, isort, MyPy | ✅ |
| **security-audit** | Bandit, Safety scans | ✅ |
| **tests** | Pytest with coverage | ✅ |
| **django-checks** | System checks, migrations | ✅ |
| **docker-build** | Dev/Prod Docker images | ✅ |
| **docs-validation** | MkDocs validation | ✅ |
| **dependency-scan** | pip-audit for CVEs | ✅ |

### Badge Status

![CI/CD](https://img.shields.io/github/actions/workflow/status/jact/openclinic-in-django/openclinic-ci.yml?branch=main&label=CI/CD)

See [`.github/workflows/openclinic-ci.yml`](.github/workflows/openclinic-ci.yml) for full pipeline configuration.

## Requirements

- Python 3.10+
- Django 5.2+
- See `pyproject.toml` for full dependencies

## Testing

```bash
# Run all tests with coverage
pytest --cov=medical --cov-report=term

# Run specific test category
pytest medical/tests/models/
pytest medical/tests/views/
pytest medical/tests/forms/
```

## Project Structure

```
openclinic-in-django/
├── medical/              # Main Django application
│   ├── models/          # Patient, Problem, History, Test, Staff
│   ├── views/           # View classes (split by domain)
│   ├── forms/           # Form classes
│   └── tests/           # Comprehensive test suite
├── docs/                # Documentation (Diátaxis structure)
│   ├── tutorials/       # Learning guides
│   ├── how-to/         # Task guides (includes docker.md)
│   ├── reference/       # Technical reference
│   └── explanation/     # Conceptual guides
├── openclinic/          # Project configuration
├── templates/           # Base templates
├── Dockerfile          # Multi-stage Docker build
├── docker-compose.yml  # Development orchestration
├── docker-compose.production.yml  # Production override
├── mkdocs.yml          # MkDocs configuration
└── .dockerignore      # Docker build exclusions
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Ensure tests pass: `pytest`
5. Update documentation as needed
6. Submit a pull request

See [docs/how-to/development.md](docs/how-to/development.md) for detailed contribution guidelines.

## Security

For security vulnerabilities, please email `openclinic@gmail.com` instead of opening a public issue.

See [role_audit_report.md](role_audit_report.md) for the comprehensive security audit.

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

See [COPYING](COPYING) for full license text.

## Contributors

https://github.com/jact/openclinic-in-django/graphs/contributors
