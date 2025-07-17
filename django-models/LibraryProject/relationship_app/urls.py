from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),  # ✅ match: views.register
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),  # ✅ match
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),  # ✅ match
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('books/', views.list_books, name='list_books'),
]
