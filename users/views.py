from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


class UserCreationForm(UserCreationForm):
    """Modification of the django form."""
    username = forms.CharField(max_length=50, required=True, label='Pseudo')
    last_name = forms.CharField(max_length=50, required=True, label='Nom')
    first_name = forms.CharField(max_length=50, required=True, label='Prénom')
    email = forms.EmailField(required=True, label='Courriel')

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name',
                  'email', 'password1', 'password2')


class ConnectionForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(
        label="Mot de passe", widget=forms.PasswordInput, max_length=150)


def register(request):
    """Creating a user account."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            messages.success(request, f'Compte créé pour {username} !')
            form.save()
            return redirect('app/home')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def connection(request):
    """"User connection."""
    error = False

    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            messages.success(request, f'Bienvenue {email} !')
            # ! ALERT [11 Avril 2019]: For DEBUG
            return render(request, 'app/home.html')
            
            if user:  # If the returned object is not None
                login(request, user)  # We connect the user
            else:
                error = True
    else:
        form = ConnectionForm()
    return render(request, 'users/connection.html', locals())


@login_required
def account(request):
    return render(request, 'users/account.html')
