"""Mistral Bureau — API backend multi-modèles (Large, Ministral, Devstral, Pixtral)."""

import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.agents import get_agent, list_agents
from app.agents.guides import get_guide
from app.mistral_client import chat, parse_json
from app.rate_gate import acquire, intervals, next_available_in
from app.secrets import ENV_PATH, load_key, save_key, validate_key

_root = Path(__file__).resolve().parents[2]
load_dotenv(_root / ".env")
load_dotenv(_root.parent / "jarvis-os" / ".env")
load_dotenv(_root.parent / "devstral-lab" / ".env")

LAB_PORT = int(os.getenv("LAB_PORT", "8789"))

app = FastAPI(title="Mistral Bureau", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5177",
        "http://127.0.0.1:5177",
        "http://localhost:5178",
        "http://127.0.0.1:5178",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    agent_id: str
    input: str = Field(default="", max_length=80_000)
    images: list[str] = Field(default_factory=list, max_length=5)


class SetupKeyRequest(BaseModel):
    api_key: str = Field(..., min_length=20, max_length=256)


class RunResponse(BaseModel):
    agent_id: str
    agent_name: str
    model: str
    result: dict
    latency_ms: float
    queue_wait_ms: float
    rate_headers: dict[str, str]
    next_available_in_sec: float
    how_to: list[str] = []
    next_steps: list[str] = []


@app.get("/api/health")
async def health():
    has_key = bool(load_key())
    return {
        "ok": has_key,
        "mistral_key": has_key,
        "env_file": str(ENV_PATH),
        "port": LAB_PORT,
        "next_available_in_sec": round(next_available_in(), 1),
        "rate_intervals": intervals(),
    }


@app.post("/api/setup/key")
async def setup_key(req: SetupKeyRequest):
    try:
        await validate_key(req.api_key)
        path = save_key(req.api_key)
        return {"ok": True, "message": "Clé Mistral validée.", "path": str(path)}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except httpx.HTTPStatusError as e:
        raise HTTPException(502, f"Mistral inaccessible : {e.response.status_code}")
    except Exception as e:
        raise HTTPException(502, str(e))


@app.get("/api/agents")
async def agents():
    return {"agents": list_agents()}


@app.post("/api/run", response_model=RunResponse)
async def run(req: RunRequest):
    try:
        agent = get_agent(req.agent_id)
    except KeyError:
        raise HTTPException(404, f"Agent '{req.agent_id}' introuvable")

    if agent.requires_image and not req.images:
        raise HTTPException(400, "Cet agent Pixtral requiert au moins une image (PNG/JPEG).")
    if not agent.requires_image and len(req.input.strip()) < 3:
        raise HTTPException(400, "Texte trop court (min 3 caractères).")
    if len(req.images) > agent.max_images:
        raise HTTPException(400, f"Maximum {agent.max_images} images.")

    for url in req.images:
        if not url.startswith("data:image/"):
            raise HTTPException(400, "Images : data URI base64 PNG/JPEG uniquement.")

    wait = await acquire(agent.model)
    try:
        raw, latency, rate_hdrs = await chat(
            model=agent.model,
            system=agent.system,
            user=req.input.strip() or "Analyse l'image fournie.",
            images=req.images or None,
            max_tokens=agent.max_tokens,
            temperature=agent.temperature,
            json_mode=True,
        )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            raise HTTPException(429, "Rate limit Mistral — le gate local est actif, réessaie.")
        raise HTTPException(e.response.status_code, e.response.text[:500])
    except Exception as e:
        if "429" in str(e):
            raise HTTPException(429, "Rate limit Mistral")
        raise HTTPException(502, str(e))

    try:
        result = parse_json(raw)
    except ValueError as e:
        raise HTTPException(502, str(e))

    guide = get_guide(agent.id)
    return RunResponse(
        agent_id=agent.id,
        agent_name=agent.name,
        model=agent.model,
        result=result,
        latency_ms=round(latency * 1000, 1),
        queue_wait_ms=round(wait * 1000, 1),
        rate_headers=rate_hdrs,
        next_available_in_sec=round(next_available_in(agent.model), 1),
        how_to=guide["how_to"],
        next_steps=guide["next_steps"],
    )