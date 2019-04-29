# https://docs.djangoproject.com/fr/2.2/topics/testing/
from django.test import TestCase, Client
from django.urls import reverse
from app.models import Product, Bookmark, User
from app.forms import UserCreationForm


class HomePageTestCase(TestCase):
    """Test Homepage."""

    def test_home_page(self):
        response = self.client.get(reverse('app:home'))
        self.assertEquals(response.status_code, 200)


class legalPageTestCase(TestCase):
    """Test Legal page."""

    def test_legal_page(self):
        response = self.client.get(reverse('app:legal'))
        self.assertEquals(response.status_code, 200)


# Product's details page
class DetailPageTestCase(TestCase):
    """
    Product's details page test
    """

    def setUp(self):
        """Fake product data."""

        Product.objects.create(id=1337,
                               code="123456789",
                               product_name="fake product",
                               fat="0.3",
                               saturated_fat="0.3",
                               sugars="0.3",
                               salt="0.3",
                               )
        self.product = Product.objects.get(product_name="fake product")

    def test_detail_page_returns_200(self):
        """Try to access page with valid query parameters. 
        It must return a http 200 code.
        """

        product_code = self.product.code
        response = self.client.get(reverse('app:detail', args=(product_code,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_returns_404(self):
        """Try to access page with invalid query parameters.
        It must return a http 404 code.
        """

        product_id = self.product.id + 1
        response = self.client.get(reverse('app:detail', args=(product_id,)))
        self.assertEqual(response.status_code, 404)


# Login page
class SigninTestPageCase(TestCase):
    """User's signin page tests."""

    def setUp(self):
        """Fake data."""

        self.username = "test"
        self.password = hash("1234abcd")
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_page(self):
        """Simple tests. Must return an http 200 code."""

        response = self.client.get(reverse('app:signin'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        """Try to connect with valid data.
        The request should return an error 302 (redirection test).
        """
        response = self.client.post(reverse('app:signin'), {
            "username": self.username,
            "password": self.password,
            })
        self.assertEqual(response.status_code, 302)

    def test_login_fail_username(self):
        """Try to login with an invalid username. 
        The request must return an error 200.
        """
        response = self.client.post(reverse('app:signin'), {
            "username": ' ',
            "password": self.password,
            })
        self.assertEqual(response.status_code, 200)

    def test_login_fail_password(self):
        """Try to login with invalid password."""

        response = self.client.post(reverse('app:signin'), {
            "username": self.username,
            "password": 'defgzpzd,',
            })
        self.assertEqual(response.status_code, 200)

    def test_csrf(self):
        """Test for the CSFR token."""

        response = self.client.get(reverse('app:signin'))
        self.assertContains(response, 'csrfmiddlewaretoken')


# User account page
class AccountTestPageCase(TestCase):
    """Tests of the user account page."""

    def setUp(self):
        """
        Temporary data
        """
        url = reverse('app:account')
        self.data = {
            'username': 'john',
            'email': 'john@doe.com',
            'password': 'abcdef123456',
        }
        self.response = self.client.post(url, self.data)
        self.user = User.objects.create_user(**self.data)

    def test_account_page_returns_200(self):
        """Try to access the page while logged in. 
        It must return an http 200 code.
        """
        self.client.login(**self.data)
        response = self.client.get(reverse('app:account'))
        self.assertEqual(response.status_code, 200)

    def test_account_page_redirects(self):
        """Try to access the page without being connected. 
        It must return an http 302 code.
        """
        response = self.client.get(reverse('app:account'))
        self.assertEqual(response.status_code, 302)
