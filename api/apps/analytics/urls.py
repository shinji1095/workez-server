from django.urls import path  # type: ignore
from .views import AnalyticsHarvestMonthlyView, AnalyticsRevenueMonthlyView, AnalyticsRevenueYearlyView

urlpatterns = [
    path("analytics/harvest/monthly", AnalyticsHarvestMonthlyView.as_view(), name="analytics-harvest-monthly"),
    path("analytics/revenue/monthly", AnalyticsRevenueMonthlyView.as_view(), name="analytics-revenue-monthly"),
    path("analytics/revenue/yearly", AnalyticsRevenueYearlyView.as_view(), name="analytics-revenue-yearly"),
]
