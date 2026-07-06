interface Props {
  title: string;
  steps: string[];
  variant?: "how" | "next";
}

export default function GuidePanel({ title, steps, variant = "how" }: Props) {
  if (!steps.length) return null;
  return (
    <div className={`guide-panel guide-${variant}`}>
      <h4 className="guide-title">{title}</h4>
      <ol className="guide-list">
        {steps.map((step, i) => (
          <li key={i}>{step}</li>
        ))}
      </ol>
    </div>
  );
}