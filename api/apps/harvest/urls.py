from django.urls import path

from .views import (
    CreateHarvestAmountAddView,
    ListHarvestDailyView,
    ListHarvestMonthlyView,
    ListHarvestWeeklyView,
    RetrieveHarvestDailyLotView,
    RetrieveHarvestDailyRankView,
    RetrieveHarvestDailySizeView,
    RetrieveHarvestDailySizeRankView,
    RetrieveHarvestMonthlyLotView,
    RetrieveHarvestMonthlyRankView,
    RetrieveHarvestMonthlySizeView,
    RetrieveHarvestMonthlySizeRankView,
    RetrieveHarvestWeeklyLotView,
    RetrieveHarvestWeeklyRankView,
    RetrieveHarvestWeeklySizeView,
    RetrieveHarvestWeeklySizeRankView,
    TabletHarvestView,
    UpdateHarvestTargetDailyView,
    UpdateHarvestTargetMonthlyView,
    UpdateHarvestTargetWeeklyView,
)

urlpatterns = [
    path("harvest/amount/add", CreateHarvestAmountAddView.as_view()),

    path("harvest/amount/daily", ListHarvestDailyView.as_view()),
    path("harvest/amount/daily/size/<str:size_id>", RetrieveHarvestDailySizeView.as_view()),
    path("harvest/amount/daily/lot/<str:lot_name>", RetrieveHarvestDailyLotView.as_view()),
    path("harvest/amount/daily/rank/<str:rank_id>", RetrieveHarvestDailyRankView.as_view()),
    path("harvest/amount/daily/size/<str:size_id>/rank/<str:rank_id>", RetrieveHarvestDailySizeRankView.as_view()),

    path("harvest/amount/weekly", ListHarvestWeeklyView.as_view()),
    path("harvest/amount/weekly/size/<str:size_id>", RetrieveHarvestWeeklySizeView.as_view()),
    path("harvest/amount/weekly/lot/<str:lot_name>", RetrieveHarvestWeeklyLotView.as_view()),
    path("harvest/amount/weekly/rank/<str:rank_id>", RetrieveHarvestWeeklyRankView.as_view()),
    path("harvest/amount/weekly/size/<str:size_id>/rank/<str:rank_id>", RetrieveHarvestWeeklySizeRankView.as_view()),

    path("harvest/amount/monthly", ListHarvestMonthlyView.as_view()),
    path("harvest/amount/monthly/size/<str:size_id>", RetrieveHarvestMonthlySizeView.as_view()),
    path("harvest/amount/monthly/lot/<str:lot_name>", RetrieveHarvestMonthlyLotView.as_view()),
    path("harvest/amount/monthly/rank/<str:rank_id>", RetrieveHarvestMonthlyRankView.as_view()),
    path("harvest/amount/monthly/size/<str:size_id>/rank/<str:rank_id>", RetrieveHarvestMonthlySizeRankView.as_view()),

    path("harvest/target/daily", UpdateHarvestTargetDailyView.as_view()),
    path("harvest/target/weekly", UpdateHarvestTargetWeeklyView.as_view()),
    path("harvest/target/monthly", UpdateHarvestTargetMonthlyView.as_view()),

    path("tablet/harvest/<str:date>", TabletHarvestView.as_view()),
]
