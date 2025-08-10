from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Handles serialization of all Book fields and includes custom validation
    for the publication_year field to ensure it's not in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Validate that the publication year is not in the future.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Includes a nested representation of the author's books using BookSerializer.
    The books field is read-only as it's dynamically generated from the relationship.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']