from django.shortcuts import render
from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
