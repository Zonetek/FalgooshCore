from .views import (
    CustomTokenObtainPairView,
    CustomRefreshTokenObtainPairView,
    UserProfileAPIView,
)
from django.urls import path

urlpatterns = [
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "api/token/refresh/",
        CustomRefreshTokenObtainPairView.as_view(),
        name="token_refresh",
    ),
    path("api/user/profile/", UserProfileAPIView.as_view(), name="user-profile"),
]
