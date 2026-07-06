"""Clé Mistral — .env gitignoré."""

import os
import re
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / ".env"


def _parse_env(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip("'\"")
    return out


def _render_env(data: dict[str, str]) -> str:
    lines = [
        "# Devstral Lab — secrets locaux (NE PAS committer)",
        "",
    ]
    order = [
        "MISTRAL_API_KEY",
        "DEVSTRAL_RATE_INTERVAL_SEC",
        "CODESTRAL_RATE_INTERVAL_SEC",
        "LAB_PORT",
    ]
    seen: set[str] = set()
    for k in order:
        if k in data:
            lines.append(f"{k}={data[k]}")
            seen.add(k)
    for k, v in sorted(data.items()):
        if k not in seen:
            lines.append(f"{k}={v}")
    lines.append("")
    return "\n".join(lines)


def load_key() -> str:
    return os.getenv("MISTRAL_API_KEY", "")


def save_key(api_key: str) -> Path:
    key = api_key.strip()
    if len(key) < 20:
        raise ValueError("Clé trop courte — vérifie sur console.mistral.ai")
    existing = _parse_env(ENV_PATH.read_text(encoding="utf-8")) if ENV_PATH.exists() else {}
    existing["MISTRAL_API_KEY"] = key
    existing.setdefault("DEVSTRAL_RATE_INTERVAL_SEC", "30")
    existing.setdefault("CODESTRAL_RATE_INTERVAL_SEC", "20")
    ENV_PATH.write_text(_render_env(existing), encoding="utf-8")
    os.chmod(ENV_PATH, 0o600)
    os.environ["MISTRAL_API_KEY"] = key
    return ENV_PATH


async def validate_key(api_key: str) -> bool:
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.get(
            "https://api.mistral.ai/v1/models",
            headers={"Authorization": f"Bearer {api_key.strip()}"},
        )
        if r.status_code == 401:
            raise ValueError("Clé refusée (401) — console.mistral.ai")
        r.raise_for_status()
        return True