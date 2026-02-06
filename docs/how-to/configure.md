
---
category: how-to
audience: Developers configuring OpenClinic
---

# Configuration Guide

## Configuring OpenClinic Settings

This guide covers OpenClinic configuration options.

## Settings Structure

OpenClinic uses environment-based configuration:

```
openclinic/settings/
├── base.py           # Shared settings
├── development.py    # Development overrides
├── production.py     # Production overrides
└── staging.py        # Staging overrides
```

## Required Settings

### Secret Key

```python
# Never commit secrets to version control!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
```

Generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Allowed Hosts

```python
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

## Database Configuration

### SQLite (Development)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'openclinic.db',
    }
}
```

### PostgreSQL (Production)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'openclinic',
        'USER': 'openclinic_user',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Security Settings

### HTTPS in Production

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Authentication

```python
AUTH_USER_MODEL = 'medical.Staff'

LOGIN_URL = 'openclinic_login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
```

## Custom User Model

OpenClinic uses a custom Staff model:

```python
class Staff(AbstractUser):
    collegiate_number = models.CharField(max_length=20, blank=True)
    specialty = models.CharField(max_length=50, blank=True)
```

## Third-Party Integration

### Email Configuration

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Secret key error | Set `DJANGO_SECRET_KEY` environment variable |
| Database connection failed | Verify DATABASE_URL or individual DB settings |
| Static files not loading | Run `python manage.py collectstatic` |
