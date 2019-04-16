from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import SignupForm


def home_page(request):
    template_name = 'app/home.html'
    return render(request, template_name)


def signup_page(request):
    """User login page"""
    form = SignupForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/app/home')
    else:
        form = SignupForm()

    template_name = 'app/signup.html'
    context = {
        'form': form,
        'title': "S'enregister"
    }

    return render(request, template_name, context)


@login_required
def account_page(request):
    template_name = 'app/account.html'
    context = {
        'user': request.user,
    }
    return render(request, template_name, context)


def legal_page(request):
    template_name = 'app/legal.html'
    return render(request, template_name)


def contact_page(request):
    template_name = 'app/contact.html'
    return render(request, template_name)
