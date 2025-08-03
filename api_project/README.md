# Django REST Framework API Documentation

## 📌 Authentication

### 1. **Obtain an API Token**
Send a `POST` request to obtain a token:

**Endpoint**:

POST /api-token-auth/
**Request Body**:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Successful Response (200 OK):**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### 2. Using the Token
Include the token in the Authorization header for protected endpoints:
Authorization: Token yourtoken12345

**Permissions**
| Endpoint            | HTTP Method | Permission Required       | Description                  |
|---------------------|-------------|---------------------------|------------------------------|
| `/api/books/`       | GET         | `IsAuthenticated`         | List all books               |
| `/api/books/`       | POST        | `IsAuthenticated`         | Create new book              |
| `/api/books/{id}/`  | GET         | `IsAuthenticated`         | Retrieve single book         |
| `/api/books/{id}/`  | PUT/PATCH   | `IsAdminUser` or `IsOwner`| Update book details          |
| `/api/books/{id}/`  | DELETE      | `IsAdminUser` or `IsOwner`| Delete a book                |


###  Setup Instructions
1. **Install dependencies:**
``` bash
pip install -r requirements.txt
```

2. **Apply migrations:**
```bash
python manage.py migrate
```

3. **Create a superuser (for admin access):**
```bash
python manage.py createsuperuser
```

4. **Generate a token for your user:**
```bash
python manage.py drf_create_token your_username
```

