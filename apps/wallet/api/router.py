from django.urls import include, path
from rest_framework import routers

from apps.wallet.api.views import WalletViewSet

router = routers.DefaultRouter()
router.register(r"wallet", WalletViewSet, basename="wallet")

urlpatterns = [
    path("", include(router.urls)),
]
