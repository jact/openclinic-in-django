# Copyright (c) 2012-2026 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of GNU General Public License as published by
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

from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy, re_path
from django.views.generic import TemplateView, RedirectView

from ajax_select import urls as ajax_select_urls

from django.contrib import admin

from . import health

admin.autodiscover()

urlpatterns = [
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    re_path(r'^grappelli/', include('grappelli.urls')),
    re_path(r'^admin/', admin.site.urls),

    re_path(r'^ajax_select/', include(ajax_select_urls)),

    re_path(
        r'^$',
        RedirectView.as_view(url=reverse_lazy('welcome'), permanent=True),
        name='bootstrap'
    ),

    re_path(
        r'^info/$',
        RedirectView.as_view(url=reverse_lazy('welcome'), permanent=True),
        name='info'
    ),

    re_path(
        r'^info/welcome/$',
        TemplateView.as_view(template_name='info/welcome.html'),
        name='welcome'
    ),

    re_path(
        r'^info/readme/$',
        TemplateView.as_view(template_name='info/readme.html'),
        name='readme'
    ),
    re_path(
        r'^info/install/$',
        TemplateView.as_view(template_name='info/install.html'),
        name='install'
    ),
    re_path(
        r'^info/license/$',
        TemplateView.as_view(template_name='info/license.html'),
        name='license'
    ),

    re_path(
        r'^login/$',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='openclinic_login'
    ),
    re_path(
        r'^logout/$',
        auth_views.LogoutView.as_view(next_page='/'),
        name='openclinic_logout'
    ),

    re_path(r'^medical_records/', include('medical.urls')),

    # Health check endpoints for container orchestration
    re_path(r'^health/$', health.health_check, name='health_check'),
    re_path(r'^health/ready/$', health.readiness_check, name='readiness_check'),
    re_path(r'^health/live/$', health.liveness_check, name='liveness_check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
                   + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    try:
        import debug_toolbar
        urlpatterns = [
            re_path(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
