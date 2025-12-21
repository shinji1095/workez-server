#!/usr/bin/env bash
set -euo pipefail

FORCE=0
if [[ "${1:-}" == "--force" ]]; then
  FORCE=1
fi

rand() {
  local n="${1:-32}"
  if command -v openssl >/dev/null 2>&1; then
    # base64 -> 記号を避けて英数中心に整形
    openssl rand -base64 256 | tr -dc 'A-Za-z0-9' | head -c "$n"
  elif command -v python3 >/dev/null 2>&1; then
    python3 - <<'PY' "$n"
import secrets, string, sys
n=int(sys.argv[1])
alphabet=string.ascii_letters+string.digits
print(''.join(secrets.choice(alphabet) for _ in range(n)))
PY
  else
    # 最後の手段（urandom）
    tr -dc 'A-Za-z0-9' </dev/urandom | head -c "$n"
  fi
}

write_env() {
  local path="$1"
  local mode="$2" # local | production

  if [[ -f "$path" && "$FORCE" -ne 1 ]]; then
    echo "Skip: $path already exists (use --force to overwrite)."
    return 0
  fi

  local pg_db="app"
  local pg_user="app"
  local pg_pass
  pg_pass="$(rand 24)"

  local secret_key
  secret_key="$(rand 64)"

  local debug allowed_hosts
  if [[ "$mode" == "local" ]]; then
    debug="1"
    allowed_hosts="localhost,127.0.0.1,0.0.0.0"
  else
    debug="0"
    # DDNSや運用ホスト名に置き換えてください
    allowed_hosts="your-ddns.example.com"
  fi

  umask 077
  cat >"$path" <<EOF
# ============================================================
# Auto-generated: $path
# ============================================================

# ---- PostgreSQL ----
POSTGRES_DB=${pg_db}
POSTGRES_USER=${pg_user}
POSTGRES_PASSWORD=${pg_pass}

# ---- Django ----
DJANGO_SECRET_KEY=${secret_key}
DJANGO_DEBUG=${debug}
DJANGO_ALLOWED_HOSTS=${allowed_hosts}

# ---- Gunicorn (used in compose command) ----
GUNICORN_WORKERS=3
GUNICORN_TIMEOUT=60
EOF

  chmod 600 "$path" || true
  echo "Wrote: $path"
}

write_env ".env.local" "local"
write_env ".env.production" "production"

echo "Done."
echo "Note: .env.production の DJANGO_ALLOWED_HOSTS は運用DDNS名に必ず置き換えてください。"
