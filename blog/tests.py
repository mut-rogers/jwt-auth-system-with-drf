from rest_framework.test import APIClient, APITestCase 
from rest_framework import status 
from django.urls import reverse, resolve 
from django.contrib.auth.models import User
from .models import Topic
from . import views 


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
        --> GET response from 'self.list_create_topic_url' returns one (1) topic and status code = 200 OK
        --> Topic model contains one (1) topic object with correct topic_name == "Web Development
        """ 
        topic = Topic.objects.first()
        get_topic_response = self.client.get(self.list_create_topic_url)
        self.assertEqual(self.new_topic_response.status_code, status.HTTP_201_CREATED)        
        self.assertEqual(len(get_topic_response.data), 1)        
        self.assertEqual(get_topic_response.status_code, status.HTTP_200_OK)
        self.assertEqual(topic.topic_name, self.new_topic_data.get("topic_name"))

    def test_topics_url_resolves_correct_view(self) -> None: 
        view = resolve(self.list_create_topic_url) 
        self.assertEqual(view.func.view_class, views.TopicListCreateAPIView)


#---------------testing PostListCreateAPIView---------------------------------
class TestPostListCreateAPIView(APITestCase):
    """ 
    Tests for PostListCreateAPIView 
    """ 
    def setUp(self) -> None:
        self.client = APIClient()

        self.posts_url = reverse("posts")
        self.topics_url = reverse("topics")
        self.register_url = reverse("register")
        self.login_url = reverse("login") 

        # creating a new user and logging in 
        self.register_data = {
            "username": "rogers",
            "password": "Macharia7",
            "email": "rogers@username.com"
        }
        self.client.post(self.register_url, data=self.register_data)
        self.login_response = self.client.post(self.login_url, data={"username": self.register_data.get("username"), "password": self.register_data.get("password")})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(self.login_response.data.get("access"))) 

        # Creating a new topic 
        self.new_topic_data = {
            "topic_name": "Web Development",
        }
        self.client.post(self.topics_url, data=self.new_topic_data)

        # Creating a new post
        self.topics = self.client.get(self.topics_url)
        self.new_post_data = {
            "topic": self.topics.data[0].get("id"),
            "title": "Introduct to ReactJS",
            "body": "React is one of the most import things..."
        }
        self.new_post_response = self.client.post(self.posts_url, data=self.new_post_data)

    def test_new_post_created(self) -> None: 
        """ 
        Tests if a new Post will be created via a POST request 
        Expected behavior;
        --> POST response status code = 201 Created 
        --> GET request returns one (1) post
        --> GET response status code = 200 OK
        """      
        self.assertEqual(self.new_post_response.status_code, status.HTTP_201_CREATED)
        posts = self.client.get(self.posts_url)
        self.assertEqual(len(posts.data), 1)
        self.assertEqual(posts.status_code, status.HTTP_200_OK)
        
        
