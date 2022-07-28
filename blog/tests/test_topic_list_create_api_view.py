from rest_framework.test import APITestCase
from rest_framework import status
from . import base_setup
from ..views import TopicListCreateAPIView
from django.urls import resolve


class TopicListCreateAPIViewTestCase(base_setup.BaseTestSetUp, APITestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_new_topic_was_created(self) -> None:
        """
        Checks if a new topic was created
        Expected behavior;
        --> response status = 201 CREATED
        --> get request data length = 1
        """
        self.assertEqual(self.new_topic_response.status_code, status.HTTP_201_CREATED)
        resp = self.client.get(self.topics_url)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0].get("topic_name"), self.new_topic_data.get("topic_name"))

    def test_topic_not_created_with_bad_data(self) -> None:
        """
        Tests if a new topic will be created with mission data attributes
        Expected;
        --> response status code = 400 BAD REQUEST
        :return:
        """
        bad_data = {}
        bad_response = self.client.post(self.topics_url, data=bad_data)
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_topics_url_resolves_correct_view(self) -> None:
        """
        Checks if the topics url uses the correct view
        Expected;
        --> topics url uses TopicListCreateAPIView CBV
        """
        view = resolve(self.topics_url)
        self.assertEqual(view.func.view_class, TopicListCreateAPIView)
