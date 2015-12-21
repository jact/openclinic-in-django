# -*- coding: UTF-8 -*-

# Copyright (c) 2012-2015 Jose Antonio Chavarría
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
#
# Author: Jose Antonio Chavarría <jachavar@gmail.com>

__author__ = 'Jose Antonio Chavarría'
__license__ = 'GPLv3'

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Patient, Problem, Staff, History, Test

admin.site.register(History)
admin.site.register(Patient)
admin.site.register(Problem)
admin.site.register(Test)


@admin.register(Staff)
class StaffAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions',
                'staff_type'
            )
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'staff_type', 'email', 'password1', 'password2'
            )
        }),
    )
    # https://www.caktusgroup.com/blog/2013/08/07/migrating-custom-user-model-django/
    # form = StaffChangeForm
    # add_form = StaffCreationForm
    list_display = ('first_name', 'last_name', 'email', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('username',)
