from django.urls import reverse
from rest_framework.test import APIClient, APITestCase


class BaseTestSetUp(APITestCase):
    """
    Common Setup class for all tests
    """
    def setUp(self) -> None:
        self.client = APIClient()
        self.blogs_url = reverse("blogs")
        self.topics_url = reverse("topics")
        self.login_url = reverse("login")
        self.register_url = reverse("register")

        # Registering a new user and Login in
        self.registration_data = {
            "username": "rogers",
            "password": "Macharia7",
            "email": "rogers@username.com"
        }
        self.client.post(self.register_url, data=self.registration_data)
        self.login_response = self.client.post(self.login_url, data={"username": self.registration_data.get("username"),
                                               "password": self.registration_data.get("password")})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(self.login_response.data.get("access")))
