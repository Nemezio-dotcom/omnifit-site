export interface Site {
  id: number;
  name: string;
  base_url: string;
  created_at: string;
}

export interface Scan {
  id: number;
  site_id: number;
  started_at: string;
  finished_at: string | null;
  status: string;
  source: string;
  pages_crawled: number;
  error: string | null;
  technical_score: number | null;
  seo_score: number | null;
  local_score: number | null;
  aio_score: number | null;
  authority_score: number | null;
  conversion_score: number | null;
  overall_score: number | null;
}

export interface PageListItem {
  id: number;
  url: string;
  status_code: number | null;
  title: string | null;
  word_count: number | null;
  is_orphan: boolean;
  is_indexable: boolean | null;
  technical_score: number | null;
  seo_score: number | null;
  aio_score: number | null;
  local_score: number | null;
  trust_score: number | null;
  conversion_score: number | null;
}

export interface PageDetail extends PageListItem {
  meta_description: string | null;
  canonical: string | null;
  h1: string[] | null;
  h2: string[] | null;
  h3: string[] | null;
  internal_links: string[] | null;
  external_links: string[] | null;
  images: { src: string; alt: string | null; has_alt: boolean }[] | null;
  json_ld: Record<string, unknown>[] | null;
  open_graph: Record<string, string> | null;
  robots_meta: string | null;
  in_sitemap: boolean | null;
  inbound_internal_link_count: number;
  response_time_ms: number | null;
  redirect_chain: string[] | null;
  final_url: string | null;
}

export interface Finding {
  id: number;
  code: string;
  category: string;
  severity: string;
  affected_url: string | null;
  evidence: string | null;
  explanation: string;
  recommended_action: string;
  estimated_effort: number;
  estimated_impact: number;
  confidence: number;
}

export interface Opportunity {
  id: number;
  site_id: number;
  title: string;
  category: string;
  affected_pages: string[] | null;
  severity: string;
  impact_score: number;
  confidence_score: number;
  effort_score: number;
  priority_score: number;
  explanation: string;
  evidence: string | null;
  recommended_fix: string;
  expected_benefit: string | null;
  implementation_notes: string | null;
  estimated_minutes: number | null;
  status: string;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface Recommendation {
  id: number;
  opportunity_id: number;
  kind: string;
  content: {
    suggested_title?: string | null;
    suggested_meta_description?: string | null;
    suggested_h1?: string | null;
    faq_items?: { question: string; answer: string }[];
    section_outline?: string[];
    internal_link_suggestions?: string[];
    schema_draft?: Record<string, unknown> | null;
    content_brief?: string | null;
    generated_by: string;
    caveat: string;
  };
  generated_by: string;
  created_at: string;
}

export interface DashboardData {
  site: Site;
  latest_scan: Scan | null;
  fix_next: Opportunity[];
  biggest_strength: string | null;
  biggest_weakness: string | null;
  recently_fixed: Opportunity[];
  site_health: Record<string, number>;
  aio_opportunities: Opportunity[];
  authority_opportunities: Opportunity[];
  competitor_gaps: string[];
  simulator_summary: Record<string, unknown> | null;
  score_trend: {
    scan_id: number;
    date: string | null;
    overall_score: number | null;
    technical_score: number | null;
    seo_score: number | null;
    local_score: number | null;
    aio_score: number | null;
    authority_score: number | null;
    conversion_score: number | null;
  }[];
  network_notice: string | null;
}

export interface Competitor {
  id: number;
  site_id: number;
  name: string;
  base_url: string;
  last_crawled_at: string | null;
}

export interface CompetitorGap {
  summary: string[];
  top_opportunities: { title: string; why: string }[];
  comparison_table: Record<string, unknown>[];
}

export interface EvidenceItem {
  requirement: string;
  evidence: string;
  source_url: string | null;
  strength: string;
  gap: string | null;
}

export interface SimulatorRun {
  id: number;
  query_id: number;
  scan_id: number;
  readiness_score: number;
  sub_scores: Record<string, number>;
  entities: {
    profession: string | null;
    location: string | null;
    audience: string | null;
    intent: string;
    cluster: string;
    decision_criteria: string[];
  };
  evidence_map: EvidenceItem[];
  strongest_evidence: string[];
  weakest_evidence: string[];
  would_recommend: boolean;
  simulated_answer: string;
  evidence_used: { url: string; note: string }[];
  page_support: { url: string; title: string | null; support_pct: number }[];
  evidence_gaps: {
    gap: string;
    importance: number;
    current_evidence: string;
    why_it_matters: string;
    recommended_action: string;
    estimated_effort: string;
  }[];
  generated_by: string;
  created_at: string;
}

export interface SavedQuery {
  id: number;
  site_id: number;
  query_text: string;
  intent: string | null;
  cluster: string | null;
  created_at: string;
  latest_run: SimulatorRun | null;
  previous_score: number | null;
}

export interface ClusterReadiness {
  clusters: Record<string, number>;
  strongest_cluster: string | null;
  weakest_cluster: string | null;
  biggest_opportunity: string | null;
  queries_tested: number;
}
