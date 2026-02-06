# -*- coding: UTF-8 -*-

# Copyright (c) 2014-2015 Jose Antonio Chavarría
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
#
# Author: Jose Antonio Chavarría <jachavar@gmail.com>

__author__ = "Jose Antonio Chavarría"
__license__ = "GPLv3"

# Django settings for openclinic project (test environment)

from .base import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "openclinic_test",
        "USER": "test_user",
        "PASSWORD": "test_pass",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Use faster password hasher for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Silence security warnings for tests (expected in test mode)
SILENCED_SYSTEM_CHECKS = [
    "security.W001",  # SecurityMiddleware not in MIDDLEWARE
    "security.W012",  # SESSION_COOKIE_SECURE not True
    "security.W016",  # CSRF_COOKIE_SECURE not True
    "security.W018",  # DEBUG is True
]
