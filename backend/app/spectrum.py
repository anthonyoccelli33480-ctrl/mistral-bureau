"""Mistral Spectrum — même input, 3 modèles, recommandation."""

from dataclasses import dataclass

SPECTRUM_SYSTEM = """Tu es un assistant Mistral en mode vitrine Spectrum.
Analyse la demande et réponds UNIQUEMENT en JSON (français) :
{
  "summary": "<2 phrases max>",
  "answer": "<réponse actionnable complète>",
  "angle": "rapid|deep|code",
  "quality_score": <0-100>,
  "best_when": "<quand utiliser ce type de modèle pour cette tâche>"
}
Sois honnête sur tes limites selon ta taille de modèle."""

CODE_HINTS = (
    "def ", "function", "class ", "import ", "error", "traceback", "bug", "fix",
    "refactor", "git diff", "```", "typescript", "python", "react", "api ",
)


@dataclass(frozen=True)
class SpectrumSlot:
    id: str
    model: str
    label: str
    tagline: str


SLOTS: tuple[SpectrumSlot, ...] = (
    SpectrumSlot("fast", "ministral-8b-latest", "Ministral 8B", "Rapide · léger"),
    SpectrumSlot("code", "devstral-small-latest", "Devstral Small 2", "Code · agentique"),
    SpectrumSlot("deep", "mistral-large-2512", "Mistral Large", "Profond · nuancé"),
)


def slot_by_id(slot_id: str) -> SpectrumSlot:
    for s in SLOTS:
        if s.id == slot_id:
            return s
    raise KeyError(slot_id)


def recommend(columns: list[dict], input_text: str) -> dict:
    """Choisit le modèle recommandé à partir des 3 réponses + heuristiques input."""
    text = input_text.lower()
    ok = [c for c in columns if not c.get("error") and c.get("result")]

    if any(h in text for h in CODE_HINTS):
        return {
            "slot": "code",
            "model": "devstral-small-latest",
            "label": "Devstral Small 2",
            "reason": "Input orienté code / debug — Devstral est conçu pour l'agentique.",
        }

    if len(input_text.strip()) > 900:
        return {
            "slot": "deep",
            "model": "mistral-large-2512",
            "label": "Mistral Large",
            "reason": "Demande longue ou complexe — Large apporte plus de nuance.",
        }

    if len(input_text.strip()) < 120:
        return {
            "slot": "fast",
            "model": "ministral-8b-latest",
            "label": "Ministral 8B",
            "reason": "Tâche courte — Ministral suffit avec moins de latence.",
        }

    if ok:
        best = max(
            ok,
            key=lambda c: int((c.get("result") or {}).get("quality_score") or 0),
        )
        slot = slot_by_id(best["slot"])
        return {
            "slot": slot.id,
            "model": slot.model,
            "label": slot.label,
            "reason": f"Meilleur quality_score ({best['result'].get('quality_score')}) sur cette tâche.",
        }

    return {
        "slot": "deep",
        "model": "mistral-large-2512",
        "label": "Mistral Large",
        "reason": "Par défaut — Large pour les cas ambigus.",
    }