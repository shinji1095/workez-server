from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class JwtConfig:
    token: str
    header_prefix: str = "Bearer"
    token_url: str = ""
    api_key: str = ""
    api_key_header: str = "X-API-KEY"
    api_key_prefix: str = ""
    sub: str = ""
    token_json_field: str = "data.access_token"
    expires_in_json_field: str = "data.expires_in"
    refresh_margin_s: int = 60


@dataclass(frozen=True)
class ServerConfig:
    base_url: str
    harvest_add_path: str
    request_timeout_s: float
    jwt: JwtConfig


@dataclass(frozen=True)
class DeviceConfig:
    device_id: str
    category_id: str


@dataclass(frozen=True)
class SerialConfig:
    port: str
    baudrate: int
    read_timeout_s: float
    reconnect_interval_s: float


@dataclass(frozen=True)
class DetectorConfig:
    threshold_on_mv: int
    threshold_off_mv: int
    ema_alpha: float
    consecutive_on: int
    consecutive_off: int
    min_active_duration_s: float
    min_gap_s: float


@dataclass(frozen=True)
class SenderConfig:
    send_interval_s: float


@dataclass(frozen=True)
class StateConfig:
    dir: str
    file: str


@dataclass(frozen=True)
class LoggingConfig:
    dir: str
    file_level: str
    console_level: str


@dataclass(frozen=True)
class AppConfig:
    server: ServerConfig
    device: DeviceConfig
    serial: SerialConfig
    detector: DetectorConfig
    sender: SenderConfig
    state: StateConfig
    logging: LoggingConfig


def _get(d: dict[str, Any], key: str) -> Any:
    if key not in d:
        raise KeyError(f"Missing config key: {key}")
    return d[key]


def load_config(path: str | Path) -> AppConfig:
    p = Path(path)
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Config YAML root must be a mapping")

    server = _get(data, "server")
    device = _get(data, "device")
    serial = _get(data, "serial")
    detector = _get(data, "detector")
    sender = _get(data, "sender")
    state = _get(data, "state")
    logging = _get(data, "logging")

    jwt = server.get("jwt", {})
    jwt_cfg = JwtConfig(
        token=str(jwt.get("token", "")),
        header_prefix=str(jwt.get("header_prefix", "Bearer")),
        token_url=str(jwt.get("token_url", "")),
        api_key=str(jwt.get("api_key", "")),
        api_key_header=str(jwt.get("api_key_header", "X-API-KEY")),
        api_key_prefix=str(jwt.get("api_key_prefix", "")),
        sub=str(jwt.get("sub", "")),
        token_json_field=str(jwt.get("token_json_field", "data.access_token")),
        expires_in_json_field=str(jwt.get("expires_in_json_field", "data.expires_in")),
        refresh_margin_s=int(jwt.get("refresh_margin_s", 60)),
    )

    return AppConfig(
        server=ServerConfig(
            base_url=str(_get(server, "base_url")).rstrip("/"),
            harvest_add_path=str(_get(server, "harvest_add_path")),
            request_timeout_s=float(_get(server, "request_timeout_s")),
            jwt=jwt_cfg,
        ),
        device=DeviceConfig(
            device_id=str(_get(device, "device_id")),
            category_id=str(_get(device, "category_id")),
        ),
        serial=SerialConfig(
            port=str(_get(serial, "port")),
            baudrate=int(_get(serial, "baudrate")),
            read_timeout_s=float(_get(serial, "read_timeout_s")),
            reconnect_interval_s=float(_get(serial, "reconnect_interval_s")),
        ),
        detector=DetectorConfig(
            threshold_on_mv=int(_get(detector, "threshold_on_mv")),
            threshold_off_mv=int(_get(detector, "threshold_off_mv")),
            ema_alpha=float(_get(detector, "ema_alpha")),
            consecutive_on=int(_get(detector, "consecutive_on")),
            consecutive_off=int(_get(detector, "consecutive_off")),
            min_active_duration_s=float(_get(detector, "min_active_duration_s")),
            min_gap_s=float(_get(detector, "min_gap_s")),
        ),
        sender=SenderConfig(send_interval_s=float(_get(sender, "send_interval_s"))),
        state=StateConfig(dir=str(_get(state, "dir")), file=str(_get(state, "file"))),
        logging=LoggingConfig(
            dir=str(_get(logging, "dir")),
            file_level=str(_get(logging, "file_level")),
            console_level=str(_get(logging, "console_level")),
        ),
    )
