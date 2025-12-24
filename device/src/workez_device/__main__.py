from __future__ import annotations

import argparse
import sys

from .app import WorkezDeviceApp


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to config YAML")
    parser.add_argument("--debug", action="store_true", help="Enable console info logs")
    args = parser.parse_args(argv)

    app = WorkezDeviceApp(config_path=args.config, debug=args.debug)
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
