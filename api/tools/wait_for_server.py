import os
import sys
import time
import urllib.request

def main() -> int:
    url = os.getenv("BASE_URL", "http://127.0.0.1:8000").rstrip("/") + "/users?page=1&page_size=1"
    timeout_s = int(os.getenv("WAIT_TIMEOUT", "30"))
    start = time.time()
    while time.time() - start < timeout_s:
        try:
            req = urllib.request.Request(url, method="GET")
            # optional JWT
            token = os.getenv("ADMIN_JWT", "")
            if token:
                req.add_header("Authorization", f"Bearer {token}")
            with urllib.request.urlopen(req, timeout=3) as resp:
                if 200 <= resp.status < 500:
                    return 0
        except Exception:
            time.sleep(0.5)
    print(f"Server not ready: {url}", file=sys.stderr)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
