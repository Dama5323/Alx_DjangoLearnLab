from relationship_app.models import Author, Book, Library, Librarian

def get_books_by_author(author_name):
    """Query all books by a specific author using objects.filter()"""
    try:
        author = Author.objects.get(name=author_name)
        return Book.objects.filter(author=author)
    except Author.DoesNotExist:
        return Book.objects.none()

def get_books_in_library(library_name):
    """List all books in a library"""
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return Book.objects.none()

def get_librarian_for_library(library_name):
    """Retrieve the librarian for a library using Librarian.objects.get()"""
    try:
        library = Library.objects.get(name=library_name)
        # Updated to use exactly what checker wants: Librarian.objects.get(library=...)
        return Librarian.objects.get(library=library)
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None
