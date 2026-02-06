# Migasfree-Specific Django Patterns

This folder contains code examples specific to the migasfree project, demonstrating advanced Django/DRF patterns in the context of a software deployment management system.

## Included Examples

### 📦 `package_viewset.py`

Complete ViewSet for software package management with:

- **Multi-tenant query optimization**: Filtering by project/organization
- **Complex relationships**: M2M with deployments, self-referential with dependencies
- **Custom actions**: Deployment statistics, mark as obsolete
- **Advanced Prefetch pattern**: Nested prefetches with filtered querysets

**Key concepts demonstrated**:

- `Prefetch()` with custom `queryset` to minimize data transfer
- `annotate()` to avoid additional queries in serializers
- Business rule validation before atomic operations
- Multi-tenant filtering in base queryset

### 🎯 Reusable Patterns

The following patterns are applicable to any migasfree ViewSet:

#### 1. **Action-Based Optimization**

```python
def get_queryset(self):
    if self.action == 'list':
        # Minimal data with aggregations
        return queryset.select_related(...).annotate(count=Count(...))
    elif self.action == 'retrieve':
        # Full data with nested prefetches
        return queryset.prefetch_related(Prefetch(...))
```

#### 2. **Prefetch with Filtering**

```python
Prefetch(
    'related_set',
    queryset=RelatedModel.objects.filter(active=True).select_related('nested'),
    to_attr='active_items'  # Direct access without additional query
)
```

#### 3. **Atomic Actions with Validation**

```python
@transaction.atomic
def custom_action(self, request, pk=None):
    obj = self.get_object()
    # 1. Validate business rules BEFORE modifying
    if not self.validate_business_rules(obj):
        return Response({'error': '...'}, status=400)
    # 2. Modify
    obj.field = value
    obj.save(update_fields=['field'])
    # 3. Record history
    History.objects.create(...)
```

## Usage in Prompts

When requesting code generation for migasfree, the AI agent should:

1. **Reference these patterns** as base examples
2. **Adapt optimization** according to the specific model's relationships
3. **Maintain the style** of documentation and type hints

## Next Examples to Add

- [ ] `deployment_viewset.py`: Deployment management with dynamic attributes
- [ ] `computer_viewset.py`: Client management with synchronization
- [ ] `serializer_patterns.py`: Serializer patterns with complex validation
- [ ] `permission_patterns.py`: Multi-tenant object-level permissions
