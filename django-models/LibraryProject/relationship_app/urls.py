from django.urls import path
from .views import list_books, LibraryDetailView  # Importing both views

urlpatterns = [
    path('books/', list_books, name='list-books'),  # Function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),  # Class-based view
]