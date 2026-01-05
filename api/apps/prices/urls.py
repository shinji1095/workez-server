from django.urls import path  # type: ignore
from .views import PricesMonthlyView, PricesSizeRankDetailView, PricesYearlyView

urlpatterns = [
    path("prices/size/<str:sizeId>/rank/<str:rankId>", PricesSizeRankDetailView.as_view(), name="prices-size-rank-detail"),
    path("prices/monthly", PricesMonthlyView.as_view(), name="prices-monthly"),
    path("prices/yearly", PricesYearlyView.as_view(), name="prices-yearly"),
]
