from django.db import models
from django.contrib.auth import get_user_model
import uuid


class Topic(models.Model):
    topic_name = models.CharField(max_length=255, blank=True, null=True)
    topic_uuid = models.UUIDField(default=uuid.uuid4())

    def __str__(self) -> str:
        return self.topic_name


class Post(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="posts"
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="posts"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title
