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

from django.conf.urls import include, url
from django.views.generic import TemplateView, RedirectView
from django.core.urlresolvers import reverse_lazy
from django.conf.urls.static import static
from django.conf import settings

from ajax_select import urls as ajax_select_urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^ajax_select/', include(ajax_select_urls)),

    url(
        r'^$',
        RedirectView.as_view(url=reverse_lazy('welcome'), permanent=True),
        name='bootstrap'
    ),

    url(
        r'^info/$',
        RedirectView.as_view(url=reverse_lazy('welcome'), permanent=True),
        name='info'
    ),

    url(
        r'^info/welcome/$',
        TemplateView.as_view(template_name='info/welcome.html'),
        name='welcome'
    ),

    url(
        r'^info/readme/$',
        TemplateView.as_view(template_name='info/readme.html'),
        name='readme'
    ),
    url(
        r'^info/install/$',
        TemplateView.as_view(template_name='info/install.html'),
        name='install'
    ),
    url(
        r'^info/license/$',
        TemplateView.as_view(template_name='info/license.html'),
        name='license'
    ),

    url(
        r'^login/$',
        'login',
        {'template_name': 'login.html'},
        name='openclinic_login',
        prefix='django.contrib.auth.views'
    ),
    url(
        r'^logout/$',
        'logout',
        {'next_page': '/'},
        name='openclinic_logout',
        prefix='django.contrib.auth.views'
    ),

    url(r'^medical_records/', include('medical.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
