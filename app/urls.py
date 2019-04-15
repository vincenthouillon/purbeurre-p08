"""homepage URL Configuration"""
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('signup/', views.signup_page, name='signup'),
    path('login/', LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='app/home.html'), name='logout'),
    path('account/', views.account_page, name='account'),
    path('mentions', views.mentions_page, name='mentions')
]
