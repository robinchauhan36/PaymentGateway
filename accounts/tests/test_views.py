from accounts.tests.test_setup import TestSetup


class TestViews(TestSetup):

    def test_user_can_register_correctly(self):
        res = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 201)

    def test_user_can_login(self):
        res = self.client.post(self.login_url, self.login_data, format="json")
        self.assertEqual(res.status_code, 201)
