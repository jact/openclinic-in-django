---
category: how-to
audience: Developers and operators deploying OpenClinic with Docker
---

# Docker Deployment Guide

## Running OpenClinic with Docker

This guide covers running OpenClinic using Docker containers.

## Prerequisites

- [Docker Engine](https://docs.docker.com/engine/install/) 20.10+
- [Docker Compose](https://docs.docker.com/compose/install/) v2.20+
- 4GB RAM minimum (8GB recommended)

---

## Quick Start

### 1. Clone and Navigate

```bash
git clone https://github.com/jact/openclinic-in-django.git
cd openclinic-in-django
```

### 2. Configure Environment

```bash
# Copy environment file
cp .env.example .env

# Edit with your settings (optional for development)
nano .env
```

### 3. Start Containers

```bash
# Development with SQLite
docker compose up -d

# Production with PostgreSQL
docker compose -f docker-compose.yml -f docker-compose.production.yml up -d
```

### 4. Access OpenClinic

```bash
# Development server
http://localhost:8000

# Create superuser
docker exec -it openclinic-dev python manage.py createsuperuser
```

---

## Development Mode

### Build and Run Development Image

```bash
# Build development image
docker build --target development -t openclinic:dev .

# Run development server
docker run -p 8000:8000 \
  -v $(pwd):/home/appuser \
  -e DJANGO_SETTINGS_MODULE=openclinic.settings.development \
  openclinic:dev
```

### With Docker Compose (Development)

```bash
# Start development services
docker compose --profile dev up -d

# View logs
docker compose logs -f openclinic-dev

# Stop services
docker compose down
```

### Development Features

- File mounts for live reloading
- SQLite database
- Debug toolbar enabled
- Full debugging output

---

## Production Mode

### Build Production Image

```bash
# Build production image
docker build --target production -t openclinic:prod .

# Run with PostgreSQL
docker run -p 8000:8000 \
  -e DJANGO_SETTINGS_MODULE=openclinic.settings.production \
  -e DATABASE_URL=postgres://user:pass@host:5432/db \
  -e SECRET_KEY=your-secret-key \
  openclinic:prod
```

### Production with Docker Compose

```bash
# Set production environment variables
export DJANGO_SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
export ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Start production services
docker compose -f docker-compose.yml -f docker-compose.production.yml up -d

# Run migrations
docker compose exec openclinic-prod python manage.py migrate

# Create superuser
docker compose exec openclinic-prod python manage.py createsuperuser

# Collect static files (already done in build)
docker compose exec openclinic-prod python manage.py collectstatic --noinput
```

### Production Features

- Multi-stage build (minimal image ~200MB)
- Gunicorn WSGI server
- PostgreSQL database
- Redis cache
- Health check endpoints
- Resource limits configured

---

## Health Check Endpoints

OpenClinic exposes health check endpoints for container orchestration:

| Endpoint | Purpose |
|----------|---------|
| `/health/` | Full health check (DB + system) |
| `/health/ready/` | Readiness probe for Kubernetes |
| `/health/live/` | Liveness probe for Kubernetes |

```bash
# Test health endpoint
curl http://localhost:8000/health/

# Response
{"status": "healthy", "database": "healthy"}
```

---

## Docker Architecture

```mermaid
graph TB
    subgraph "Development"
        D[Dockerfile\nDevelopment] --> Dc[openclinic-dev]
        Dc --> S[(SQLite)]
    end
    
    subgraph "Production"
        P[Dockerfile\nProduction] --> Pc[openclinic-prod]
        Pc --> Pg[(PostgreSQL)]
        Pc --> R[(Redis)]
        Pc --> G[Gunicorn\nWorkers]
    end
    
    subgraph "Orchestration"
        C[docker-compose.yml]
        C --> D
        C --> P
    end
```

---

## Multi-Stage Build

The Dockerfile uses multi-stage builds for optimized images:

| Stage | Base Image | Purpose | Size |
|-------|------------|---------|------|
| `builder` | python:3.13-slim | Install dependencies | ~500MB |
| `development` | python:3.13-slim | Dev with debug tools | ~800MB |
| `production` | python:3.13-slim | Minimal production | ~250MB |
| `test` | python:3.13-slim | CI/CD testing | ~700MB |

---

## Environment Variables

### Required for Production

```bash
DJANGO_SECRET_KEY=<your-secure-secret-key>
DJANGO_SETTINGS_MODULE=openclinic.settings.production
DATABASE_URL=postgres://user:pass@host:5432/database
ALLOWED_HOSTS=domain.com,www.domain.com
```

### Optional

```bash
DEBUG=False
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
REDIS_URL=redis://redis:6379/0
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Container won't start | Check logs: `docker compose logs` |
| Database connection failed | Verify `DATABASE_URL` format |
| Static files not loading | Ensure `collectstatic` ran |
| Memory issues | Increase Docker memory limit |
| Port already in use | Change port mapping: `-p 8080:8000` |

### View Logs

```bash
# All containers
docker compose logs

# Specific service
docker compose logs openclinic-dev

# Follow logs
docker compose logs -f
```

### Rebuild After Changes

```bash
# Force rebuild
docker compose build --no-cache

# Or rebuild specific service
docker compose build openclinic-dev
```

---

## Security Considerations

- Non-root user in containers
- Read-only filesystem option for production
- Secrets via environment variables
- SSL/TLS termination at load balancer

### Production Security Checklist

```bash
# Generate strong secret key
python -c "import secrets; print(secrets.token_urlsafe(64))"

# Use secrets management in production
# - Docker Swarm: docker secret
# - Kubernetes: Kubernetes Secrets
# - Cloud: AWS Secrets Manager, etc.
```

---

## CI/CD Integration

### Run Tests in Container

```bash
# Build test image
docker build --target test -t openclinic:test .

# Run tests
docker run --rm openclinic:test pytest -v
```

### GitHub Actions Example

```yaml
name: Docker Build
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker image
        run: docker build -t openclinic:test .
      
      - name: Run tests
        run: docker run --rm openclinic:test pytest
```
