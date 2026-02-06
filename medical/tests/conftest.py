# Copyright (c) 2012-2026 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Pytest fixtures shared across all tests."""

import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from medical.models import Patient, Problem


User = get_user_model()


@pytest.fixture(autouse=True)
def enable_db_access(db):
    """Enable database access for all tests."""
    pass


@pytest.fixture
def client_logged_in(client):
    """Provide a logged-in client for tests."""
    User.objects.create_user(
        username='testuser',
        password='testpass123'
    )
    client.login(username='testuser', password='testpass123')
    return client


@pytest.fixture
def test_patient(db):
    """Create a test patient."""
    return Patient.objects.create(
        first_name="John",
        last_name="Doe",
        gender="M"
    )


@pytest.fixture
def test_problem(db, test_patient):
    """Create a test problem associated with test_patient."""
    return Problem.objects.create(
        patient=test_patient,
        wording="Test medical problem",
        order_number=1
    )
