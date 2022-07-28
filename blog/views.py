from rest_framework import permissions, generics, mixins
from . import models
from . import permissions as custom_permissions
from . import serializers


class BlogListCreateAPIView(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    """
    This view returns a list of all blogs objects.
    Facilitate creation of new blog objects.
    Methods --> GET, POST
    Only authenticated users can make POST requests / Creating new Posts objects
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, custom_permissions.IsAuthorOrReadOnly]
    serializer_class = serializers.PostSerializer
    queryset = models.Post.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer = serializer.save(author=self.request.user)
        return serializer


class BlogRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    The view is used to retrieve, update, or delete Blog objects.
    Only Blog authors can perform update and delete actions
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, custom_permissions.IsAuthorOrReadOnly]
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
