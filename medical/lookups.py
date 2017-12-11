# -*- coding: utf-8 -*-

# Copyright (c) 2012-2017 Jose Antonio Chavarría <jachavar@gmail.com>
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

from django.db.models import Q
from django.core.urlresolvers import reverse
from django.utils.html import escape

from ajax_select import register, LookupChannel

from .models import Patient, Problem


@register('patients')
class PatientLookup(LookupChannel):
    model = Patient

    def can_add(self, user, model):
        return False

    def format_item_display(self, obj):
        return u'<a href="{}">{}</a>'.format(
            reverse('patient_redirect_detail', args=(obj.id,)),
            escape(obj.__str__())
        )

    def get_query(self, q, request):
        return self.model.objects.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(last_name_optional__icontains=q)
        )

    def get_objects(self, ids):
        return self.model.objects.filter(pk__in=ids).order_by('first_name')


@register('problems')
class ProblemLookup(LookupChannel):
    model = Problem

    def can_add(self, user, model):
        return False

    def format_item_display(self, obj):
        return u'<a href="{}">{}</a>'.format(
            reverse('problem_detail', args=(obj.id,)),
            escape(obj.__str__())
        )

    def get_query(self, q, request):
        return self.model.objects.filter(
            Q(wording__icontains=q)
            | Q(subjetive__icontains=q)
            | Q(objetive__icontains=q)
        )

    def get_objects(self, ids):
        return self.model.objects.filter(pk__in=ids).order_by('wording')
