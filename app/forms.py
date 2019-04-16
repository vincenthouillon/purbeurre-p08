from django import forms

# from django.forms import ModelForm, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# User registration form
class SignupForm(UserCreationForm):
    """Form used to register a user"""
    email = forms.EmailField(max_length=255, help_text='Entrez une adresse email.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)