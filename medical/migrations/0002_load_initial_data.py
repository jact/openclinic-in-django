# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core.management import call_command

fixture = 'initial_data'


def load_fixture(apps, schema_editor):
    call_command('loaddata', fixture, app_label='medical')


def unload_fixture(apps, schema_editor):
    """Brutally deleting all entries for this model..."""

    MyModel = apps.get_model("medical", "Staff")
    MyModel.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]
