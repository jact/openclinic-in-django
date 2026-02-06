
---
category: reference
audience: Developers needing model documentation
---

# Models Reference

## Model Overview

OpenClinic uses 5 core models to manage medical records data.

---

## Patient Model

```python
class Patient(TimeStampedModel):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    last_name_optional = models.CharField(max_length=30, null=True, blank=True)
    
    address = models.TextField(null=True, blank=True)
    phone_contact = models.TextField(null=True, blank=True)
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    race = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=50, null=True, blank=True)
    decease_date = models.DateField(null=True, blank=True)
    
    tin = models.CharField(max_length=20, null=True, blank=True)  # Tax ID
    ssn = models.CharField(max_length=30, null=True, blank=True)
    health_card_number = models.CharField(max_length=30, null=True, blank=True)
    
    family_situation = models.TextField(null=True, blank=True)
    labour_situation = models.TextField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    
    insurance_company = models.CharField(max_length=30, null=True, blank=True)
    doctor_assigned = models.ForeignKey('Staff', on_delete=models.SET_NULL, null=True)
    
    relatives = models.ManyToManyField('self', blank=True)
```

### Patient Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `age()` | float | Calculates patient age |
| `clean()` | None | Validates birth date before decease date |
| `gender_description()` | str | Returns gender in human-readable format |

### Patient Meta

```python
class Meta:
    ordering = ['last_name', 'last_name_optional', 'first_name']
    indexes = [
        models.Index(fields=['last_name', 'first_name']),
        models.Index(fields=['birth_date']),
        models.Index(fields=['tin']),
    ]
```

---

## Problem Model

```python
class Problem(TimeStampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    
    order_number = models.PositiveIntegerField()
    wording = models.TextField()
    
    meeting_place = models.CharField(max_length=50, null=True, blank=True)
    subjetive = models.TextField()
    objetive = models.TextField()
    appreciation = models.TextField()
    action_plan = models.TextField()
    prescription = models.TextField()
    
    closing_date = models.DateTimeField(null=True, blank=True)
    connection = models.ManyToManyField('self', blank=True, symmetrical=False)
```

### Custom Managers

```python
class OpenedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(closing_date__isnull=True)

class ClosedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(closing_date__isnull=False)

class Problem(TimeStampedModel):
    objects = models.Manager()  # Default manager
    opened = OpenedManager()     # Active problems
    closed = ClosedManager()     # Historical problems
```

### Problem Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_last_order_number()` | int | Gets highest order number for patient |

---

## History Model

```python
class History(TimeStampedModel):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    
    # Personal antecedents
    medical_intolerance = models.TextField(null=True, blank=True)
    birth_growth = models.TextField(null=True, blank=True)
    growth_sexuality = models.TextField(null=True, blank=True)
    feed = models.TextField(null=True, blank=True)
    habits = models.TextField(null=True, blank=True)
    peristaltic_conditions = models.TextField(null=True, blank=True)
    psychological = models.TextField(null=True, blank=True)
    children_complaint = models.TextField(null=True, blank=True)
    venereal_disease = models.TextField(null=True, blank=True)
    accident_surgical_operation = models.TextField(null=True, blank=True)
    mental_illness = models.TextField(null=True, blank=True)
    
    # Family antecedents
    parents_status_health = models.TextField(null=True, blank=True)
    brothers_status_health = models.TextField(null=True, blank=True)
    spouse_childs_status_health = models.TextField(null=True, blank=True)
    family_illness = models.TextField(null=True, blank=True)
```

---

## Test Model

```python
class Test(TimeStampedModel):
    document_type = models.CharField(max_length=128, null=True, blank=True)
    document = models.FileField(upload_to='medical_tests/%Y/%m/%d')
    
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
```

### Test Signals

```python
@receiver(pre_delete, sender=Test)
def test_delete(sender, instance, **kwargs):
    instance.document.delete(False)  # Delete file on model delete
```

---

## Staff Model

```python
class Staff(AbstractUser):
    collegiate_number = models.CharField(max_length=20, blank=True)
    specialty = models.CharField(max_length=50, blank=True)
```

---

## TimeStampedModel (Abstract Base)

All models inherit from this base:

```python
class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
```
