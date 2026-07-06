#!/bin/bash
# Benchmark Bureau JD (3 runs, rate-gate Large 30s)
set -euo pipefail
API="http://127.0.0.1:8789/api/run"
INPUT='Alternance développeur IA full-stack React Python Bordeaux 2026'
N=3
TMP=$(mktemp)
for i in $(seq 1 $N); do
  RESP=$(curl -sf -X POST "$API" -H "Content-Type: application/json" \
    -d "{\"agent_id\":\"jd\",\"input\":\"$INPUT\"}") || { echo "fail $i"; continue; }
  echo "$RESP" | python3 -c "import sys,json; print(int(float(json.load(sys.stdin).get('latency_ms',0))))" >> "$TMP"
  echo "  run $i done"
  [[ $i -lt $N ]] && sleep 31
done
python3 -c "
import pathlib
v=sorted(int(x) for x in pathlib.Path('$TMP').read_text().split() if x.strip())
print(f'n={len(v)} P50={v[len(v)//2]} min={min(v)} max={max(v)}' if v else 'NO_DATA')
"
rm -f "$TMP"