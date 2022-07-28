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

        # Registering and logging a new user
        # Registering and logging in a new user/author
        self.new_user_registration_data = {
            "username": "peter",
            "password": "StrongPassword7!",
            "email": "pters@username.com"
        }
        self.client.post(self.register_url, data=self.new_user_registration_data)
        self.new_user_login_response = self.client.post(self.login_url, data={"username": "peter",
                                                                              "password": "StrongPassword7!"})

        # Creating a new blog post
        self.new_blog_data = {
            "topic": 1,
            "title": "Introduction to ReactJS",
            "body": "React is one of the most import things..."
        }
        self.new_blog_response = self.client.post(self.blogs_url, data=self.new_blog_data)

    def test_blog_post_can_be_updated(self) -> None:
        """
        Checks if an existing blog post can be updated
        Expected;
        --> PUT response status code = 200 OK
        --> new blog post title == 'Introduction to Node.js'
        """
        blog_update_data = {
            "topic": 1,
            "title": "Introduction to Node.js",
            "body": "Everyone should run Node.js..."
        }
        blog_update_url = reverse("blog-update", kwargs={"pk": 1})
        blog_update_response = self.client.put(blog_update_url, data=blog_update_data)
        self.assertEqual(blog_update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(blog_update_response.data.get("title"), blog_update_data.get("title"))

    def test_only_authors_can_update_a_blog(self) -> None:
        """
        Tests if only authors are allowed to update existing blog posts
        Expected;
        --> attempt to update returns 403 FORBIDDEN for non-authors
        """
        # Resetting HTTP_AUTHORIZATION header
        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(self.new_user_login_response.data.get("access")))
        blog_update_url = reverse("blog-update", kwargs={"pk": 1})
        self.new_blog_data["title"] = "Introduction Python"
        blog_update_response = self.client.put(blog_update_url, data=self.new_blog_data)
        self.assertEqual(blog_update_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_blog_post_can_be_deleted(self) -> None:
        """
        Tests if an existing post can be deleted
        Expected;
        --> response status code = 204 NO CONTENT
        """
        blog_delete_url = reverse("blog-update", kwargs={"pk": 1})
        blog_delete_response = self.client.delete(blog_delete_url)
        self.assertEqual(blog_delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_only_authors_can_delete_a_blog(self) -> None:
        """
        Tests if only authors can perform DELETE action
        Expected;
        --> attempt to delete returns 403 FORBIDDEN status code for non-authors
        """
        # Resetting HTTP_AUTHORIZATION Header
        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(self.new_user_login_response.data.get("access")))
        blog_delete_url = reverse("blog-update", kwargs={"pk": 1})
        blog_delete_response = self.client.delete(blog_delete_url)
        self.assertEqual(blog_delete_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_blog_update_url_resolves_correct_view(self) -> None:
        """
        Tests if blog-update url uses the correct view
        Expected;
        --> url resolves BlogRetrieveUpdateDestroyAPIView
        :return:
        """
        view = resolve(reverse("blog-update", kwargs={"pk": 1}))
        self.assertEqual(view.func.view_class, BlogRetrieveUpdateDestroyAPIView)
