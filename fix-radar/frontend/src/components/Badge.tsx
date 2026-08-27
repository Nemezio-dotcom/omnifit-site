const SEVERITY_STYLES: Record<string, string> = {
  CRITICAL: "bg-red-100 text-red-800 border-red-200",
  HIGH: "bg-orange-100 text-orange-800 border-orange-200",
  MEDIUM: "bg-amber-100 text-amber-800 border-amber-200",
  LOW: "bg-slate-100 text-slate-700 border-slate-200",
  INFO: "bg-blue-100 text-blue-700 border-blue-200",
};

export function SeverityBadge({ severity }: { severity: string }) {
  return (
    <span className={`rounded border px-2 py-0.5 text-xs font-semibold ${SEVERITY_STYLES[severity] || SEVERITY_STYLES.INFO}`}>
      {severity}
    </span>
  );
}

const STATUS_STYLES: Record<string, string> = {
  OPEN: "bg-slate-100 text-slate-700",
  IN_PROGRESS: "bg-blue-100 text-blue-700",
  FIXED: "bg-emerald-100 text-emerald-700",
  IGNORED: "bg-slate-100 text-slate-400",
};

export function StatusBadge({ status }: { status: string }) {
  return (
    <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${STATUS_STYLES[status] || STATUS_STYLES.OPEN}`}>
      {status.replace("_", " ")}
    </span>
  );
}

export function CategoryTag({ category }: { category: string }) {
  return <span className="rounded bg-navy-950/5 px-2 py-0.5 text-xs font-medium text-navy-900">{category.replace("_", " ")}</span>;
}
