# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Book

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'date_of_birth', 'profile_photo')

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book  # Replace with the model you want to use
        fields = ['title', 'author', 'publication_year']