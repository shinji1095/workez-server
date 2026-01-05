from django.urls import path

from .views import (
    CreateHarvestAmountAddView,
    ListHarvestDailyView,
    ListHarvestMonthlyView,
    ListHarvestWeeklyView,
    RetrieveHarvestDailySizeView,
    RetrieveHarvestMonthlySizeView,
    RetrieveHarvestWeeklySizeView,
    TabletHarvestView,
)

urlpatterns = [
    path("harvest/amount/add", CreateHarvestAmountAddView.as_view()),

    path("harvest/amount/daily", ListHarvestDailyView.as_view()),
    path("harvest/amount/daily/size/<str:size_id>", RetrieveHarvestDailySizeView.as_view()),

    path("harvest/amount/weekly", ListHarvestWeeklyView.as_view()),
    path("harvest/amount/weekly/size/<str:size_id>", RetrieveHarvestWeeklySizeView.as_view()),

    path("harvest/amount/monthly", ListHarvestMonthlyView.as_view()),
    path("harvest/amount/monthly/size/<str:size_id>", RetrieveHarvestMonthlySizeView.as_view()),

    path("tablet/harvest/<str:date>", TabletHarvestView.as_view()),
]
