from django.urls import include, path
from rest_framework import routers

from apps.wallet.api.views import QuickStatsView, WalletSearchView, WalletViewSet

router = routers.DefaultRouter()
router.register(r"wallet", WalletViewSet, basename="wallet")

urlpatterns = [
    path("quick-stats/", QuickStatsView.as_view(), name="quick-stats"),
    path("wallet/search/", WalletSearchView.as_view(), name="wallet-search"),
    path("", include(router.urls)),
]
