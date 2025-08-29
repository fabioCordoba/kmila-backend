from django.urls import include, path
from rest_framework import routers

from apps.loan.api.views import LoanSearchView, LoanViewSet

router = routers.DefaultRouter()
router.register(r"loan", LoanViewSet, basename="loan")

urlpatterns = [
    path("loan/search/", LoanSearchView.as_view(), name="loan-search"),
    path("", include(router.urls)),
]
