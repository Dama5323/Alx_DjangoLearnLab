from django.db import models

class Author(models.Model):
    """
    Represents an author who writes books.
    Fields:
        name (CharField): The name of the author (max 100 characters)
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Represents a book written by an author.
    Fields:
        title (CharField): The title of the book (max 200 characters)
        publication_year (IntegerField): The year the book was published
        author (ForeignKey): Reference to the Author who wrote this book
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

    class Meta:
        # Ensure each author doesn't have multiple books with the same title
        unique_together = ['author', 'title']