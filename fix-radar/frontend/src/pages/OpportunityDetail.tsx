import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api/client";
import { Card } from "../components/Card";
import { CategoryTag, SeverityBadge, StatusBadge } from "../components/Badge";
import type { Opportunity, Recommendation } from "../types/api";

const STATUSES = ["OPEN", "IN_PROGRESS", "FIXED", "IGNORED"];

export default function OpportunityDetail() {
  const { opportunityId } = useParams();
  const [opp, setOpp] = useState<Opportunity | null>(null);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [notes, setNotes] = useState("");
  const [generating, setGenerating] = useState(false);

  const load = async () => {
    if (!opportunityId) return;
    const o = await api.get<Opportunity>(`/opportunities/${opportunityId}`);
    setOpp(o);
    setNotes(o.notes || "");
    setRecommendations(await api.get<Recommendation[]>(`/opportunities/${opportunityId}/recommendations`));
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [opportunityId]);

  const setStatus = async (status: string) => {
    if (!opportunityId) return;
    const updated = await api.patch<Opportunity>(`/opportunities/${opportunityId}`, { status });
    setOpp(updated);
  };

  const saveNotes = async () => {
    if (!opportunityId) return;
    const updated = await api.patch<Opportunity>(`/opportunities/${opportunityId}`, { notes });
    setOpp(updated);
  };

  const generate = async () => {
    if (!opportunityId) return;
    setGenerating(true);
    try {
      const rec = await api.post<Recommendation>(`/opportunities/${opportunityId}/generate-recommendation`);
      setRecommendations((prev) => [rec, ...prev]);
    } finally {
      setGenerating(false);
    }
  };

  if (!opp) return <p className="text-slate-500">Loading...</p>;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="mb-2 flex gap-2">
            <SeverityBadge severity={opp.severity} />
            <CategoryTag category={opp.category} />
            <StatusBadge status={opp.status} />
          </div>
          <h1 className="font-display text-2xl font-bold text-navy-950">{opp.title}</h1>
        </div>
        <div className="text-right">
          <p className="font-display text-3xl font-bold text-navy-950">{opp.priority_score}</p>
          <p className="text-xs uppercase tracking-wide text-slate-400">priority score (heuristic)</p>
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        {opp.status === "OPEN" && (
          <button onClick={() => setStatus("IN_PROGRESS")} className="rounded-lg bg-navy-950 px-5 py-2.5 font-medium text-white hover:bg-navy-900">
            Start Fix
          </button>
        )}
        {STATUSES.filter((s) => s !== opp.status).map((s) => (
          <button key={s} onClick={() => setStatus(s)} className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
            Mark {s.replace("_", " ")}
          </button>
        ))}
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card title="Problem">
          <p className="text-slate-700">{opp.explanation}</p>
        </Card>
        <Card title="Why it matters">
          <p className="text-slate-700">{opp.expected_benefit}</p>
        </Card>
        <Card title="Evidence">
          <pre className="whitespace-pre-wrap text-sm text-slate-700">{opp.evidence}</pre>
        </Card>
        <Card title="Exact location">
          {opp.affected_pages && opp.affected_pages.length > 0 ? (
            <ul className="space-y-1 text-sm">
              {opp.affected_pages.map((url) => (
                <li key={url}>
                  <a href={url} target="_blank" rel="noreferrer" className="text-navy-900 hover:text-gold-500">
                    {url}
                  </a>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-slate-500">Site-wide -- not tied to a single page.</p>
          )}
        </Card>
        <Card title="Recommended fix">
          <p className="text-slate-700">{opp.recommended_fix}</p>
        </Card>
        <Card title="Effort">
          <p className="text-slate-700">{opp.effort_score}/10{opp.estimated_minutes ? ` -- roughly ${opp.estimated_minutes} minutes` : ""}</p>
        </Card>
      </div>

      <Card title="Suggested implementation" subtitle="AI-drafted. Always review before publishing -- nothing here is auto-published.">
        <button onClick={generate} disabled={generating} className="mb-4 rounded-lg bg-navy-950 px-4 py-2 text-sm font-medium text-white hover:bg-navy-900 disabled:opacity-50">
          {generating ? "Generating..." : "Generate draft"}
        </button>
        {recommendations.length === 0 && <p className="text-sm text-slate-500">No draft generated yet.</p>}
        {recommendations.map((rec) => (
          <div key={rec.id} className="mb-4 rounded-lg border border-slate-200 p-4 text-sm">
            <p className="mb-2 text-xs uppercase tracking-wide text-slate-400">{rec.generated_by} &middot; {new Date(rec.created_at).toLocaleString()}</p>
            {rec.content.suggested_title && <p><span className="font-semibold">Title:</span> {rec.content.suggested_title}</p>}
            {rec.content.suggested_meta_description && <p><span className="font-semibold">Meta description:</span> {rec.content.suggested_meta_description}</p>}
            {rec.content.suggested_h1 && <p><span className="font-semibold">H1:</span> {rec.content.suggested_h1}</p>}
            {rec.content.section_outline && rec.content.section_outline.length > 0 && (
              <div className="mt-2">
                <p className="font-semibold">Section outline:</p>
                <ul className="list-disc pl-5">
                  {rec.content.section_outline.map((s, i) => <li key={i}>{s}</li>)}
                </ul>
              </div>
            )}
            {rec.content.content_brief && (
              <div className="mt-2">
                <p className="font-semibold">Content brief:</p>
                <p className="whitespace-pre-wrap text-slate-700">{rec.content.content_brief}</p>
              </div>
            )}
            <p className="mt-3 rounded bg-amber-50 p-2 text-xs text-amber-800">{rec.content.caveat}</p>
          </div>
        ))}
      </Card>

      <Card title="Notes">
        <textarea value={notes} onChange={(e) => setNotes(e.target.value)} rows={3} className="w-full rounded-lg border border-slate-300 p-3 text-sm" placeholder="Add implementation notes..." />
        <button onClick={saveNotes} className="mt-2 rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium hover:bg-slate-50">
          Save notes
        </button>
      </Card>
    </div>
  );
}
