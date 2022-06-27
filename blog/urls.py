from django.urls import path
from . import views


urlpatterns = [
    path("", views.PostListCreateAPIView.as_view(), name="posts"),
]
