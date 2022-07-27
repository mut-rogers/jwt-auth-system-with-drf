from django.db.models import QuerySet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, permissions, generics, views
from . import serializers
from . import models
from rest_framework.decorators import action
from . import permissions as custom_permissions


class PostListCreateAPIView(generics.ListCreateAPIView):
    """
    This view returns a list of all blogs objects.
    Facilitate creations of new blog objects.
    Methods --> GET, POST 

    Only authenticated users can make POST requests / Creating new Posts objects
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = serializers.PostSerializer 
    queryset = models.Post.objects.all() 

    def perform_create(self, serializer):
        """
        Associating a Post object with logged in user
        """
        serializer = serializer.save(author=self.request.user)
        return serializer


class PostRetrieveDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view retrieves, updates, and deletes Post objects.
    Users only delete objects they have created
    """
    permissions = [custom_permissions.IsAuthorOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    serializer_class = serializers.PostSerializer
    queryset = models.Post.objects.all()


class TopicListCreateAPIView(generics.ListCreateAPIView):
    """
    This view is used to return a list of all Topic objects while allow creation of new ones
    Methods --> GET, POST

    Only Authenticated Users can make POST requests / Creating new Topic objects
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = serializers.TopicSerializer 
    queryset = models.Topic.objects.all()
