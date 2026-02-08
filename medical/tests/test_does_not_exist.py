import pytest
from django.urls import reverse

from medical.models import History, Patient, Problem


class TestPatientRedirectDetail:
    """Tests for PatientRedirectDetail view."""

    def test_patient_redirect_detail_404(self, client_logged_in):
        """Test that non-existent patient returns 404."""
        url = reverse("patient_redirect_detail", kwargs={"pk": 999999})
        resp = client_logged_in.get(url)
        assert resp.status_code == 404

    def test_patient_redirect_detail_success(self, client_logged_in, test_patient):
        """Test that existing patient redirects correctly."""
        url = reverse("patient_redirect_detail", kwargs={"pk": test_patient.pk})
        resp = client_logged_in.get(url)
        assert resp.status_code == 302


class TestPatientDetail:
    """Tests for PatientDetail view."""

    def test_patient_detail_404(self, client_logged_in):
        """Test that non-existent patient returns 404."""
        url = reverse("patient_detail", kwargs={"pk": 999999, "slug": "non-existent"})
        resp = client_logged_in.get(url)
        assert resp.status_code == 404

    def test_patient_detail_success(self, client_logged_in, test_patient):
        """Test that existing patient detail loads."""
        url = reverse(
            "patient_detail", kwargs={"pk": test_patient.pk, "slug": "john-doe"}
        )
        resp = client_logged_in.get(url)
        assert resp.status_code == 200


class TestPatientRelatives:
    """Tests for PatientRelatives view."""

    def test_patient_relatives_404(self, client_logged_in):
        """Test that non-existent patient returns 404."""
        url = reverse("patient_relatives", kwargs={"pk": 999999})
        resp = client_logged_in.get(url)
        assert resp.status_code == 404

    def test_patient_relatives_success(self, client_logged_in, test_patient):
        """Test that existing patient relatives page loads."""
        url = reverse("patient_relatives", kwargs={"pk": test_patient.pk})
        resp = client_logged_in.get(url)
        assert resp.status_code == 200


class TestPatientMedicalReport:
    """Tests for PatientMedicalReport view."""

    def test_medical_report_patient_404(self, client_logged_in):
        """Test that non-existent patient returns 404."""
        url = reverse("patient_medical_report", kwargs={"pk": 999999})
        resp = client_logged_in.get(url)
        assert resp.status_code == 404

    def test_medical_report_history_404(self, client_logged_in, test_patient):
        """Test that patient without history returns 404."""
        url = reverse("patient_medical_report", kwargs={"pk": test_patient.pk})
        resp = client_logged_in.get(url)
        assert resp.status_code == 404

    def test_medical_report_success(self, client_logged_in, test_patient):
        """Test that patient with history loads report."""
        History.objects.create(patient=test_patient)
        url = reverse("patient_medical_report", kwargs={"pk": test_patient.pk})
        resp = client_logged_in.get(url)
        assert resp.status_code == 200


class TestHistoryAntecedentsDetail:
    """Tests for HistoryAntecedentsDetail view."""

    def test_history_antecedents_detail_404(self, client_logged_in):
        """Test that non-existent patient returns 404."""
        url = reverse("patient_history_antecedents", kwargs={"pk": 999999})
        resp = client_logged_in.get(url)
        assert resp.status_code == 404

    def test_history_antecedents_detail_no_history(
        self, client_logged_in, test_patient
    ):
        """Test that patient without history redirects to create page."""
        url = reverse("patient_history_antecedents", kwargs={"pk": test_patient.pk})
        resp = client_logged_in.get(url)
        assert resp.status_code == 302
        assert resp.url == reverse(
            "patient_history_antecedents_add", kwargs={"pk": test_patient.pk}
        )

    @pytest.mark.django_db(transaction=True)
    def test_history_antecedents_detail_success(self, client_logged_in):
        """Test that patient with history loads."""
        from medical.models import History, Patient

        patient = Patient.objects.create(
            first_name="John", last_name="Doe", last_name_optional="Smith"
        )
        History.objects.create(patient=patient, medical_intolerance="Test")
        url = reverse("patient_history_antecedents", kwargs={"pk": patient.pk})
        resp = client_logged_in.get(url)
        assert resp.status_code == 302


class TestProblemDetail:
    """Tests for ProblemDetail view."""

    def test_problem_detail_404(self, client_logged_in):
        """Test that non-existent problem returns 404."""
        url = reverse("problem_detail", kwargs={"pk": 999999})
        resp = client_logged_in.get(url)
        assert resp.status_code == 404

    def test_problem_detail_success(self, client_logged_in, test_problem):
        """Test that existing problem loads."""
        url = reverse("problem_detail", kwargs={"pk": test_problem.pk})
        resp = client_logged_in.get(url)
        assert resp.status_code == 200


class TestAuthenticationRequired:
    """Tests for views that require authentication."""

    def test_patient_list_requires_login(self, client):
        """Test that patient list requires login."""
        url = reverse("patient_list")
        resp = client.get(url)
        assert resp.status_code == 302
        assert "/login/" in resp.url

    def test_patient_detail_requires_login(self, client):
        """Test that patient detail requires login."""
        url = reverse("patient_detail", kwargs={"pk": 1, "slug": "test"})
        resp = client.get(url)
        assert resp.status_code == 302
        assert "/login/" in resp.url

    def test_problem_list_requires_login(self, client):
        """Test that problem list requires login."""
        url = reverse("problem_list", kwargs={"pk": 1})
        resp = client.get(url)
        assert resp.status_code == 302
        assert "/login/" in resp.url


class TestPatientCRUD:
    """Tests for Patient CRUD operations."""

    def test_patient_create_success(self, client_logged_in):
        """Test that patient creation works."""
        url = reverse("patient_add")
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
        }
        resp = client_logged_in.post(url, data)
        assert resp.status_code == 302
        assert Patient.objects.filter(first_name="Jane").exists()

    def test_patient_update_success(self, client_logged_in, test_patient):
        """Test that patient update works."""
        url = reverse("patient_change", kwargs={"pk": test_patient.pk})
        data = {
            "first_name": "Jane Updated",
            "last_name": test_patient.last_name,
        }
        resp = client_logged_in.post(url, data)
        assert resp.status_code == 302
        test_patient.refresh_from_db()
        assert test_patient.first_name == "Jane Updated"

    def test_patient_delete_success(self, client_logged_in, test_patient):
        """Test that patient delete works."""
        url = reverse("patient_delete", kwargs={"pk": test_patient.pk})
        resp = client_logged_in.post(url)
        assert resp.status_code == 302
        assert not Patient.objects.filter(pk=test_patient.pk).exists()


class TestProblemCRUD:
    """Tests for Problem CRUD operations."""

    def test_problem_create_success(self, client_logged_in, test_patient):
        """Test that problem creation works."""
        url = reverse("problem_add", kwargs={"pk": test_patient.pk})
        data = {
            "patient": test_patient.pk,
            "order_number": 1,
            "wording": "New medical issue",
            "subjetive": "Patient reports symptoms",
            "objetive": "Clinical findings",
            "closed": False,
        }
        resp = client_logged_in.post(url, data)
        assert resp.status_code == 302
        assert Problem.objects.filter(wording="New medical issue").exists()

    def test_problem_update_success(self, client_logged_in, test_problem):
        """Test that problem update works."""
        url = reverse("problem_change", kwargs={"pk": test_problem.pk})
        data = {
            "patient": test_problem.patient.pk,
            "order_number": test_problem.order_number,
            "wording": "Updated medical issue",
            "subjetive": "Updated subjective",
            "objetive": "Updated objective",
            "closed": False,
        }
        resp = client_logged_in.post(url, data)
        assert resp.status_code == 302
        test_problem.refresh_from_db()
        assert test_problem.wording == "Updated medical issue"

    def test_problem_delete_success(self, client_logged_in, test_problem):
        """Test that problem delete works."""
        url = reverse("problem_delete", kwargs={"pk": test_problem.pk})
        resp = client_logged_in.post(url)
        assert resp.status_code == 302
        assert not Problem.objects.filter(pk=test_problem.pk).exists()
