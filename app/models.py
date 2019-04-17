# https://docs.djangoproject.com/fr/2.2/topics/db/models/
from django.db import models


class Categorie(models.Model):
    """OpenFoodFacts Food Categories
    """
    category_name = models.CharField(
        max_length=255, unique=True, verbose_name='catégorie')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'catégorie'


class Nutriscore(models.Model):
    """OpenFoodFacts Food Nutriscores
    """
    nutrition_grades = models.CharField(
        max_length=10, unique=True, verbose_name='nutriscore')

    def __str__(self):
        return self.nutrition_grades

    class Meta:
        verbose_name = 'nutriscore'


class Product(models.Model):
    """Food details retrieved from OpenFoodFacts and saved by the user
    """
    product_name = models.CharField(
        max_length=255, verbose_name='nom du produit')
    brands = models.CharField(max_length=255, null=True, verbose_name='marque')
    quantity = models.CharField(
        max_length=40, null=True, verbose_name='quantité')
    code = models.CharField(max_length=40, unique=True, verbose_name='code barre')
    url = models.URLField()
    image_url = models.URLField(
        null=True, verbose_name='lien vers la page OFF', help_text='OFF : Open Food Facts')
    fat = models.DecimalField(max_digits=5, decimal_places=2,
                              null=True, verbose_name='matières grasses pour 100g')
    satured_fat = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, verbose_name='acides gras saturés pour 100g')
    sugars = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, verbose_name='sucres pour 100g')
    salt = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, verbose_name='sel pour 100g')
    nutriscore = models.ForeignKey(
        "Nutriscore", on_delete=models.CASCADE)
    category = models.ForeignKey(
        "Categorie", on_delete=models.CASCADE, verbose_name='catégorie')

    class Meta:
        verbose_name = 'produit'
