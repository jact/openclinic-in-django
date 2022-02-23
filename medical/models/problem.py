# -*- coding: UTF-8 -*-

# Copyright (c) 2012-2022 Jose Antonio Chavarría <jachavar@gmail.com>
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
from django.utils.translation import ugettext_lazy as _

from . import TimeStampedModel


class OpenedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(closing_date__isnull=True)


class ClosedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(closing_date__isnull=False)


class Problem(TimeStampedModel):
    order_number = models.PositiveSmallIntegerField(
        verbose_name=_('order number')
    )
    closing_date = models.DateField(
        blank=True,
        null=True,
        editable=False,
        verbose_name=_('closing date')
    )

    meeting_place = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('meeting place')
    )

    wording = models.TextField(
        verbose_name=_('wording')
    )

    subjetive = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('subjetive')
    )
    objetive = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('objetive')
    )
    appreciation = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('appreciation')
    )
    action_plan = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('action plan')
    )
    prescription = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("doctor's orders")
    )

    patient = models.ForeignKey(
        'Patient',
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        'medical.Staff',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('attending physician')
    )

    connections = models.ManyToManyField('self', blank=True)

    objects = models.Manager()
    opened = OpenedManager()
    closed = ClosedManager()

    @staticmethod
    def get_last_order_number(patient_id):
        last_order_number = Problem.objects.filter(
            patient_id__exact=patient_id
        ).aggregate(models.Max('order_number'))['order_number__max']
        if not last_order_number:
            last_order_number = 0

        return last_order_number

    def __str__(self):
        return f'{self.order_number}: {self.wording}'

    class Meta:
        app_label = 'medical'
        db_table = 'problem'
        ordering = ['order_number']
        verbose_name = _('Medical Problem')
        verbose_name_plural = _('Medical Problems')
