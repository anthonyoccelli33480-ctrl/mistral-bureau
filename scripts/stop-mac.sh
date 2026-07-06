#!/bin/bash
for port in 8789 5177 5178; do
  pids=$(lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null || true)
  [[ -n "$pids" ]] && kill $pids 2>/dev/null || true
done
echo "  ✓ Mistral Bureau arrêté"
read -r _