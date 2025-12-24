from __future__ import annotations

from typing import Any, Dict

from rest_framework.request import Request  # type: ignore


def success_envelope(request: Request, data: Any) -> Dict[str, Any]:
    """Return the standard success envelope."""

    request_id = getattr(request, "request_id", None)
    body: Dict[str, Any] = {"status": "success", "data": data}
    if request_id:
        body["request_id"] = request_id
    return body


def error_envelope(request: Request, code: str, message: str, details: list) -> Dict[str, Any]:
    """Return the standard error envelope."""

    request_id = getattr(request, "request_id", None)
    err = {
        "code": code,
        "message": message,
        "details": details,
        "request_id": request_id or "",
    }
    return {"error": err}


# -----------------------------------------------------------------------------
# Backward-compatible aliases
# -----------------------------------------------------------------------------

def success_response(request: Request, data: Any) -> Dict[str, Any]:
    """Alias for success_envelope.

    Some modules historically imported `success_response`.
    """

    return success_envelope(request, data)


def error_response(
    request: Request,
    code: str,
    message: str,
    details: list[dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    """Alias for error_envelope.

    Some modules historically imported `error_response`.
    """

    return error_envelope(request, code, message, details or [])
