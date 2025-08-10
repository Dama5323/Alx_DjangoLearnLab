from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .permissions import IsCreatorOrReadOnly


class CustomAPIResponseMixin:
    """Mixin for custom API responses"""
    def create_response(self, serializer, status_code=status.HTTP_200_OK):
        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status_code)


class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookListView(generics.ListAPIView):
    """
    View to list all books (GET)
    Accessible to all users (authenticated or not)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['publication_year', 'author']
    # Consider adding pagination
    # pagination_class = PageNumberPagination


class BookDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a single book by ID (GET)
    Accessible to all users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(CustomAPIResponseMixin, generics.CreateAPIView):
    """
    View to create a new book (POST)
    Restricted to authenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return self.create_response(serializer, status.HTTP_201_CREATED, headers=headers)


class BookUpdateView(CustomAPIResponseMixin, generics.UpdateAPIView):
    """
    View to update an existing book (PUT/PATCH)
    Restricted to authenticated users who are the creators
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
            
        return self.create_response(serializer)


class BookDeleteView(generics.DestroyAPIView):
    """
    View to delete a book (DELETE)
    Restricted to authenticated users who are the creators
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': 'success',
            'message': 'Book deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]