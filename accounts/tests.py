from rest_framework.test import APIClient, APITestCase 
from rest_framework_simplejwt import views as jwt_views 
from rest_framework import status
from django.contrib.auth.models import User 
from django.urls import resolve, reverse 
from .views import UserRegistrationAPIView 


class AuthSystemTestCase(APITestCase):
    """
    This TestCase is used to test Login/Register functionality
    """
    def setUp(self) -> None:
        self.credentials = {
            "username": "james",
            "password": "djaldkfjadlfhad",
            "email": "james@username.com"
        }
    
        self.client = APIClient()
        self.register_url = reverse("register") 
        self.login_url = reverse("login")
        self.refresh_url = reverse("refresh")
        self.response = self.client.post(self.register_url, self.credentials)
        self.user = User.objects.get(pk=1)
        self.login_info = {
            "username": self.credentials.get("username"),
            "password": self.credentials.get("password")
        }

    def test_user_was_created(self) -> None: 
        """
        This test tests whether the user was created 
        Expected behavior; 
        --> response status = 201
        --> username in the used credentials is similar to username of the retrieved user
        """ 
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED) 
        self.assertEqual(self.credentials.get("username"), self.user.username)
        self.assertEqual(self.credentials.get("email"), self.user.email)

    def test_user_not_created_with_bad_credentials(self) -> None:
        """ 
        This test checks if the user will be created when required fields are not entered
        Expected behavior;
        --> response status = 400 Bad Request
        """ 
        register_info = {}
        response = self.client.post(self.register_url, register_info)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_successful_login_contains_access_and_refresh_token(self) -> None:
        """ 
        This test checks if response from a successful login contains both access and refresh tokens
        Expected behavior;
        --> response contains access and refresh tokens
        """
        login_response = self.client.post(self.login_url, data=self.login_info)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)

    def test_bad_login_credentials_returns_401_not_authorized(self) -> None:
        """ 
        This test checks if bad login credentials returns unauthorized response
        Expected behavior;
        --> response returns a 401 UNAUTHORIZED
        """ 
        bad_credentials = {
            "username": "bad-user",
            "password": "bad-password"
        }
        bad_response = self.client.post(self.login_url, data=bad_credentials)
        self.assertEqual(bad_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self) -> None:
        """
        Testing if an expired token will be refreshed
        """
        login_response = self.client.post(self.login_url, data=self.login_info)
        refresh_data = {
            "refresh": login_response.data.get("refresh")
        }
        refresh_response = self.client.post(self.refresh_url, data=refresh_data)
        self.assertIn("access", refresh_response.data)
        self.assertIn("refresh", refresh_response.data)

    def test_register_url_resolves_correct_view(self) -> None:
        """  
        This test checks if the register url resolves/users the correct register view 
        Expected behavior;
        --> register url resolves/uses UserRegistrationAPIView from the views module
        """ 
        view = resolve(self.register_url) 
        self.assertEqual(view.func.view_class, UserRegistrationAPIView)

    def test_login_url_resolves_correct_view(self) -> None:
        """
        This test checks if the login url resolves/uses the correct login view from jwt_views 
        Expected bevhavior;
        --> login url users jwt_vies.TokenObtainPairView 
        """ 
        view = resolve(self.login_url)
        self.assertEqual(view.func.view_class, jwt_views.TokenObtainPairView)