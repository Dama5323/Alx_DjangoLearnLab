## API Endpoints Documentation

### Book Endpoints

#### List Books
- **URL**: `/api/books/`
- **Method**: `GET`
- **Permissions**: Public
- **Filters**:
  - `publication_year`: Filter by publication year
  - `author`: Filter by author ID

#### Create Book
- **URL**: `/api/books/create/`
- **Method**: `POST`
- **Permissions**: Authenticated users only
- **Fields**:
  - `title` (required)
  - `publication_year` (required, must not be future)
  - `author` (required, existing author ID)

#### Retrieve Book
- **URL**: `/api/books/<id>/`
- **Method**: `GET`
- **Permissions**: Public

#### Update Book
- **URL**: `/api/books/<id>/update/`
- **Method**: `PUT/PATCH`
- **Permissions**: Only the creator can update
- **Fields**: Same as create, all optional for PATCH

#### Delete Book
- **URL**: `/api/books/<id>/delete/`
- **Method**: `DELETE`
- **Permissions**: Only the creator can delete