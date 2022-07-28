from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from rest_framework import status
from . import base_setup
from ..views import BlogListCreateAPIView


class BlogListCreateAPIViewTestCase(base_setup.BaseTestSetUp, APITestCase):
    """
    Tests BlogListCreateAPIView
    """
    def setUp(self) -> None:
        super().setUp()

        # Creating a new topic
        self.new_topic_data = {
            "topic_name": "Web Development",
        }
        self.client.post(self.topics_url, data=self.new_topic_data)

        # Creating a new blog post
        self.new_blog_data = {
            "topic": 1,
            "title": "Introduction to ReactJS",
            "body": "React is one of the most import things..."
        }
        self.new_blog_response = self.client.post(self.blogs_url, data=self.new_blog_data)

    def test_blog_post_was_created(self) -> None:
        """
        Check if a new blog post will be created
        Expected;
        --> response status code = 201 CREATED
        --> GET request data has length = 1
        """
        self.assertEqual(self.new_blog_response.status_code, status.HTTP_201_CREATED)
        data = self.client.get(self.blogs_url).data
        self.assertEqual(len(data), 1)

    def test_blog_post_not_created_with_bad_data(self) -> None:
        """
        Tests if a blog post will be created with wrong or missing data attributes
        Expected;
        --> response status code = 400 BAD REQUEST
        """
        bad_data = {}
        bad_response = self.client.post(self.blogs_url, data=bad_data)
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_authenticated_users_can_create_blog_posts(self) -> None:
        """
        Tests if only authenticated users can create new blog posts
        Expected;
        --> unauthenticated users cannot create blog posts
        --> POST response status code = 401 UNAUTHORIZED
        """
        # Resetting HTTP_AUTHORIZATION Header
        self.client.credentials()
        resp = self.client.post(self.blogs_url, data=self.new_blog_data)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_blogs_url_resolves_correct_view(self) -> None:
        """
        Tests if blogs_url resolves correct API View
        Expected;
        --> url uses BlogListCreateAPIView
        """
        view = resolve(self.blogs_url)
        self.assertEqual(view.func.view_class, BlogListCreateAPIView)