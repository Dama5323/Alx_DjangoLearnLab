from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView  
from .models import Book, Library
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.urls import reverse_lazy

# ✅ Function-based view to list books
def list_books(request):
    books = Book.objects.all()  
    return render(request, 'relationship_app/list_books.html', {'books': books})

# ✅ Class-based view using DetailView
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# ✅ Function-based user registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')  
    else:
        form = UserCreationForm() 
    return render(request, 'relationship_app/register.html', {'form': form})

# ✅ Custom login/logout views
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'
