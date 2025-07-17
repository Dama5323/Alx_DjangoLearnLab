# CRUD Operations for Book Model

---

## Create Book

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

---

## Retrieve Book

```python
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
```

### Output:
```
('1984', 'George Orwell', 1949)
```

---

## Update Book

```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book.title
```

### Output:
```
'Nineteen Eighty-Four'
```

---

## Delete Book

```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
```

### Output:
```
<QuerySet []>
```
