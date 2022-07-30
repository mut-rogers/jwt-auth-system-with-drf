from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from . import serializers


class UserRegistrationAPIView(APIView):
    """
    An APIView to register new users into the systems
    """ 
    # Authentication is not required to access this view 

    # Defining a serializer class 
    serializer_class = serializers.UserRegistrationSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=self.request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

