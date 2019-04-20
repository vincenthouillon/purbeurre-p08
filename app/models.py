# https://docs.djangoproject.com/fr/2.2/topics/db/models/
from django.db import models
from django.contrib import admin



class Product(models.Model):
    """Food details retrieved from OpenFoodFacts and saved by the user
    """
    product_name = models.CharField(
        max_length=255, verbose_name='nom du produit')
    brands = models.CharField(max_length=255, null=True, verbose_name='marque')
    quantity = models.CharField(
        max_length=40, null=True, verbose_name='quantité')
    code = models.CharField(max_length=40, unique=True,
                            verbose_name='code barre')
    url = models.URLField(verbose_name="lien vers le site OFF", help_text="OFF = Open Food Facts")
    image_url = models.URLField(
        null=True, verbose_name="lien vers l'image")
    fat = models.DecimalField(max_digits=5, decimal_places=2,
                              null=True, verbose_name='matières grasses pour 100g')
    saturated_fat = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, verbose_name='acides gras saturés pour 100g')
    sugars = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, verbose_name='sucres pour 100g')
    salt = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, verbose_name='sel pour 100g')
    nutrition_grades = models.CharField(
        max_length=1, null=True, verbose_name='nutriscore')
    category = models.CharField(
        max_length=255, null=True, verbose_name='catégorie')

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'produit'
        ordering = ['product_name']

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['product_name']
