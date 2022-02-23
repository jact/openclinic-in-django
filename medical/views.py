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

from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.views.generic import (
    ListView,
    CreateView,
    RedirectView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.utils.translation import ugettext_lazy as _

from el_pagination.views import AjaxListView

# from django.utils.log import getLogger
# logger = getLogger('django.request')

from .models import Patient, Problem, History, Test
from .forms import (
    PatientForm, PatientSearchForm, PatientSearchByMedicalProblemForm,
    ProblemForm, HistoryAntecedentsForm, PatientRelativesForm,
    ProblemConnectionsForm, TestForm,
)


class PatientCreate(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patient_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('New Patient')

        return context

    def get_success_url(self):
        messages.success(self.request, _("Patient, %s, added!") % self.object)

        return reverse_lazy('patient_redirect_detail', args=(self.object.id,))


class PatientUpdate(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patient_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object} ({_("Update patient social data")})'

        return context

    def get_object(self, queryset=None):
        return Patient.objects.get(id=self.kwargs['pk'])

    def get_success_url(self):
        messages.success(self.request, _("Patient, %s, updated!") % self.object)

        return reverse_lazy('patient_redirect_detail', args=(self.object.id,))


class PatientDelete(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'object_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{_("Delete patient")}: {self.object}'
        context['cancel_url'] = reverse_lazy(
            'patient_redirect_detail',
            args=(self.object.id,)
        )

        return context

    def get_success_url(self):
        messages.success(self.request, _("Patient, %s, deleted!") % self.object)

        return reverse_lazy('patient_list')


class PatientList(LoginRequiredMixin, AjaxListView):
    model = Patient
    template_name = 'patient_search.html'
    page_template = 'includes/patient_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = PatientSearchForm(request=self.request)
        context['search_form_problem'] = PatientSearchByMedicalProblemForm(
            request=self.request
        )

        return context


class PatientListView(PatientList):
    def get_queryset(self):
        queryset = super().get_queryset()

        search_type = self.request.GET.get('search_type', None)
        search_text = self.request.GET.get('search_text', '')
        if search_type:
            search_filter = f'{search_type}__icontains'
            return queryset.filter(**{search_filter: search_text})

        return None


class PatientSearch(PatientList):
    def get_queryset(self):
        queryset = super().get_queryset()
        pattern = self.request.GET.get('q', None)

        if pattern:
            return queryset.filter(
                Q(first_name__icontains=pattern)
                | Q(last_name__icontains=pattern)
                | Q(last_name_optional__icontains=pattern)
            )

        return queryset


class PatientRedirectDetail(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        patient_id = self.kwargs.get('pk', None)
        patient = Patient.objects.get(pk=patient_id)
        self.url = reverse(
            'patient_detail',
            kwargs={'pk': patient.id, 'slug': slugify(patient)}
        )

        return super().get(self, request, *args, **kwargs)


class PatientDetail(LoginRequiredMixin, DetailView):
    model = Patient
    context_object_name = 'patient'
    template_name = 'patient_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = Patient.objects.get(
            pk=self.kwargs.get('pk', None)
        )

        return context


class PatientRelatives(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientRelativesForm
    template_name = 'patient_relatives.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object

        return context

    def get_object(self, queryset=None):
        return Patient.objects.get(id=self.kwargs['pk'])

    def get_success_url(self):
        messages.success(self.request, _("Patient, %s, updated!") % self.object)
        return reverse_lazy('patient_relatives', args=(self.object.id,))

    def form_valid(self, form):
        # avoid IntegrityError
        if self.kwargs['pk'] in form.cleaned_data['relatives']:
            form.cleaned_data['relatives'].remove(self.kwargs['pk'])

        return super().form_valid(form)


class PatientMedicalReport(LoginRequiredMixin, DetailView):
    model = Patient
    context_object_name = 'patient'
    template_name = 'patient_medical_report.html'

    def get_context_data(self, **kwargs):
        patient_id = self.kwargs.get('pk', None)
        context = super().get_context_data(**kwargs)
        patient = get_object_or_404(Patient, pk=patient_id)
        history = get_object_or_404(History, patient__id=patient_id)

        context['patient'] = patient
        context['history'] = history
        context['problem_list'] = Problem.opened.filter(
            patient__id=self.kwargs['pk']
        ).order_by('-modified')
        context['closed_problem_list'] = Problem.closed.filter(
            patient__id=self.kwargs['pk']
        ).order_by('-modified')

        return context


class PatientTests(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patient_tests.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = get_object_or_404(Patient, pk=self.kwargs['pk'])

        return context

    def get_queryset(self):
        super().get_queryset()

        return Test.objects.filter(problem__patient__id=self.kwargs['pk'])


class ProblemCreate(LoginRequiredMixin, CreateView):
    model = Problem
    form_class = ProblemForm
    template_name = 'problem_form.html'

    def get_initial(self):
        patient_id = self.kwargs['pk']
        return {
            'patient': patient_id,
            'order_number': Problem.get_last_order_number(patient_id) + 1
        }

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.closing_date = None
        if form.cleaned_data['closed']:
            instance.closing_date = timezone.now()
        self.object = instance

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = get_object_or_404(Patient, pk=self.kwargs['pk'])
        context['title'] = f'{patient.__str__()} ({_("New medical problem")})'

        return context

    def get_success_url(self):
        return reverse_lazy('problem_detail', args=(self.object.pk,))


class ProblemUpdate(LoginRequiredMixin, UpdateView):
    model = Problem
    form_class = ProblemForm
    template_name = 'problem_form.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.closing_date = None
        if form.cleaned_data['closed']:
            instance.closing_date = timezone.now()
        self.object = instance

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.patient} [{self.object.wording}] ({_("Update medical problem")})'

        return context

    def get_object(self, queryset=None):
        return Problem.objects.get(id=self.kwargs['pk'])

    def get_success_url(self):
        messages.success(self.request, _('Medical problem, %s, updated!') % self.object)

        return reverse_lazy('problem_detail', args=(self.object.pk,))


class ProblemSearch(LoginRequiredMixin, AjaxListView):
    model = Problem
    template_name = 'problem_search.html'
    page_template = 'includes/problem_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = PatientSearchForm(request=self.request)
        context['search_form_problem'] = PatientSearchByMedicalProblemForm(request=self.request)

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        search_type = self.request.GET.get('search_type_problem', None)
        search_text = self.request.GET.get('search_text_problem', '')
        if search_type:
            search_filter = f'{search_type}__icontains'
            return queryset.filter(**{search_filter: search_text})

        return None


class ProblemList(LoginRequiredMixin, AjaxListView):
    model = Problem
    template_name = 'problem_list.html'
    page_template = 'includes/problem_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = get_object_or_404(Patient, pk=self.kwargs['pk'])

        return context

    def get_queryset(self):
        super().get_queryset()

        return Problem.opened.filter(patient__id=self.kwargs['pk']).order_by('-modified')


class ProblemDetail(LoginRequiredMixin, DetailView):
    model = Problem
    template_name = 'problem_detail.html'
    context_object_name = 'problem'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        problem = get_object_or_404(Problem, pk=self.kwargs.get('pk', None))
        patient = get_object_or_404(Patient, pk=problem.patient.id)
        context['problem'] = problem
        context['patient'] = patient

        return context


class ProblemDelete(LoginRequiredMixin, DeleteView):
    model = Problem
    template_name = 'object_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{_("Delete medical problem")}: {self.object}'
        context['cancel_url'] = reverse_lazy(
            'problem_detail',
            args=(self.object.id,)
        )

        return context

    def get_success_url(self):
        messages.success(
            self.request,
            _("Medical problem, %s, deleted!") % self.object
        )

        return reverse_lazy(
            'problem_list',
            args=(self.object.patient.id,)
        )


class ProblemConnections(LoginRequiredMixin, UpdateView):
    model = Problem
    form_class = ProblemConnectionsForm
    template_name = 'problem_connections.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = get_object_or_404(Patient, pk=self.object.patient.id)
        context['problem'] = self.object
        context['patient'] = patient

        return context

    def get_object(self, queryset=None):
        return Problem.objects.get(id=self.kwargs['pk'])

    def get_success_url(self):
        messages.success(
            self.request,
            _("Medical problem, %s, updated!") % self.object
        )

        return reverse_lazy('problem_connections', args=(self.object.id,))

    def form_valid(self, form):
        # avoid IntegrityError
        if self.kwargs['pk'] in form.cleaned_data['connections']:
            form.cleaned_data['connections'].remove(self.kwargs['pk'])

        return super().form_valid(form)


class HistoryList(LoginRequiredMixin, AjaxListView):
    model = Problem
    template_name = 'history_list.html'
    page_template = 'includes/problem_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = get_object_or_404(Patient, pk=self.kwargs['pk'])

        return context

    def get_queryset(self):
        super().get_queryset()

        return Problem.closed.filter(patient__id=self.kwargs['pk']).order_by('-modified')


class HistoryAntecedentsDetail(LoginRequiredMixin, DetailView):
    model = History
    context_object_name = 'history'
    template_name = 'history_antecedents_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = get_object_or_404(Patient, pk=self.kwargs['pk'])
        history = History.objects.get(patient__id=self.kwargs['pk'])

        context['patient'] = patient
        context['history'] = history

        return context

    def get_queryset(self):
        return History.objects.filter(patient__id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except:
            return redirect(
                'patient_history_antecedents_add',
                pk=self.kwargs['pk']
            )


class HistoryAntecedentsCreate(LoginRequiredMixin, CreateView):
    model = History
    form_class = HistoryAntecedentsForm
    template_name = 'history_antecedents_form.html'

    def get_initial(self):
        return {
            'patient': self.kwargs['pk'],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = get_object_or_404(Patient, pk=self.kwargs['pk'])
        context['title'] = f'{patient} ({_("Update antecedents")})'
        context['patient'] = patient

        return context

    def get_success_url(self):
        messages.success(self.request, _("Antecedents have been updated!"))

        return reverse_lazy(
            'patient_history_antecedents',
            args=(self.object.patient.id,)
        )


class HistoryAntecedentsUpdate(LoginRequiredMixin, UpdateView):
    model = History
    form_class = HistoryAntecedentsForm
    template_name = 'history_antecedents_form.html'

    def get_initial(self):
        return {
            'patient': self.kwargs['pk'],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = get_object_or_404(Patient, pk=self.kwargs['pk'])
        context['title'] = f'{patient} ({_("Update antecedents")})'
        context['patient'] = patient

        return context

    def get_object(self, queryset=None):
        return History.objects.get(patient__id=self.kwargs['pk'])

    def get_success_url(self):
        messages.success(self.request, _("Antecedents have been updated!"))

        return reverse_lazy(
            'patient_history_antecedents',
            args=(self.object.patient.id,)
        )


class ProblemTests(LoginRequiredMixin, CreateView):
    model = Test
    form_class = TestForm
    template_name = "problem_tests.html"

    def get_initial(self):
        return {
            'problem': self.kwargs['pk'],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        problem = get_object_or_404(Problem, pk=self.kwargs['pk'])
        patient = get_object_or_404(Patient, pk=problem.patient.id)
        tests = Test.objects.filter(problem=problem)

        context['problem'] = problem
        context['patient'] = patient
        context['object_list'] = tests

        return context

    def get_success_url(self):
        messages.success(
            self.request,
            _('Medical test, %s, added!') % self.object
        )

        return reverse_lazy('problem_tests', args=(self.object.problem.id,))


class ProblemTestDelete(LoginRequiredMixin, DeleteView):
    model = Test
    template_name = 'object_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{_("Delete medical test")}: {self.object.filename()}'
        context['cancel_url'] = reverse_lazy(
            'problem_tests',
            args=(self.object.problem.id,)
        )

        return context

    def get_success_url(self):
        messages.success(
            self.request,
            _('Medical test, %s, deleted!') % str(self.object.filename())
        )

        return reverse_lazy('problem_tests', args=(self.object.problem.id,))
