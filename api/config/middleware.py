import uuid
from django.utils.deprecation import MiddlewareMixin  # type: ignore

class RequestIdMiddleware(MiddlewareMixin):
    """Attach a request_id to each request for traceability."""

    def process_request(self, request):
        request.request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
