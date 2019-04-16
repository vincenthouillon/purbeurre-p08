from django.db import models

# https://docs.djangoproject.com/fr/2.2/topics/db/models/
class Categories(models.Model):
    """Manage OpenFoodFacts Food Categories
    """
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name


class Products(models.Model):
    """Food details retrieved from OpenFoodFacts and saved by the user
    """
    product_name = models.CharField(max_length=255)
    url = models.URLField()
    image_url = models.URLField()
    fat = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    satured_fat = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    sugars = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    salt = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    nutrition_grades = models.CharField(max_length=1, null=True)
    category = models.ForeignKey("Categories", on_delete=models.CASCADE)

    def __str__(self):
        return str({
            "name": self.product_name,
            "url": self.url,
            "image": self.image_url,
            "nutriscore": self.nutrition_grades,
            "category": self.category
        })
