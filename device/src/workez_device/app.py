from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path

from .config import load_config, AppConfig
from .detector import PassDetector
from .logging_setup import setup_logging
from .sender import HarvestSender, JwtProvider, new_event_id
from .serial_reader import SerialSensorReader
from .state_store import StateStore, DeviceState


class WorkezDeviceApp:
    def __init__(self, config_path: str, debug: bool) -> None:
        self._config_path = config_path
        self._debug = debug

        self._boot_ts = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d_%H%M%S")
        self._cfg: AppConfig | None = None
        self._logger = None

    def run(self) -> int:
        cfg = load_config(self._config_path)
        self._cfg = cfg

        log_dir = Path(cfg.logging.dir)
        logger = setup_logging(
            log_dir=log_dir,
            boot_ts=self._boot_ts,
            file_level=cfg.logging.file_level,
            console_level=cfg.logging.console_level,
            enable_console=self._debug,
        )
        self._logger = logger
        logger.info("boot_ts=%s", self._boot_ts)

        # state
        state_path = Path(cfg.state.dir) / cfg.state.file
        store = StateStore(state_path)
        state = store.load()
        logger.info("loaded state: pending_count=%d pending_event_id=%s", state.pending_count, state.pending_event_id)

        # components
        det = PassDetector(
            threshold_on_mv=cfg.detector.threshold_on_mv,
            threshold_off_mv=cfg.detector.threshold_off_mv,
            ema_alpha=cfg.detector.ema_alpha,
            consecutive_on=cfg.detector.consecutive_on,
            consecutive_off=cfg.detector.consecutive_off,
            min_active_duration_s=cfg.detector.min_active_duration_s,
            min_gap_s=cfg.detector.min_gap_s,
        )

        jwt = JwtProvider(token=cfg.server.jwt.token, header_prefix=cfg.server.jwt.header_prefix)
        sender = HarvestSender(
            base_url=cfg.server.base_url,
            path=cfg.server.harvest_add_path,
            jwt=jwt,
            timeout_s=cfg.server.request_timeout_s,
        )

        next_send_at = time.time() + cfg.sender.send_interval_s

        while True:
            try:
                self._loop_serial(det, sender, store, state, next_send_at)
                # if loop returns, reset next_send_at
                next_send_at = time.time() + cfg.sender.send_interval_s
            except Exception as e:
                logger.exception("fatal loop error: %s", e)
                time.sleep(2.0)

    def _loop_serial(
        self,
        det: PassDetector,
        sender: HarvestSender,
        store: StateStore,
        state: DeviceState,
        next_send_at: float,
    ) -> None:
        assert self._cfg is not None
        assert self._logger is not None
        cfg = self._cfg
        logger = self._logger

        reader = SerialSensorReader(
            port=cfg.serial.port,
            baudrate=cfg.serial.baudrate,
            timeout_s=cfg.serial.read_timeout_s,
        )

        while True:
            try:
                logger.info("opening serial port: %s @%d", cfg.serial.port, cfg.serial.baudrate)
                reader.open()
                break
            except Exception as e:
                logger.warning("serial open failed: %s (retry in %.1fs)", e, cfg.serial.reconnect_interval_s)
                time.sleep(cfg.serial.reconnect_interval_s)

        try:
            for sample in reader:
                now = time.time()

                ev = det.update(sample.voltage_mv, now=now)
                if ev is not None:
                    state.pending_count += 1
                    store.save(state)
                    logger.info("detected: pending_count=%d v=%dmV", state.pending_count, ev.value_mv)

                if now >= next_send_at:
                    next_send_at = now + cfg.sender.send_interval_s
                    self._try_send(sender, store, state)

        finally:
            reader.close()

    def _try_send(self, sender: HarvestSender, store: StateStore, state: DeviceState) -> None:
        assert self._cfg is not None
        assert self._logger is not None
        cfg = self._cfg
        logger = self._logger

        if state.pending_count <= 0:
            logger.info("send skipped (pending_count=0)")
            return

        if not state.pending_event_id:
            state.pending_event_id = new_event_id()
            store.save(state)

        logger.info("sending increment: count=%d event_id=%s", state.pending_count, state.pending_event_id)

        r = sender.send_increment(
            event_id=state.pending_event_id,
            device_id=cfg.device.device_id,
            category_id=cfg.device.category_id,
            count=state.pending_count,
        )

        if r.ok:
            logger.info("send ok: status=%s", r.status_code)
            state.pending_count = 0
            state.pending_event_id = ""
            store.save(state)
            return

        # When timeout occurs, we keep the same event_id for idempotent retry.
        logger.warning("send failed: status=%s err=%s", r.status_code, r.error)
