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

get_env_value() {
  local path="$1"
  local key="$2"
  awk -F= -v k="$key" '$1 == k {print substr($0, index($0, "=") + 1); exit}' "$path"
}

append_env() {
  local path="$1"
  local key="$2"
  local value="$3"
  if grep -q "^${key}=" "$path"; then
    return 0
  fi
  echo "${key}=${value}" >>"$path"
}

write_env() {
  local path="$1"
  local mode="$2" # local | production

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

  local admin_api_key user_api_key device_api_key
  admin_api_key="$(rand 32)"
  user_api_key="$(rand 32)"
  device_api_key="$(rand 32)"

  umask 077
  if [[ -f "$path" && "$FORCE" -ne 1 ]]; then
    local existing_secret existing_debug existing_allowed
    existing_secret="$(get_env_value "$path" "SECRET_KEY")"
    if [[ -z "$existing_secret" ]]; then
      existing_secret="$(get_env_value "$path" "DJANGO_SECRET_KEY")"
    fi
    secret_key="${existing_secret:-$secret_key}"

    existing_debug="$(get_env_value "$path" "DEBUG")"
    if [[ -z "$existing_debug" ]]; then
      existing_debug="$(get_env_value "$path" "DJANGO_DEBUG")"
    fi
    debug="${existing_debug:-$debug}"

    existing_allowed="$(get_env_value "$path" "ALLOWED_HOSTS")"
    if [[ -z "$existing_allowed" ]]; then
      existing_allowed="$(get_env_value "$path" "DJANGO_ALLOWED_HOSTS")"
    fi
    allowed_hosts="${existing_allowed:-$allowed_hosts}"

    append_env "$path" "SECRET_KEY" "$secret_key"
    append_env "$path" "DEBUG" "$debug"
    append_env "$path" "ALLOWED_HOSTS" "$allowed_hosts"
    append_env "$path" "ADMIN_API_KEY" "$admin_api_key"
    append_env "$path" "USER_API_KEY" "$user_api_key"
    append_env "$path" "DEVICE_API_KEY" "$device_api_key"
    echo "Updated: $path"
    return 0
  fi

  cat >"$path" <<EOF
# ============================================================
# Auto-generated: $path
# ============================================================

# ---- PostgreSQL ----
POSTGRES_DB=${pg_db}
POSTGRES_USER=${pg_user}
POSTGRES_PASSWORD=${pg_pass}

# ---- Django ----
SECRET_KEY=${secret_key}
DEBUG=${debug}
ALLOWED_HOSTS=${allowed_hosts}
DJANGO_SECRET_KEY=${secret_key}
DJANGO_DEBUG=${debug}
DJANGO_ALLOWED_HOSTS=${allowed_hosts}

# ---- Token issuance API keys ----
ADMIN_API_KEY=${admin_api_key}
USER_API_KEY=${user_api_key}
DEVICE_API_KEY=${device_api_key}

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
echo "Note: .env.production の ALLOWED_HOSTS（/ DJANGO_ALLOWED_HOSTS）は運用DDNS名に必ず置き換えてください。"
