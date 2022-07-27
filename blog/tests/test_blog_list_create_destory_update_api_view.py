from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from rest_framework import status
from . import base_setup
from ..views import BlogRetrieveUpdateDestroyAPIView


class BlogListCreateAPIViewTestCase(base_setup.BaseTestSetUp, APITestCase):
    """
    Tests BlogListCreateUpdateDestroyAPIView
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
        --> get request data has length = 1
        """
        self.assertEqual(self.new_blog_response.status_code, status.HTTP_201_CREATED)
        data = self.client.get(self.blogs_url).data
        self.assertEqual(len(data), 1)

    def test_blog_post_can_be_updated(self) -> None:
        """
        Checks if an existing blog post can be updated
        Expected;
        --> PUT response status code = 200 OK
        --> new blog post title == 'Introduction to Node.js'
        :return:
        """

        update_data = {
            "topic": 1,
            "title": "Introduction to Node.js",
            "body": "Everyone should run Node.js..."
        }
        blog_update_url = reverse("blog-update", kwargs={"pk": 1})
        blog_update_response = self.client.put(blog_update_url, data=update_data)
        self.assertEqual(blog_update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(blog_update_response.data.get("title"), update_data.get("title"))

    def test_post_can_be_deleted(self) -> None:
        """
        Tests if an existing post can be deleted
        Expected;
        --> response status code = 204 NO CONTENT
        :return:
        """
        blog_delete_url = reverse("blog-update", kwargs={"pk": 1})
        blog_delete_response = self.client.delete(blog_delete_url)
        self.assertEqual(blog_delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_blog_post_not_created_with_bad_data(self) -> None:
        """
        Tests if a blog post will be created with wrong or missing data attributes
        Expected;
        --> response status code = 400 BAD REQUEST
        :return:
        """
        bad_data = {}
        bad_response = self.client.post(self.blogs_url, data=bad_data)
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_blog_update_url_resolves_correct_view(self) -> None:
        """
        Tests if blog-update url uses the correct view
        Expected;
        --> url resolves BlogRetrieveUpdateDestroyAPIView
        :return:
        """
        view = resolve(reverse("blog-update", kwargs={"pk": 1}))
        self.assertEqual(view.func.view_class, BlogRetrieveUpdateDestroyAPIView)

    def test_only_authors_can_delete_blog_posts(self) -> None:
        """
        Tests only authors can perform DELETE actions
        Expected;
        --> DELETE request status code = 401 UNAUTHORIZED
        :return:
        """
        # Reset HTTP_AUTHORIZATION Header
        self.client.credentials()
        blog_delete_url = reverse("blog-update", kwargs={"pk": 1})
        blog_delete_response = self.client.delete(blog_delete_url)
        self.assertEqual(blog_delete_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_only_authors_can_update_blog_posts(self) -> None:
        """
        Tests only authors can perform PUT actions
        Expected;
        --> PUT request status code = 401 UNAUTHORIZED
        :return:
        """
        # Reset HTTP_AUTHORIZATION Header
        self.client.credentials()
        update_data = {
            "topic": 1,
            "title": "Introduction to Node.js",
            "body": "Everyone should run Node.js..."
        }
        blog_update_url = reverse("blog-update", kwargs={"pk": 1})
        blog_update_response = self.client.put(blog_update_url, data=update_data)
        self.assertEqual(blog_update_response.status_code, status.HTTP_401_UNAUTHORIZED)
