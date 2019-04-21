from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SignupForm
from .models import Product

# Banner's images
IMG = '/static/app/img/bg-masthead.jpg'
IMG2 = '/static/app/img/bg-masthead-2.jpg'


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
        'img': IMG2
    }
    return render(request, template_name, context)


def legal_page(request):
    template_name = 'app/legal.html'
    return render(request, template_name)


def contact_page(request):
    template_name = 'app/contact.html'
    return render(request, template_name)


def search_page(request):
    query = request.GET.get('query')

    qs = Product.objects.filter(product_name__icontains=query)  # option

    title = f"Résultat pour : {query}"
    first_product = Product.objects.filter(
        product_name__icontains=query).first()
    
    products_list = Product.objects.filter(
        category=first_product.category)
    products_list = Product.objects.filter(
        category=first_product.nutrition_grades)
    products_list = products_list.order_by('nutrition_grades')

    print('#'*20, qs)
    print('#'*10, title)
    print('#'*5, products_list)


    template_name = 'app/search.html'
    context = {
        'img': IMG,
        'query': title,
        'first_product': first_product,
        'products': products_list,
        # 'category': Product.category,
        # 'brands': Product.brands,
        # 'quantity': Product.quantity,
        # 'image_url': Product.image_url
    }
    return render(request, template_name, context)
