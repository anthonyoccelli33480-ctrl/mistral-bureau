import { useState } from "react";
import ResultView from "./ResultView";
import {
  SpectrumColumn,
  SpectrumMeta,
  fetchSpectrumMeta,
  runSpectrumSlot,
} from "../lib/api";

const SLOT_ORDER = ["fast", "code", "deep"] as const;

const MODEL_LABELS: Record<string, string> = {
  "ministral-8b-latest": "Ministral 8B",
  "devstral-small-latest": "Devstral Small 2",
  "mistral-large-2512": "Mistral Large",
};

interface Props {
  healthOk: boolean;
  onHealth: () => void;
}

export default function SpectrumView({ healthOk, onHealth }: Props) {
  const [input, setInput] = useState("");
  const [columns, setColumns] = useState<SpectrumColumn[]>([]);
  const [recommendation, setRecommendation] = useState<Record<string, string> | null>(null);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(-1);
  const [error, setError] = useState<string | null>(null);
  const [meta, setMeta] = useState<SpectrumMeta | null>(null);
  const [totalMs, setTotalMs] = useState(0);

  const canRun = healthOk && input.trim().length >= 3 && !loading;

  async function handleRun() {
    if (!canRun) return;
    setLoading(true);
    setError(null);
    setColumns([]);
    setRecommendation(null);
    setTotalMs(0);
    const t0 = performance.now();

    try {
      const m = meta ?? (await fetchSpectrumMeta());
      if (!meta) setMeta(m);

      const results: SpectrumColumn[] = [];
      for (let i = 0; i < SLOT_ORDER.length; i++) {
        setStep(i);
        const col = await runSpectrumSlot(input, SLOT_ORDER[i]);
        results.push(col);
        setColumns([...results]);
        onHealth();
      }

      setTotalMs(Math.round(performance.now() - t0));
      setRecommendation(pickRecommendation(results, input));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erreur Spectrum");
    } finally {
      setStep(-1);
      setLoading(false);
    }
  }

  return (
    <div className="spectrum">
      <div className="agent-header">
        <h2>🌈 Bureau Spectrum</h2>
        <p>Même input → 3 modèles côte à côte · file séquentielle anti-429</p>
        <span className="badge">Ministral · Devstral · Large</span>
      </div>

      <div className="guide-panel guide-how">
        <h4 className="guide-title">Comment l'utiliser</h4>
        <ol className="guide-list">
          <li>Colle une question, un extrait de code, ou un brief produit</li>
          <li>Spectrum interroge les 3 modèles l'un après l'autre (~60–90s)</li>
          <li>Compare les colonnes — la recommandation suggère le meilleur tier</li>
        </ol>
      </div>

      <textarea
        className="input"
        placeholder="Ex: Explique cette erreur Python… / Résume cette offre d'emploi… / Scope un MVP SaaS…"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        rows={8}
      />

      <button className="run-btn spectrum-btn" onClick={handleRun} disabled={!canRun}>
        {loading
          ? `Spectrum ${step + 1}/3 — ${SLOT_ORDER[step] ?? "…"}…`
          : "Lancer Spectrum 🌈"}
      </button>

      {loading && (
        <div className="spectrum-progress">
          {SLOT_ORDER.map((id, i) => (
            <span key={id} className={`sp-step ${i < step ? "done" : i === step ? "active" : ""}`}>
              {i < step ? "✓" : i === step ? "…" : "○"} {MODEL_LABELS[meta?.slots.find((s) => s.id === id)?.model ?? ""] ?? id}
            </span>
          ))}
          {meta && <span className="sp-est">~{meta.estimate_sec}s total</span>}
        </div>
      )}

      {error && <div className="error">{error}</div>}

      {recommendation && (
        <div className="spectrum-rec">
          <strong>★ Recommandation : {recommendation.label}</strong>
          <p>{recommendation.reason}</p>
        </div>
      )}

      {totalMs > 0 && (
        <div className="metrics">
          <span className="metric hi">{totalMs} ms total</span>
          <span className="metric">3 appels séquentiels</span>
        </div>
      )}

      {columns.length > 0 && (
        <div className="spectrum-grid">
          {columns.map((col) => (
            <div
              key={col.slot}
              className={`spectrum-col ${recommendation?.slot === col.slot ? "winner" : ""}`}
            >
              <div className="col-head">
                <h3>{col.label}</h3>
                <span className="col-tag">{col.tagline}</span>
                {(col.latency_ms ?? 0) > 0 && (
                  <span className="col-ms">{col.latency_ms} ms</span>
                )}
              </div>
              {col.error ? (
                <div className="col-err">{col.error}</div>
              ) : col.result ? (
                <ResultView data={col.result} />
              ) : null}
            </div>
          ))}
        </div>
      )}

      <style>{`
        .spectrum-btn { background: linear-gradient(135deg, #a855f7, #ff7000) !important; }
        .spectrum-progress {
          display: flex; flex-wrap: wrap; gap: 0.5rem 1rem; margin-top: 1rem;
          font-size: 0.8rem; font-family: var(--mono); color: var(--muted);
        }
        .sp-step.done { color: var(--green); }
        .sp-step.active { color: var(--accent); font-weight: 600; }
        .sp-est { color: var(--yellow); margin-left: auto; }
        .spectrum-rec {
          margin-top: 1.25rem; padding: 1rem 1.25rem; border-radius: 10px;
          background: linear-gradient(135deg, #ff700018, #a855f718);
          border: 1px solid #ff700055;
        }
        .spectrum-rec strong { color: var(--accent); display: block; margin-bottom: 0.35rem; }
        .spectrum-rec p { color: var(--muted); font-size: 0.9rem; margin: 0; }
        .spectrum-grid {
          display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
          gap: 1rem; margin-top: 1.25rem;
        }
        .spectrum-col {
          padding: 1rem; border-radius: 12px; border: 1px solid var(--border);
          background: var(--surface); min-width: 0;
        }
        .spectrum-col.winner {
          border-color: var(--accent); box-shadow: 0 0 0 1px #ff700044;
        }
        .col-head { margin-bottom: 0.75rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); }
        .col-head h3 { font-size: 0.95rem; margin-bottom: 0.2rem; }
        .col-tag { font-size: 0.72rem; color: var(--muted); display: block; }
        .col-ms { font-size: 0.72rem; font-family: var(--mono); color: var(--accent); }
        .col-err { font-size: 0.8rem; color: var(--red); }
        .spectrum-col .results { gap: 0.65rem; }
        .spectrum-col .result-section { padding: 0.65rem; font-size: 0.85rem; }
      `}</style>
    </div>
  );
}

function pickRecommendation(columns: SpectrumColumn[], input: string): Record<string, string> {
  const text = input.toLowerCase();
  const codeHints = ["def ", "function", "error", "traceback", "```", "import ", "bug", "fix"];
  if (codeHints.some((h) => text.includes(h))) {
    return {
      slot: "code",
      label: "Devstral Small 2",
      reason: "Input orienté code — Devstral est le tier agentique.",
    };
  }
  if (input.length > 900) {
    return {
      slot: "deep",
      label: "Mistral Large",
      reason: "Demande longue — Large apporte plus de nuance.",
    };
  }
  if (input.length < 120) {
    return {
      slot: "fast",
      label: "Ministral 8B",
      reason: "Tâche courte — Ministral suffit.",
    };
  }
  const ok = columns.filter((c) => !c.error && c.result);
  if (ok.length) {
    const best = ok.reduce((a, b) =>
      Number(b.result?.quality_score ?? 0) > Number(a.result?.quality_score ?? 0) ? b : a
    );
    return {
      slot: best.slot,
      label: best.label,
      reason: `Meilleur score qualité (${best.result?.quality_score ?? "?"}) sur cette tâche.`,
    };
  }
  return { slot: "deep", label: "Mistral Large", reason: "Par défaut pour cas ambigus." };
}