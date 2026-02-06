# Copyright (c) 2012-2026 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Tests for additional forms."""

import pytest
from django.test import RequestFactory

from medical.forms import (
    HistoryAntecedentsForm,
    PatientSearchByMedicalProblemForm,
    TestForm,
)
from medical.models import History, Patient, Problem


@pytest.mark.django_db
class TestPatientSearchByMedicalProblemForm:
    """Tests for PatientSearchByMedicalProblemForm."""

    def test_form_initialization_from_request(self):
        """Test form initializes fields from request GET params."""
        factory = RequestFactory()
        request = factory.get(
            "/test/",
            {"search_type_problem": "subjetive", "search_text_problem": "test query"},
        )
        form = PatientSearchByMedicalProblemForm(request=request)
        assert form.fields["search_type_problem"].initial == "subjetive"
        assert form.fields["search_text_problem"].initial == "test query"

    def test_form_default_initialization(self):
        """Test form initializes with default values."""
        factory = RequestFactory()
        request = factory.get("/test/")
        form = PatientSearchByMedicalProblemForm(request=request)
        assert form.fields["search_type_problem"].initial == "wording"
        assert form.fields["search_text_problem"].initial == ""

    def test_form_field_choices(self):
        """Test that form has correct field choices."""
        factory = RequestFactory()
        request = factory.get("/test/")
        form = PatientSearchByMedicalProblemForm(request=request)
        choices = dict(form.fields["search_type_problem"].choices)
        assert "wording" in choices
        assert "subjetive" in choices
        assert "objetive" in choices


@pytest.mark.django_db
class TestHistoryAntecedentsForm:
    """Tests for HistoryAntecedentsForm."""

    def test_form_fields(self):
        """Test that form has all required fields."""
        form = HistoryAntecedentsForm()
        assert "patient" in form.fields
        assert "medical_intolerance" in form.fields
        assert "birth_growth" in form.fields
        assert "family_illness" in form.fields
        assert "parents_status_health" in form.fields

    def test_form_patient_widget_hidden(self):
        """Test that patient field uses hidden widget."""
        form = HistoryAntecedentsForm()
        from django import forms

        assert isinstance(form.fields["patient"].widget, forms.HiddenInput)

    def test_form_save(self):
        """Test form save creates history."""
        patient = Patient.objects.create(first_name="John", last_name="Doe")
        data = {
            "patient": patient.pk,
            "medical_intolerance": "None",
            "birth_growth": "Normal",
            "growth_sexuality": "Normal",
            "feed": "Normal",
            "habits": "No smoking",
            "peristaltic_conditions": "Normal",
            "psychological": "Stable",
            "children_complaint": "None",
            "venereal_disease": "None",
            "accident_surgical_operation": "None",
            "mental_illness": "None",
            "parents_status_health": "Good",
            "brothers_status_health": "Good",
            "spouse_childs_status_health": "Good",
            "family_illness": "None",
        }
        form = HistoryAntecedentsForm(data=data)
        assert form.is_valid()
        history = form.save()
        assert history.patient == patient
        assert history.medical_intolerance == "None"

    def test_form_update_existing_history(self):
        """Test form updates existing history."""
        patient = Patient.objects.create(first_name="John", last_name="Doe")
        history = History.objects.create(
            patient=patient, medical_intolerance="Old value"
        )
        data = {
            "patient": patient.pk,
            "medical_intolerance": "Updated value",
            "birth_growth": "",
            "growth_sexuality": "",
            "feed": "",
            "habits": "",
            "peristaltic_conditions": "",
            "psychological": "",
            "children_complaint": "",
            "venereal_disease": "",
            "accident_surgical_operation": "",
            "mental_illness": "",
            "parents_status_health": "",
            "brothers_status_health": "",
            "spouse_childs_status_health": "",
            "family_illness": "",
        }
        form = HistoryAntecedentsForm(data=data, instance=history)
        assert form.is_valid()
        updated = form.save()
        assert updated.medical_intolerance == "Updated value"


@pytest.mark.django_db
class TestTestForm:
    """Tests for TestForm."""

    def test_form_fields(self):
        """Test that form has correct fields."""
        form = TestForm()
        assert "document" in form.fields
        assert "document_type" in form.fields
        assert "problem" in form.fields

    def test_form_problem_widget_hidden(self):
        """Test that problem field uses hidden widget."""
        form = TestForm()
        from django import forms

        assert isinstance(form.fields["problem"].widget, forms.HiddenInput)

    def test_form_save(self):
        """Test form save creates test."""
        from django.core.files.uploadedfile import SimpleUploadedFile

        patient = Patient.objects.create(first_name="John", last_name="Doe")
        problem = Problem.objects.create(
            patient=patient, wording="Test problem", order_number=1
        )
        test_file = SimpleUploadedFile(
            "document.pdf", b"content", content_type="application/pdf"
        )
        data = {
            "problem": problem.pk,
            "document_type": "application/pdf",
        }
        files = {"document": test_file}
        form = TestForm(data=data, files=files)
        assert form.is_valid()
        test = form.save()
        assert test.problem == problem
        assert test.document_type == "application/pdf"
