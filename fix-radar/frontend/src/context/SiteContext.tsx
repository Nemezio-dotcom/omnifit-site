import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { api } from "../api/client";
import type { Site } from "../types/api";

interface SiteContextValue {
  sites: Site[];
  siteId: number | null;
  setSiteId: (id: number) => void;
  loading: boolean;
  refreshSites: () => Promise<Site[]>;
}

const SiteContext = createContext<SiteContextValue | undefined>(undefined);

const DEFAULT_SITE = { name: "OmniFit Performance", base_url: "https://omnifittraining.com/" };
const STORAGE_KEY = "fixradar.siteId";

// Module-scoped (not component-scoped) so React 18 StrictMode's intentional
// double-invoke of effects in dev can't race two "no sites yet" checks into
// creating two default sites -- both mounts share this one in-flight promise.
let initPromise: Promise<Site[]> | null = null;

async function initSites(): Promise<Site[]> {
  if (!initPromise) {
    initPromise = (async () => {
      const list = await api.get<Site[]>("/sites");
      if (list.length > 0) return list;
      const created = await api.post<Site>("/sites", DEFAULT_SITE);
      return [created];
    })();
  }
  return initPromise;
}

export function SiteProvider({ children }: { children: ReactNode }) {
  const [sites, setSites] = useState<Site[]>([]);
  const [siteId, setSiteIdState] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshSites = async () => {
    const list = await api.get<Site[]>("/sites");
    setSites(list);
    return list;
  };

  useEffect(() => {
    (async () => {
      setLoading(true);
      const list = await initSites();
      setSites(list);
      const stored = Number(localStorage.getItem(STORAGE_KEY));
      const initial = list.find((s) => s.id === stored)?.id ?? list[0].id;
      setSiteIdState(initial);
      setLoading(false);
    })();
  }, []);

  const setSiteId = (id: number) => {
    setSiteIdState(id);
    localStorage.setItem(STORAGE_KEY, String(id));
  };

  return (
    <SiteContext.Provider value={{ sites, siteId, setSiteId, loading, refreshSites }}>
      {children}
    </SiteContext.Provider>
  );
}

export function useSite() {
  const ctx = useContext(SiteContext);
  if (!ctx) throw new Error("useSite must be used within SiteProvider");
  return ctx;
}
