from django.urls import path  # type: ignore
from .views import PricesCategoryDetailView, PricesMonthlyView, PricesYearlyView

urlpatterns = [
    path("prices/category/<str:categoryId>", PricesCategoryDetailView.as_view(), name="prices-category-detail"),
    path("prices/monthly", PricesMonthlyView.as_view(), name="prices-monthly"),
    path("prices/yearly", PricesYearlyView.as_view(), name="prices-yearly"),
]
