import { useCallback, useEffect, useState } from "react";
import GuidePanel from "./components/GuidePanel";
import ImageUpload from "./components/ImageUpload";
import Onboarding from "./components/Onboarding";
import ResultView from "./components/ResultView";
import SpectrumView from "./components/SpectrumView";
import { AgentMeta, RunResponse, fetchAgents, fetchHealth, runAgent } from "./lib/api";

const SPECTRUM_ID = "__spectrum__";

const CATEGORIES: Record<string, string> = {
  carriere: "Carrière",
  produit: "Produit",
  contenu: "Contenu",
  securite: "Sécurité",
  vision: "Vision · Pixtral",
  ia: "IA / ML",
  dev: "Dev & Code",
};

const MODEL_LABELS: Record<string, string> = {
  "mistral-large-2512": "Mistral Large",
  "ministral-8b-latest": "Ministral 8B",
  "devstral-small-latest": "Devstral Small 2",
  "pixtral-large-latest": "Pixtral Large",
};

export default function App() {
  const [agents, setAgents] = useState<AgentMeta[]>([]);
  const [selected, setSelected] = useState("review");
  const [input, setInput] = useState("");
  const [images, setImages] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<RunResponse | null>(null);
  const [health, setHealth] = useState({
    ok: false,
    mistral_key: false,
    next_available_in_sec: 0,
    rate_intervals: {} as Record<string, number>,
  });
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [booting, setBooting] = useState(true);

  const isSpectrum = selected === SPECTRUM_ID;
  const current = isSpectrum ? null : agents.find((a) => a.id === selected);

  const refreshHealth = useCallback(async () => {
    try {
      setHealth(await fetchHealth());
    } catch {
      setHealth({ ok: false, mistral_key: false, next_available_in_sec: 0, rate_intervals: {} });
    }
  }, []);

  useEffect(() => {
    fetchAgents().then((list) => {
      setAgents(list);
      if (list.length) setSelected(list[0].id);
    });
    void refreshHealth().finally(() => setBooting(false));
    const t = setInterval(refreshHealth, 2000);
    return () => clearInterval(t);
  }, [refreshHealth]);

  useEffect(() => {
    if (booting) return;
    const done = localStorage.getItem("mistral-bureau-onboarding");
    if (!health.mistral_key || !done) setShowOnboarding(true);
  }, [booting, health.mistral_key]);

  const canRun =
    current &&
    !loading &&
    health.ok &&
    (current.requires_image ? images.length > 0 : input.trim().length >= 3);

  async function handleRun() {
    if (!canRun) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      setResult(await runAgent(selected, input, images));
      refreshHealth();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erreur");
    } finally {
      setLoading(false);
    }
  }

  const grouped = agents.reduce<Record<string, AgentMeta[]>>((acc, a) => {
    (acc[a.category] ??= []).push(a);
    return acc;
  }, {});

  if (booting) {
    return (
      <div className="boot">
        🏛️ Mistral Bureau
        <style>{`
          .boot {
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
            color: var(--muted); background: linear-gradient(180deg, var(--accent-glow), transparent);
          }
        `}</style>
      </div>
    );
  }

  return (
    <div className="app">
      {showOnboarding && (
        <Onboarding
          hasKey={health.mistral_key}
          onComplete={() => {
            setShowOnboarding(false);
            localStorage.setItem("mistral-bureau-onboarding", "1");
            void refreshHealth();
          }}
        />
      )}
      <header className="header">
        <div className="header-glow" aria-hidden />
        <div className="header-inner">
          <div>
            <h1>
              <span className="logo">🏛️</span> Mistral Bureau
            </h1>
            <p className="subtitle">
              La Plateforme multi-modèles · agents FR one-shot · Mistral Large · Ministral · Devstral · Pixtral
            </p>
          </div>
          <div className="header-right">
            <span className={`status ${health.ok ? "on" : "off"}`}>
              {health.ok ? "● Mistral connecté" : "○ Clé manquante"}
            </span>
            {health.next_available_in_sec > 0 && (
              <span className="cooldown">Gate {Math.ceil(health.next_available_in_sec)}s</span>
            )}
            <button type="button" className="link-btn" onClick={() => setShowOnboarding(true)}>
              Clé API
            </button>
          </div>
        </div>
      </header>

      <div className="layout">
        <aside className="sidebar">
          <div className="cat-group spectrum-nav">
            <h2 className="cat-label">Spectrum</h2>
            <button
              className={`agent-btn spectrum-btn-nav ${isSpectrum ? "active" : ""}`}
              onClick={() => {
                setSelected(SPECTRUM_ID);
                setResult(null);
                setError(null);
                setImages([]);
              }}
            >
              <span>🌈</span>
              <span className="agent-info">
                <span className="agent-name">Bureau Spectrum</span>
                <span className="agent-model">3 modèles · 1 input</span>
              </span>
            </button>
          </div>
          {Object.entries(grouped).map(([cat, list]) => (
            <div key={cat} className="cat-group">
              <h2 className="cat-label">{CATEGORIES[cat] ?? cat}</h2>
              {list.map((a) => (
                <button
                  key={a.id}
                  className={`agent-btn ${selected === a.id ? "active" : ""}`}
                  onClick={() => {
                    setSelected(a.id);
                    setResult(null);
                    setError(null);
                    setImages([]);
                  }}
                >
                  <span>{a.icon}</span>
                  <span className="agent-info">
                    <span className="agent-name">{a.name}</span>
                    <span className="agent-model">{MODEL_LABELS[a.model] ?? a.model}</span>
                  </span>
                </button>
              ))}
            </div>
          ))}
        </aside>

        <main className={`main ${isSpectrum ? "main-wide" : ""}`}>
          {isSpectrum && <SpectrumView healthOk={health.ok} onHealth={refreshHealth} />}
          {current && (
            <>
              <div className="agent-header">
                <h2>
                  {current.icon} {current.name}
                </h2>
                <p>{current.tagline}</p>
                <span className="badge">{MODEL_LABELS[current.model] ?? current.model}</span>
              </div>
              <GuidePanel title="Comment l'utiliser" steps={current.how_to} variant="how" />
              {current.requires_image && (
                <ImageUpload
                  images={images}
                  maxImages={current.max_images ?? 5}
                  onChange={setImages}
                />
              )}
              <textarea
                className="input"
                placeholder={current.placeholder}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                rows={current.requires_image ? 4 : 12}
              />
              <button className="run-btn" onClick={handleRun} disabled={!canRun}>
                {loading ? "Mistral réfléchit…" : "Lancer 🏛️"}
              </button>
              {error && <div className="error">{error}</div>}
              {result && (
                <div className="output">
                  <div className="metrics">
                    <span className="metric hi">{result.latency_ms} ms</span>
                    <span className="metric">{MODEL_LABELS[result.model] ?? result.model}</span>
                    {result.queue_wait_ms > 0 && (
                      <span className="metric">queue {result.queue_wait_ms} ms</span>
                    )}
                  </div>
                  <ResultView data={result.result} />
                  <GuidePanel title="Et ensuite ?" steps={result.next_steps} variant="next" />
                </div>
              )}
            </>
          )}
        </main>
      </div>

      <footer className="footer">
        Phase 2 · Mistral Bureau · Devstral Lab → phase 1
      </footer>

      <style>{`
        .app { display: flex; flex-direction: column; min-height: 100vh; }
        .header {
          position: relative; border-bottom: 1px solid var(--border);
          background: var(--surface); overflow: hidden;
        }
        .header-glow {
          position: absolute; inset: 0;
          background: linear-gradient(135deg, #ff700022 0%, transparent 45%, #ff70000a 100%);
          pointer-events: none;
        }
        .header-inner {
          position: relative; display: flex; justify-content: space-between;
          padding: 1.5rem 2rem; align-items: flex-start;
        }
        .header h1 { font-size: 1.55rem; display: flex; gap: 0.5rem; align-items: center; font-weight: 700; }
        .logo { filter: drop-shadow(0 0 8px #ff700066); }
        .subtitle { color: var(--muted); font-size: 0.84rem; margin-top: 0.3rem; max-width: 520px; line-height: 1.45; }
        .header-right { text-align: right; font-size: 0.8rem; display: flex; flex-direction: column; gap: 0.25rem; }
        .status.on { color: var(--green); }
        .status.off { color: var(--red); }
        .cooldown { color: var(--yellow); font-family: var(--mono); }
        .link-btn {
          background: none; border: none; color: var(--muted); cursor: pointer;
          font-size: 0.75rem; text-decoration: underline;
        }
        .link-btn:hover { color: var(--accent); }

        .layout { display: flex; flex: 1; }
        .sidebar {
          width: 280px; border-right: 1px solid var(--border);
          padding: 1rem 0.75rem; background: var(--surface); overflow-y: auto;
        }
        .cat-label {
          font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em;
          color: var(--muted); padding: 0 0.5rem; margin-bottom: 0.5rem;
        }
        .cat-group { margin-bottom: 1rem; }
        .agent-btn {
          display: flex; gap: 0.65rem; width: 100%; padding: 0.55rem 0.7rem;
          border: none; border-radius: 8px; background: transparent;
          color: var(--text); cursor: pointer; text-align: left;
        }
        .agent-btn:hover { background: var(--surface-2); }
        .agent-btn.active {
          background: var(--accent-dim); border: 1px solid #ff700066;
          box-shadow: inset 3px 0 0 var(--accent);
        }
        .agent-info { display: flex; flex-direction: column; }
        .agent-name { font-size: 0.85rem; font-weight: 600; }
        .agent-model { font-size: 0.68rem; color: var(--muted); font-family: var(--mono); }

        .main { flex: 1; padding: 1.5rem 2rem; max-width: 900px; overflow-y: auto; }
        .main.main-wide { max-width: 1200px; }
        .spectrum-nav { margin-bottom: 1.25rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border); }
        .spectrum-btn-nav.active {
          background: linear-gradient(135deg, #a855f722, #ff700022);
          border-color: #a855f766;
          box-shadow: inset 3px 0 0 #a855f7;
        }
        .agent-header { margin-bottom: 1rem; }
        .agent-header h2 { font-size: 1.2rem; }
        .agent-header p { color: var(--muted); font-size: 0.9rem; }
        .badge {
          display: inline-block; margin-top: 0.4rem; padding: 0.15rem 0.55rem;
          background: var(--accent-dim); color: var(--accent); border-radius: 4px;
          font-size: 0.72rem; font-family: var(--mono);
        }

        .guide-panel { padding: 1rem; border-radius: 10px; margin-bottom: 1rem; border: 1px solid var(--border); }
        .guide-how { background: var(--surface); }
        .guide-next { background: linear-gradient(135deg, #ff700018, #ff700008); border-color: #ff700044; }
        .guide-title { font-size: 0.75rem; text-transform: uppercase; margin-bottom: 0.5rem; font-weight: 600; }
        .guide-how .guide-title { color: var(--muted); }
        .guide-next .guide-title { color: var(--accent); }
        .guide-list { padding-left: 1.2rem; font-size: 0.88rem; line-height: 1.5; }

        .input {
          width: 100%; padding: 1rem; border-radius: 10px; border: 1px solid var(--border);
          background: var(--surface); color: var(--text); font-family: var(--mono);
          font-size: 0.85rem; resize: vertical;
        }
        .input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-glow); }

        .run-btn {
          margin-top: 1rem; padding: 0.75rem 1.75rem; border: none; border-radius: 8px;
          background: linear-gradient(135deg, #ff7000, #ff9030); color: #fff;
          font-weight: 600; cursor: pointer;
        }
        .run-btn:hover:not(:disabled) { filter: brightness(1.08); }
        .run-btn:disabled { opacity: 0.4; cursor: not-allowed; }

        .error {
          margin-top: 1rem; padding: 0.75rem; border-radius: 8px;
          background: #ef444422; border: 1px solid var(--red); color: var(--red); font-size: 0.85rem;
        }
        .output { margin-top: 1.5rem; }
        .metrics { display: flex; gap: 0.75rem; margin-bottom: 1rem; flex-wrap: wrap; }
        .metric {
          font-family: var(--mono); font-size: 0.78rem; color: var(--muted);
          padding: 0.3rem 0.65rem; background: var(--surface); border: 1px solid var(--border); border-radius: 6px;
        }
        .metric.hi { color: var(--accent); font-size: 1rem; font-weight: 600; border-color: var(--accent); }

        .results { display: flex; flex-direction: column; gap: 1rem; }
        .result-section {
          padding: 1rem; background: var(--surface); border-radius: 10px; border: 1px solid var(--border);
        }
        .result-key {
          font-size: 0.72rem; text-transform: uppercase; color: var(--accent);
          margin-bottom: 0.4rem; font-family: var(--mono);
        }
        .list { padding-left: 1.2rem; }
        .nested-card { padding: 0.6rem; background: var(--surface-2); border-radius: 6px; margin-top: 0.35rem; }
        .row { display: flex; gap: 0.5rem; margin-bottom: 0.3rem; flex-wrap: wrap; }
        .key { font-family: var(--mono); font-size: 0.78rem; color: var(--muted); min-width: 100px; }
        .code-block {
          font-family: var(--mono); font-size: 0.78rem; white-space: pre-wrap;
          background: var(--bg); padding: 0.6rem; border-radius: 6px;
        }
        .muted { color: var(--muted); }
        .ok { color: var(--green); }
        .warn { color: var(--yellow); }
        .num { color: var(--accent); font-family: var(--mono); }

        .footer {
          padding: 1rem; text-align: center; font-size: 0.78rem;
          color: var(--muted); border-top: 1px solid var(--border);
          background: linear-gradient(180deg, transparent, var(--accent-glow));
        }
      `}</style>
    </div>
  );
}