from __future__ import annotations

from dataclasses import dataclass
import time


@dataclass
class DetectionEvent:
    detected_at: float
    value_mv: int


class PassDetector:
    def __init__(
        self,
        threshold_on_mv: int,
        threshold_off_mv: int,
        ema_alpha: float,
        consecutive_on: int,
        consecutive_off: int,
        min_active_duration_s: float,
        min_gap_s: float,
    ) -> None:
        if threshold_off_mv >= threshold_on_mv:
            raise ValueError("threshold_off_mv must be < threshold_on_mv")
        self._th_on = threshold_on_mv
        self._th_off = threshold_off_mv
        self._alpha = ema_alpha
        self._consec_on = max(1, consecutive_on)
        self._consec_off = max(1, consecutive_off)
        self._min_active = max(0.0, min_active_duration_s)
        self._min_gap = max(0.0, min_gap_s)

        self._ema: float | None = None
        self._state = "idle"  # idle | active
        self._on_hits = 0
        self._off_hits = 0
        self._active_since: float | None = None
        self._last_event_at: float = 0.0

    def update(self, value_mv: int, now: float | None = None) -> DetectionEvent | None:
        t = time.time() if now is None else now

        if self._ema is None:
            self._ema = float(value_mv)
        else:
            self._ema = self._alpha * float(value_mv) + (1.0 - self._alpha) * self._ema

        v = int(self._ema)

        if self._state == "idle":
            if v >= self._th_on:
                self._on_hits += 1
            else:
                self._on_hits = 0

            if self._on_hits >= self._consec_on and (t - self._last_event_at) >= self._min_gap:
                self._state = "active"
                self._active_since = t
                self._off_hits = 0
                self._on_hits = 0
                return DetectionEvent(detected_at=t, value_mv=v)

        else:  # active
            if v <= self._th_off:
                self._off_hits += 1
            else:
                self._off_hits = 0

            if self._off_hits >= self._consec_off:
                active_since = self._active_since or t
                if (t - active_since) >= self._min_active:
                    self._last_event_at = active_since
                self._state = "idle"
                self._active_since = None
                self._off_hits = 0

        return None
