"""Issue a JWT for local development / E2E.

This project uses a lightweight JWT auth implementation (see /auth/token).
Tokens are signed with settings.JWT_SIGNING_KEY (default: SECRET_KEY).

Usage:
  export DJANGO_SETTINGS_MODULE=config.settings.local
  export ENV_FILE=.env.local
  python tools/issue_jwt.py --role admin --sub admin_001
"""

from __future__ import annotations

import argparse
import os

import django


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", required=True, choices=["admin", "user", "device"])
    parser.add_argument("--sub", required=True)
    parser.add_argument("--ttl", type=int, default=3600)
    args = parser.parse_args()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    django.setup()

    from apps.common.auth import issue_jwt  # noqa: WPS433

    print(issue_jwt(sub=args.sub, role=args.role, lifetime_seconds=args.ttl))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
