from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('account/', views.account, name='account'),
    path('connection/', views.connection, name='connection'),
]