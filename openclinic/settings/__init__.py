# -*- coding: UTF-8 -*-

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
#
# Author: Jose Antonio Chavarría <jachavar@gmail.com>

__author__ = 'Jose Antonio Chavarría'
__license__ = 'GPLv3'

import os
import importlib

# Get the Django settings module from environment variable
# Format: DJANGO_SETTINGS_MODULE=openclinic.settings.development|staging|production|test
# Default: openclinic.settings.base if not set (to use base.py by default)

django_settings = os.environ.get('DJANGO_SETTINGS_MODULE', '')

# Load the base settings by default (includes logging configuration)
from .base import *
