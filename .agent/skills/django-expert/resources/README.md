# Django Expert Resources

This directory contains reusable resources for the Django Expert skill, including templates, examples, and validation tools.

## 📁 Directory Structure

```text
resources/
├── templates/          # Reusable code templates
├── examples/           # Working examples organized by context
│   └── migasfree-patterns/  # Patterns specific to migasfree
└── scripts/            # Validation and helper scripts
```

---

## 📝 Templates

### `viewset-template.py`

Production-ready Django REST Framework ViewSet template following all Django Expert best practices:

**Features**:

- ✅ Optimized querysets with `select_related`/`prefetch_related`
- ✅ Action-based optimization (list vs retrieve)
- ✅ Proper permission classes and object-level permissions
- ✅ `drf-spectacular` schema documentation
- ✅ Atomic transactions for write operations
- ✅ Full type hints and comprehensive docstrings

**Usage**:

```bash
cp resources/templates/viewset-template.py your_app/views/my_viewset.py
# Replace {Model}, {Serializer}, {Permission} placeholders
```

---

## 💡 Examples

### Migasfree Patterns (`examples/migasfree-patterns/`)

Real-world examples from the migasfree project demonstrating advanced Django patterns.

#### `package_viewset.py`

Complete ViewSet for managing software packages in migasfree showing:

- Complex multi-tenant filtering (by project/organization)
- Nested relationship optimization (deployments, dependencies)
- Custom actions (deployment stats, mark obsolete)
- Business rule validation in atomic transactions

**Key Patterns Demonstrated**:

- `Prefetch()` with custom querysets to minimize data transfer
- `annotate()` to avoid N+1 in serializers
- Multi-level `select_related()` for nested ForeignKeys
- Conditional queryset optimization based on action

**Reusable Concepts**:

```python
# Pattern: Action-based optimization
if self.action == 'list':
    queryset = queryset.select_related('fk').annotate(count=Count('m2m'))
elif self.action == 'retrieve':
    queryset = queryset.prefetch_related(Prefetch('m2m', queryset=...))

# Pattern: Atomic action with validation
@transaction.atomic
def custom_action(self, request, pk=None):
    obj = self.get_object()
    if not self.validate_business_rules(obj):
        return Response({'error': '...'}, status=400)
    obj.modify()
    History.objects.create(...)
```

---

## 🛠️ Scripts

### `check_queryset_optimization.py`

Static analysis tool to detect N+1 query patterns and missing optimizations in Django code.

**Features**:

- 🔍 AST-based analysis (no code execution required)
- 🚨 Detects missing `select_related`/`prefetch_related` in `get_queryset()`
- 🔄 Identifies potential N+1 queries inside loops
- ⚠️ Warns about missing action-based optimization
- 📊 Severity levels: critical, warning, info

**Usage**:

```bash
# Check a single file
python resources/scripts/check_queryset_optimization.py views.py

# Check entire app directory
python resources/scripts/check_queryset_optimization.py --check-all ./myapp/

# JSON output for CI/CD integration
python resources/scripts/check_queryset_optimization.py --json views.py
```

**Example Output**:

```text
🔴 [CRITICAL] myapp/views.py:45
   PackageViewSet.get_queryset() lacks select_related/prefetch_related optimization

   Code:
     44 | def get_queryset(self):
     45 |     return Package.objects.filter(project=self.request.user.project)
     46 |

🟡 [WARNING] myapp/views.py:112
   Potential N+1 query: accessing 'deployment_set' inside loop in list()
```

**Integration in Workflow**:
Add to your CI/CD pipeline or pre-commit hooks:

```yaml
# .github/workflows/django-quality.yml
- name: Check QuerySet Optimization
  run: python skills/frameworks/django-expert/resources/scripts/check_queryset_optimization.py --check-all ./backend/
```

---

## 🎯 How to Use These Resources

### For Developers

1. **Start with templates**: Copy `viewset-template.py` as your base for new ViewSets
2. **Reference examples**: Check `migasfree-patterns/` for real-world patterns
3. **Validate your code**: Run `check_queryset_optimization.py` before committing

### For AI Agents

When generating Django code:

1. **Reference templates** for structure and best practices
2. **Adapt patterns** from migasfree examples to the specific domain
3. **Recommend validation** using the optimization checker script

---

## 📚 Next Steps

**Planned Additions**:

- [ ] `serializer-template.py`: Template for DRF serializers with validation
- [ ] `deployment_viewset.py`: Example with dynamic attributes (JSONField)
- [ ] `manager-template.py`: Custom QuerySet Manager template
- [ ] `permission-patterns.py`: Multi-tenant object-level permissions
- [ ] `check_transaction_usage.py`: Verify atomic decorators on write operations

**Contribution Guidelines**:

- All templates must be production-ready (no TODOs or placeholders)
- Examples must be runnable or clearly document why they're not (e.g., mock models)
- Scripts must include comprehensive docstrings and help text
- Follow Django Expert 6-Pillar Protocol for documentation
