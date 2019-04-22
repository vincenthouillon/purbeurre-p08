import os

import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.http import Http404
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

    def articles_filter(name):
        """Delete articles in product names

        Arguments:
            name {str} -- Name or generic name of product
        """
        exclude = ("de", "des", "au", "aux", 'en', "le",
                   "la", "les", "et", "un", "une", "du", "à")

        produit = name.lower()
        produit = produit.split(" ")

        for e in exclude:
            for x in produit:
                if x in e:
                    try:
                        produit.remove(e)
                    except:
                        return x
        keyword = (" ".join(produit[0:5]))
        keyword = keyword.replace(",", "")
        return keyword

    query = request.GET.get('query')

    URL = 'https://fr.openfoodfacts.org/cgi/search.pl?'

    PARAMETERS = {
        'action': 'process',
        'search_terms': query,
        'sort_by': 'unique_scans_n',
        'axis_x': 'energy',
        'axis_y': 'products_n',
        'page_size': '1',
        'page': '1',
        'json': '1'
    }

    r = requests.get(URL, params=PARAMETERS)
    requested_product = r.json()

    try:
        substitution_products = Product.objects.annotate(
            search=SearchVector('product_name'),).filter(
                search=articles_filter(query))
        substitution_products = substitution_products.order_by('nutrition_grades')
        
        if not substitution_products:
            substitution_products = Product.objects.annotate(
                search=SearchVector('product_name'),).filter(
                    search=articles_filter(requested_product['products'][0]['product_name']))
            substitution_products = substitution_products.order_by('nutrition_grades')
        
        if not substitution_products:
            substitution_products = Product.objects.annotate(
                search=SearchVector('product_name'),).filter(
                    search=articles_filter(requested_product['products'][0]['generic_name_fr']))
            substitution_products = substitution_products.order_by('nutrition_grades')
    except:
        raise Http404

    # qs = Product.objects.filter(product_name__icontains=query)  # option

    # first_product = Product.objects.filter(
    #     product_name__icontains=query).first()

    # products_list = Product.objects.filter(
    #     category=first_product.category)
    # products_list = Product.objects.filter(
    #     category=first_product.nutrition_grades)
    # products_list = products_list.order_by('nutrition_grades')

    # print('#'*20, qs)
    # print('#'*5, products_list)

    template_name = 'app/search.html'
    context = {
        'img': IMG,
        'requested_title': f"1er résultat Open Food Facts pour : {query}",
        'requested_product_name': requested_product['products'][0]['product_name'],
        'requested_product_brands': requested_product['products'][0]['brands'],
        'requested_product_quantity': requested_product['products'][0]['quantity'],
        'requested_product_image': requested_product['products'][0]['image_url'],
        'products': substitution_products,
        # 'category': Product.category,
        # 'brands': Product.brands,
        # 'quantity': Product.quantity,
        # 'image_url': Product.image_url
    }

    # * IMPORTANT [22 Avril 2019]: For debug
    os.system('cls')
    print('#'*80)
    print(requested_product['products'][0]['generic_name_fr'])
    print(articles_filter(requested_product['products'][0]['generic_name_fr']))
    print(requested_product['products'][0]['product_name'])
    print(
        f"Nutriscore: {requested_product['products'][0]['nutrition_grades']}")
    print(substitution_products)
    print(type(substitution_products))
    print('#'*80)

    return render(request, template_name, context)
