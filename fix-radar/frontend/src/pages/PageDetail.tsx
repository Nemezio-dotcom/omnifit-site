import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api/client";
import { Card } from "../components/Card";
import { ScoreDial } from "../components/ScoreDial";
import { SeverityBadge } from "../components/Badge";
import { useSite } from "../context/SiteContext";
import type { Finding, PageDetail as PageDetailType } from "../types/api";

interface AIAnalysis {
  strengths: string[];
  weaknesses: string[];
  missing_information: string[];
  unsupported_claims: string[];
  content_gaps: string[];
  entity_ambiguity: string[];
  authority_gaps: string[];
  recommended_improvements: string[];
  suggested_questions: string[];
  citation_worthy_passages: string[];
  recommended_internal_links: string[];
  confidence: number;
  generated_by: string;
}

export default function PageDetail() {
  const { pageId } = useParams();
  const { siteId } = useSite();
  const [page, setPage] = useState<PageDetailType | null>(null);
  const [findings, setFindings] = useState<Finding[]>([]);
  const [analysis, setAnalysis] = useState<AIAnalysis | null>(null);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    if (!siteId || !pageId) return;
    api.get<PageDetailType>(`/sites/${siteId}/pages/${pageId}`).then(setPage);
    api.get<Finding[]>(`/sites/${siteId}/findings`).then((all) => {
      setFindings(all);
    });
  }, [siteId, pageId]);

  const runAnalysis = async () => {
    if (!siteId || !pageId) return;
    setAnalyzing(true);
    try {
      setAnalysis(await api.post<AIAnalysis>(`/sites/${siteId}/pages/${pageId}/analyze`));
    } finally {
      setAnalyzing(false);
    }
  };

  if (!page) return <p className="text-slate-500">Loading...</p>;

  const pageFindings = findings.filter((f) => f.affected_url === page.url);
  const wrong = pageFindings.filter((f) => f.severity === "CRITICAL" || f.severity === "HIGH");
  const toFix = pageFindings.filter((f) => f.severity === "MEDIUM" || f.severity === "LOW");

  return (
    <div className="space-y-6">
      <div>
        <h1 className="break-all font-display text-2xl font-bold text-navy-950">{page.title || page.url}</h1>
        <a href={page.url} target="_blank" rel="noreferrer" className="text-sm text-slate-500 hover:text-gold-500">
          {page.url}
        </a>
      </div>

      <Card title="Page scores">
        <div className="grid grid-cols-3 gap-4 sm:grid-cols-6">
          <ScoreDial score={page.technical_score} size={90} label="Technical" />
          <ScoreDial score={page.seo_score} size={90} label="SEO" />
          <ScoreDial score={page.aio_score} size={90} label="AIO" />
          <ScoreDial score={page.local_score} size={90} label="Local" />
          <ScoreDial score={page.trust_score} size={90} label="Trust" />
          <ScoreDial score={page.conversion_score} size={90} label="Conversion" />
        </div>
      </Card>

      <div className="grid gap-6 md:grid-cols-2">
        <Card title="What's wrong">
          {wrong.length === 0 ? (
            <p className="text-sm text-slate-500">No high-severity issues on this page.</p>
          ) : (
            <ul className="space-y-2">
              {wrong.map((f) => (
                <li key={f.id} className="text-sm">
                  <SeverityBadge severity={f.severity} /> <span className="ml-1 text-slate-700">{f.explanation}</span>
                </li>
              ))}
            </ul>
          )}
        </Card>
        <Card title="What to fix">
          {toFix.length === 0 ? (
            <p className="text-sm text-slate-500">Nothing else flagged.</p>
          ) : (
            <ul className="space-y-2">
              {toFix.map((f) => (
                <li key={f.id} className="text-sm">
                  <SeverityBadge severity={f.severity} /> <span className="ml-1 text-slate-700">{f.recommended_action}</span>
                </li>
              ))}
            </ul>
          )}
        </Card>
      </div>

      <Card title="Metadata">
        <dl className="grid gap-3 text-sm sm:grid-cols-2">
          <div>
            <dt className="text-slate-500">Meta description</dt>
            <dd className="text-slate-800">{page.meta_description || <span className="text-red-600">Missing</span>}</dd>
          </div>
          <div>
            <dt className="text-slate-500">Canonical</dt>
            <dd className="text-slate-800">{page.canonical || <span className="text-red-600">Missing</span>}</dd>
          </div>
          <div>
            <dt className="text-slate-500">Robots meta</dt>
            <dd className="text-slate-800">{page.robots_meta || "none (indexable)"}</dd>
          </div>
          <div>
            <dt className="text-slate-500">In sitemap</dt>
            <dd className="text-slate-800">{page.in_sitemap ? "Yes" : "No"}</dd>
          </div>
          <div>
            <dt className="text-slate-500">Inbound internal links</dt>
            <dd className="text-slate-800">{page.inbound_internal_link_count}</dd>
          </div>
        </dl>
      </Card>

      <Card title="Content structure">
        <p className="mb-2 text-sm text-slate-500">{page.word_count} words</p>
        <div className="space-y-2 text-sm">
          <p><span className="font-semibold">H1:</span> {(page.h1 || []).join(", ") || "none"}</p>
          <p><span className="font-semibold">H2:</span> {(page.h2 || []).join(" | ") || "none"}</p>
          <p><span className="font-semibold">H3:</span> {(page.h3 || []).join(" | ") || "none"}</p>
        </div>
      </Card>

      <Card title="Schema">
        {page.json_ld && page.json_ld.length > 0 ? (
          <pre className="max-h-64 overflow-auto rounded bg-slate-900 p-3 text-xs text-emerald-300">{JSON.stringify(page.json_ld, null, 2)}</pre>
        ) : (
          <p className="text-sm text-slate-500">No structured data found on this page.</p>
        )}
      </Card>

      <Card title="AI recommendations" subtitle="Grounded only in this page's own content -- never invents facts">
        {!analysis ? (
          <button onClick={runAnalysis} disabled={analyzing} className="rounded-lg bg-navy-950 px-4 py-2 text-sm font-medium text-white hover:bg-navy-900 disabled:opacity-50">
            {analyzing ? "Analyzing..." : "Run AI analysis"}
          </button>
        ) : (
          <div className="space-y-4 text-sm">
            <p className="text-xs uppercase tracking-wide text-slate-400">Generated by: {analysis.generated_by} (confidence {Math.round(analysis.confidence * 100)}%)</p>
            <AnalysisList label="Strengths" items={analysis.strengths} />
            <AnalysisList label="Weaknesses" items={analysis.weaknesses} />
            <AnalysisList label="Missing information" items={analysis.missing_information} />
            <AnalysisList label="Unsupported claims" items={analysis.unsupported_claims} />
            <AnalysisList label="Content gaps" items={analysis.content_gaps} />
            <AnalysisList label="Entity ambiguity" items={analysis.entity_ambiguity} />
            <AnalysisList label="Recommended improvements" items={analysis.recommended_improvements} />
            <AnalysisList label="Suggested questions this page should answer" items={analysis.suggested_questions} />
            <AnalysisList label="Citation-worthy passages" items={analysis.citation_worthy_passages} />
          </div>
        )}
      </Card>
    </div>
  );
}

function AnalysisList({ label, items }: { label: string; items: string[] }) {
  if (!items || items.length === 0) return null;
  return (
    <div>
      <p className="mb-1 font-semibold text-slate-800">{label}</p>
      <ul className="list-disc space-y-1 pl-5 text-slate-600">
        {items.map((item, i) => (
          <li key={i}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
