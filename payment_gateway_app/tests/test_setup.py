from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from faker import Faker


class TestSetup(APITestCase):

    def setup(self):
        self.payment_url = reverse('user_payment')

        self.payment_data = {
            'card': {
                'number': "3232323232322212",
                'expiration_month': "12",
                'expiration_year': "2023",
                'cvv': "123",
            },
            'amount': "12",
            'currency': "USD",
            'type': "credit_card",
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
