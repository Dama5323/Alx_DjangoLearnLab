from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            bio='Test bio'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )

    def test_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_profile_update(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('profile'), {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'bio': 'Updated bio'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updated@example.com')

   