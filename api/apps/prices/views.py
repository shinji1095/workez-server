from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore

from apps.common.responses import success_envelope
from apps.common.pagination import parse_page_params, paginate_list
from apps.common.permissions import RoleAdminOnly

from .serializers import (
    CreatePriceCategoryRequestSerializer,
    UpdatePriceCategoryRequestSerializer,
    PriceRecordSerializer,
)
from . import services

class PricesCategoryDetailView(APIView):
    permission_classes = [RoleAdminOnly]

    def post(self, request, categoryId: str):
        # CSV: POST /prices/category/{categoryId}
        ser = CreatePriceCategoryRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        rec = services.create_price(categoryId, ser.validated_data)
        return Response(success_envelope(request, PriceRecordSerializer(rec).data), status=status.HTTP_201_CREATED)

    def put(self, request, categoryId: str):
        ser = UpdatePriceCategoryRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        rec = services.update_price(categoryId, ser.validated_data)
        return Response(success_envelope(request, PriceRecordSerializer(rec).data), status=status.HTTP_200_OK)

    def delete(self, request, categoryId: str):
        services.delete_price(categoryId)
        return Response(success_envelope(request, {"deleted": True, "category_id": categoryId}), status=status.HTTP_200_OK)

class PricesMonthlyView(APIView):
    permission_classes = [RoleAdminOnly]
    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_monthly()
        return Response(success_envelope(request, paginate_list(items, page, page_size)), status=status.HTTP_200_OK)

class PricesYearlyView(APIView):
    permission_classes = [RoleAdminOnly]
    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_yearly()
        return Response(success_envelope(request, paginate_list(items, page, page_size)), status=status.HTTP_200_OK)
