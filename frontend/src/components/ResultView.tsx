import type { ReactNode } from "react";

interface Props {
  data: Record<string, unknown>;
}

function renderValue(val: unknown, depth = 0): ReactNode {
  if (val === null || val === undefined) return <span className="muted">—</span>;
  if (typeof val === "boolean") return <span className={val ? "ok" : "warn"}>{String(val)}</span>;
  if (typeof val === "number") return <span className="num">{val}</span>;
  if (typeof val === "string") {
    if (val.length > 120 && depth > 0) return <pre className="code-block">{val}</pre>;
    return <span>{val}</span>;
  }
  if (Array.isArray(val)) {
    if (!val.length) return <span className="muted">[]</span>;
    if (typeof val[0] === "string") {
      return (
        <ul className="list">
          {val.map((item, i) => (
            <li key={i}>{item as string}</li>
          ))}
        </ul>
      );
    }
    return (
      <div className="nested">
        {val.map((item, i) => (
          <div key={i} className="card nested-card">
            {typeof item === "object" && item !== null
              ? Object.entries(item as Record<string, unknown>).map(([k, v]) => (
                  <div key={k} className="row">
                    <span className="key">{k}</span>
                    <div className="val">{renderValue(v, depth + 1)}</div>
                  </div>
                ))
              : renderValue(item, depth + 1)}
          </div>
        ))}
      </div>
    );
  }
  if (typeof val === "object") {
    return (
      <div className="nested">
        {Object.entries(val as Record<string, unknown>).map(([k, v]) => (
          <div key={k} className="row">
            <span className="key">{k}</span>
            <div className="val">{renderValue(v, depth + 1)}</div>
          </div>
        ))}
      </div>
    );
  }
  return <span>{String(val)}</span>;
}

export default function ResultView({ data }: Props) {
  const priority = [
    "summary",
    "verdict",
    "root_cause",
    "score",
    "refactored_code",
    "patch",
    "dockerfile",
    "query",
    "openapi_yaml",
    "tests",
    "goal",
    "analysis",
    "recommendations",
  ];
  const ordered = [
    ...priority.filter((k) => k in data),
    ...Object.keys(data).filter((k) => !priority.includes(k)),
  ];

  return (
    <div className="results">
      {ordered.map((key) => (
        <section key={key} className="result-section">
          <h3 className="result-key">{key.replace(/_/g, " ")}</h3>
          <div className="result-val">{renderValue(data[key])}</div>
        </section>
      ))}
    </div>
  );
}