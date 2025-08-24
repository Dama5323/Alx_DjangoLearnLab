from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import user_feed
from .views import PostViewSet, CommentViewSet, user_feed
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')

# For nested comments
comments_router = DefaultRouter()
comments_router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'posts/(?P<post_pk>[^/.]+)/comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_pk>/', include(comments_router.urls)),
    path('feed/', user_feed, name='user-feed'),  
    path('posts/<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('posts/<int:pk>/unlike/', PostViewSet.as_view({'post': 'unlike'}), name='post-unlike'),
]
