function colorFor(score: number | null | undefined): string {
  if (score === null || score === undefined) return "#94a3b8";
  if (score >= 85) return "#1a7f4b";
  if (score >= 70) return "#c9a84c";
  if (score >= 50) return "#d97706";
  return "#c0392b";
}

export function ScoreDial({ score, size = 120, label }: { score: number | null | undefined; size?: number; label?: string }) {
  const radius = size / 2 - 8;
  const circumference = 2 * Math.PI * radius;
  const pct = score ?? 0;
  const offset = circumference * (1 - pct / 100);

  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="#e2e8f0" strokeWidth={8} />
        <circle
          className="score-ring"
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={colorFor(score)}
          strokeWidth={8}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
        <text x="50%" y="50%" textAnchor="middle" dominantBaseline="central" className="fill-slate-900 font-display text-2xl font-bold">
          {score ?? "--"}
        </text>
      </svg>
      {label && <p className="mt-1 text-sm font-medium text-slate-600">{label}</p>}
    </div>
  );
}

export function ScoreBar({ label, score }: { label: string; score: number | null | undefined }) {
  const pct = score ?? 0;
  return (
    <div>
      <div className="mb-1 flex items-center justify-between text-sm">
        <span className="font-medium text-slate-700">{label}</span>
        <span className="font-semibold text-slate-900">{score ?? "--"}</span>
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-slate-200">
        <div className="h-full rounded-full" style={{ width: `${pct}%`, backgroundColor: colorFor(score) }} />
      </div>
    </div>
  );
}
