# Create Book

```python
from bookshelf.models import Book

# Create a new book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Confirm it was created
book
```

### Output
```
<Book: 1984 by George Orwell (1949)>
```
