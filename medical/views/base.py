# Copyright (c) 2012-2026 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
Base imports and utilities for medical views.
This module contains common imports used across all view modules.
"""

import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    RedirectView,
    UpdateView,
)
from el_pagination.views import AjaxListView

logger = logging.getLogger(__name__)


class PatientContextMixin:
    """Mixin to add patient to context based on pk in URL kwargs."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from medical.models import Patient

        context["patient"] = get_object_or_404(
            Patient, pk=self.kwargs.get("pk") or self.object.patient.id
        )
        return context


class SuccessMessageMixin:
    """Mixin providing success message and redirect after form submission."""

    success_message = ""
    success_url_name = ""

    def get_success_url(self):
        messages.success(self.request, self.success_message % self.object)
        return reverse(self.success_url_name, args=(self.object.id,))


class DeleteConfirmationMixin:
    """Mixin providing title and cancel_url for delete confirmation templates."""

    title_prefix = ""
    cancel_url_name = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"{self.title_prefix}: {self.object}"
        context["cancel_url"] = reverse(self.cancel_url_name, args=(self.object.id,))
        return context


class ProblemClosingMixin:
    """Mixin handling problem closing logic in form_valid."""

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.closing_date = timezone.now() if form.cleaned_data["closed"] else None
        instance.save()
        return super().form_valid(form)
