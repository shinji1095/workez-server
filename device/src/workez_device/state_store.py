from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json


@dataclass
class DeviceState:
    pending_count: int = 0
    pending_event_id: str = ""


class StateStore:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> DeviceState:
        if not self._path.exists():
            return DeviceState()
        data = json.loads(self._path.read_text(encoding="utf-8"))
        return DeviceState(
            pending_count=int(data.get("pending_count", 0)),
            pending_event_id=str(data.get("pending_event_id", "")),
        )

    def save(self, state: DeviceState) -> None:
        tmp = self._path.with_suffix(".tmp")
        tmp.write_text(
            json.dumps(
                {"pending_count": state.pending_count, "pending_event_id": state.pending_event_id},
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        tmp.replace(self._path)
