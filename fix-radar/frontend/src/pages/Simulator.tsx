import { useEffect, useState } from "react";
import { api } from "../api/client";
import { Card } from "../components/Card";
import { useSite } from "../context/SiteContext";
import type { ClusterReadiness, SavedQuery, SimulatorRun } from "../types/api";

export default function Simulator() {
  const { siteId } = useSite();
  const [examples, setExamples] = useState<string[]>([]);
  const [query, setQuery] = useState("");
  const [run, setRun] = useState<SimulatorRun | null>(null);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [savedQueries, setSavedQueries] = useState<SavedQuery[]>([]);
  const [clusters, setClusters] = useState<ClusterReadiness | null>(null);

  const load = async () => {
    if (!siteId) return;
    setSavedQueries(await api.get<SavedQuery[]>(`/sites/${siteId}/simulator/queries`));
    setClusters(await api.get<ClusterReadiness>(`/sites/${siteId}/simulator/clusters`));
  };

  useEffect(() => {
    api.get<string[]>(`/sites/${siteId}/simulator/example-queries`).then(setExamples);
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [siteId]);

  const analyze = async (q?: string) => {
    const text = q ?? query;
    if (!siteId || !text.trim()) return;
    setRunning(true);
    setError(null);
    try {
      const result = await api.post<SimulatorRun>(`/sites/${siteId}/simulator/run`, { query_text: text });
      setRun(result);
      await load();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setRunning(false);
    }
  };

  const runAll = async () => {
    if (!siteId) return;
    setRunning(true);
    try {
      await api.post(`/sites/${siteId}/simulator/run-all`);
      await load();
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-display text-2xl font-bold text-navy-950">AI Recommendation Simulator</h1>
        <p className="text-sm text-slate-500">
          Evidence-based recommendation readiness -- NOT a claim about how ChatGPT, Claude, Gemini, or any AI system actually ranks OmniFit.
        </p>
      </div>

      <Card title="What would an AI need to know?">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          rows={2}
          placeholder="Who is the best personal trainer for executives in San Diego?"
          className="w-full rounded-lg border border-slate-300 p-3 text-sm"
        />
        <div className="mt-2 flex flex-wrap items-center gap-2">
          <button onClick={() => analyze()} disabled={running} className="rounded-lg bg-navy-950 px-5 py-2 text-sm font-medium text-white hover:bg-navy-900 disabled:opacity-50">
            {running ? "Analyzing..." : "Analyze query"}
          </button>
          <button onClick={runAll} disabled={running} className="rounded-lg border border-slate-300 px-4 py-2 text-sm hover:bg-slate-50 disabled:opacity-50">
            Run all saved queries
          </button>
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          {examples.map((ex) => (
            <button key={ex} onClick={() => { setQuery(ex); analyze(ex); }} className="rounded-full border border-slate-200 px-3 py-1 text-xs text-slate-600 hover:border-gold-500 hover:text-gold-600">
              {ex}
            </button>
          ))}
        </div>
        {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
      </Card>

      {run && (
        <>
          <Card title="Recommendation readiness" subtitle="Internal heuristic score, not an actual AI ranking probability">
            <div className="flex flex-wrap items-center gap-8">
              <div className="text-center">
                <p className="font-display text-5xl font-bold text-navy-950">{run.readiness_score}</p>
                <p className="text-xs uppercase tracking-wide text-slate-400">/ 100</p>
              </div>
              <div className="grid flex-1 grid-cols-3 gap-x-6 gap-y-3 text-sm">
                {Object.entries(run.sub_scores).map(([key, val]) => (
                  <div key={key}>
                    <p className="text-slate-500">{key.replace(/_/g, " ")}</p>
                    <p className="font-semibold text-slate-900">{val}</p>
                  </div>
                ))}
              </div>
            </div>
            <p className={`mt-4 rounded-lg p-3 text-sm ${run.would_recommend ? "bg-emerald-50 text-emerald-800" : "bg-amber-50 text-amber-800"}`}>
              {run.would_recommend ? "The evidence currently supports a recommendation for this query." : "The evidence does not yet clearly support a confident recommendation for this query."}
            </p>
          </Card>

          <div className="grid gap-6 md:grid-cols-2">
            <Card title="Why would an AI recommend you?">
              {run.strongest_evidence.length === 0 ? <p className="text-sm text-slate-500">No strong evidence found.</p> : (
                <ol className="list-decimal space-y-1 pl-5 text-sm text-slate-700">
                  {run.strongest_evidence.map((e, i) => <li key={i}>{e}</li>)}
                </ol>
              )}
            </Card>
            <Card title="Where the evidence is weaker">
              {run.weakest_evidence.length === 0 ? <p className="text-sm text-slate-500">No major gaps found.</p> : (
                <ol className="list-decimal space-y-1 pl-5 text-sm text-slate-700">
                  {run.weakest_evidence.map((e, i) => <li key={i}>{e}</li>)}
                </ol>
              )}
            </Card>
          </div>

          <Card title="Evidence map">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="text-left text-xs uppercase tracking-wide text-slate-500">
                  <tr>
                    <th className="py-2 pr-4">Requirement</th>
                    <th className="py-2 pr-4">Evidence</th>
                    <th className="py-2 pr-4">Strength</th>
                    <th className="py-2 pr-4">Source</th>
                  </tr>
                </thead>
                <tbody>
                  {run.evidence_map.map((item, i) => (
                    <tr key={i} className="border-t border-slate-100">
                      <td className="py-2 pr-4 font-medium text-slate-800">{item.requirement}</td>
                      <td className="py-2 pr-4 text-slate-600">{item.evidence}</td>
                      <td className="py-2 pr-4">
                        <StrengthPill strength={item.strength} />
                      </td>
                      <td className="py-2 pr-4">
                        {item.source_url ? <a href={item.source_url} target="_blank" rel="noreferrer" className="text-navy-900 hover:text-gold-500">link</a> : "--"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>

          <Card title="Top evidence gaps">
            <div className="space-y-3">
              {run.evidence_gaps.map((g, i) => (
                <div key={i} className="rounded-lg border border-slate-200 p-3 text-sm">
                  <div className="flex items-center justify-between">
                    <p className="font-medium text-slate-900">{g.gap}</p>
                    <span className="text-xs text-slate-400">importance {g.importance}/10</span>
                  </div>
                  <p className="mt-1 text-slate-600">{g.why_it_matters}</p>
                  <p className="mt-1 text-slate-700"><span className="font-semibold">Recommended action:</span> {g.recommended_action}</p>
                  <p className="text-xs text-slate-400">Estimated effort: {g.estimated_effort}</p>
                </div>
              ))}
            </div>
          </Card>

          <Card title="Simulated AI response" subtitle="Assembled only from indexed evidence -- never fabricated">
            <p className="text-slate-700">{run.simulated_answer}</p>
            {run.evidence_used.length > 0 && (
              <div className="mt-3">
                <p className="mb-1 text-xs uppercase tracking-wide text-slate-400">Evidence used</p>
                <ul className="space-y-1 text-sm">
                  {run.evidence_used.map((e, i) => (
                    <li key={i}>
                      <a href={e.url} target="_blank" rel="noreferrer" className="text-navy-900 hover:text-gold-500">{e.note}</a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </Card>

          <Card title="Query -> page mapping">
            <div className="space-y-2">
              {run.page_support.map((p) => (
                <div key={p.url}>
                  <div className="mb-1 flex justify-between text-sm">
                    <span className="truncate text-slate-700">{p.title || p.url}</span>
                    <span className="text-slate-500">{p.support_pct}%</span>
                  </div>
                  <div className="h-2 rounded-full bg-slate-200">
                    <div className="h-full rounded-full bg-gold-500" style={{ width: `${p.support_pct}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </>
      )}

      {clusters && clusters.queries_tested > 0 && (
        <Card title="Query cluster readiness" subtitle={`${clusters.queries_tested} queries tested`}>
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            {Object.entries(clusters.clusters).map(([cluster, score]) => (
              <div key={cluster} className="rounded-lg bg-slate-50 p-3 text-center">
                <p className="font-display text-xl font-bold text-navy-950">{score}</p>
                <p className="text-xs uppercase tracking-wide text-slate-500">{cluster}</p>
              </div>
            ))}
          </div>
          <p className="mt-3 text-sm text-slate-600">
            Strongest: <span className="font-medium">{clusters.strongest_cluster}</span> &middot; Weakest: <span className="font-medium">{clusters.weakest_cluster}</span>
          </p>
          {clusters.biggest_opportunity && <p className="mt-1 text-sm text-slate-600">Biggest opportunity: {clusters.biggest_opportunity}</p>}
        </Card>
      )}

      <Card title="Query library">
        {savedQueries.length === 0 ? (
          <p className="text-sm text-slate-500">Analyze a query above to start building your benchmark.</p>
        ) : (
          <table className="w-full text-sm">
            <thead className="text-left text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="py-2 pr-4">Query</th>
                <th className="py-2 pr-4">Cluster</th>
                <th className="py-2 pr-4">Score</th>
                <th className="py-2 pr-4">Change</th>
              </tr>
            </thead>
            <tbody>
              {savedQueries.map((q) => {
                const delta = q.latest_run && q.previous_score !== null ? Math.round((q.latest_run.readiness_score - (q.previous_score ?? 0)) * 10) / 10 : null;
                return (
                  <tr key={q.id} className="cursor-pointer border-t border-slate-100 hover:bg-slate-50" onClick={() => { setQuery(q.query_text); setRun(q.latest_run); }}>
                    <td className="py-2 pr-4">{q.query_text}</td>
                    <td className="py-2 pr-4">{q.cluster}</td>
                    <td className="py-2 pr-4 font-semibold">{q.latest_run?.readiness_score ?? "--"}</td>
                    <td className="py-2 pr-4">
                      {delta === null ? "--" : delta === 0 ? "→" : delta > 0 ? `↑ ${delta}` : `↓ ${Math.abs(delta)}`}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </Card>
    </div>
  );
}

function StrengthPill({ strength }: { strength: string }) {
  const styles: Record<string, string> = {
    VERY_STRONG: "bg-emerald-100 text-emerald-800",
    STRONG: "bg-emerald-50 text-emerald-700",
    MODERATE: "bg-amber-100 text-amber-800",
    WEAK: "bg-orange-100 text-orange-800",
    MISSING: "bg-red-100 text-red-800",
  };
  return <span className={`rounded px-2 py-0.5 text-xs font-semibold ${styles[strength] || ""}`}>{strength.replace("_", " ")}</span>;
}
