from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional

import requests


@dataclass
class SendResult:
    ok: bool
    status_code: int | None = None
    error: str | None = None


class JwtProvider:
    def __init__(self, token: str, header_prefix: str = "Bearer") -> None:
        self._token = token.strip()
        self._prefix = header_prefix.strip() or "Bearer"

    def get_auth_header(self) -> dict[str, str]:
        if not self._token:
            raise RuntimeError("JWT token is empty. Fill server.jwt.token in config.")
        return {"Authorization": f"{self._prefix} {self._token}"}


class HarvestSender:
    def __init__(self, base_url: str, path: str, jwt: JwtProvider, timeout_s: float) -> None:
        self._url = base_url.rstrip("/") + path
        self._jwt = jwt
        self._timeout_s = timeout_s
        self._sess = requests.Session()

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).astimezone().isoformat()

    def send_increment(
        self,
        *,
        event_id: str,
        device_id: str,
        category_id: str,
        count: int,
        occurred_at: str | None = None,
    ) -> SendResult:
        payload = {
            "event_id": event_id,
            "device_id": device_id,
            "category_id": category_id,
            "count": int(count),
            "occurred_at": occurred_at or self._now_iso(),
        }
        headers = {"Content-Type": "application/json"}
        headers.update(self._jwt.get_auth_header())

        try:
            r = self._sess.post(self._url, json=payload, headers=headers, timeout=self._timeout_s)
            if 200 <= r.status_code < 300:
                return SendResult(ok=True, status_code=r.status_code)
            return SendResult(ok=False, status_code=r.status_code, error=r.text[:500])
        except Exception as e:
            return SendResult(ok=False, error=str(e))


def new_event_id() -> str:
    return str(uuid.uuid4())
