"""app URL Configuration"""
from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('signup/', views.signup_page, name='signup'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('account/', views.account_page, name='account'),
    path('legal/', views.legal_page, name='legal'),
    path('search/', views.search_page, name='search'),
    path('bookmarks/', views.saved_page, name='bookmarks'),
    path('<code_product>/', views.detail_page, name='detail'),
]
