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

__author__ = 'Jose Antonio Chavarría'
__license__ = 'GPLv3'

import os

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.utils.translation import gettext_lazy as _

from . import TimeStampedModel


class Test(TimeStampedModel):
    document_type = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name=_('MIME type')
    )
    document = models.FileField(
        upload_to='medical_tests/%Y/%m/%d',
        verbose_name=_('document')
    )

    problem = models.ForeignKey(
        'Problem',
        on_delete=models.CASCADE
    )

    class Meta:
        app_label = 'medical'
        indexes = [
            models.Index(fields=['problem']),
        ]

    def __str__(self):
        return str(self.document)

    def filename(self):
        return os.path.basename(self.document.name)


@receiver(pre_delete, sender=Test)
def test_delete(sender, instance, **kwargs):
    instance.document.delete(False)
