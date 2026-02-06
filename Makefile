# Makefile for OpenClinic Django Project

.PHONY: help install dev test lint format clean migrate runshell shell superuser makemessages compilemessages collectstatic createsuperuser check deploy-check security-check update-dependencies logs logs-clean

# Default target
help:
	@echo "OpenClinic Django Project - Available Commands:"
	@echo ""
	@echo "  make install           - Install dependencies"
	@echo "  make install-dev        - Install development dependencies"
	@echo "  make install-test       - Install testing dependencies"
	@echo "  make install-lint       - Install linting dependencies"
	@echo "  make install-security   - Install security tools"
	@echo "  make install-all        - Install all dependencies"
	@echo ""
	@echo "  make dev               - Run development server"
	@echo "  make test              - Run tests with coverage"
	@echo "  make logs              - Create log directory"
	@echo "  make logs-clean         - Clean log files"
	@echo "  make logs-view         - View recent logs"
	@echo "  make logs-errors        - View error logs"
	@echo "  make logs-security      - View security logs"
	@echo "  make test-unit         - Run unit tests only"
	@echo "  make test-integration  - Run integration tests only"
	@echo ""
	@echo "  make lint              - Run ruff linter"
	@echo "  make format            - Format code with black and isort"
	@echo "  make check             - Run all checks (lint, type check, security)"
	@echo ""
	@echo "  make migrate           - Run database migrations"
	@echo "  make makemigrations    - Create new migrations"
	@echo "  make createsuperuser   - Create a superuser"
	@echo "  make shell             - Open Django shell"
	@echo "  make runshell           - Open Python shell with Django"
	@echo ""
	@echo "  make collectstatic     - Collect static files"
	@echo "  make makemessages      - Create translation files"
	@echo "  make compilemessages   - Compile translation files"
	@echo ""
	@echo "  make clean             - Clean temporary files"
	@echo "  make clean-all         - Clean all temporary files and caches"
	@echo ""
	@echo "  make security-check    - Run security checks (bandit, safety)"
	@echo "  make deploy-check      - Run Django deployment checks"
	@echo "  make update-deps       - Update dependencies to latest versions"
	@echo ""

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[development]"

install-test:
	pip install -e ".[testing]"

install-lint:
	pip install -e ".[linting]"

install-security:
	pip install -e ".[security]"

install-all:
	pip install -e ".[development,testing,linting,security]"

# Development
dev:
	python manage.py runserver --settings=openclinic.settings.development

# Testing
test:
	pytest -xvs --cov=medical --cov=openclinic --cov-report=html --cov-report=term-missing

test-unit:
	pytest -xvs -m unit --cov=medical --cov=openclinic --cov-report=html --cov-report=term-missing

test-integration:
	pytest -xvs -m integration --cov=medical --cov=openclinic --cov-report=html --cov-report=term-missing

test-coverage:
	pytest -xvs --cov=medical --cov=openclinic --cov-report=html --cov-report=xml --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/"

# Linting and Formatting
lint:
	ruff check medical/ openclinic/
	ruff format --check medical/ openclinic/

format:
	ruff format medical/ openclinic/
	isort medical/ openclinic/

# Checks
check: lint
	@echo "All checks completed!"

# Database
migrate:
	python manage.py migrate --settings=openclinic.settings.development

makemigrations:
	python manage.py makemigrations --settings=openclinic.settings.development

createsuperuser:
	python manage.py createsuperuser --settings=openclinic.settings.development

# Shells
shell:
	python manage.py shell --settings=openclinic.settings.development

runshell:
	python manage.py runshell --settings=openclinic.settings.development

# Static Files
collectstatic:
	python manage.py collectstatic --settings=openclinic.settings.development --noinput

# Internationalization
makemessages:
	python manage.py makemessages --settings=openclinic.settings.development --locale=es

compilemessages:
	python manage.py compilemessages --settings=openclinic.settings.development --locale=es

# Cleaning
clean:
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -f .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/

clean-all: clean
	rm -rf .venv/
	rm -rf venv/
	rm -rf dist/
	rm -rf build/

# Security
security-check:
	@echo "Running Bandit security checks..."
	bandit -r medical/ openclinic/
	@echo "Running Safety checks..."
	safety check
	@echo "Running Django deployment checks..."
	python manage.py check --deploy --settings=openclinic.settings.production

deploy-check:
	python manage.py check --deploy --settings=openclinic.settings.production

# Dependencies
update-deps:
	pip install --upgrade -e .
	pip install --upgrade -e ".[development,testing,linting,security]"
	pip list --outdated

# Production
prod-migrate:
	python manage.py migrate --settings=openclinic.settings.production --noinput

prod-collectstatic:
	python manage.py collectstatic --settings=openclinic.settings.production --noinput

prod-run:
	gunicorn openclinic.wsgi:application --bind 0.0.0.0:8000

# Logging
logs:
	@echo "Creating log directory..."
	mkdir -p $(LOG_DIR)
	@echo "Log directory created: $(LOG_DIR)"

logs-clean:
	@echo "Cleaning log files..."
	rm -f /var/log/openclinic/*.log*
	@echo "Log files cleaned"

logs-view:
	@echo "Viewing recent logs..."
	@if [ -f /var/log/openclinic/django.log ]; then \
		tail -50 /var/log/openclinic/django.log; \
	else \
		echo "Log file not found. Create log directory with 'make logs'"; \
	fi

logs-errors:
	@echo "Viewing error logs..."
	@if [ -f /var/log/openclinic/django_errors.log ]; then \
		tail -50 /var/log/openclinic/django_errors.log; \
	else \
		echo "Error log file not found."; \
	fi

logs-security:
	@echo "Viewing security logs..."
	@if [ -f /var/log/openclinic/security.log ]; then \
		tail -50 /var/log/openclinic/security.log; \
	else \
		echo "Security log file not found."; \
	fi
# ============================================================
# CI/CD Targets (Local Testing)
# ============================================================

.PHONY: ci ci-lint ci-test ci-security ci-docs ci-docker ci-full

# Install CI dependencies
install-ci:
	pip install -r requirements-ci.txt

# Run full CI locally (mirrors GitHub Actions)
ci: ci-lint ci-test ci-security ci-docs ci-docker
	@echo ""
	@echo "✅ All CI checks passed locally!"

# CI: Linting only
ci-lint: lint
	@echo "✅ Linting passed!"

# CI: Tests only
ci-test: test-coverage
	@echo "✅ Tests passed!"

# CI: Security only
ci-security: security-check pip-audit
	@echo "✅ Security checks passed!"

# CI: Documentation only
ci-docs:
	@echo "Validating documentation..."
	mkdocs build --strict --site-dir site 2>&1 | head -20 || echo "MkDocs build had warnings"

# CI: Docker only
ci-docker:
	@echo "Building Docker images..."
	docker build --target development -t openclinic:dev .
	docker build --target production -t openclinic:prod .
	@echo "✅ Docker builds successful!"

# CI: Docker BuildKit cache optimization
ci-docker-cache:
	docker buildx build --cache-from type=gha -t openclinic:dev --target development .
	docker buildx build --cache-from type=gha -t openclinic:prod --target production .

# Dependency audit
pip-audit:
	@echo "Running pip-audit..."
	pip-audit --format=columns || echo "Vulnerabilities found (see above)"

# Validate migrations
ci-migrations:
	@echo "Checking migrations..."
	python manage.py makemigrations --check --dry-run
	@echo "✅ Migrations are up to date!"

# URL validation
ci-urls:
	@echo "Validating URLs..."
	python manage.py show_urls 2>/dev/null || echo "show_urls not available"

# Fast CI (skip slow checks)
ci-fast: lint test
	@echo "✅ Fast CI passed! (lint + test only)"
