# Copyright (c) 2012-2026 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Problem-related views."""

from ..forms import (
    PatientSearchByMedicalProblemForm,
    PatientSearchForm,
    ProblemConnectionsForm,
    ProblemForm,
)
from ..models import Patient, Problem
from .base import (
    AjaxListView,
    CreateView,
    DeleteConfirmationMixin,
    DeleteView,
    DetailView,
    LoginRequiredMixin,
    PatientContextMixin,
    ProblemClosingMixin,
    SuccessMessageMixin,
    UpdateView,
    _,
    get_object_or_404,
    messages,
    reverse,
)


class ProblemCreate(LoginRequiredMixin, ProblemClosingMixin, CreateView):
    model = Problem
    form_class = ProblemForm
    template_name = "problem_form.html"

    def get_initial(self):
        patient_id = self.kwargs["pk"]
        return {
            "patient": patient_id,
            "order_number": Problem.get_last_order_number(patient_id) + 1,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = get_object_or_404(Patient, pk=self.kwargs["pk"])
        context["title"] = f"{patient.__str__()} ({_('New medical problem')})"
        return context

    def get_success_url(self):
        return reverse("problem_detail", args=(self.object.pk,))


class ProblemUpdate(
    LoginRequiredMixin, ProblemClosingMixin, SuccessMessageMixin, UpdateView
):
    model = Problem
    form_class = ProblemForm
    template_name = "problem_form.html"
    success_message = _("Medical problem, %s, updated!")
    success_url_name = "problem_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = (
            f"{self.object.patient} [{self.object.wording}] ({_('Update medical problem')})"
        )
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Problem, id=self.kwargs["pk"])


class ProblemSearch(LoginRequiredMixin, AjaxListView):
    model = Problem
    template_name = "problem_search.html"
    page_template = "includes/problem_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = PatientSearchForm(request=self.request)
        context["search_form_problem"] = PatientSearchByMedicalProblemForm(
            request=self.request
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        search_type = self.request.GET.get("search_type_problem", None)
        search_text = self.request.GET.get("search_text_problem", "")
        if search_type:
            search_filter = f"{search_type}__icontains"
            return queryset.filter(**{search_filter: search_text})

        return None


class ProblemList(LoginRequiredMixin, PatientContextMixin, AjaxListView):
    model = Problem
    template_name = "problem_list.html"
    page_template = "includes/problem_list.html"

    def get_queryset(self):
        super().get_queryset()
        # Optimizado: select_related para evitar consultas N+1
        return (
            Problem.opened.filter(patient__id=self.kwargs["pk"])
            .select_related("patient", "doctor")
            .order_by("-modified")
        )


class ProblemDetail(LoginRequiredMixin, DetailView):
    model = Problem
    template_name = "problem_detail.html"
    context_object_name = "problem"

    def get_object(self, queryset=None):
        # Optimizado: select_related carga patient en una sola consulta
        return get_object_or_404(
            Problem.objects.select_related("patient"), pk=self.kwargs.get("pk", None)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # patient ya está cargado via select_related
        context["problem"] = self.object
        context["patient"] = self.object.patient

        return context


class ProblemDelete(
    LoginRequiredMixin, DeleteConfirmationMixin, SuccessMessageMixin, DeleteView
):
    model = Problem
    template_name = "object_confirm_delete.html"
    title_prefix = _("Delete medical problem")
    cancel_url_name = "problem_detail"
    success_message = _("Medical problem, %s, deleted!")

    def get_success_url(self):
        return reverse("problem_list", args=(self.object.patient.id,))


class ProblemConnections(
    LoginRequiredMixin, PatientContextMixin, SuccessMessageMixin, UpdateView
):
    model = Problem
    form_class = ProblemConnectionsForm
    template_name = "problem_connections.html"
    success_message = _("Medical problem, %s, updated!")
    success_url_name = "problem_connections"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["problem"] = self.object
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Problem, id=self.kwargs["pk"])

    def form_valid(self, form):
        if self.kwargs["pk"] in form.cleaned_data["connections"]:
            form.cleaned_data["connections"].remove(self.kwargs["pk"])

        return super().form_valid(form)


# NOTE: HistoryList class has been moved to history_views.py
# Import from there: from .history_views import HistoryList
