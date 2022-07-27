from django.urls import path
from . import views


urlpatterns = [
    path("<int:pk>/", views.PostListCreateAPIView.as_view(), name="posts"),
    path("topics/", views.TopicListCreateAPIView.as_view(), name="topics"),
]
