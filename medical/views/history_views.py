# Copyright (c) 2012-2026 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""History-related views."""

from django.http import Http404

from .base import (
    LoginRequiredMixin, AjaxListView, CreateView, UpdateView,
    DetailView, redirect, get_object_or_404, messages, logger, _
)
from ..models import Patient, Problem, History
from ..forms import HistoryAntecedentsForm


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
        # Optimizado: select_related para evitar consultas N+1
        return Problem.closed.filter(
            patient__id=self.kwargs['pk']
        ).select_related('patient', 'doctor').order_by('-modified')


class HistoryAntecedentsDetail(LoginRequiredMixin, DetailView):
    model = History
    context_object_name = 'history'
    template_name = 'history_antecedents_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = get_object_or_404(Patient, pk=self.kwargs['pk'])
        history = get_object_or_404(History, patient__id=self.kwargs['pk'])

        context['patient'] = patient
        context['history'] = history

        return context

    def get_queryset(self):
        return History.objects.filter(
            patient__id=self.kwargs['pk']
        ).select_related('patient')

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            # Verificar que el paciente existe primero
            get_object_or_404(Patient, pk=self.kwargs['pk'])
            # Paciente existe pero history no - redirigir a creación
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

        return reverse(
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
        # Optimizado: select_related para cargar patient
        return History.objects.select_related('patient').get(
            patient__id=self.kwargs['pk']
        )

    def get_success_url(self):
        messages.success(self.request, _("Antecedents have been updated!"))

        return reverse(
            'patient_history_antecedents',
            args=(self.object.patient.id,)
        )
