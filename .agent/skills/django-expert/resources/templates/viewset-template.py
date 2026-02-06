"""
Django REST Framework ViewSet Template
========================================

This template provides a production-ready ViewSet following Django Expert best practices:
- Optimized querysets with select_related/prefetch_related
- @permission_classes decorator at class and method level
- drf-spectacular schema documentation
- Atomic transactions for write operations
- Type hints and comprehensive docstrings

Usage:
    1. Copy this template to your app's views.py
    2. Replace {Model}, {Serializer}, and {Permission} placeholders
    3. Customize queryset optimization based on your model relationships
    4. Set default permissions using @permission_classes class decorator
    5. Override specific actions with @permission_classes method decorator if needed
    6. Add custom actions as needed
"""

from typing import Any

from django.db import transaction
from django.db.models import QuerySet, Prefetch
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

# Replace with your actual imports
# from .models import YourModel
# from .serializers import YourSerializer, YourDetailSerializer
# from .permissions import YourObjectPermission, IsOwnerOrReadOnly


@permission_classes([IsAuthenticated])  # Default permissions for all actions in this ViewSet
class OptimizedModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for {Model} with optimized queries and comprehensive documentation.
    
    This ViewSet implements:
    - N+1 query prevention via select_related/prefetch_related
    - Class-level @permission_classes decorator for default permissions
    - Method-level @permission_classes decorator for action-specific overrides
    - OpenAPI schema documentation
    - Atomic write operations
    
    Permission Pattern:
    - Class decorator @permission_classes([...]) defines default for all actions
    - Method decorator @permission_classes([...]) overrides default for specific actions
    - Example: Public read access, authenticated write access
    """
    
    # Replace with your serializer
    serializer_class = None  # YourSerializer
    
    # Pagination and filtering
    filterset_fields = ['field1', 'field2']  # Customize
    search_fields = ['name', 'description']  # Customize
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self) -> QuerySet:
        """
        Optimized queryset with intelligent prefetching.
        
        CRITICAL: Always use select_related for ForeignKey/OneToOne
        and prefetch_related for ManyToMany/reverse ForeignKey.
        
        Returns:
            QuerySet: Optimized queryset for the current action
        """
        queryset = self.get_base_queryset()
        
        # Optimize based on action
        if self.action == 'list':
            # List view: minimal data
            queryset = queryset.select_related(
                'foreign_key_relation',  # Replace with actual ForeignKey fields
            ).prefetch_related(
                'many_to_many_relation',  # Replace with actual M2M fields
            )
        elif self.action == 'retrieve':
            # Detail view: full data with nested prefetches
            queryset = queryset.select_related(
                'foreign_key_relation',
                'foreign_key_relation__nested_relation',  # Nested optimization
            ).prefetch_related(
                Prefetch(
                    'reverse_foreign_key_set',
                    queryset=None,  # Replace with filtered queryset if needed
                ),
                'many_to_many_relation__related_field',
            )
        
        return queryset
    
    def get_base_queryset(self) -> QuerySet:
        """
        Base queryset with user-specific filtering.
        
        Override this method for custom filtering logic.
        """
        # Replace YourModel with your actual model
        # return YourModel.objects.filter(user=self.request.user)
        raise NotImplementedError("Replace with your model's queryset")
    
    @extend_schema(
        summary="List all {Model} instances",
        description="Returns a paginated list of {Model} instances accessible to the current user.",
        responses={
            status.HTTP_200_OK: None,  # Replace with YourSerializer(many=True)
        }
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        List endpoint with schema documentation.
        
        Uses default permission_classes from class attribute.
        """
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Retrieve a {Model} instance",
        description="Returns detailed information about a specific {Model} instance.",
        responses={
            status.HTTP_200_OK: None,  # Replace with YourDetailSerializer
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Object not found"),
        }
    )
    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Retrieve endpoint with schema documentation.
        
        Uses default permission_classes from class attribute.
        """
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create a new {Model}",
        description="Creates a new {Model} instance. Uses atomic transaction.",
        responses={
            status.HTTP_201_CREATED: None,  # Replace with YourSerializer
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Validation error"),
        }
    )
    @transaction.atomic
    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Create endpoint with atomic transaction.
        
        CRITICAL: All write operations must be atomic to prevent partial updates.
        Uses default permission_classes from class attribute.
        """
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update a {Model}",
        description="Updates an existing {Model} instance. Uses atomic transaction.",
        responses={
            status.HTTP_200_OK: None,  # Replace with YourSerializer
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Validation error"),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Object not found"),
        }
    )
    @transaction.atomic
    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Update endpoint with atomic transaction.
        
        Uses default permission_classes from class attribute.
        """
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Partially update a {Model}",
        description="Partially updates a {Model} instance. Uses atomic transaction.",
        responses={
            status.HTTP_200_OK: None,  # Replace with YourSerializer
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Validation error"),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Object not found"),
        }
    )
    @transaction.atomic
    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Partial update endpoint with atomic transaction.
        
        Uses default permission_classes from class attribute.
        """
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Delete a {Model}",
        description="Soft-deletes a {Model} instance (if applicable).",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description="Successfully deleted"),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Object not found"),
        }
    )
    @transaction.atomic
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Destroy endpoint with atomic transaction.
        
        Uses default permission_classes from class attribute.
        
        Consider implementing soft-delete pattern:
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=['is_active'])
        return Response(status=status.HTTP_204_NO_CONTENT)
        """
        return super().destroy(request, *args, **kwargs)
    
    @extend_schema(
        summary="Custom action example",
        description="Example of a custom action with proper documentation.",
        parameters=[
            OpenApiParameter(
                name='param1',
                description='Example parameter',
                required=True,
                type=str,
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(description="Action completed successfully"),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Invalid parameters"),
        }
    )
    @action(detail=True, methods=['post'], url_path='custom-action')
    @permission_classes([IsAuthenticated])  # EXAMPLE: Override class permissions for this action
    @transaction.atomic
    def custom_action(self, request: Request, pk: Any = None) -> Response:
        """
        Example custom action.
        
        CRITICAL: Custom actions should:
        1. Be atomic if they modify data
        2. Have proper OpenAPI documentation
        3. Use @permission_classes decorator to override class permissions if needed
        4. Validate input parameters
        5. Use optimized queries
        
        NOTE: This action uses @permission_classes decorator to override the default
        class-level permissions. Remove the decorator to use class defaults.
        
        Returns:
            Response with custom data
        """
        instance = self.get_object()
        
        # Your custom logic here
        # Example: instance.perform_action(request.data.get('param1'))
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
