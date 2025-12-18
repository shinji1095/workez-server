import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

def _render(s: str) -> str:
    # ${VAR} substitution
    out = s
    for k, v in os.environ.items():
        out = out.replace(f"${{{k}}}", v)
    return out

def run_case(base_url: str, case: Dict[str, Any]) -> bool:
    method = case.get("method", "GET").upper()
    path = _render(case["path"])
    url = base_url.rstrip("/") + path
    headers = case.get("headers", {})
    headers = {k: _render(v) for k, v in headers.items()}

    cmd = ["curl", "-sS", "-X", method, url, "-H", "Accept: application/json"]
    for k, v in headers.items():
        cmd += ["-H", f"{k}: {v}"]

    payload_file = case.get("payload")
    if payload_file:
        p = Path(payload_file)
        body = p.read_text(encoding="utf-8")
        cmd += ["-H", "Content-Type: application/json", "--data", body]

    expected_status = int(case.get("expect_status", 200))

    # Use -w to capture status code
    cmd2 = cmd + ["-w", "\n%{http_code}\n"]
    proc = subprocess.run(cmd2, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr)
        return False

    stdout = proc.stdout
    # last line is status
    lines = stdout.rstrip("\n").split("\n")
    got_status = int(lines[-1])
    body_text = "\n".join(lines[:-1])

    ok = got_status == expected_status
    print(f"[{ 'OK' if ok else 'NG' }] {method} {path} -> {got_status} (expect {expected_status})")
    if not ok or case.get("print_body", False):
        print(body_text[:2000])
    return ok

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python e2e/run_curl_suite.py <suite.json>")
        return 2

    suite_path = Path(sys.argv[1])
    suite = json.loads(suite_path.read_text(encoding="utf-8"))

    base_url = _render(suite.get("base_url") or os.getenv("BASE_URL", "http://127.0.0.1:8000"))
    cases = suite.get("cases", [])
    if not cases:
        print("No cases in suite")
        return 2

    all_ok = True
    for case in cases:
        ok = run_case(base_url, case)
        all_ok = all_ok and ok

    return 0 if all_ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
