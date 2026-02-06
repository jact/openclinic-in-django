# Copyright (c) 2012-2026 Jose Antonio Chavarría <jachavar@gmail.com>
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

"""
Base imports and utilities for medical views.
This module contains common imports used across all view modules.
"""

import logging

from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.views.generic import (
    ListView,
    CreateView,
    RedirectView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.utils.translation import gettext_lazy as _

from el_pagination.views import AjaxListView

logger = logging.getLogger(__name__)
