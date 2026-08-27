import { NavLink, Outlet } from "react-router-dom";
import { useSite } from "../context/SiteContext";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", end: true },
  { to: "/pages", label: "Pages" },
  { to: "/opportunities", label: "Opportunities" },
  { to: "/simulator", label: "AI Simulator" },
  { to: "/competitors", label: "Competitors" },
];

export default function Layout() {
  const { sites, siteId, setSiteId, loading } = useSite();

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-navy-950 text-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div>
            <p className="font-display text-lg font-semibold tracking-tight">
              OmniFit <span className="text-gold-500">Fix Radar</span>
            </p>
            <p className="text-xs text-white/50">Internal diagnostic system</p>
          </div>
          <nav className="flex items-center gap-6">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  `text-sm font-medium transition-colors ${
                    isActive ? "text-gold-500" : "text-white/70 hover:text-white"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
          {!loading && sites.length > 0 && (
            <select
              className="rounded border border-white/20 bg-navy-900 px-2 py-1 text-sm text-white"
              value={siteId ?? ""}
              onChange={(e) => setSiteId(Number(e.target.value))}
            >
              {sites.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name}
                </option>
              ))}
            </select>
          )}
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-6 py-8">
        {loading ? <p className="text-slate-500">Loading...</p> : <Outlet />}
      </main>
    </div>
  );
}
