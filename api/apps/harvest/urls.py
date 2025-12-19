from django.urls import path  # type: ignore
from .views import (
    HarvestAmountAddView,
    HarvestAmountDailyView,
    HarvestAmountWeeklyView,
    HarvestAmountMonthlyView,
    HarvestAmountDailyCategoryView,
    HarvestAmountWeeklyCategoryView,
    HarvestAmountMonthlyCategoryView,
    HarvestTargetDailyView,
    HarvestTargetWeeklyView,
    HarvestTargetMonthlyView,
)

urlpatterns = [
    path("harvest/amount/add", HarvestAmountAddView.as_view(), name="harvest-amount-add"),
    path("harvest/amount/daily", HarvestAmountDailyView.as_view(), name="harvest-amount-daily"),
    path("harvest/amount/weekly", HarvestAmountWeeklyView.as_view(), name="harvest-amount-weekly"),
    path("harvest/amount/monthly", HarvestAmountMonthlyView.as_view(), name="harvest-amount-monthly"),
    path("harvest/amount/daily/category/<str:categoryId>", HarvestAmountDailyCategoryView.as_view(), name="harvest-amount-daily-category"),
    path("harvest/amount/weekly/category/<str:categoryId>", HarvestAmountWeeklyCategoryView.as_view(), name="harvest-amount-weekly-category"),
    path("harvest/amount/monthly/category/<str:categoryId>", HarvestAmountMonthlyCategoryView.as_view(), name="harvest-amount-monthly-category"),
    path("harvest/target/daily", HarvestTargetDailyView.as_view(), name="harvest-target-daily"),
    path("harvest/target/weekly", HarvestTargetWeeklyView.as_view(), name="harvest-target-weekly"),
    path("harvest/target/monthly", HarvestTargetMonthlyView.as_view(), name="harvest-target-monthly"),
]
