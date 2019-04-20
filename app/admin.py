from django.contrib import admin
from .models import Product, ProductAdmin

# Register your models here.
admin.site.register(Product, ProductAdmin)
