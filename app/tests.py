from django.test import TestCase, Client
from django.urls import reverse

# https://docs.djangoproject.com/fr/2.2/topics/testing/
class HomePageTestCase(TestCase):
    """[summary]
    
    Arguments:
        TestCase {[type]} -- [description]
    """
    def test_home_page(self):
        response = self.client.get(reverse('app:home'))
        self.assertEquals(response.status_code, 200)

class legalPageTestCase(TestCase):
    def test_legal_page(self):
        response = self.client.get(reverse('app:legal'))
        self.assertEquals(response.status_code, 200)