from django.urls import path
from .views import (
    register_user, login_user, user_profile, 
    get_followers, get_following, user_profile_with_follow_info,
    FollowUserView, UnfollowUserView  # Add the class-based views
)

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('profile/', user_profile, name='profile'),
    path('profile/follow-info/', user_profile_with_follow_info, name='profile-follow-info'),
    path('follow/<int:pk>/', FollowUserView.as_view(), name='follow-user'),  # Use class-based view
    path('unfollow/<int:pk>/', UnfollowUserView.as_view(), name='unfollow-user'),  # Use class-based view
    path('followers/', get_followers, name='followers'),
    path('following/', get_following, name='following'),
]