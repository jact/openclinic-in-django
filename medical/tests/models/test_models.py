import pytest
from django.core.exceptions import ValidationError
from datetime import date, timedelta

from medical.models import Patient, Problem, History, Test


@pytest.mark.django_db
class TestPatientModel:
    """Tests for Patient model."""
    
    def test_patient_creation(self):
        """Test basic patient creation."""
        patient = Patient.objects.create(
            first_name="John",
            last_name="Doe",
            last_name_optional="Smith"
        )
        assert patient.pk is not None
        assert str(patient) == "John Doe Smith"
    
    def test_patient_age_calculation(self):
        """Test age calculation with birth date."""
        birth_date = date.today() - timedelta(days=365*25)
        patient = Patient.objects.create(
            first_name="Jane",
            last_name="Doe",
            birth_date=birth_date
        )
        assert patient.age() > 24
        assert patient.age() < 26
    
    def test_patient_validation_birth_after_death(self):
        """Test validation fails when birth date is after death date."""
        patient = Patient(
            first_name="Invalid",
            last_name="Patient",
            birth_date=date(2020, 1, 1),
            decease_date=date(2019, 1, 1)
        )
        with pytest.raises(ValidationError):
            patient.clean()
    
    def test_patient_gender_description(self):
        """Test gender description mapping."""
        patient_male = Patient.objects.create(
            first_name="Male",
            last_name="Patient",
            gender='M'
        )
        patient_female = Patient.objects.create(
            first_name="Female",
            last_name="Patient",
            gender='F'
        )
        assert patient_male.gender_description() == "Male"
        assert patient_female.gender_description() == "Female"
    
    def test_patient_without_gender(self):
        """Test patient without gender returns None."""
        patient = Patient.objects.create(
            first_name="NoGender",
            last_name="Patient"
        )
        assert patient.gender_description() is None


@pytest.mark.django_db
class TestProblemModel:
    """Tests for Problem model."""
    
    def test_problem_creation(self):
        """Test basic problem creation."""
        patient = Patient.objects.create(first_name="John", last_name="Doe")
        problem = Problem.objects.create(
            patient=patient,
            wording="Test problem",
            order_number=1
        )
        assert problem.pk is not None
    
    def test_problem_opened_manager(self):
        """Test that opened problems are accessible via manager."""
        patient = Patient.objects.create(first_name="John", last_name="Doe")
        open_problem = Problem.objects.create(
            patient=patient,
            wording="Open problem",
            order_number=1,
            closing_date=None  # Open problem has no closing date
        )
        assert open_problem in Problem.opened.all()
        assert open_problem not in Problem.closed.all()
    
    def test_problem_closed_manager(self):
        """Test that closed problems are accessible via manager."""
        patient = Patient.objects.create(first_name="John", last_name="Doe")
        closed_problem = Problem.objects.create(
            patient=patient,
            wording="Closed problem",
            order_number=1,
            closing_date=date.today()  # Closed problem has closing date
        )
        assert closed_problem in Problem.closed.all()
        assert closed_problem not in Problem.opened.all()


@pytest.mark.django_db
class TestHistoryModel:
    """Tests for History model."""
    
    def test_history_creation(self):
        """Test basic history creation linked to patient."""
        patient = Patient.objects.create(first_name="John", last_name="Doe")
        history = History.objects.create(
            patient=patient,
            medical_intolerance="Penicillin"
        )
        assert history.pk is not None
        assert history.patient == patient
    
    def test_history_one_to_one_relation(self):
        """Test that history has one-to-one relation with patient."""
        patient = Patient.objects.create(first_name="John", last_name="Doe")
        History.objects.create(patient=patient)
        
        with pytest.raises(Exception):
            History.objects.create(patient=patient)
