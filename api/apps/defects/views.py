from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore

from apps.common.responses import success_envelope
from apps.common.pagination import parse_page_params, paginate_list
from apps.common.permissions import RoleAdminOnly, RoleAtLeastUser

from .serializers import DefectsAddRequestSerializer, DefectsRecordSerializer
from . import services

class DefectsAmountAddView(APIView):
    # CSV権限未記載: 暫定で device|admin を許可
    from apps.devices.permissions import RoleDeviceOrAdmin
    permission_classes = [RoleDeviceOrAdmin]

    def post(self, request):
        ser = DefectsAddRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        rec = services.add_record(ser.validated_data)
        return Response(success_envelope(request, DefectsRecordSerializer(rec).data), status=status.HTTP_201_CREATED)

class DefectsAmountWeeklyView(APIView):
    permission_classes = [RoleAtLeastUser]
    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_amount("weekly")
        return Response(success_envelope(request, paginate_list(items, page, page_size)), status=status.HTTP_200_OK)

class DefectsAmountMonthlyView(APIView):
    permission_classes = [RoleAtLeastUser]
    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_amount("monthly")
        return Response(success_envelope(request, paginate_list(items, page, page_size)), status=status.HTTP_200_OK)

class DefectsRatioWeeklyView(APIView):
    permission_classes = [RoleAtLeastUser]
    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_ratio("weekly")
        return Response(success_envelope(request, paginate_list(items, page, page_size)), status=status.HTTP_200_OK)

class DefectsRatioMonthlyView(APIView):
    permission_classes = [RoleAtLeastUser]
    def get(self, request):
        page, page_size = parse_page_params(request.query_params)
        items = services.list_ratio("monthly")
        return Response(success_envelope(request, paginate_list(items, page, page_size)), status=status.HTTP_200_OK)
