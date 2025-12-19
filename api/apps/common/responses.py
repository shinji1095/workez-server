from typing import Any, Dict
from rest_framework.request import Request  # type: ignore

def success_envelope(request: Request, data: Any) -> Dict[str, Any]:
    request_id = getattr(request, "request_id", None)
    body: Dict[str, Any] = {"status": "success", "data": data}
    if request_id:
        body["request_id"] = request_id
    return body

def error_envelope(request: Request, code: str, message: str, details: list) -> Dict[str, Any]:
    request_id = getattr(request, "request_id", None)
    err = {
        "code": code,
        "message": message,
        "details": details,
        "request_id": request_id or "",
    }
    return {"error": err}
