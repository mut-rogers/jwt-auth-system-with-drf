from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, permissions, generics, views
from . import serializers
from . import models


class PostListCreateAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        print(self.request.META)
        return Response({"info": "Hello World"})
