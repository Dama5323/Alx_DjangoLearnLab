# Django Blog Project

## Initial Project Setup

### Features Implemented
- Django project and blog app configuration
- PostgreSQL database setup
- Post model with:
  - Title (CharField)
  - Content (TextField)
  - Published date (DateTimeField)
  - Author (ForeignKey to User)
- Static files structure (CSS/JS)
- Base templates with HTML5 boilerplate

### Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/django_blog
   ```

2. **Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure PostgreSQL:**

- Create database named django_blog

- Update settings in .env file:

```text
DB_NAME=django_blog
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

5. **Apply migrations:**
```bash
python manage.py migrate
```

6. **Create superuser:**
```bash
python manage.py createsuperuser
```

7. **Run development server:**
```bash
python manage.py runserver
```

### User Authentication System
**Features Implemented**

- User registration with:

    - Username

    - Email

    - Password validation

- Login/logout functionality

- Profile management:

    - Email updates

    - Bio field

- Protected views for authenticated users

- CSRF protection on all forms

### Authentication Endpoints

| URL Path    | Description                | Access          |
|-------------|----------------------------|-----------------|
| /register   | User registration          | Public          |
| /login      | User login                 | Public          |
| /logout     | User logout                | Authenticated   |
| /profile    | User profile management    | Authenticated   |

### Testing Authentication

1. **Registration Test:**
```bash
python manage.py test blog.tests.AuthTests.test_registration
```

2. **Login Test:**
```bash
python manage.py test blog.tests.AuthTests.test_login
```

3. **Profile Update Test:**
```bash
python manage.py test blog.tests.AuthTests.test_profile_update
```

4. **Run all tests:**
```bash
python manage.py test blog
```

### Troubleshooting
- If getting connection errors, verify PostgreSQL is running

- For migration issues, try:

```bash
python manage.py makemigrations
python manage.py migrate
```

- For static files not loading, run:

```bash
python manage.py collectstatic
```

## Blog Post Management

### Features
- View all posts (public)
- View post details (public)
- Create new posts (authenticated users)
- Edit posts (authors only)
- Delete posts (authors only)

### URL Endpoints
| URL Pattern | View | Access |
|-------------|------|--------|
| /posts/ | Post list | Public |
| /posts/new/ | Create post | Authenticated |
| /posts/<id>/ | Post details | Public |
| /posts/<id>/update/ | Edit post | Author only |
| /posts/<id>/delete/ | Delete post | Author only |