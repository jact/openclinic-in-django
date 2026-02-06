"""
Migasfree-Specific Package ViewSet Example
===========================================

Real-world example of a ViewSet for managing software packages in migasfree,
demonstrating:
- Complex queryset optimization for deployment/package relationships
- Multi-tenant filtering (by project/organization)
- Custom actions for package operations
- Proper permission handling
"""

from typing import Any

from django.db import transaction
from django.db.models import QuerySet, Prefetch, Count, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse


@permission_classes([IsAuthenticated])  # Default permissions for all Package operations
class PackageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing migasfree Packages.
    
    Handles package CRUD operations with optimized queries for:
    - Package deployments (M2M relationship)
    - Package dependencies (self-referential M2M)
    - Store and project associations
    - Computer installations (reverse FK)
    """
    
    filterset_fields = ['project', 'store', 'name']
    search_fields = ['name', 'fullname', 'version']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self) -> QuerySet:
        """
        Optimized queryset based on action and user permissions.
        
        CRITICAL OPTIMIZATION PATTERNS:
        1. select_related for 'project' and 'store' (ForeignKey)
        2. prefetch_related for deployments (M2M)
        3. Prefetch with filtered queryset to minimize data transfer
        4. Annotate counts to avoid separate queries in serializers
        """
        # Base queryset filtered by user's project scope
        queryset = Package.objects.filter(
            project__in=self.request.user.get_accessible_projects()
        )
        
        if self.action == 'list':
            # List view: minimal data with counts
            queryset = queryset.select_related(
                'project',
                'store',
            ).prefetch_related(
                # Only prefetch deployment names for list view
                Prefetch(
                    'deployment_set',
                    queryset=Deployment.objects.only('id', 'name').order_by('name'),
                    to_attr='deployments_list'
                ),
            ).annotate(
                deployments_count=Count('deployment_set', distinct=True),
                installations_count=Count('computer_set', distinct=True),
            )
            
        elif self.action == 'retrieve':
            # Detail view: full data with nested relationships
            queryset = queryset.select_related(
                'project',
                'project__platform',  # Nested optimization
                'store',
                'store__project',
            ).prefetch_related(
                # Full deployment data with their attributes
                Prefetch(
                    'deployment_set',
                    queryset=Deployment.objects.select_related('project').prefetch_related(
                        'packages',
                        'attributes'
                    ).order_by('name'),
                ),
                # Package dependencies (self-referential M2M)
                Prefetch(
                    'depends_on',
                    queryset=Package.objects.only('id', 'name', 'version'),
                ),
                # Recent installations
                Prefetch(
                    'computer_set',
                    queryset=Computer.objects.select_related('project', 'user').order_by('-sync_date')[:100],
                    to_attr='recent_installations'
                ),
            ).annotate(
                deployments_count=Count('deployment_set', distinct=True),
                installations_count=Count('computer_set', distinct=True),
            )
        
        return queryset
    
    @extend_schema(
        summary="Get package deployment statistics",
        description="Returns statistics about package deployments and installations across projects.",
        parameters=[
            OpenApiParameter(
                name='date_from',
                description='Start date for statistics (YYYY-MM-DD)',
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name='date_to',
                description='End date for statistics (YYYY-MM-DD)',
                required=False,
                type=str,
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(description="Statistics data"),
        }
    )
    @action(detail=True, methods=['get'], url_path='deployment-stats')
    def deployment_stats(self, request: Request, pk: Any = None) -> Response:
        """
        Custom action: Get deployment statistics for a package.
        
        OPTIMIZATION: Uses a single aggregate query instead of multiple DB hits.
        """
        package = self.get_object()
        
        # Get date filters
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        # Build filters
        filters = Q(deployment__packages=package)
        if date_from:
            filters &= Q(created_at__gte=date_from)
        if date_to:
            filters &= Q(created_at__lte=date_to)
        
        # Single optimized query with aggregation
        stats = Computer.objects.filter(filters).select_related(
            'project'
        ).values('project__name').annotate(
            count=Count('id', distinct=True)
        ).order_by('-count')
        
        return Response({
            'package': package.name,
            'version': package.version,
            'deployments_by_project': list(stats),
            'total_installations': sum(s['count'] for s in stats),
        })
    
    @extend_schema(
        summary="Mark package as obsolete",
        description="Marks a package as obsolete and removes it from active deployments.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(description="Package marked as obsolete"),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Cannot obsolete: package has active deployments"),
        }
    )
    @action(detail=True, methods=['post'], url_path='mark-obsolete')
    @transaction.atomic
    def mark_obsolete(self, request: Request, pk: Any = None) -> Response:
        """
        Mark package as obsolete (atomic operation).
        
        CRITICAL PATTERN:
        1. Check business rules before modification
        2. Use atomic transaction
        3. Update related objects in bulk when possible
        """
        package = self.get_object()
        
        # Business rule: Cannot obsolete if in active deployments
        active_deployments = package.deployment_set.filter(
            enabled=True
        ).select_related('project').only('id', 'name', 'project__name')
        
        if active_deployments.exists():
            deployment_names = [
                f"{d.project.name}/{d.name}" 
                for d in active_deployments[:5]
            ]
            return Response(
                {
                    'error': 'Cannot mark as obsolete: package is in active deployments',
                    'active_deployments': deployment_names,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mark as obsolete
        package.is_obsolete = True
        package.save(update_fields=['is_obsolete'])
        
        # Log the action
        PackageHistory.objects.create(
            package=package,
            action='marked_obsolete',
            user=request.user,
        )
        
        return Response({
            'message': f'Package {package.name} marked as obsolete',
            'package_id': package.id,
        })


# Mock models for reference (not executable)
# In a real migasfree implementation, these would be in models.py
class Package:
    """Package model placeholder for reference."""
    pass


class Deployment:
    """Deployment model placeholder for reference."""
    pass


class Computer:
    """Computer model placeholder for reference."""
    pass


class PackageHistory:
    """PackageHistory model placeholder for reference."""
    pass
