from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.api.views import (
    CheckTokenView,
    CustomTokenObtainPairView,
    LogoutView,
    RegisterView,
    SendEmailTest,
    UserSearchView,
    UserViewSet,
    UserView,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("auth/register", RegisterView.as_view()),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/check-token/", CheckTokenView.as_view(), name="check_token"),
    path("auth/token/refresh", TokenRefreshView.as_view()),
    path("auth/me", UserView.as_view()),
    path("email/test", SendEmailTest.as_view()),
    path("users/search/", UserSearchView.as_view(), name="user-search"),
    path("", include(router.urls)),
]
