from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        """Set up test data and client with separate test database"""
        # Using APIClient for API requests
        self.client = APIClient()
        
        # Create test users in the test database
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Create test author in the test database
        self.author = Author.objects.create(name='Test Author')
        
        # Create test books in the test database
        self.book1 = Book.objects.create(
            title='Django for Beginners',
            publication_year=2020,
            author=self.author,
            created_by=self.user
        )
        self.book2 = Book.objects.create(
            title='Advanced Django',
            publication_year=2022,
            author=self.author,
            created_by=self.admin_user
        )
        
        # URLs
        self.list_url = reverse('book-list')
        self.detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})

    def test_list_books_unauthenticated(self):
        """Test listing books without authentication"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book_unauthenticated(self):
        """Test creating book without authentication should fail"""
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_book_authenticated_with_login(self):
        """Test creating book using self.client.login for authentication"""
        login_successful = self.client.login(
            username='testuser',
            password='testpass123'
        )
        self.assertTrue(login_successful)

        data = {
            'title': 'Book via Login',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['data']['title'], 'Book via Login')
    
    def test_retrieve_book(self):
        """Test retrieving a single book"""
        url = self.detail_url(self.book1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Django for Beginners')

    def test_update_book_not_owner(self):
        """Test updating book by non-owner should fail"""
        self.client.force_authenticate(user=self.user)
        url = self.detail_url(self.book2.id)
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_owner(self):
        """Test updating book by owner"""
        self.client.force_authenticate(user=self.user)
        url = self.detail_url(self.book1.id)
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_delete_book_not_owner(self):
        """Test deleting book by non-owner should fail"""
        self.client.force_authenticate(user=self.user)
        url = self.detail_url(self.book2.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2)

    def test_delete_book_owner(self):
        """Test deleting book by owner"""
        self.client.force_authenticate(user=self.user)
        url = self.detail_url(self.book1.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filtering_by_title(self):
        """Test filtering books by title"""
        response = self.client.get(self.list_url, {'title__icontains': 'django'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django for Beginners')

    def test_filtering_by_publication_year(self):
        """Test filtering books by publication year"""
        response = self.client.get(self.list_url, {'publication_year__gte': 2021})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Advanced Django')

    def test_search_functionality(self):
        """Test search across title and author name"""
        response = self.client.get(self.list_url, {'search': 'advanced'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Advanced Django')

    def test_ordering(self):
        """Test ordering books by publication year"""
        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Advanced Django')
        self.assertEqual(response.data[1]['title'], 'Django for Beginners')

    def test_author_creation(self):
        """Test author creation endpoint"""
        self.client.force_authenticate(user=self.user)
        url = reverse('author-list')
        data = {'name': 'New Author'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)