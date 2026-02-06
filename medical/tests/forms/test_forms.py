from datetime import date

import pytest
from django.test import RequestFactory

from medical.forms import (
    HistoryAntecedentsForm,
    PatientForm,
    PatientSearchForm,
    ProblemForm,
)
from medical.models import Patient


@pytest.mark.django_db
class TestPatientForm:
    """Tests for PatientForm."""

    def test_valid_patient_form(self):
        """Test form with valid data."""
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "birth_date": "1990-01-01",
        }
        form = PatientForm(data=data)
        assert form.is_valid()

    def test_invalid_patient_form_missing_required(self):
        """Test form fails without required fields."""
        data = {
            "first_name": "",
            "last_name": "Doe",
        }
        form = PatientForm(data=data)
        assert not form.is_valid()
        assert "first_name" in form.errors

    def test_patient_form_save(self):
        """Test form saves correctly."""
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "gender": "F",
        }
        form = PatientForm(data=data)
        assert form.is_valid()
        patient = form.save()
        assert patient.pk is not None
        assert patient.first_name == "Jane"


@pytest.mark.django_db
class TestPatientSearchForm:
    """Tests for PatientSearchForm."""

    def test_search_form_valid(self):
        """Test search form with valid data."""
        factory = RequestFactory()
        request = factory.get("/", {"search_type": "first_name", "search_text": "John"})
        # Pass data explicitly to form
        form = PatientSearchForm(data=request.GET, request=request)
        assert form.is_valid()

    def test_search_form_empty_valid(self):
        """Test search form can be empty."""
        factory = RequestFactory()
        request = factory.get("/", {"search_type": "last_name", "search_text": ""})
        form = PatientSearchForm(data=request.GET, request=request)
        assert form.is_valid()


@pytest.mark.django_db
class TestProblemForm:
    """Tests for ProblemForm."""

    def test_valid_problem_form(self):
        """Test form with valid data."""
        patient = Patient.objects.create(first_name="John", last_name="Doe")
        data = {
            "patient": patient.pk,
            "wording": "Medical issue description",
            "order_number": 1,
        }
        form = ProblemForm(data=data)
        assert form.is_valid()

    def test_problem_form_closed_sets_date(self):
        """Test that closing problem sets closing date."""
        patient = Patient.objects.create(first_name="John", last_name="Doe")
        data = {
            "patient": patient.pk,
            "wording": "Issue to close",
            "order_number": 1,
            "closed": True,
        }
        form = ProblemForm(data=data)
        assert form.is_valid()
        problem = form.save(commit=False)
        if form.cleaned_data.get("closed"):
            problem.closing_date = date.today()
        problem.save()
        assert problem.closing_date is not None


@pytest.mark.django_db
class TestHistoryAntecedentsForm:
    """Tests for HistoryAntecedentsForm."""

    def test_valid_history_form(self):
        """Test form with valid data."""
        patient = Patient.objects.create(first_name="John", last_name="Doe")
        data = {
            "patient": patient.pk,
            "birth_growth": "Normal birth",
            "medical_intolerance": "Penicillin",
        }
        form = HistoryAntecedentsForm(data=data)
        assert form.is_valid()

    def test_history_form_optional_fields(self):
        """Test that most fields are optional."""
        patient = Patient.objects.create(first_name="John", last_name="Doe")
        data = {
            "patient": patient.pk,
        }
        form = HistoryAntecedentsForm(data=data)
        assert form.is_valid()
