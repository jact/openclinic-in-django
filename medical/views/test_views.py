# Copyright (c) 2012-2026 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Test-related views."""

from ..forms import TestForm
from ..models import Problem, Test
from .base import (
    CreateView,
    DeleteView,
    LoginRequiredMixin,
    _,
    get_object_or_404,
    messages,
    reverse,
)


class ProblemTests(LoginRequiredMixin, CreateView):
    model = Test
    form_class = TestForm
    template_name = "problem_tests.html"

    def get_initial(self):
        return {
            "problem": self.kwargs["pk"],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Optimizado: select_related carga patient en una sola consulta
        problem = get_object_or_404(
            Problem.objects.select_related("patient"), pk=self.kwargs["pk"]
        )
        # Optimizado: select_related para tests
        tests = Test.objects.filter(problem=problem).select_related("problem")

        context["problem"] = problem
        context["patient"] = problem.patient
        context["object_list"] = tests

        return context

    def get_success_url(self):
        messages.success(self.request, _("Medical test, %s, added!") % self.object)

        return reverse("problem_tests", args=(self.object.problem.id,))


class ProblemTestDelete(LoginRequiredMixin, DeleteView):
    model = Test
    template_name = "object_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"{_('Delete medical test')}: {self.object.filename()}"
        context["cancel_url"] = reverse("problem_tests", args=(self.object.problem.id,))

        return context

    def get_success_url(self):
        messages.success(
            self.request, _("Medical test, %s, deleted!") % str(self.object.filename())
        )

        return reverse("problem_tests", args=(self.object.problem.id,))
