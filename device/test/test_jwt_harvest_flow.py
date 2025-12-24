import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from workez_device.sender import HarvestSender, JwtProvider


class FakeResponse:
    def __init__(self, status_code: int, json_data: dict, text: str = "") -> None:
        self.status_code = status_code
        self._json = json_data
        self.text = text

    def json(self) -> dict:
        return self._json


class FakeSession:
    def __init__(self) -> None:
        self.calls = []
        self.issued_token = "device.jwt.token"

    def post(self, url, json=None, headers=None, timeout=None):
        self.calls.append(
            {
                "url": url,
                "json": json,
                "headers": headers or {},
                "timeout": timeout,
            }
        )

        if url.endswith("/auth/token"):
            payload = {
                "status": "success",
                "data": {
                    "access_token": self.issued_token,
                    "token_type": "Bearer",
                    "expires_in": 3600,
                    "sub": json.get("sub") if isinstance(json, dict) else None,
                    "role": "device",
                },
            }
            return FakeResponse(200, payload, text="ok")

        if url.endswith("/harvest/amount/add"):
            return FakeResponse(201, {"status": "success", "data": {}}, text="created")

        return FakeResponse(404, {"error": "not found"}, text="not found")


class JwtFlowTest(unittest.TestCase):
    def test_device_fetches_token_and_sends_harvest(self) -> None:
        session = FakeSession()
        with patch("workez_device.sender.requests.Session", return_value=session):
            jwt = JwtProvider(
                token="",
                header_prefix="Bearer",
                token_url="http://api.local/auth/token",
                api_key="device-key",
                api_key_header="X-API-KEY",
                api_key_prefix="",
                sub="device-1",
                token_json_field="data.access_token",
                expires_in_json_field="data.expires_in",
                refresh_margin_s=60,
                timeout_s=5.0,
            )
            sender = HarvestSender(
                base_url="http://api.local",
                path="/harvest/amount/add",
                jwt=jwt,
                timeout_s=5.0,
            )

            result = sender.send_increment(
                event_id="event-1",
                device_id="D1",
                category_id="C1",
                count=1,
            )

        self.assertTrue(result.ok)
        self.assertEqual(result.status_code, 201)
        self.assertEqual(len(session.calls), 2)

        token_call = session.calls[0]
        self.assertEqual(token_call["url"], "http://api.local/auth/token")
        self.assertEqual(token_call["headers"]["X-API-KEY"], "device-key")
        self.assertEqual(token_call["json"]["sub"], "device-1")

        harvest_call = session.calls[1]
        self.assertEqual(harvest_call["url"], "http://api.local/harvest/amount/add")
        self.assertEqual(
            harvest_call["headers"]["Authorization"],
            f"Bearer {session.issued_token}",
        )


if __name__ == "__main__":
    unittest.main()
