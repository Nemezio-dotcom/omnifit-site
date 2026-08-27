import { useEffect, useState } from "react";
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "../api/client";
import { Card } from "../components/Card";
import { OpportunityCard } from "../components/OpportunityCard";
import { ScoreBar, ScoreDial } from "../components/ScoreDial";
import { useSite } from "../context/SiteContext";
import type { DashboardData } from "../types/api";

export default function Dashboard() {
  const { siteId } = useSite();
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    if (!siteId) return;
    setLoading(true);
    try {
      const data = await api.get<DashboardData>(`/sites/${siteId}/dashboard`);
      setDashboard(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [siteId]);

  const runScan = async (useLocalFixture: boolean) => {
    if (!siteId) return;
    setScanning(true);
    setError(null);
    try {
      await api.post(`/sites/${siteId}/scan`, { use_local_fixture: useLocalFixture });
      await load();
    } catch (e) {
      if (!useLocalFixture) {
        setError(
          `Live scan failed (${(e as Error).message}). This environment may not have outbound network access. ` +
            `Retrying against the local fixture...`,
        );
        await runScan(true);
        return;
      }
      setError((e as Error).message);
    } finally {
      setScanning(false);
    }
  };

  if (loading && !dashboard) return <p className="text-slate-500">Loading dashboard...</p>;
  if (!dashboard) return null;

  const { site, latest_scan, fix_next, biggest_strength, biggest_weakness, recently_fixed, site_health, aio_opportunities, authority_opportunities, network_notice, score_trend } = dashboard;

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="font-display text-3xl font-bold text-navy-950">{site.name} Website Fix Radar</h1>
          <p className="text-slate-500">
            {latest_scan?.finished_at ? `Last scanned ${new Date(latest_scan.finished_at).toLocaleString()}` : "No scan yet"}
            {latest_scan && <span className="ml-2 text-xs uppercase tracking-wide text-slate-400">({latest_scan.source})</span>}
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => runScan(false)}
            disabled={scanning}
            className="rounded-lg bg-navy-950 px-5 py-2.5 font-medium text-white transition hover:bg-navy-900 disabled:opacity-50"
          >
            {scanning ? "Scanning..." : "Scan Now"}
          </button>
        </div>
      </div>

      {error && <div className="rounded-lg border border-amber-300 bg-amber-50 p-3 text-sm text-amber-900">{error}</div>}
      {network_notice && <div className="rounded-lg border border-blue-200 bg-blue-50 p-3 text-sm text-blue-900">{network_notice}</div>}

      {!latest_scan ? (
        <Card>
          <p className="text-slate-600">No completed scan yet. Click "Scan Now" to analyze {site.base_url}.</p>
        </Card>
      ) : (
        <>
          <Card title="Overall Score" subtitle="Heuristic 0-100 composite across all six dimensions below">
            <div className="flex flex-wrap items-center gap-10">
              <ScoreDial score={latest_scan.overall_score} size={160} />
              <div className="grid flex-1 grid-cols-2 gap-x-8 gap-y-4 sm:grid-cols-3">
                <ScoreBar label="Technical" score={latest_scan.technical_score} />
                <ScoreBar label="SEO" score={latest_scan.seo_score} />
                <ScoreBar label="Local" score={latest_scan.local_score} />
                <ScoreBar label="AIO" score={latest_scan.aio_score} />
                <ScoreBar label="Authority" score={latest_scan.authority_score} />
                <ScoreBar label="Conversion" score={latest_scan.conversion_score} />
              </div>
            </div>
          </Card>

          <Card title="What should I fix next?" subtitle="Ranked by a heuristic priority score -- impact x confidence, weighted against effort">
            {fix_next.length === 0 ? (
              <p className="text-slate-500">No open opportunities. Great shape, or run a scan.</p>
            ) : (
              <div className="space-y-3">
                {fix_next.map((opp, i) => (
                  <OpportunityCard key={opp.id} opportunity={opp} rank={i + 1} />
                ))}
              </div>
            )}
          </Card>

          <div className="grid gap-6 md:grid-cols-2">
            <Card title="Biggest strength">
              <p className="text-slate-700">{biggest_strength || "Not enough data yet."}</p>
            </Card>
            <Card title="Biggest weakness">
              <p className="text-slate-700">{biggest_weakness || "Not enough data yet."}</p>
            </Card>
          </div>

          <Card title="Site health">
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
              {Object.entries(site_health).map(([key, value]) => (
                <div key={key} className="rounded-lg bg-slate-50 p-4 text-center">
                  <p className="font-display text-2xl font-bold text-navy-950">{value}</p>
                  <p className="text-xs uppercase tracking-wide text-slate-500">{key.replace(/_/g, " ")}</p>
                </div>
              ))}
            </div>
          </Card>

          {score_trend.length > 1 && (
            <Card title="Score trend" subtitle="Overall score across completed scans">
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={score_trend}>
                    <XAxis dataKey="date" tickFormatter={(d) => new Date(d).toLocaleDateString()} fontSize={12} />
                    <YAxis domain={[0, 100]} fontSize={12} />
                    <Tooltip labelFormatter={(d) => new Date(d).toLocaleString()} />
                    <Line type="monotone" dataKey="overall_score" stroke="#c9a84c" strokeWidth={2} dot={false} name="Overall" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </Card>
          )}

          <div className="grid gap-6 md:grid-cols-2">
            <Card title="AIO opportunities">
              {aio_opportunities.length === 0 ? (
                <p className="text-sm text-slate-500">None open right now.</p>
              ) : (
                <div className="space-y-3">
                  {aio_opportunities.map((o) => (
                    <OpportunityCard key={o.id} opportunity={o} />
                  ))}
                </div>
              )}
            </Card>
            <Card title="Authority opportunities">
              {authority_opportunities.length === 0 ? (
                <p className="text-sm text-slate-500">None open right now.</p>
              ) : (
                <div className="space-y-3">
                  {authority_opportunities.map((o) => (
                    <OpportunityCard key={o.id} opportunity={o} />
                  ))}
                </div>
              )}
            </Card>
          </div>

          <Card title="Recently fixed">
            {recently_fixed.length === 0 ? (
              <p className="text-sm text-slate-500">Nothing marked fixed yet.</p>
            ) : (
              <ul className="space-y-2">
                {recently_fixed.map((o) => (
                  <li key={o.id} className="flex items-center justify-between text-sm">
                    <span className="text-slate-700">{o.title}</span>
                    <span className="text-slate-400">{new Date(o.updated_at).toLocaleDateString()}</span>
                  </li>
                ))}
              </ul>
            )}
          </Card>
        </>
      )}
    </div>
  );
}
