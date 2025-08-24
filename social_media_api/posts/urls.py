from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import FeedView

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')

# For nested comments
comments_router = DefaultRouter()
comments_router.register(r'comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_pk>/', include(comments_router.urls)),
    path('feed/', FeedView.as_view(), name='user-feed'),
]