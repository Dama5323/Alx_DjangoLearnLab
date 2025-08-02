from django.urls import path
from .views import BookListCreate

urlpatterns = [
    path('books/', BookListCreate.as_view(), name='book-list-create'),
]