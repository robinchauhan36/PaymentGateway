from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from faker import Faker


class TestSetup(APITestCase):

    def setup(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.fake = Faker()

        self.user_data = {
            'email': self.fake.email(),
            'username': self.fake.email().split('@')[0],
            'password': self.fake.email(),
        }

        self.login_data = {
            'username': 'email',
            'password': 'password'
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
