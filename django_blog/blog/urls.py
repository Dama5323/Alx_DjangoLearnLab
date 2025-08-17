from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
]