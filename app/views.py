import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SignupForm
from .models import Product

# Banner's images
IMG = '/static/app/img/bg-masthead.jpg'
IMG2 = '/static/app/img/bg-masthead-2.jpg'


def home_page(request):
    """Display home page."""

    template_name = 'app/home.html'
    return render(request, template_name)


def signup_page(request):
    """User login page."""

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
    """Displays the user account page."""

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
    """Page with search results."""

    def _articles_filter(name):
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
                search=_articles_filter(query))
        substitution_products = substitution_products.order_by(
            'nutrition_grades')

        if not substitution_products:
            substitution_products = Product.objects.annotate(
                search=SearchVector('product_name'),).filter(
                    search=_articles_filter(requested_product['products'][0]['product_name']))
            substitution_products = substitution_products.order_by(
                'nutrition_grades')

        if not substitution_products:
            substitution_products = Product.objects.annotate(
                search=SearchVector('product_name'),).filter(
                    search=_articles_filter(requested_product['products'][0]['generic_name_fr']))
            substitution_products = substitution_products.order_by(
                'nutrition_grades')
    except:
        raise Http404

    template_name = 'app/search.html'
    context = {
        'img': IMG,
        'requested_title': f"1er résultat Open Food Facts pour : {query}",
        'requested_product_name': requested_product['products'][0]['product_name'],
        'requested_product_brands': requested_product['products'][0]['brands'],
        'requested_product_quantity': requested_product['products'][0]['quantity'],
        'requested_product_image': requested_product['products'][0]['image_url'],
        'products': substitution_products,
    }

    return render(request, template_name, context)


def detail_page(request, code_product):
    """Page with product detail.

    Arguments:
        code_product {str} -- Code product
    """

    product = get_object_or_404(Product, code=code_product)

    URL = "https://static.openfoodfacts.org/images/misc/"

    # For drinks, nutritional benchmarks are divided by 2.
    if product.category == "Boissons":
        coef = 0.5
    else:
        coef = 1

    # Traffic lights - fat
    if product.fat < 3 * coef:
        fat_landmark = URL + "low_30.png"
    elif 3 * coef <= product.fat < 20 * coef:
        fat_landmark = URL + "moderate_30.png"
    else:
        fat_landmark = URL + "high_30.png"

    # Traffic lights - saturated_fat
    if product.saturated_fat < 1.5 * coef:
        saturated_fat_landmark = URL + "low_30.png"
    elif 1.5 * coef <= product.saturated_fat < 5 * coef:
        saturated_fat_landmark = URL + "moderate_30.png"
    else:
        saturated_fat_landmark = URL + "high_30.png"

    # Traffic lights - sugars
    if product.sugars < 5 * coef:
        sugars_landmark = URL + "low_30.png"
    elif 5 * coef <= product.sugars < 12.5 * coef:
        sugars_landmark = URL + "moderate_30.png"
    else:
        sugars_landmark = URL + "high_30.png"

    # Traffic lights - salt
    if product.salt < 0.3 * coef:
        salt_landmark = URL + "low_30.png"
    elif 0.3 * coef <= product.salt < 1.5 * coef:
        salt_landmark = URL + "moderate_30.png"
    else:
        salt_landmark = URL + "high_30.png"

    template_name = 'app/detail.html'
    context = {
        'code_product': code_product,
        'product_name': product.product_name,
        'product_img': product.image_url,
        'product_brands': product.brands,
        'product_quantity': product.quantity,
        'product_nutriscore': product.nutrition_grades,
        'fat_landmark': fat_landmark,
        'product_fat': product.fat,
        'saturated_fat_landmark': saturated_fat_landmark,
        'product_saturated_fat': product.saturated_fat,
        'sugars_landmark': sugars_landmark,
        'product_sugars': product.sugars,
        'salt_landmark': salt_landmark,
        'product_salt': product.salt,
        'product_url': product.url
    }
    return render(request, template_name, context)
