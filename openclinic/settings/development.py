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

__author__ = "Jose Antonio Chavarría"
__license__ = "GPLv3"

# Django settings for develop openclinic project

from .base import *

DEBUG = True
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG

# python manage.py graph_models -a -o myapp_models.png
INSTALLED_APPS += ("debug_toolbar", "django_extensions")
INTERNAL_IPS = ("127.0.0.1",)

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
