from rest_framework.test import APIClient, APITestCase 
from rest_framework import status 
from django.urls import reverse, resolve 
from django.contrib.auth.models import User
from .models import Topic


class TestTopicListCreateAPIView(APITestCase):
    """
    Tests TopicListCreateAPIView view
    """
    def setUp(self) -> None: 
        self.client = APIClient()
        self.login_url = reverse("login")
        self.register_url = reverse("register")
        self.list_create_topic_url = reverse("topics")

        # Creating a new user and logging in
        self.register_data = {
            "username": "rogers",
            "password": "Macharia7",
            "email": "rogers@username.com"
        }
        self.client.post(self.register_url, data=self.register_data)
        self.login_response = self.client.post(self.login_url, data={"username": self.register_data.get("username"), "password": self.register_data.get("password")})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(self.login_response.data.get("access")))
        
        # New topic data
        self.new_topic_data = {
            "topic_name": "Web Development",
        }
        self.new_topic_response = self.client.post(self.list_create_topic_url, data=self.new_topic_data)

    def test_topic_was_created(self) -> None: 
        """ 
        Checks if a new topic was created via POST request 
        Expected behavior;
        --> POST request status code = 201 Created
        --> GET response from 'self.list_create_topic_url' returns one (1) topic
        --> Topic model contains one (1) topic object with correct topic_name == "Web Development
        """ 
        topic = Topic.objects.first()
        get_topic_response = self.client.get(self.list_create_topic_url)
        self.assertEqual(self.new_topic_response.status_code, status.HTTP_201_CREATED)        
        self.assertEqual(len(get_topic_response.data), 1)        
        self.assertEqual(topic.topic_name, self.new_topic_data.get("topic_name"))
