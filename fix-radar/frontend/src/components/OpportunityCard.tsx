import { Link } from "react-router-dom";
import type { Opportunity } from "../types/api";
import { CategoryTag, SeverityBadge } from "./Badge";

export function OpportunityCard({ opportunity, rank }: { opportunity: Opportunity; rank?: number }) {
  return (
    <Link
      to={`/opportunities/${opportunity.id}`}
      className="block rounded-lg border border-slate-200 p-4 transition-colors hover:border-gold-500 hover:bg-gold-500/5"
    >
      <div className="flex items-start gap-4">
        {rank !== undefined && (
          <div className="flex h-9 w-9 flex-none items-center justify-center rounded-full bg-navy-950 font-display text-base font-bold text-gold-500">
            {rank}
          </div>
        )}
        <div className="min-w-0 flex-1">
          <div className="mb-1 flex flex-wrap items-center gap-2">
            <SeverityBadge severity={opportunity.severity} />
            <CategoryTag category={opportunity.category} />
          </div>
          <h3 className="font-medium text-slate-900">{opportunity.title}</h3>
          <p className="mt-1 line-clamp-2 text-sm text-slate-600">{opportunity.explanation}</p>
          <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-500">
            <span>Impact {opportunity.impact_score}/10</span>
            <span>Confidence {opportunity.confidence_score}/10</span>
            <span>Effort {opportunity.effort_score}/10</span>
            {opportunity.estimated_minutes && <span>~{opportunity.estimated_minutes} min</span>}
          </div>
        </div>
        <div className="flex-none text-right">
          <p className="font-display text-xl font-bold text-navy-950">{opportunity.priority_score}</p>
          <p className="text-[10px] uppercase tracking-wide text-slate-400">priority</p>
        </div>
      </div>
    </Link>
  );
}
