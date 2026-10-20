// /api/assistant-log - the last 30 days of assistant conversations as CSV,
// newest first. The admin key never travels in the URL:
//   - browser: GET shows a one-field form; it POSTs the key and the CSV downloads.
//   - script:  GET or POST with the header "Authorization: Bearer <ADMIN_KEY>".
// A ?key= query parameter is ignored (not accepted, not logged back); the form
// is shown instead. 503 until ADMIN_KEY and the D1 binding DB exist; 403 for a
// wrong key.
import { csvCell, maybeCleanup, safeEqual } from "../_lib/assistant.js";

const COLUMNS = ["ts", "page_path", "session_id", "user_message", "reply", "handoff"];
const NO_STORE = { "cache-control": "no-store", "x-robots-tag": "noindex" };

function plain(text, status) {
  return new Response(text, { status, headers: { "content-type": "text/plain; charset=utf-8", ...NO_STORE } });
}

function form(status = 200, notice = "") {
  const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><title>Assistant log export</title>
<style>body{font:16px/1.5 system-ui,sans-serif;max-width:28rem;margin:3rem auto;padding:0 1rem;color:#14213d;background:#fff}
label{display:block;margin:0 0 .4rem;font-weight:600}input{width:100%;box-sizing:border-box;padding:.6rem;font:inherit;border:1px solid #888;border-radius:6px}
button{margin-top:1rem;padding:.6rem 1.2rem;font:inherit;border:0;border-radius:6px;background:#14213d;color:#fff;cursor:pointer}
.n{color:#a00}</style></head><body>
<h1>Assistant log export</h1>
<p>Downloads the last 30 days of Ask OmniFit conversations as CSV.</p>
${notice ? `<p class="n" role="alert">${notice}</p>` : ""}
<form method="post" action="/api/assistant-log">
<label for="key">Admin key</label>
<input id="key" name="key" type="password" autocomplete="current-password" required>
<button type="submit">Download CSV</button>
</form></body></html>`;
  return new Response(html, {
    status,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "content-security-policy": "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'",
      "referrer-policy": "no-referrer",
      ...NO_STORE,
    },
  });
}

function bearer(request) {
  const m = /^Bearer\s+(.+)$/i.exec(request.headers.get("Authorization") || "");
  return m ? m[1].trim() : "";
}

function cleanupLater(context) {
  const p = maybeCleanup(context.env.DB, new Date()).catch((e) => console.error("assistant cleanup failed", e && e.message));
  if (context.waitUntil) context.waitUntil(p);
}

async function csv(db) {
  const since = new Date(Date.now() - 30 * 86400000).toISOString();
  const { results } = await db
    .prepare(`SELECT ${COLUMNS.join(", ")} FROM assistant_log WHERE ts >= ?1 ORDER BY ts DESC`)
    .bind(since)
    .all();
  const lines = [COLUMNS.join(",")];
  for (const row of results || []) lines.push(COLUMNS.map((c) => csvCell(row[c])).join(","));
  const day = new Date().toISOString().slice(0, 10);
  return new Response(lines.join("\r\n") + "\r\n", {
    headers: {
      "content-type": "text/csv; charset=utf-8",
      "content-disposition": `attachment; filename="assistant-log-${day}.csv"`,
      ...NO_STORE,
    },
  });
}

export async function onRequestGet(context) {
  const { request, env } = context;
  if (!env.ADMIN_KEY || !env.DB) return plain("Not configured.", 503);
  cleanupLater(context);
  const key = bearer(request);
  if (!key) {
    const inUrl = new URL(request.url).searchParams.has("key");
    return form(200, inUrl ? "Keys in the address are no longer accepted. Enter the key below." : "");
  }
  if (!(await safeEqual(key, env.ADMIN_KEY))) return plain("Forbidden.", 403);
  return csv(env.DB);
}

export async function onRequestPost(context) {
  const { request, env } = context;
  if (!env.ADMIN_KEY || !env.DB) return plain("Not configured.", 503);
  cleanupLater(context);
  let key = bearer(request);
  const fromForm = !key;
  if (fromForm) {
    try {
      const data = await request.formData();
      key = String(data.get("key") || "");
    } catch {
      key = "";
    }
  }
  if (!key || !(await safeEqual(key, env.ADMIN_KEY))) {
    return fromForm ? form(403, "That key is not right.") : plain("Forbidden.", 403);
  }
  return csv(env.DB);
}
