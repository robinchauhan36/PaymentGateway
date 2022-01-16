from payment_gateway_app.tests.test_setup import TestSetup


class TestViews(TestSetup):

    def test_payment_user(self):
        res = self.client.post(self.payment_url, self.payment_data, format="json")
        self.assertEqual(res.status_code, 201)
