from django.urls import path  # type: ignore
from .views import (
    DefectsAmountAddView,
    DefectsAmountWeeklyView,
    DefectsAmountMonthlyView,
    DefectsRatioWeeklyView,
    DefectsRatioMonthlyView,
)

urlpatterns = [
    path("defects/amount/add", DefectsAmountAddView.as_view(), name="defects-amount-add"),
    path("defects/amount/weekly", DefectsAmountWeeklyView.as_view(), name="defects-amount-weekly"),
    path("defects/amount/monthly", DefectsAmountMonthlyView.as_view(), name="defects-amount-monthly"),
    path("defects/ratio/weekly", DefectsRatioWeeklyView.as_view(), name="defects-ratio-weekly"),
    path("defects/ratio/monthly", DefectsRatioMonthlyView.as_view(), name="defects-ratio-monthly"),
]
