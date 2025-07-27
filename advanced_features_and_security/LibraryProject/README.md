# 📚 LibraryProject

## 0. Introduction to Django Development Environment Setup

### 🎯 Objective

Gain familiarity with Django by setting up a Django development environment and creating a basic Django project. This task introduces the standard Django workflow, including project creation and running the development server.

---

### 🧰 Prerequisites

- Python 3.x installed
- `pip` (Python package manager)
- Internet connection

---

### 🛠️ Setup Instructions

1. **Create a Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows

## Permissions and Groups Setup

- Custom permissions (`can_view`, `can_create`, `can_edit`, `can_delete`) are defined in the `Book` model.
- Groups created via admin:
  - **Viewers**: can_view
  - **Editors**: can_view, can_create, can_edit
  - **Admins**: All permissions
- Views are protected using `@permission_required('app_label.permission_codename')`.

# Security Measures Implemented

- `DEBUG = False` in production to hide sensitive information
- HTTPS enforced with `SECURE_SSL_REDIRECT` and HSTS headers
- CSRF protection with `{% csrf_token %}` in all forms
- SQL injection prevented using Django ORM (e.g., `filter(title__icontains=query)`)
- Cookies secured using `CSRF_COOKIE_SECURE` and `SESSION_COOKIE_SECURE`
- XSS and clickjacking prevented using browser headers (`X_FRAME_OPTIONS`, CSP)
- Content Security Policy applied via `django-csp`
