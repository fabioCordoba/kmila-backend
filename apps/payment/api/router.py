from django.urls import include, path
from rest_framework import routers

from apps.loan.api.views import LoanViewSet
from apps.payment.api.views import PaymentSearchView, PaymentViewSet

router = routers.DefaultRouter()
router.register(r"payment", PaymentViewSet, basename="payment")

urlpatterns = [
    path("payment/search/", PaymentSearchView.as_view(), name="payment-search"),
    path("", include(router.urls)),
]
