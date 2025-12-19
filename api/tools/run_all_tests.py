import os
import subprocess
import sys

def run(cmd: list[str]) -> int:
    print(" ".join(cmd))
    proc = subprocess.run(cmd)
    return proc.returncode

def main() -> int:
    # unit + integration (pytest) then e2e local
    rc = run([sys.executable, "-m", "pytest", "-q"])
    if rc != 0:
        return rc

    base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000")
    suite = "e2e/suites/local.json"
    rc = run([sys.executable, "e2e/run_curl_suite.py", suite])
    return rc

if __name__ == "__main__":
    raise SystemExit(main())
