# Copyright (c) 2012-2026 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Medical views package.

This module provides backward compatibility by re-exporting all view classes
from the split view modules.
"""

# Import base utilities
from .base import logger

# History views
from .history_views import (
    HistoryAntecedentsCreate,
    HistoryAntecedentsDetail,
    HistoryAntecedentsUpdate,
)

# Patient views
from .patient_views import (
    PatientCreate,
    PatientDelete,
    PatientDetail,
    PatientList,
    PatientListView,
    PatientMedicalReport,
    PatientRedirectDetail,
    PatientRelatives,
    PatientSearch,
    PatientTests,
    PatientUpdate,
)

# Problem views
from .problem_views import (
    HistoryList,
    ProblemConnections,
    ProblemCreate,
    ProblemDelete,
    ProblemDetail,
    ProblemList,
    ProblemSearch,
    ProblemUpdate,
)

# Test views
from .test_views import (
    ProblemTestDelete,
    ProblemTests,
)

__all__ = [
    # Base
    "logger",
    # Patient views
    "PatientCreate",
    "PatientUpdate",
    "PatientDelete",
    "PatientList",
    "PatientListView",
    "PatientSearch",
    "PatientRedirectDetail",
    "PatientDetail",
    "PatientRelatives",
    "PatientMedicalReport",
    "PatientTests",
    # Problem views
    "ProblemCreate",
    "ProblemUpdate",
    "ProblemSearch",
    "ProblemList",
    "ProblemDetail",
    "ProblemDelete",
    "ProblemConnections",
    "HistoryList",
    # History views
    "HistoryAntecedentsDetail",
    "HistoryAntecedentsCreate",
    "HistoryAntecedentsUpdate",
    # Test views
    "ProblemTests",
    "ProblemTestDelete",
]
