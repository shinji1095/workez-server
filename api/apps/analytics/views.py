from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore

from apps.common.responses import success_envelope
from apps.common.pagination import parse_page_params, paginate_list
from apps.common.permissions import RoleAdminOnly

from . import services

class AnalyticsHarvestMonthlyView(APIView):
    permission_classes = [RoleAdminOnly]
    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_harvest_monthly_forecast()
        return Response(success_envelope(request, paginate_list(items, page, page_size)), status=status.HTTP_200_OK)

class AnalyticsRevenueMonthlyView(APIView):
    permission_classes = [RoleAdminOnly]
    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_revenue_monthly()
        return Response(success_envelope(request, paginate_list(items, page, page_size)), status=status.HTTP_200_OK)

class AnalyticsRevenueYearlyView(APIView):
    permission_classes = [RoleAdminOnly]
    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_revenue_yearly()
        return Response(success_envelope(request, paginate_list(items, page, page_size)), status=status.HTTP_200_OK)
