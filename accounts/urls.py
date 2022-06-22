from django.urls import path  
from . import views 
from rest_framework_simplejwt import views as jwt_views 


urlpatterns = [
    path("login/", jwt_views.TokenObtainPairView.as_view(), name="login"),
    path("refresh/", jwt_views.TokenRefreshView.as_view(), name="refresh"),
]