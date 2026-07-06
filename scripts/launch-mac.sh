#!/bin/bash
set -euo pipefail

# Repo root, derived from this script's location (portable — works wherever the repo is cloned).
PROJECT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$HOME/Library/Logs/Mistral Bureau"
FRONT_URL="http://127.0.0.1:5177"

mkdir -p "$LOG_DIR"
port_in_use() { lsof -iTCP:"$1" -sTCP:LISTEN -t >/dev/null 2>&1; }
http_ready() { curl -sf --max-time 2 "$1" >/dev/null 2>&1; }

echo ""; echo "  🇫🇷 Mistral Bureau — démarrage"; echo ""

if [[ ! -x "$PROJECT/backend/.venv/bin/uvicorn" ]]; then
  (cd "$PROJECT" && make install)
fi

if port_in_use 8789 && http_ready "http://127.0.0.1:8789/api/health"; then
  echo "  ✓ Backend (:8789)"
else
  echo "  → Backend…"
  (cd "$PROJECT/backend" && nohup .venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8789 >>"$LOG_DIR/backend.log" 2>&1 &)
  for _ in $(seq 1 60); do http_ready "http://127.0.0.1:8789/api/health" && break; sleep 0.5; done
fi

if http_ready "$FRONT_URL"; then
  echo "  ✓ Frontend ($FRONT_URL)"
else
  echo "  → Frontend…"
  (cd "$PROJECT/frontend" && nohup npm run dev >>"$LOG_DIR/frontend.log" 2>&1 &)
  for port in 5177 5178; do
    for _ in $(seq 1 60); do
      if http_ready "http://127.0.0.1:$port/"; then FRONT_URL="http://127.0.0.1:$port"; break 2; fi
      sleep 0.5
    done
  done
fi

HEALTH=$(curl -sf "http://127.0.0.1:8789/api/health" 2>/dev/null || true)
if echo "$HEALTH" | grep -q '"mistral_key": true'; then
  echo "  ✓ Mistral connecté"
else
  echo "  ○ Configure la clé dans l'onboarding"
fi

echo "  → $FRONT_URL"
open "$FRONT_URL"
echo ""; echo "  Appuyez sur Entrée pour fermer (serveurs restent actifs)."; read -r _