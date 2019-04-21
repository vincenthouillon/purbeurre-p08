"""Script to fill and update the PurBeurre database with OpenFoodFacts data via 
its API.

To run this script run "manage.py getdata" command in your console.
"""

import requests
import time
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from app.models import Product


class Command(BaseCommand):
    """Class to handle the "manage.py getdata" command.
    This class updates the DB with the latest info from Open Food Facts.
    """

    help = "Run this script to update the database from OpenFoodFacts"

    def handle(self, *args, **kwargs):
        """List of categories."""

        # Gives infos about updating process
        self.stdout.write(
            "Creating or updating PurBeurre database...", ending='\n')

        CATEGORIES = (
            "Petit-déjeuners",
            "Snacks sucrés",
            "Snacks salés",
            "Boissons",
            "Desserts",
            "Produits laitiers",
            "Viandes",
            "Produits de la mer",
            "Plats préparés",
            "Epicerie",
            "Matières grasses"
        )

        for nutriscore in ('a', 'b'):
            for page in range(1, 3):
                for category in CATEGORIES:
                    products_data = self._api_requests(
                        category, nutriscore, page)
                    self._insert_data(products_data)

        # Gives infos about updating process
        self.stdout.write(f"Finish, the database contains {Product.objects.count()} products", ending='\n')
        
    def _insert_data(self, products_data):
        """Insert data in database."""
        idx = 0
        animation = "|/-\\"
        for product in products_data:
            print("Loading...", animation[idx % len(animation)], end="\r")
            idx += 1
            try:
                if product['product_name']:
                    Product.objects.update_or_create(
                        product_name=product['product_name'],
                        brands=product['brands'],
                        quantity=product['quantity'],
                        code=product['code'],
                        url=product['url'],
                        image_url=product['image_url'],
                        fat=product['fat'],
                        saturated_fat=product['saturated_fat'],
                        sugars=product['sugars'],
                        salt=product['salt'],
                        nutrition_grades=product['nutriscore'],
                        category=product['category']
                    )
            # Ignore duplicate value
            except IntegrityError:
                continue
            except KeyError:
                pass
            except:
                pass

    def _api_requests(self, category, nutriscore, page):
        """Calls the OpenFoodFacts API for informations."""

        URL = 'https://fr.openfoodfacts.org/cgi/search.pl'

        parameters = {
            'action': 'process',
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': category,
            'tagtype_1': 'nutrition_grades',
            'tag_contains_1': 'contains',
            'tag_1': nutriscore,
            'sort_by': 'unique_scans_n',
            'axis_x': 'energy',
            'axis_y': 'products_n',
            'page_size': '200',
            'page': page,
            'json': '1',
        }

        try:
            r = requests.get(URL, params=parameters)
            products_json = r.json()

            content = list()
            for product in products_json['products']:
                try:
                    data = {
                        "product_name": product['product_name'],
                        "brands": product['brands'],
                        "quantity": product['quantity'],
                        "code": product['code'],
                        "url": product['url'],
                        "image_url": product['image_url'],
                        "fat": product['nutriments']['fat_100g'],
                        "saturated_fat": product['nutriments']['saturated-fat_100g'],
                        "sugars": product['nutriments']['sugars_100g'],
                        "salt": product['nutriments']['salt_100g'],
                        "nutriscore": product['nutrition_grades'],
                        "category": category
                    }
                    content.append(data)
                except KeyError:
                    pass
            return content
        except requests.exceptions.ConnectionError:
            print("You must be connected in order to create or update the database")
