from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post, Comment,Like
from accounts.models import CustomUser

User = get_user_model()

class PostTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser', 
            email='other@example.com', 
            password='testpass123'
        )
        
        # Create a post for testing
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='This is a test post content'
        )
        
        # Create a comment for testing
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment'
        )
    
    def test_create_post(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('post-list')
        data = {
            'title': 'New Post',
            'content': 'Content of the new post'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.latest('id').title, 'New Post')
    
    def test_get_posts_list(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_single_post(self):
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post.title)
    
    def test_update_post_authorized(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
    
    def test_update_post_unauthorized(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'title': 'Unauthorized Update'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_post(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
    
    def test_create_comment(self):
        self.client.force_authenticate(user=self.user)
        # Use the comments action on the post
        url = reverse('post-comments', kwargs={'pk': self.post.pk})
        data = {'content': 'New comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
    
    def test_get_comments_via_action(self):
        # Test getting comments through the post action
        url = reverse('post-comments', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Since we're using pagination, response.data will have a 'results' key
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_comments_via_viewset(self):
        # Test getting comments through the CommentViewSet
        url = reverse('comment-list', kwargs={'post_pk': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # CommentViewSet also uses pagination
        self.assertEqual(len(response.data['results']), 1)
    
    def test_search_posts(self):
        # Create another post for search testing
        Post.objects.create(
            author=self.user,
            title='Another Post',
            content='Different content here'
        )
        
        url = reverse('post-list')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Post')
    
    def test_filter_posts_by_author(self):
        # Create a post by another user
        Post.objects.create(
            author=self.other_user,
            title='Other User Post',
            content='Content by other user'
        )
        
        url = reverse('post-list')
        response = self.client.get(url, {'author': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Post')


class LikeTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass')
        self.other_user = CustomUser.objects.create_user(username='otheruser', password='testpass')
        self.post = Post.objects.create(author=self.other_user, title='Test Post', content='Test Content')
        self.client.force_authenticate(user=self.user)
    
    def test_like_post(self):
        url = f'/api/posts/{self.post.id}/like/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(user=self.user, post=self.post).exists())
    
    def test_cannot_like_twice(self):
        Like.objects.create(user=self.user, post=self.post)
        url = f'/api/posts/{self.post.id}/like/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_unlike_post(self):
        Like.objects.create(user=self.user, post=self.post)
        url = f'/api/posts/{self.post.id}/unlike/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(user=self.user, post=self.post).exists())