import { useState } from "react";
import { saveApiKey } from "../lib/api";

interface Props {
  onComplete: () => void;
  hasKey?: boolean;
}

export default function Onboarding({ onComplete, hasKey = false }: Props) {
  const [step, setStep] = useState<"welcome" | "key" | "done">("welcome");
  const [apiKey, setApiKey] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSave() {
    setLoading(true);
    setError(null);
    try {
      await saveApiKey(apiKey);
      setStep("done");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erreur");
    } finally {
      setLoading(false);
    }
  }

  function finish() {
    localStorage.setItem("mistral-bureau-onboarding", "1");
    onComplete();
  }

  return (
    <div className="ob-overlay">
      <div className="ob-card">
        {step === "welcome" && (
          <>
            <h1>🏛️ Mistral Bureau</h1>
            <p>
              Vitrine <strong>multi-modèles</strong> sur{" "}
              <a href="https://docs.mistral.ai" target="_blank" rel="noreferrer">
                La Plateforme Mistral
              </a>
              . Agents one-shot · Mistral Large, Ministral, Devstral, Pixtral · zéro 429.
            </p>
            <ul>
              <li>Carrière & produit → Mistral Large</li>
              <li>Contenu & IA → Ministral 8B</li>
              <li>Dev & sécurité → Devstral Small</li>
              <li>Vision → Pixtral Large (images)</li>
            </ul>
            <button onClick={() => (hasKey ? setStep("done") : setStep("key"))}>
              {hasKey ? "Entrer →" : "Configurer MISTRAL_API_KEY →"}
            </button>
          </>
        )}
        {step === "key" && (
          <>
            <h1>Clé La Plateforme</h1>
            <p>
              Stockée dans <code>mistral-bureau/.env</code> (gitignoré).{" "}
              <a href="https://console.mistral.ai" target="_blank" rel="noreferrer">
                console.mistral.ai →
              </a>
            </p>
            <input
              type="password"
              placeholder="MISTRAL_API_KEY"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
            />
            {error && <div className="ob-err">{error}</div>}
            <button disabled={apiKey.length < 20 || loading} onClick={handleSave}>
              {loading ? "Validation…" : "Enregistrer"}
            </button>
          </>
        )}
        {step === "done" && (
          <>
            <h1>✓ Prêt</h1>
            <p>
              Explore les agents par catégorie — commence par <strong>Carrière</strong> ou{" "}
              <strong>Vision</strong> si tu as une image.
            </p>
            <button onClick={finish}>Ouvrir le Bureau →</button>
          </>
        )}
      </div>
      <style>{`
        .ob-overlay {
          position: fixed; inset: 0; z-index: 100;
          background: linear-gradient(160deg, #0a0a0fee 0%, #1a1008ee 50%, #0a0a0fee 100%);
          display: flex; align-items: center; justify-content: center; padding: 1.5rem;
        }
        .ob-card {
          max-width: 500px; background: var(--surface);
          border: 1px solid #ff700044; border-radius: 16px; padding: 2rem;
          box-shadow: 0 0 40px var(--accent-glow);
        }
        .ob-card h1 { margin-bottom: 0.75rem; font-size: 1.45rem; }
        .ob-card p, .ob-card li { color: var(--muted); line-height: 1.6; margin-bottom: 0.75rem; }
        .ob-card a, .ob-card code { color: var(--accent); }
        .ob-card code { font-family: var(--mono); font-size: 0.85em; }
        .ob-card ul { padding-left: 1.2rem; margin-bottom: 1rem; }
        .ob-card input {
          width: 100%; padding: 0.75rem; border-radius: 8px;
          border: 1px solid var(--border); background: var(--bg);
          color: var(--text); font-family: var(--mono); margin-bottom: 1rem;
        }
        .ob-card input:focus { outline: none; border-color: var(--accent); }
        .ob-card button {
          padding: 0.75rem 1.4rem; border-radius: 8px; border: none;
          background: linear-gradient(135deg, #ff7000, #ff9030);
          color: #fff; font-weight: 600; cursor: pointer;
        }
        .ob-card button:disabled { opacity: 0.4; cursor: not-allowed; }
        .ob-err { color: var(--red); font-size: 0.85rem; margin-bottom: 0.75rem; }
      `}</style>
    </div>
  );
}