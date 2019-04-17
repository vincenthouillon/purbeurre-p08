from django.contrib import admin
from .models import Categorie, Product, Nutriscore

# Register your models here.
admin.site.register(Categorie)
admin.site.register(Product)
admin.site.register(Nutriscore)
