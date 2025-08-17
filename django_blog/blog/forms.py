from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Post
from .models import Comment

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'profile_picture']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': forms.TextInput(attrs={
                'placeholder': 'Enter tags separated by commas',
                'data-role': 'tagsinput'  # For Bootstrap Tags Input if using
            })
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4})
        }