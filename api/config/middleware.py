import uuid
from django.utils.deprecation import MiddlewareMixin  # type: ignore

class RequestIdMiddleware(MiddlewareMixin):
    """Attach a request_id to each request for traceability."""

    def process_request(self, request):
        rid = request.headers.get("X-Request-ID")
        if rid:
            request.request_id = str(rid)
            return
        request.request_id = f"req_{uuid.uuid4()}"
