from rest_framework import serializers
from . import models


class PostSerializer(serializers.ModelSerializer):
    """
    A Model serializer class for Post Model
    """
    class Meta:
        model = models.Post
        fields = ["id", "author", "topic", "date_created", "title", "body"]
        extra_kwargs = {
            "topic": {
                "required": True
            },
            "title": {
                "required": True
            }
        }


class TopicSerializer(serializers.ModelSerializer):
    """
    This is a serializer class for Topic model
    """
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = models.Topic
        fields = ["id", "topic_name", "topic_uuid", "posts"]
        extra_kwargs = {
            "topic_name": {
                "required": True
            },
        }
