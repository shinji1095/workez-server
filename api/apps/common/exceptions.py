from __future__ import annotations
from typing import Any, Dict, List, Optional
from rest_framework.views import exception_handler as drf_exception_handler  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.exceptions import APIException, ValidationError, NotAuthenticated, PermissionDenied, NotFound  # type: ignore
from django.db import IntegrityError  # type: ignore

from .responses import error_envelope

def _details_from_validation(detail: Any) -> List[Dict[str, Any]]:
    details: List[Dict[str, Any]] = []
    if isinstance(detail, dict):
        for field, msg in detail.items():
            # msg could be list or string
            if isinstance(msg, list):
                for m in msg:
                    details.append({"field": str(field), "reason": str(m), "value": None})
            else:
                details.append({"field": str(field), "reason": str(msg), "value": None})
    elif isinstance(detail, list):
        for msg in detail:
            details.append({"field": "non_field", "reason": str(msg), "value": None})
    else:
        details.append({"field": "non_field", "reason": str(detail), "value": None})
    return details

def exception_handler(exc: Exception, context: Dict[str, Any]) -> Optional[Response]:
    request = context.get("request")
    request_id = getattr(request, "request_id", None) if request else None

    # Let DRF handle common cases first
    response = drf_exception_handler(exc, context)

    if response is not None and request is not None:
        # Map status to OpenAPI-like error envelope
        http_status = response.status_code

        if http_status == status.HTTP_400_BAD_REQUEST:
            code = "bad_request"
            message = "Bad request"
            details = _details_from_validation(response.data)
        elif http_status == status.HTTP_401_UNAUTHORIZED:
            code = "unauthorized"
            message = "Unauthorized"
            details = []
        elif http_status == status.HTTP_403_FORBIDDEN:
            code = "forbidden"
            message = "Forbidden"
            details = []
        elif http_status == status.HTTP_404_NOT_FOUND:
            code = "not_found"
            message = "Not found"
            details = []
        else:
            code = "error"
            message = "Error"
            details = []

        body = error_envelope(request, code=code, message=message, details=details)
        response.data = body
        return response

    # Non-DRF exceptions
    if request is None:
        return response

    if isinstance(exc, IntegrityError):
        body = error_envelope(request, code="conflict", message="Conflict", details=[])
        return Response(body, status=status.HTTP_409_CONFLICT)

    body = error_envelope(request, code="internal_server_error", message="Internal server error", details=[])
    return Response(body, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
