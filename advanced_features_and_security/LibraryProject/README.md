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

## settings.py
- Enforced HTTPS with `SECURE_SSL_REDIRECT`
- Enabled HSTS with `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, and `SECURE_HSTS_PRELOAD`
- Configured secure cookie settings: `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE`
- Added protection headers: `X_FRAME_OPTIONS`, `SECURE_CONTENT_TYPE_NOSNIFF`, `SECURE_BROWSER_XSS_FILTER`

## Deployment
- Configured Nginx for HTTPS with SSL certificate
- Added HTTP-to-HTTPS redirect
- Set HSTS and other secure headers

## Potential Improvements
- Use automated tools like [Mozilla Observatory](https://observatory.mozilla.org/) for security scanning.
- Implement Content Security Policy (CSP).
- Regularly rotate TLS certificates.


