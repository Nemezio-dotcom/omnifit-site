// GET /api/assistant-log?key=<ADMIN_KEY> - the last 30 days of assistant
// conversations as CSV, newest first. 503 until ADMIN_KEY and the D1 binding DB
// exist; 403 for a missing or wrong key.
import { csvCell, safeEqual } from "../_lib/assistant.js";

const COLUMNS = ["ts", "page_path", "session_id", "user_message", "reply", "handoff"];

function plain(text, status) {
  return new Response(text, {
    status,
    headers: { "content-type": "text/plain; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex" },
  });
}

export async function onRequestGet({ request, env }) {
  if (!env.ADMIN_KEY || !env.DB) return plain("Not configured.", 503);
  const key = new URL(request.url).searchParams.get("key") || "";
  if (!key || !(await safeEqual(key, env.ADMIN_KEY))) return plain("Forbidden.", 403);

  const since = new Date(Date.now() - 30 * 86400000).toISOString();
  const { results } = await env.DB.prepare(
    `SELECT ${COLUMNS.join(", ")} FROM assistant_log WHERE ts >= ?1 ORDER BY ts DESC`,
  )
    .bind(since)
    .all();
  const lines = [COLUMNS.join(",")];
  for (const row of results || []) lines.push(COLUMNS.map((c) => csvCell(row[c])).join(","));
  const day = new Date().toISOString().slice(0, 10);
  return new Response(lines.join("\r\n") + "\r\n", {
    headers: {
      "content-type": "text/csv; charset=utf-8",
      "content-disposition": `attachment; filename="assistant-log-${day}.csv"`,
      "cache-control": "no-store",
      "x-robots-tag": "noindex",
    },
  });
}
