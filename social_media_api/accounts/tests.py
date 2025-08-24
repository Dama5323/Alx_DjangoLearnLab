from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Notification
from .models import Like  
from accounts.models import CustomUser
User = get_user_model()

class NotificationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass')
        self.client.force_authenticate(user=self.user)
    
    def test_get_notifications(self):
        # Create a notification
        Notification.objects.create(
            recipient=self.user,
            actor=self.other_user,
            verb="liked your post"
        )
        
        url = '/api/notifications/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_unread_count(self):
        # Create unread notifications
        Notification.objects.create(
            recipient=self.user,
            actor=self.other_user,
            verb="liked your post"
        )
        Notification.objects.create(
            recipient=self.user,
            actor=self.other_user,
            verb="commented on your post"
        )
        
        url = '/api/notifications/unread-count/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 2)