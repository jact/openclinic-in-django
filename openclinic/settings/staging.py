# Copyright (c) 2014-2026 Jose Antonio Chavarría
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of GNU General Public License as published by
# Free Software Foundation, either version 3 of the License, or
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

# Django settings for openclinic project (staging environment)

from .base import *

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# Staging logging configuration (less verbose than development)
LOGGING['handlers']['default']['level'] = 'INFO'
LOGGING['handlers']['console']['level'] = 'INFO'

LOGGING['loggers']['django.db.backends']['level'] = 'INFO'
LOGGING['loggers']['django']['level'] = 'INFO'
