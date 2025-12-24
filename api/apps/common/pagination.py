from __future__ import annotations

from typing import Any, Dict, List, Tuple

from django.conf import settings  # type: ignore
from rest_framework.exceptions import ValidationError  # type: ignore


def parse_page_params(query_params) -> Tuple[int, int]:
    """Parse and validate pagination parameters.

    - page: integer >= 1
    - page_size: integer in [1, settings.MAX_PAGE_SIZE]

    Unlike a clamping implementation, this function raises a 400 ValidationError
    when parameters are out of range.
    """

    page_raw = query_params.get("page", "1")
    page_size_raw = query_params.get("page_size", str(getattr(settings, "DEFAULT_PAGE_SIZE", 20)))

    try:
        page = int(page_raw)
    except (TypeError, ValueError):
        raise ValidationError({"page": ["must be an integer"]})

    try:
        page_size = int(page_size_raw)
    except (TypeError, ValueError):
        raise ValidationError({"page_size": ["must be an integer"]})

    if page < 1:
        raise ValidationError({"page": ["must be >= 1"]})

    max_page_size = int(getattr(settings, "MAX_PAGE_SIZE", 200))
    if page_size < 1 or page_size > max_page_size:
        raise ValidationError({"page_size": [f"must be between 1 and {max_page_size}"]})

    return page, page_size


def paginate_list(items: List[Any], page: int, page_size: int) -> Dict[str, Any]:
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "items": items[start:end],
        "page": page,
        "page_size": page_size,
        "total": total,
    }
