import { useEffect, useState } from "react";
import { api } from "../api/client";
import { Card } from "../components/Card";
import { OpportunityCard } from "../components/OpportunityCard";
import { useSite } from "../context/SiteContext";
import type { Opportunity } from "../types/api";

const STATUSES = ["OPEN", "IN_PROGRESS", "FIXED", "IGNORED"];

export default function Opportunities() {
  const { siteId } = useSite();
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [status, setStatus] = useState("OPEN");

  useEffect(() => {
    if (!siteId) return;
    api.get<Opportunity[]>(`/sites/${siteId}/opportunities?status=${status}`).then(setOpportunities);
  }, [siteId, status]);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="font-display text-2xl font-bold text-navy-950">Opportunities</h1>
        <div className="flex gap-2">
          {STATUSES.map((s) => (
            <button
              key={s}
              onClick={() => setStatus(s)}
              className={`rounded-full px-3 py-1 text-sm font-medium ${
                status === s ? "bg-navy-950 text-white" : "bg-slate-100 text-slate-600 hover:bg-slate-200"
              }`}
            >
              {s.replace("_", " ")}
            </button>
          ))}
        </div>
      </div>
      <Card>
        {opportunities.length === 0 ? (
          <p className="text-slate-500">Nothing here.</p>
        ) : (
          <div className="space-y-3">
            {opportunities.map((o) => (
              <OpportunityCard key={o.id} opportunity={o} />
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
