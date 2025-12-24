from __future__ import annotations

import base64
import json
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
    def __init__(
        self,
        token: str,
        header_prefix: str = "Bearer",
        token_url: str = "",
        api_key: str = "",
        api_key_header: str = "X-API-KEY",
        api_key_prefix: str = "",
        sub: str = "",
        token_json_field: str = "data.access_token",
        expires_in_json_field: str = "data.expires_in",
        refresh_margin_s: int = 60,
        timeout_s: float = 5.0,
    ) -> None:
        self._token = token.strip()
        self._prefix = header_prefix.strip() or "Bearer"
        self._token_url = token_url.strip()
        self._api_key = api_key.strip()
        self._api_key_header = api_key_header.strip() or "X-API-KEY"
        self._api_key_prefix = api_key_prefix.strip()
        self._sub = sub.strip()
        self._token_json_field = token_json_field.strip() or "data.access_token"
        self._expires_in_json_field = expires_in_json_field.strip() or "data.expires_in"
        self._refresh_margin_s = int(refresh_margin_s)
        self._timeout_s = float(timeout_s)
        self._expires_at = _jwt_exp_from_token(self._token) or 0
        self._sess = requests.Session()

    def get_auth_header(self) -> dict[str, str]:
        self._ensure_token()
        if not self._token:
            raise RuntimeError(
                "JWT token is empty. Fill server.jwt.token or token_url/api_key/sub in config."
            )
        return {"Authorization": f"{self._prefix} {self._token}"}

    def _ensure_token(self) -> None:
        if not self._token_url:
            return

        now = int(time.time())
        if self._token and self._expires_at and now < (self._expires_at - self._refresh_margin_s):
            return

        self._issue_token()

    def _issue_token(self) -> None:
        if not self._api_key or not self._sub:
            raise RuntimeError("token_url is set but api_key/sub are missing.")

        headers = {"Content-Type": "application/json"}
        if self._api_key_prefix:
            headers[self._api_key_header] = f"{self._api_key_prefix} {self._api_key}"
        else:
            headers[self._api_key_header] = self._api_key

        payload = {"sub": self._sub}
        try:
            r = self._sess.post(
                self._token_url, json=payload, headers=headers, timeout=self._timeout_s
            )
        except Exception as e:
            raise RuntimeError(f"token request failed: {e}") from e

        if not (200 <= r.status_code < 300):
            raise RuntimeError(f"token request failed: status={r.status_code} body={r.text[:200]}")

        try:
            body = r.json()
        except Exception as e:
            raise RuntimeError("token response is not valid JSON") from e

        token = _json_path(body, self._token_json_field)
        if not token:
            raise RuntimeError("token response missing access token.")

        self._token = str(token).strip()
        expires_in = _json_path(body, self._expires_in_json_field)
        if isinstance(expires_in, (int, float)):
            self._expires_at = int(time.time()) + int(expires_in)
        else:
            self._expires_at = _jwt_exp_from_token(self._token) or 0


def _json_path(payload: dict[str, Any], path: str) -> Any:
    cur: Any = payload
    if not path:
        return None
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _jwt_exp_from_token(token: str) -> Optional[int]:
    parts = token.split(".")
    if len(parts) < 2:
        return None

    payload_b64 = parts[1]
    padding = "=" * (-len(payload_b64) % 4)
    try:
        payload_raw = base64.urlsafe_b64decode(payload_b64 + padding)
        payload = json.loads(payload_raw.decode("utf-8"))
    except Exception:
        return None

    exp = payload.get("exp")
    if isinstance(exp, (int, float)):
        return int(exp)
    return None


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
