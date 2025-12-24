from django.urls import path

from .views import (
    CreateHarvestAmountAddView,
    ListHarvestDailyCategoryView,
    ListHarvestDailyView,
    ListHarvestMonthlyCategoryView,
    ListHarvestMonthlyView,
    ListHarvestWeeklyCategoryView,
    ListHarvestWeeklyView,
)

urlpatterns = [
    path("harvest/amount/add", CreateHarvestAmountAddView.as_view()),

    path("harvest/amount/daily", ListHarvestDailyView.as_view()),
    path("harvest/amount/daily/category/<str:category_id>", ListHarvestDailyCategoryView.as_view()),

    path("harvest/amount/weekly", ListHarvestWeeklyView.as_view()),
    # PATCH weekly override is also handled by this view for admin
    path("harvest/amount/weekly/category/<str:category_id>", ListHarvestWeeklyCategoryView.as_view()),

    path("harvest/amount/monthly", ListHarvestMonthlyView.as_view()),
    path("harvest/amount/monthly/category/<str:category_id>", ListHarvestMonthlyCategoryView.as_view()),
]
