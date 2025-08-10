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

    
    path('books/update', BookUpdateView.as_view(), name='book-update'),
    path('books/delete', BookDeleteView.as_view(), name='book-delete'),

    path('books-alt/', BookListCreateView.as_view(), name='book-list-create'),

    # Author endpoints
    path('authors/', AuthorListCreateView.as_view(), name='author-list'),
]
