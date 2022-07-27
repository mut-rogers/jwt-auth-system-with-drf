from rest_framework import permissions, generics, mixins

from . import models
from . import permissions as custom_permissions
from . import serializers


class PostListCreateAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    This view returns a list of all blogs objects.
    Facilitate creations of new blog objects.
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

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class TopicListCreateAPIView(generics.ListCreateAPIView):
    """
    This view is used to return a list of all Topic objects while allow creation of new ones
    Methods --> GET, POST

    Only Authenticated Users can make POST requests / Creating new Topic objects
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = serializers.TopicSerializer 
    queryset = models.Topic.objects.all()
