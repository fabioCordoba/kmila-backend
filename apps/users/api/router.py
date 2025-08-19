from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.users.api.views import RegisterView, UserViewSet, UserView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("auth/register", RegisterView.as_view()),
    path("auth/login", TokenObtainPairView.as_view()),
    path("auth/token/refresh", TokenRefreshView.as_view()),
    path("auth/me", UserView.as_view()),
    path("", include(router.urls)),
]
