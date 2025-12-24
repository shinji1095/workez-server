from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional


def setup_logging(
    log_dir: Path,
    boot_ts: str,
    file_level: str = "INFO",
    console_level: str = "INFO",
    enable_console: bool = False,
) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("workez_device")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()
    logger.propagate = False

    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

    fh = logging.FileHandler(log_dir / f"{boot_ts}.log", encoding="utf-8")
    fh.setLevel(getattr(logging, file_level.upper(), logging.INFO))
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    if enable_console:
        sh = logging.StreamHandler()
        sh.setLevel(getattr(logging, console_level.upper(), logging.INFO))
        sh.setFormatter(fmt)
        logger.addHandler(sh)

    return logger
