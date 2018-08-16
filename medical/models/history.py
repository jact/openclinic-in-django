# -*- coding: UTF-8 -*-

# Copyright (c) 2012-2018 Jose Antonio Chavarría <jachavar@gmail.com>
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

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class History(models.Model):
    patient = models.OneToOneField(
        'Patient',
        on_delete=models.CASCADE
    )

    birth_growth = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('birth and growth')
    )
    growth_sexuality = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('growth and sexuality')
    )

    feed = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('feed')
    )
    habits = models.TextField(
        verbose_name=_('habits'),
        blank=True,
        null=True
    )
    peristaltic_conditions = models.TextField(
        verbose_name=_('peristaltic conditions'),
        blank=True,
        null=True
    )
    psychological_conditions = models.TextField(
        verbose_name=_('psychological conditions'),
        blank=True,
        null=True
    )

    children_complaint = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('children complaint')
    )
    venereal_disease = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('veneral disease')
    )
    accident_surgical_operation = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('accidents and surgical operations')
    )
    medical_intolerance = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('medical intolerance')
    )
    mental_illness = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('mental illness')
    )

    parents_status_health = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('parents status health')
    )
    brothers_status_health = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('brothers status health')
    )
    spouse_childs_status_health = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('spouse and childs status health')
    )
    family_illness = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('family illness')
    )

    def __str__(self):
        return '%s (%s)' % (
            self.patient,
            self.medical_intolerance
        )

    class Meta:
        app_label = 'medical'
        db_table = 'history'
