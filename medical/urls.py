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

from django.conf.urls import url
from django.views.generic import RedirectView
from django.urls import reverse_lazy

from .views import (
    PatientListView, PatientSearch, PatientCreate, PatientUpdate,
    PatientDelete, PatientRedirectDetail, PatientDetail, PatientRelatives,
    ProblemSearch, ProblemList, ProblemCreate, ProblemUpdate,
    ProblemDetail, ProblemDelete, ProblemConnections,
    HistoryList, HistoryAntecedentsDetail,
    HistoryAntecedentsCreate, HistoryAntecedentsUpdate,
    PatientMedicalReport, ProblemTests, ProblemTestDelete, PatientTests,
)

urlpatterns = [
    url(
        r'^$',
        RedirectView.as_view(
            url=reverse_lazy('patient_list'), permanent=True
        ),
        name='medical_records',
    ),

    url(
        r'^patient/$',
        PatientListView.as_view(),
        name='patient_list',
    ),

    url(
        r'^patient/search/$',
        PatientSearch.as_view(),
        name='patient_search',
    ),

    url(
        r'^patient/add/$',
        PatientCreate.as_view(),
        name='patient_add',
    ),

    url(
        r'^patient/(?P<pk>\d+)/change/$',
        PatientUpdate.as_view(),
        name='patient_change',
    ),

    url(
        r'^patient/(?P<pk>\d+)/delete/$',
        PatientDelete.as_view(),
        name='patient_delete',
    ),

    url(
        r'^patient/(?P<pk>\d+)/$',
        PatientRedirectDetail.as_view(),
        name='patient_redirect_detail',
    ),

    url(
        r'^patient/(?P<pk>\d+)-(?P<slug>[-\w]+)/$',
        PatientDetail.as_view(),
        name='patient_detail',
    ),

    url(
        r'^patient/(?P<pk>\d+)/report/$',
        PatientMedicalReport.as_view(),
        name='patient_medical_report',
    ),

    url(
        r'^patient/(?P<pk>\d+)/relatives/$',
        PatientRelatives.as_view(),
        name='patient_relatives',
    ),

    url(
        r'^patient/(?P<pk>\d+)/tests/$',
        PatientTests.as_view(),
        name='patient_tests',
    ),

    url(
        r'^problem/search/$',
        ProblemSearch.as_view(),
        name='problem_search',
    ),

    url(
        r'^patient/(?P<pk>\d+)/problem/$',
        ProblemList.as_view(),
        name='problem_list',
    ),

    url(
        r'^patient/(?P<pk>\d+)/problem/add/$',
        ProblemCreate.as_view(),
        name='problem_add',
    ),

    url(
        r'^problem/(?P<pk>\d+)/change/$',
        ProblemUpdate.as_view(),
        name='problem_change',
    ),

    url(
        r'^problem/(?P<pk>\d+)/$',
        ProblemDetail.as_view(),
        name='problem_detail',
    ),

    url(
        r'^problem/(?P<pk>\d+)/delete/$',
        ProblemDelete.as_view(),
        name='problem_delete',
    ),

    url(
        r'^problem/(?P<pk>\d+)/connections/$',
        ProblemConnections.as_view(),
        name='problem_connections',
    ),

    url(
        r'^problem/(?P<pk>\d+)/tests/$',
        ProblemTests.as_view(),
        name='problem_tests',
    ),

    url(
        r'^test/(?P<pk>\d+)/delete/$',
        ProblemTestDelete.as_view(),
        name='problem_test_delete',
    ),

    url(
        r'^patient/(?P<pk>\d+)/history/$',
        HistoryList.as_view(),
        name='patient_history',
    ),

    url(
        r'^patient/(?P<pk>\d+)/history/antecedents/$',
        HistoryAntecedentsDetail.as_view(),
        name='patient_history_antecedents',
    ),

    url(
        r'^patient/(?P<pk>\d+)/history/antecedents/add/$',
        HistoryAntecedentsCreate.as_view(),
        name='patient_history_antecedents_add',
    ),

    url(
        r'^patient/(?P<pk>\d+)/history/antecedents/change/$',
        HistoryAntecedentsUpdate.as_view(),
        name='patient_history_antecedents_change',
    ),
]
