# Copyright (c) 2012-2026 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Additional tests for views."""

import pytest
from django.urls import reverse

from medical.models import History, Patient, Problem


@pytest.mark.django_db
class TestPatientUpdateView:
    """Tests for PatientUpdate view."""

    def test_patient_update_success(self, client_logged_in, test_patient):
        """Test successful patient update."""
        url = reverse("patient_change", kwargs={"pk": test_patient.pk})
        data = {
            "first_name": "Updated",
            "last_name": "Name",
            "gender": "M",
            "address": "123 Test St",
            "phone_contact": "555-1234",
        }
        resp = client_logged_in.post(url, data)
        assert resp.status_code == 302
        test_patient.refresh_from_db()
        assert test_patient.first_name == "Updated"

    def test_patient_update_404(self, client_logged_in):
        """Test update non-existent patient returns 404."""
        url = reverse("patient_change", kwargs={"pk": 999999})
        resp = client_logged_in.get(url)
        assert resp.status_code == 404


@pytest.mark.django_db
class TestPatientDeleteView:
    """Tests for PatientDelete view."""

    def test_patient_delete_success(self, client_logged_in, test_patient):
        """Test successful patient deletion."""
        url = reverse("patient_delete", kwargs={"pk": test_patient.pk})
        resp = client_logged_in.post(url)
        assert resp.status_code == 302
        assert Patient.objects.filter(pk=test_patient.pk).count() == 0

    def test_patient_delete_get_shows_confirmation(
        self, client_logged_in, test_patient
    ):
        """Test GET request shows delete confirmation."""
        url = reverse("patient_delete", kwargs={"pk": test_patient.pk})
        resp = client_logged_in.get(url)
        assert resp.status_code == 200


@pytest.mark.django_db
class TestProblemDeleteView:
    """Tests for ProblemDelete view."""

    def test_problem_delete_success(self, client_logged_in, test_problem):
        """Test successful problem deletion."""
        url = reverse("problem_delete", kwargs={"pk": test_problem.pk})
        resp = client_logged_in.post(url)
        assert resp.status_code == 302
        assert Problem.objects.filter(pk=test_problem.pk).count() == 0

    def test_problem_delete_redirects_to_list(self, client_logged_in, test_problem):
        """Test problem deletion redirects to problem list."""
        url = reverse("problem_delete", kwargs={"pk": test_problem.pk})
        resp = client_logged_in.post(url)
        assert resp.status_code == 302
        expected_url = reverse("problem_list", kwargs={"pk": test_problem.patient.pk})
        assert resp.url == expected_url


@pytest.mark.django_db
class TestPatientSearchView:
    """Tests for PatientSearch view."""

    def test_patient_search_by_pattern(self, client_logged_in, test_patient):
        """Test searching patients by name pattern."""
        url = reverse("patient_search")
        resp = client_logged_in.get(url, {"q": "John"})
        assert resp.status_code == 200

    def test_patient_search_no_pattern(self, client_logged_in):
        """Test search without pattern returns all."""
        url = reverse("patient_search")
        resp = client_logged_in.get(url)
        assert resp.status_code == 200


@pytest.mark.django_db
class TestHistoryAntecedentsCreateView:
    """Tests for HistoryAntecedentsCreate view."""

    def test_history_create_success(self, client_logged_in, test_patient):
        """Test successful history antecedents creation."""
        url = reverse("patient_history_antecedents_add", kwargs={"pk": test_patient.pk})
        data = {
            "patient": test_patient.pk,
            "medical_intolerance": "None",
            "birth_growth": "Normal",
            "parents_status_health": "Good",
        }
        resp = client_logged_in.post(url, data)
        assert resp.status_code == 302
        assert History.objects.filter(patient=test_patient).count() == 1

    def test_history_create_page_loads(self, client_logged_in, test_patient):
        """Test history creation page loads successfully."""
        url = reverse("patient_history_antecedents_add", kwargs={"pk": test_patient.pk})
        resp = client_logged_in.get(url)
        assert resp.status_code == 200


@pytest.mark.django_db
class TestHistoryAntecedentsUpdateView:
    """Tests for HistoryAntecedentsUpdate view."""

    def test_history_update_success(self, client_logged_in, test_patient):
        """Test successful history antecedents update."""
        history = History.objects.create(
            patient=test_patient, medical_intolerance="Old"
        )
        url = reverse(
            "patient_history_antecedents_change", kwargs={"pk": test_patient.pk}
        )
        data = {
            "patient": test_patient.pk,
            "medical_intolerance": "Updated",
        }
        resp = client_logged_in.post(url, data)
        assert resp.status_code == 302
        history.refresh_from_db()
        assert history.medical_intolerance == "Updated"


@pytest.mark.django_db
class TestPatientMedicalReportView:
    """Tests for PatientMedicalReport view."""

    def test_medical_report_loads(self, client_logged_in, test_patient):
        """Test medical report page loads."""
        History.objects.create(patient=test_patient)
        url = reverse("patient_medical_report", kwargs={"pk": test_patient.pk})
        resp = client_logged_in.get(url)
        assert resp.status_code == 200

    def test_medical_report_with_problems(self, client_logged_in, test_patient):
        """Test medical report with open and closed problems."""
        History.objects.create(patient=test_patient)
        Problem.objects.create(
            patient=test_patient,
            wording="Open problem",
            order_number=1,
            closing_date=None,
        )
        url = reverse("patient_medical_report", kwargs={"pk": test_patient.pk})
        resp = client_logged_in.get(url)
        assert resp.status_code == 200
        assert "problem_list" in resp.context
