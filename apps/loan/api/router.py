from django.urls import include, path
from rest_framework import routers

from apps.loan.api.views import LoanViewSet

router = routers.DefaultRouter()
router.register(r"loan", LoanViewSet, basename="loan")

urlpatterns = [
    path("", include(router.urls)),
]
