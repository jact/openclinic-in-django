# Copyright (c) 2012-2026 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Health check endpoints for container orchestration."""

from django.http import JsonResponse
from django.db import connection


def health_check(request):
    """Basic health check endpoint.

    Returns:
        JsonResponse: Health status with database connectivity.
    """
    db_status = "healthy"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:
        db_status = "unhealthy"

    status = 200 if db_status == "healthy" else 503

    return JsonResponse({
        "status": "healthy" if status == 200 else "unhealthy",
        "database": db_status,
    }, status=status)


def readiness_check(request):
    """Readiness check endpoint.

    Returns:
        JsonResponse: Readiness status for Kubernetes/Container orchestration.
    """
    return JsonResponse({"ready": True})


def liveness_check(request):
    """Liveness check endpoint.

    Returns:
        JsonResponse: Liveness status for Kubernetes.
    """
    return JsonResponse({"alive": True})
