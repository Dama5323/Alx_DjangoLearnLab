from django.urls import path
from .views import BookListCreate
from .views import BookList

urlpatterns = [
    path('books/', BookListCreate.as_view(), name='book-list-create'),
    path('books/', BookList.as_view(), name='book-list'),
]