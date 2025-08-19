from django.urls import include, path
from rest_framework import routers

from apps.wallet.api.views import QuickStatsView, WalletViewSet

router = routers.DefaultRouter()
router.register(r"wallet", WalletViewSet, basename="wallet")

urlpatterns = [
    path("quick-stats/", QuickStatsView.as_view(), name="quick-stats"),
    path("", include(router.urls)),
]
