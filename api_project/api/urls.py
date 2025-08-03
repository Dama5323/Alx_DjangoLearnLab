from django.urls import path
from .views import BookListCreate
from .views import BookList
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('books/', BookListCreate.as_view(), name='book-list-create'),
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
]