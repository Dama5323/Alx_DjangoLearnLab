from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    BookListCreateView,
    AuthorListCreateView
)

urlpatterns = [
    # Book endpoints
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),  # Added update endpoint
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),  # Added delete endpoint
    
    # Alternative combined endpoint
    path('books-alt/', BookListCreateView.as_view(), name='book-list-create'),
    
    # Author endpoints
    path('authors/', AuthorListCreateView.as_view(), name='author-list'),
]