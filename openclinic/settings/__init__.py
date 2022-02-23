# -*- coding: UTF-8 -*-

import os

django_settings = os.environ.get('DJANGO_SETTINGS_MODULE', '')

if django_settings != '' and django_settings != 'openclinic.settings':
    exec(f'from .{django_settings.split(".")[-1]} import *')
else:
    from .production import *
