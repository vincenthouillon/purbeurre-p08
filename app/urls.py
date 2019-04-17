"""app URL Configuration"""
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('signup/', views.signup_page, name='signup'),
    path('login/', LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='app/logout.html'), name='logout'),
    path('account/', views.account_page, name='account'),
    path('legal', views.legal_page, name='legal'),
    path('contact', views.contact_page, name='contact'),
    path('search', views.search_page, name='search'),
]
