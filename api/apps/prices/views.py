from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.exceptions import ValidationError  # type: ignore

from apps.common.responses import success_envelope
from apps.common.pagination import parse_page_params, paginate_list
from apps.common.permissions import RoleAdminOnly

from .serializers import (
    PriceRecordSerializer,
    UpsertPricesSizeRankRequestSerializer,
)
from . import services

def _require_int_param(value: str | None, field: str) -> int:
    if value is None:
        raise ValidationError({field: "required"})
    try:
        return int(value)
    except Exception as e:
        raise ValidationError({field: "must be an integer"}) from e


class PricesSizeRankDetailView(APIView):
    permission_classes = [RoleAdminOnly]

    def post(self, request, sizeId: str, rankId: str):
        ser = UpsertPricesSizeRankRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        rec = services.create_price(sizeId, rankId, ser.validated_data)
        return Response(success_envelope(request, PriceRecordSerializer(rec).data), status=status.HTTP_201_CREATED)

    def put(self, request, sizeId: str, rankId: str):
        ser = UpsertPricesSizeRankRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        rec = services.update_price(sizeId, rankId, ser.validated_data)
        return Response(success_envelope(request, PriceRecordSerializer(rec).data), status=status.HTTP_200_OK)

    def delete(self, request, sizeId: str, rankId: str):
        year = _require_int_param(request.query_params.get("year"), "year")
        month = _require_int_param(request.query_params.get("month"), "month")
        services.delete_price(sizeId, rankId, year=year, month=month)
        return Response(
            success_envelope(request, {"deleted": True, "size_id": sizeId, "rank_id": rankId, "year": year, "month": month}),
            status=status.HTTP_200_OK,
        )

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
