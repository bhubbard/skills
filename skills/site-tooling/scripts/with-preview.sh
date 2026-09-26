#!/usr/bin/env bash
# Boots `astro preview` against the current dist/ build, waits for it to
# respond with a real 200, runs the given command against it, then always
# tears the server down again — regardless of whether that command passed
# or failed.
#
# Used by local test:a11y, test:a11y:themes, and audit:lighthouse scripts so
# neither one needs an extra "run this alongside a dev server" npm dependency.
#
# Usage: ./scripts/with-preview.sh <command> [args...]
set -uo pipefail

PORT="${PREVIEW_PORT:-4321}"
URL="http://localhost:${PORT}/"
LOG="$(mktemp)"

# Bail early and loudly if the port is already taken — most commonly `astro
# dev` left running in another terminal.
if command -v lsof >/dev/null && lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Port $PORT is already in use — stop whatever is running there first" >&2
  echo "(commonly \`npm run dev\` left open in another terminal). Details:" >&2
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >&2
  exit 1
fi

npm run preview -- --port "$PORT" >"$LOG" 2>&1 &
SERVER_PID=$!

cleanup() {
  kill "$SERVER_PID" >/dev/null 2>&1
  wait "$SERVER_PID" 2>/dev/null
  rm -f "$LOG"
}
trap cleanup EXIT INT TERM

echo "Waiting for preview server at $URL ..."
for _ in $(seq 1 30); do
  code=$(curl -s -o /dev/null -w "%{http_code}" -m 2 "$URL")
  if [ "$code" = "200" ]; then
    echo "Preview server is up. Running: $*"
    "$@"
    exit $?
  fi
  sleep 1
done

echo "Preview server did not respond 200 within 30s (last status: ${code:-none}). Server log:" >&2
cat "$LOG" >&2
exit 1
