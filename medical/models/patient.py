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

from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from . import TimeStampedModel


class Patient(TimeStampedModel):
    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )

    first_name = models.CharField(max_length=30, verbose_name=_('first name'))
    last_name = models.CharField(max_length=30, verbose_name=_('last name'))
    last_name_optional = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_('last name optional')
    )

    address = models.TextField(null=True, blank=True, verbose_name=_('address'))
    phone_contact = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('phone contact')
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
        verbose_name=_('gender')
    )
    race = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_('race')
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('birth date'),
        help_text=f'{_("yyyy")-{_("mm")}-{_("dd")}}'
    )
    birth_place = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('birth place')
    )
    decease_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('decease date'),
        help_text=f'{_("yyyy")-{_("mm")}-{_("dd")}}'
    )

    tin = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name=_('taxpayer Identification Number (TIN)')
    )
    ssn = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_('social Security Number (SSN)')
    )
    health_card_number = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_('health card number')
    )

    family_situation = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('family situation')
    )
    labour_situation = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('labour situation')
    )
    education = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('education')
    )

    insurance_company = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_('insurance company')
    )

    doctor_assigned = models.ForeignKey(
        'medical.Staff',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('doctor allocated by quota')
    )

    relatives = models.ManyToManyField('self', blank=True)

    class Meta:
        app_label = 'medical'
        db_table = 'patient'
        ordering = ['last_name', 'last_name_optional', 'first_name']
        verbose_name = _('Patient')
        verbose_name_plural = _('Patients')

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.last_name_optional}'

    def clean(self):
        super().clean()
        if self.birth_date and self.decease_date \
                and self.birth_date > self.decease_date:
            raise ValidationError(_('Can not die before birth'))

    def age(self):
        age = 0
        if self.birth_date:
            begin = self.birth_date
            end = self.decease_date or datetime.today().date()
            age = (end - begin).days / 365

        return age

    def gender_description(self):
        if self.gender:
            return dict(self.GENDER_CHOICES)[self.gender]

        return None
