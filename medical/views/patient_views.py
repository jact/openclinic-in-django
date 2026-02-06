# Copyright (c) 2012-2026 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Patient-related views."""

from .base import (
    LoginRequiredMixin, AjaxListView, ListView, CreateView, UpdateView,
    DeleteView, DetailView, RedirectView,
    Q, messages, reverse, get_object_or_404, redirect, slugify, logger, _
)
from ..models import Patient, Problem, History
from ..forms import PatientForm, PatientSearchForm, PatientSearchByMedicalProblemForm, PatientRelativesForm


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
        return reverse('patient_redirect_detail', args=(self.object.id,))


class PatientUpdate(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patient_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object} ({_("Update patient social data")})'
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Patient, id=self.kwargs['pk'])

    def get_success_url(self):
        messages.success(self.request, _("Patient, %s, updated!") % self.object)
        return reverse('patient_redirect_detail', args=(self.object.id,))


class PatientDelete(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'object_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{_("Delete patient")}: {self.object}'
        context['cancel_url'] = reverse(
            'patient_redirect_detail',
            args=(self.object.id,)
        )
        return context

    def get_success_url(self):
        messages.success(self.request, _("Patient, %s, deleted!") % self.object)
        return reverse('patient_list')


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
        patient = get_object_or_404(Patient, pk=patient_id)
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
        patient = get_object_or_404(Patient, pk=self.kwargs['pk'])
        context['patient'] = patient
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
        return reverse('patient_relatives', args=(self.object.id,))

    def form_valid(self, form):
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
        # Optimizado: select_related reduce consultas N+1 al acceder a doctor
        context['problem_list'] = Problem.opened.filter(
            patient__id=self.kwargs['pk']
        ).select_related('doctor').order_by('-modified')
        context['closed_problem_list'] = Problem.closed.filter(
            patient__id=self.kwargs['pk']
        ).select_related('doctor').order_by('-modified')

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
        from ..models import Test
        # Optimizado: select_related reduce consultas al acceder a problem y patient
        return Test.objects.filter(
            problem__patient__id=self.kwargs['pk']
        ).select_related('problem', 'problem__patient')
