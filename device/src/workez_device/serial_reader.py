from __future__ import annotations

from dataclasses import dataclass
import json
import time
from typing import Iterator, Optional

import serial  # type: ignore


@dataclass(frozen=True)
class SensorSample:
    ts_ms: int
    voltage_mv: int
    raw: int | None = None


class SerialSensorReader:
    def __init__(self, port: str, baudrate: int, timeout_s: float) -> None:
        self._port = port
        self._baudrate = baudrate
        self._timeout_s = timeout_s
        self._ser: serial.Serial | None = None

    def open(self) -> None:
        self._ser = serial.Serial(self._port, self._baudrate, timeout=self._timeout_s)

    def close(self) -> None:
        if self._ser is not None:
            try:
                self._ser.close()
            finally:
                self._ser = None

    def __iter__(self) -> Iterator[SensorSample]:
        if self._ser is None:
            raise RuntimeError("Serial port is not open")

        while True:
            line = self._ser.readline()
            if not line:
                continue
            try:
                s = line.decode("utf-8", errors="ignore").strip()
                if not s:
                    continue
                obj = json.loads(s)
                ts_ms = int(obj.get("ts_ms", 0))
                voltage_mv = int(obj.get("voltage_mv"))
                raw = obj.get("raw")
                raw_i = int(raw) if raw is not None else None
                yield SensorSample(ts_ms=ts_ms, voltage_mv=voltage_mv, raw=raw_i)
            except Exception:
                # ignore malformed line
                continue
