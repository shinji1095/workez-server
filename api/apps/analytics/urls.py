from django.urls import path  # type: ignore
from .views import AnalyticsHarvestMonthlyView, AnalyticsRevenueMonthlyView, AnalyticsRevenueYealyView

urlpatterns = [
    path("analytics/harvest/monthly", AnalyticsHarvestMonthlyView.as_view(), name="analytics-harvest-monthly"),
    path("analytics/revenue/monthly", AnalyticsRevenueMonthlyView.as_view(), name="analytics-revenue-monthly"),
    path("analytics/revenue/yealy", AnalyticsRevenueYealyView.as_view(), name="analytics-revenue-yealy"),
]
