# syntax=docker/dockerfile:1
# ============================================================
# OpenClinic Dockerfile - Multi-stage Build
# ============================================================
# This Dockerfile supports development, production, and test modes.
#
# Build Options:
#   - Development:  docker build --target development -t openclinic:dev .
#   - Production:   docker build --target production -t openclinic:prod .
#   - Test:         docker build --target test -t openclinic:test .
#
# Usage:
#   - Development:  docker run -p 8000:8000 openclinic:dev
#   - Production:   docker run -p 8000:8000 -e DJANGO_SETTINGS_MODULE=openclinic.settings.production openclinic:prod
#   - Test:         docker run --rm openclinic:test pytest -v
# ============================================================

# -----------------------------------------------------------------------------
# STAGE 1: Builder - Install dependencies and collect assets
# -----------------------------------------------------------------------------
FROM python:3.13-slim-bookworm AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set Python environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_PYTHON_VERSION_WARNING=1 \
    PYTHONPATH=/install

# Set work directory
WORKDIR /src

# Copy source code first, then install dependencies
COPY . .

# Install Python dependencies
RUN pip install --target=/install .

# Create static directory and collect static files (for production)
RUN mkdir -p /src/staticcollected && \
    DJANGO_SETTINGS_MODULE=openclinic.settings.production \
    python manage.py collectstatic --noinput \
    --settings=openclinic.settings.production

# -----------------------------------------------------------------------------
# STAGE 2: Development - Full development environment with debug tools
# -----------------------------------------------------------------------------
FROM python:3.13-slim-bookworm AS development

# Install development dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Set Python environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=openclinic.settings.development

# Create non-root user for security
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Install Python dependencies
# First copy only pyproject.toml to leverage Docker cache
COPY pyproject.toml .

# Then copy source code and install
COPY --chown=appuser:appgroup . .
RUN pip install -e ".[development,testing]" --no-cache-dir

# Switch to non-root user
USER appuser

WORKDIR /home/appuser

# Expose development port
EXPOSE 8000

# Health check for development
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')" || exit 1

# Default command for development
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# -----------------------------------------------------------------------------
# STAGE 3: Production - Minimal production image with Gunicorn
# -----------------------------------------------------------------------------
FROM python:3.13-slim-bookworm AS production

# Install production dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set Python environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=openclinic.settings.production \
    PYTHONPATH=/usr/local

# Create non-root user
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy static files from builder
COPY --from=builder /src/staticcollected /home/appuser/staticcollected

# Copy application code
COPY --chown=appuser:appgroup --chmod=755 . /home/appuser

# Switch to non-root user
USER appuser

WORKDIR /home/appuser

# Expose production port
EXPOSE 8000

# Health check for production
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')" || exit 1

# Default command for production (Gunicorn)
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--worker-class", "sync", \
     "--timeout", "120", \
     "--keep-alive", "5", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "openclinic.wsgi:application"]

# -----------------------------------------------------------------------------
# STAGE 4: Test - Minimal image for running tests in CI/CD
# -----------------------------------------------------------------------------
FROM python:3.13-slim-bookworm AS test

# Install testing dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Set Python environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=openclinic.settings.test

# Create non-root user for security
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Copy source code and install dependencies
COPY --chown=appuser:appgroup . /home/appuser
RUN cd /home/appuser && pip install -e ".[testing]" --no-cache-dir

USER appuser
WORKDIR /home/appuser

CMD ["pytest", "-v"]
