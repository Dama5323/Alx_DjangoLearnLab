from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .permissions import IsCreatorOrReadOnly


class CustomAPIResponseMixin:
    """Mixin for standardized API responses"""
    def create_response(self, serializer, status_code=status.HTTP_200_OK, headers=None):
        """Create a consistent response format"""
        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status_code, headers=headers)


class AuthorListCreateView(generics.ListCreateAPIView):
    """
    View to list and create authors
    - GET: Available to all (read-only)
    - POST: Requires authentication
    """
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class BookListView(generics.ListAPIView):
    """
    View to list books with filtering, searching and ordering
    Example queries:
    /api/books/?title__icontains=django
    /api/books/?author=1&publication_year__gte=2020
    /api/books/?search=rowling
    /api/books/?ordering=-publication_year,title
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = {
        'title': ['exact', 'icontains'],
        'author': ['exact'],
        'publication_year': ['exact', 'gt', 'gte', 'lt', 'lte'],
    }
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a single book
    Available to all users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(CustomAPIResponseMixin, generics.CreateAPIView):
    """
    View to create a new book
    Requires authentication
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Set the created_by field to current user"""
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        """Custom response format for creation"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return self.create_response(
            serializer, 
            status.HTTP_201_CREATED, 
            headers=headers
        )


class BookUpdateView(CustomAPIResponseMixin, generics.UpdateAPIView):
    """
    View to update an existing book
    Requires authentication and creator ownership
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]

    def update(self, request, *args, **kwargs):
        """Handle partial updates and return custom response"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return self.create_response(serializer)


class BookDeleteView(generics.DestroyAPIView):
    """
    View to delete a book
    Requires authentication and creator ownership
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        """Custom delete response"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': 'success',
            'message': 'Book deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class BookListCreateView(generics.ListCreateAPIView):
    """
    Combined view for listing and creating books
    - GET: Available to all
    - POST: Requires authentication
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']

    def get_permissions(self):
        """Set permissions based on request method"""
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]