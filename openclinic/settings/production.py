# Copyright (c) 2014-2026 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Jose Antonio Chavarría'
__license__ = 'GPLv3'

# Django settings for openclinic project (production environment)

from .base import *

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# Security: Read allowed hosts from environment variable
# Format: comma-separated list of domains, e.g., "example.com,www.example.com"
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

STATIC_ROOT = '/var/tmp/static'

# Production logging configuration
import os

LOG_DIR = os.environ.get('LOG_DIR', '/var/log/openclinic')
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING['handlers']['file'] = {
    'level': 'INFO',
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': os.path.join(LOG_DIR, 'django.log'),
    'maxBytes': 1024 * 1024 * 10,  # 10 MB
    'backupCount': 5,
    'formatter': 'verbose',
}

LOGGING['handlers']['error_file'] = {
    'level': 'ERROR',
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': os.path.join(LOG_DIR, 'django_errors.log'),
    'maxBytes': 1024 * 1024 * 10,  # 10 MB
    'backupCount': 10,
    'formatter': 'verbose',
}

LOGGING['handlers']['security_file'] = {
    'level': 'WARNING',
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': os.path.join(LOG_DIR, 'security.log'),
    'maxBytes': 1024 * 1024 * 5,  # 5 MB
    'backupCount': 10,
    'formatter': 'verbose',
}

LOGGING['loggers']['django.security'] = {
    'handlers': ['security_file', 'mail_admins'],
    'level': 'WARNING',
    'propagate': False,
}

LOGGING['loggers']['django']['handlers'] = ['file', 'mail_admins']
