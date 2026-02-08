import pytest
from django.urls import reverse

from medical.models import History, Patient


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


class TestPatientListView:
    """Tests for PatientListView."""

    def test_patient_list_requires_login(self, client):
        """Test that list requires login."""
        url = reverse("patient_list")
        resp = client.get(url)
        assert resp.status_code == 302
        assert "/login/" in resp.url

    def test_patient_list_success(self, client_logged_in, test_patient):
        """Test that list loads for authenticated user."""
        url = reverse("patient_list")
        resp = client_logged_in.get(url)
        assert resp.status_code == 200


class TestPatientCreateView:
    """Tests for PatientCreateView."""

    def test_create_patient_success(self, client_logged_in):
        """Test successful patient creation."""
        url = reverse("patient_add")
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
        }
        resp = client_logged_in.post(url, data)
        assert resp.status_code == 302
        assert Patient.objects.filter(first_name="Jane").exists()


class TestProblemViews:
    """Tests for Problem views."""

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

    def test_create_problem_success(self, client_logged_in, test_patient):
        """Test successful problem creation."""
        url = reverse("problem_add", kwargs={"pk": test_patient.pk})
        data = {
            "patient": test_patient.pk,
            "order_number": 1,
            "wording": "New medical issue",
            "subjetive": "Patient reports headache",
            "objetive": "Normal vital signs",
            "closed": False,
        }
        resp = client_logged_in.post(url, data)
        assert resp.status_code == 302


class TestHistoryViews:
    """Tests for History views."""

    def test_history_antecedents_detail_404(self, client_logged_in):
        """Test that non-existent patient returns 404."""
        url = reverse("patient_history_antecedents", kwargs={"pk": 999999})
        resp = client_logged_in.get(url)
        assert resp.status_code == 404

    @pytest.mark.django_db(transaction=True)
    def test_history_antecedents_success(self, client_logged_in):
        """Test that patient with history loads."""
        from medical.models import History, Patient

        patient = Patient.objects.create(first_name="John", last_name="Doe", gender="M")
        History.objects.create(patient=patient, medical_intolerance="Penicillin")
        url = reverse("patient_history_antecedents", kwargs={"pk": patient.pk})
        resp = client_logged_in.get(url)
        assert resp.status_code == 302

    def test_history_antecedents_no_history(self, client_logged_in, test_patient):
        """Test that patient without history redirects to create page."""
        url = reverse("patient_history_antecedents", kwargs={"pk": test_patient.pk})
        resp = client_logged_in.get(url)
        assert resp.status_code == 302
        assert resp.url == reverse(
            "patient_history_antecedents_add", kwargs={"pk": test_patient.pk}
        )


class TestAuthenticationRequired:
    """Tests for authentication requirements."""

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

    def test_problem_list_requires_login(self, client):
        """Test that problem list requires login."""
        url = reverse("problem_list", kwargs={"pk": 1})
        resp = client.get(url)
        assert resp.status_code == 302
