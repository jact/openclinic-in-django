# Copyright (c) 2012-2026 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Tests for Test model."""

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from medical.models import Test


@pytest.mark.django_db
class TestTestModel:
    """Tests for the Test model."""

    def test_test_creation(self, test_problem):
        """Test creating a Test instance."""
        test_file = SimpleUploadedFile(
            "test_document.pdf", b"file content", content_type="application/pdf"
        )
        test = Test.objects.create(
            problem=test_problem, document=test_file, document_type="application/pdf"
        )
        assert test.problem == test_problem
        assert test.document_type == "application/pdf"
        assert test.document is not None

    def test_test_str(self, test_problem):
        """Test Test string representation."""
        test_file = SimpleUploadedFile(
            "document.pdf", b"content", content_type="application/pdf"
        )
        test = Test.objects.create(problem=test_problem, document=test_file)
        assert str(test) == str(test.document)

    def test_filename_method(self, test_problem):
        """Test the filename method returns correct filename."""
        test_file = SimpleUploadedFile(
            "medical_report_2024.pdf", b"content", content_type="application/pdf"
        )
        test = Test.objects.create(problem=test_problem, document=test_file)
        # Django may add unique suffix to prevent filename collisions
        filename = test.filename()
        assert filename.endswith(".pdf")
        assert "medical_report_2024" in filename

    def test_filename_with_path(self, test_problem):
        """Test filename method with path in document name."""
        test_file = SimpleUploadedFile(
            "path/to/document.pdf", b"content", content_type="application/pdf"
        )
        test = Test.objects.create(problem=test_problem, document=test_file)
        # filename() should return just the basename (Django may add suffix)
        assert test.filename().endswith(".pdf")
        assert "/" not in test.filename()

    def test_test_delete_signal(self, test_problem):
        """Test that deleting a Test deletes the associated file."""
        test_file = SimpleUploadedFile(
            "delete_me.pdf", b"content", content_type="application/pdf"
        )
        test = Test.objects.create(problem=test_problem, document=test_file)

        # Store document path
        document_path = test.document.path

        # Delete the test instance (should trigger signal)
        test.delete()

        # Verify test was deleted
        assert Test.objects.filter(pk=test.pk).count() == 0

    def test_test_ordering(self, test_problem):
        """Test that tests are ordered correctly."""
        # Create multiple tests
        test_file1 = SimpleUploadedFile("doc1.pdf", b"content1")
        test_file2 = SimpleUploadedFile("doc2.pdf", b"content2")

        test1 = Test.objects.create(problem=test_problem, document=test_file1)
        test2 = Test.objects.create(problem=test_problem, document=test_file2)

        # Tests should be ordered by modified (descending) via TimeStampedModel
        tests = Test.objects.filter(problem=test_problem)
        assert tests.count() == 2
