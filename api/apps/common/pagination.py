from typing import Any, Dict, List, Tuple
from django.conf import settings  # type: ignore

def parse_page_params(query_params) -> Tuple[int, int]:
    try:
        page = int(query_params.get("page", 1))
    except Exception:
        page = 1
    try:
        page_size = int(query_params.get("page_size", settings.DEFAULT_PAGE_SIZE))
    except Exception:
        page_size = settings.DEFAULT_PAGE_SIZE
    page = max(1, page)
    page_size = max(1, min(settings.MAX_PAGE_SIZE, page_size))
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
