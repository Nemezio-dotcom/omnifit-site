import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { Card } from "../components/Card";
import { useSite } from "../context/SiteContext";
import type { PageListItem } from "../types/api";

export default function PagesList() {
  const { siteId } = useSite();
  const [pages, setPages] = useState<PageListItem[]>([]);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    if (!siteId) return;
    api.get<PageListItem[]>(`/sites/${siteId}/pages`).then(setPages);
  }, [siteId]);

  const filtered = pages.filter((p) => p.url.toLowerCase().includes(filter.toLowerCase()) || (p.title || "").toLowerCase().includes(filter.toLowerCase()));

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="font-display text-2xl font-bold text-navy-950">Pages ({pages.length})</h1>
        <input
          placeholder="Filter by URL or title..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="w-72 rounded-lg border border-slate-300 px-3 py-2 text-sm"
        />
      </div>
      <Card className="!p-0">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="border-b border-slate-200 bg-slate-50 text-left text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-4 py-3">URL</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Words</th>
                <th className="px-4 py-3">Technical</th>
                <th className="px-4 py-3">SEO</th>
                <th className="px-4 py-3">AIO</th>
                <th className="px-4 py-3">Local</th>
                <th className="px-4 py-3">Flags</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((p) => (
                <tr key={p.id} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="max-w-md truncate px-4 py-3">
                    <Link to={`/pages/${p.id}`} className="font-medium text-navy-900 hover:text-gold-500">
                      {p.title || p.url}
                    </Link>
                    <p className="truncate text-xs text-slate-400">{p.url}</p>
                  </td>
                  <td className="px-4 py-3">
                    <span className={p.status_code && p.status_code < 400 ? "text-emerald-600" : "text-red-600"}>{p.status_code ?? "err"}</span>
                  </td>
                  <td className="px-4 py-3">{p.word_count ?? "--"}</td>
                  <td className="px-4 py-3">{p.technical_score ?? "--"}</td>
                  <td className="px-4 py-3">{p.seo_score ?? "--"}</td>
                  <td className="px-4 py-3">{p.aio_score ?? "--"}</td>
                  <td className="px-4 py-3">{p.local_score ?? "--"}</td>
                  <td className="px-4 py-3">
                    <div className="flex gap-1">
                      {p.is_orphan && <span className="rounded bg-amber-100 px-1.5 py-0.5 text-[10px] font-semibold text-amber-800">ORPHAN</span>}
                      {p.is_indexable === false && <span className="rounded bg-slate-200 px-1.5 py-0.5 text-[10px] font-semibold text-slate-700">NOINDEX</span>}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {filtered.length === 0 && <p className="p-6 text-center text-slate-500">No pages found. Run a scan first.</p>}
        </div>
      </Card>
    </div>
  );
}
