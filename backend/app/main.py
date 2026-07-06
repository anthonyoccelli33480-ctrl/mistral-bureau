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
from app.spectrum import SLOTS, SPECTRUM_SYSTEM, recommend, slot_by_id

_root = Path(__file__).resolve().parents[2]
load_dotenv(_root / ".env")
load_dotenv(_root.parent / "jarvis-os" / ".env")
load_dotenv(_root.parent / "devstral-lab" / ".env")

BUREAU_PORT = int(os.getenv("BUREAU_PORT", "8789"))

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


class SpectrumRequest(BaseModel):
    input: str = Field(..., min_length=3, max_length=80_000)


class SpectrumSlotRequest(BaseModel):
    input: str = Field(..., min_length=3, max_length=80_000)
    slot_id: str = Field(..., pattern="^(fast|code|deep)$")


class SpectrumColumn(BaseModel):
    slot: str
    model: str
    label: str
    tagline: str
    result: dict | None = None
    latency_ms: float = 0
    queue_wait_ms: float = 0
    error: str | None = None


class SpectrumResponse(BaseModel):
    input: str
    columns: list[SpectrumColumn]
    recommendation: dict
    total_ms: float
    slots_order: list[str]


@app.get("/api/health")
async def health():
    has_key = bool(load_key())
    return {
        "ok": has_key,
        "mistral_key": has_key,
        "env_file": str(ENV_PATH),
        "port": BUREAU_PORT,
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


@app.get("/api/spectrum/meta")
async def spectrum_meta():
    return {
        "slots": [
            {"id": s.id, "model": s.model, "label": s.label, "tagline": s.tagline}
            for s in SLOTS
        ],
        "estimate_sec": sum(intervals().get(s.model, 20) for s in SLOTS) + 15,
    }


async def _run_spectrum_slot(input_text: str, slot_id: str) -> SpectrumColumn:
    slot = slot_by_id(slot_id)
    wait = await acquire(slot.model)
    try:
        raw, latency, _ = await chat(
            model=slot.model,
            system=SPECTRUM_SYSTEM,
            user=input_text.strip(),
            max_tokens=1536,
            temperature=0.25,
            json_mode=True,
        )
        result = parse_json(raw)
        return SpectrumColumn(
            slot=slot.id,
            model=slot.model,
            label=slot.label,
            tagline=slot.tagline,
            result=result,
            latency_ms=round(latency * 1000, 1),
            queue_wait_ms=round(wait * 1000, 1),
        )
    except Exception as e:
        return SpectrumColumn(
            slot=slot.id,
            model=slot.model,
            label=slot.label,
            tagline=slot.tagline,
            error=str(e)[:400],
            queue_wait_ms=round(wait * 1000, 1),
        )


@app.post("/api/spectrum/slot", response_model=SpectrumColumn)
async def spectrum_slot(req: SpectrumSlotRequest):
    """Un modèle Spectrum — pour progression UI (3 appels séquentiels côté client)."""
    try:
        slot_by_id(req.slot_id)
    except KeyError:
        raise HTTPException(404, f"Slot '{req.slot_id}' inconnu")
    return await _run_spectrum_slot(req.input, req.slot_id)


@app.post("/api/spectrum", response_model=SpectrumResponse)
async def spectrum_full(req: SpectrumRequest):
    """Les 3 modèles en séquence serveur — zero-429 garanti."""
    import time

    t0 = time.perf_counter()
    columns: list[SpectrumColumn] = []
    for slot in SLOTS:
        columns.append(await _run_spectrum_slot(req.input, slot.id))

    raw_cols = [c.model_dump() for c in columns]
    rec = recommend(raw_cols, req.input)
    return SpectrumResponse(
        input=req.input,
        columns=columns,
        recommendation=rec,
        total_ms=round((time.perf_counter() - t0) * 1000, 1),
        slots_order=[s.id for s in SLOTS],
    )


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