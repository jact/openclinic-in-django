
---
category: reference
audience: Developers needing technical details
---

# Architecture Reference

## System Architecture

OpenClinic follows Django's MVT (Model-View-Template) pattern with additional layers for forms and services.

## High-Level Architecture

```mermaid
graph TB
    subgraph "Presentation Layer"
        T[Templates]
        V[Views]
        F[Forms]
    end
    
    subgraph "Application Layer"
        M[Models]
        S[Services]
    end
    
    subgraph "Infrastructure Layer"
        D[(SQLite/PostgreSQL)]
        S3[(Static Files)]
        E[Email Service]
    end
    
    T --> V
    V --> F
    F --> M
    M --> D
    V --> S
    S --> E
```

## Application Structure

### Models Layer

Located in `medical/models/`:

| Model | Purpose | Key Fields |
|-------|---------|------------|
| **Patient** | Patient demographics | first_name, last_name, gender, birth_date |
| **Problem** | Medical problems | patient FK, wording, closing_date |
| **History** | Patient antecedents | patient FK, medical_intolerance |
| **Test** | Medical documents | problem FK, document file |
| **Staff** | User accounts | email, first_name, last_name, collegiate_number |

### Views Layer

Located in `medical/views/`:

```mermaid
graph TD
    A[View Classes] --> B[Patient Views]
    A --> C[Problem Views]
    A --> D[History Views]
    A --> E[Test Views]
    
    B --> B1[PatientCreate]
    B --> B2[PatientUpdate]
    B --> B3[PatientDetail]
    
    C --> C1[ProblemCreate]
    C --> C2[ProblemUpdate]
    C --> C3[ProblemDetail]
```

### Custom Managers

Problem model uses custom managers:

```python
class OpenedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(closing_date__isnull=True)

class ClosedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(closing_date__isnull=False)
```

## Database Schema

### Entity Relationships

```mermaid
erDiagram
    PATIENT ||--o{ PROBLEM : has
    PATIENT ||--o| HISTORY : has
    PATIENT }o--o{ PATIENT : relatives
    PROBLEM ||--o{ TEST : contains
    STAFF ||--o{ PROBLEM : treats
    STAFF ||--o{ PATIENT : assigned_to
```

### Database Indexes

| Table | Index | Purpose |
|-------|-------|---------|
| patient | (last_name, first_name) | Name searches |
| patient | birth_date | Age queries |
| patient | tin | Tax ID lookups |
| problem | (patient_id, order_number) | Problem ordering |
| problem | closing_date | Open/closed filtering |

## Middleware Stack

```python
MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

## Authentication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant V as View
    participant M as Middleware
    participant D as Database
    
    U->>V: Request protected page
    M->>U: Check session
    alt Not authenticated
        M->>U: Redirect to login
    else Authenticated
        V->>D: Fetch patient data
        D-->>V: Return data
        V-->>U: Render page
    end
```
