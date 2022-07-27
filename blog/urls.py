from django.urls import path
from . import views


urlpatterns = [
    path("", views.BlogListCreateAPIView.as_view(), name="blogs"),
    path("<int:pk>/", views.BlogRetrieveUpdateDestroyAPIView.as_view(), name="blog-update"),
    path("topics/", views.TopicListCreateAPIView.as_view(), name="topics"),
]
