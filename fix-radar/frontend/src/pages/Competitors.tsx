import { useEffect, useState } from "react";
import { api } from "../api/client";
import { Card } from "../components/Card";
import { useSite } from "../context/SiteContext";
import type { Competitor, CompetitorGap } from "../types/api";

export default function Competitors() {
  const { siteId } = useSite();
  const [competitors, setCompetitors] = useState<Competitor[]>([]);
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");
  const [gap, setGap] = useState<CompetitorGap | null>(null);
  const [crawling, setCrawling] = useState<number | null>(null);

  const load = async () => {
    if (!siteId) return;
    setCompetitors(await api.get<Competitor[]>(`/competitors?site_id=${siteId}`));
    setGap(await api.get<CompetitorGap>(`/competitors/gap-analysis/${siteId}`));
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [siteId]);

  const addCompetitor = async () => {
    if (!siteId || !name || !url) return;
    await api.post("/competitors", { site_id: siteId, name, base_url: url });
    setName("");
    setUrl("");
    await load();
  };

  const crawl = async (id: number) => {
    setCrawling(id);
    try {
      await api.post(`/competitors/${id}/crawl`);
      await load();
    } catch (e) {
      alert(`Could not crawl this competitor: ${(e as Error).message}`);
    } finally {
      setCrawling(null);
    }
  };

  const remove = async (id: number) => {
    await api.del(`/competitors/${id}`);
    await load();
  };

  return (
    <div className="space-y-6">
      <h1 className="font-display text-2xl font-bold text-navy-950">Competitor Gap Analysis</h1>

      <Card title="Add a competitor">
        <div className="flex flex-wrap gap-2">
          <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} className="rounded-lg border border-slate-300 px-3 py-2 text-sm" />
          <input placeholder="https://competitor.com/" value={url} onChange={(e) => setUrl(e.target.value)} className="w-72 rounded-lg border border-slate-300 px-3 py-2 text-sm" />
          <button onClick={addCompetitor} className="rounded-lg bg-navy-950 px-4 py-2 text-sm font-medium text-white hover:bg-navy-900">
            Add
          </button>
        </div>
      </Card>

      <Card title="Competitors">
        {competitors.length === 0 ? (
          <p className="text-sm text-slate-500">Add up to 5 competitor URLs to unlock gap analysis.</p>
        ) : (
          <ul className="space-y-2">
            {competitors.map((c) => (
              <li key={c.id} className="flex items-center justify-between rounded-lg border border-slate-200 p-3 text-sm">
                <div>
                  <p className="font-medium text-slate-900">{c.name}</p>
                  <p className="text-slate-500">{c.base_url}</p>
                  <p className="text-xs text-slate-400">{c.last_crawled_at ? `Crawled ${new Date(c.last_crawled_at).toLocaleString()}` : "Not crawled yet"}</p>
                </div>
                <div className="flex gap-2">
                  <button onClick={() => crawl(c.id)} disabled={crawling === c.id} className="rounded-lg border border-slate-300 px-3 py-1.5 hover:bg-slate-50 disabled:opacity-50">
                    {crawling === c.id ? "Crawling..." : "Crawl"}
                  </button>
                  <button onClick={() => remove(c.id)} className="rounded-lg border border-red-200 px-3 py-1.5 text-red-600 hover:bg-red-50">
                    Remove
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </Card>

      {gap && (
        <>
          <Card title="Competitor gap summary" subtitle="Based only on what's genuinely crawlable -- no backlink or ranking claims">
            <ul className="list-disc space-y-1 pl-5 text-sm text-slate-700">
              {gap.summary.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </Card>

          {gap.top_opportunities.length > 0 && (
            <Card title="Top competitive opportunities">
              <ul className="space-y-2">
                {gap.top_opportunities.map((o, i) => (
                  <li key={i} className="rounded-lg border border-slate-200 p-3 text-sm">
                    <p className="font-medium text-slate-900">{o.title}</p>
                    <p className="text-slate-600">{o.why}</p>
                  </li>
                ))}
              </ul>
            </Card>
          )}

          {gap.comparison_table.length > 0 && (
            <Card title="Comparison" className="!p-0">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="border-b border-slate-200 bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-500">
                    <tr>
                      <th className="px-4 py-3">Site</th>
                      <th className="px-4 py-3">Pages</th>
                      <th className="px-4 py-3">Topics covered</th>
                      <th className="px-4 py-3">Testimonial pages</th>
                      <th className="px-4 py-3">Schema pages</th>
                    </tr>
                  </thead>
                  <tbody>
                    {gap.comparison_table.map((row: any, i) => (
                      <tr key={i} className="border-b border-slate-100">
                        <td className="px-4 py-3 font-medium">{row.name}</td>
                        <td className="px-4 py-3">{row.page_count}</td>
                        <td className="px-4 py-3">{(row.topics_covered || []).join(", ") || "--"}</td>
                        <td className="px-4 py-3">{row.testimonial_signal_pages}</td>
                        <td className="px-4 py-3">{row.schema_pages}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          )}
        </>
      )}
    </div>
  );
}
