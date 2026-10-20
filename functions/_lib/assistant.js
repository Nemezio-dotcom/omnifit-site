// Shared logic for the "Ask OmniFit" assistant (functions/api/ask.js and
// functions/api/assistant-log.js). No dependencies: Web Crypto, fetch and the
// D1 binding only. Everything here is exported so tests/assistant.test.mjs can
// exercise it with a mocked fetch and an in-memory database.

export const ALLOWED_ORIGINS = new Set([
  "https://omnifittraining.com",
  "https://www.omnifittraining.com",
  "https://omnifit-site.pages.dev",
]);
export const ALLOWED_HOSTS = new Set([...ALLOWED_ORIGINS].map((o) => new URL(o).hostname));

export const API_URL = "https://api.anthropic.com/v1/messages";
export const DEFAULT_MODEL = "claude-sonnet-5-5";
export const MAX_TOKENS = 400;
export const MAX_USER_CHARS = 600;
export const MAX_ASSISTANT_CHARS = 2000; // history replayed by the browser; replies are far shorter
export const HISTORY_SENT = 10;
export const MAX_USER_TURNS = 12;
export const RATE_LIMIT_PER_HOUR = 30;
export const LOG_RETENTION_DAYS = 90;
export const UPSTREAM_TIMEOUT_MS = 25000;

// Returned instead of a model call once a conversation passes MAX_USER_TURNS.
export const TURN_CAP_REPLY =
  "We've covered a lot here. The best next step is a 45-minute consultation, where Nemezio can answer the rest of your questions directly.";

const TOKENS = { "[[BOOK]]": "book", "[[FIT_CHECK]]": "fit_check" };
const TOKEN_RE = /\[\[(BOOK|FIT_CHECK)\]\]/g;

// Thinking settings that keep a 400-token reply from being spent on reasoning.
// Keyed by model so ASSISTANT_MODEL can name a model that takes neither field.
const MODEL_PARAMS = {
  "claude-sonnet-5-5": { thinking: { type: "between_tools" } },
  "claude-opus-5-5": { output_config: { effort: "low" } },
  "claude-haiku-5-5": { output_config: { effort: "low" } },
};

export function json(body, status = 200, extra = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      "x-robots-tag": "noindex",
      ...extra,
    },
  });
}

export function isConfigured(env) {
  return Boolean(env && env.ANTHROPIC_API_KEY && env.DB);
}

export function originAllowed(request) {
  return ALLOWED_ORIGINS.has(request.headers.get("Origin") || "");
}

// "[[BOOK]] Sure." -> { reply: "Sure.", handoff: "book" }. The first token wins;
// every token is removed from the text either way.
export function extractHandoff(text) {
  const m = String(text || "").match(TOKEN_RE);
  const handoff = m ? TOKENS[m[0]] : null;
  const reply = String(text || "")
    .replace(TOKEN_RE, "")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/[ \t]{2,}/g, " ")
    .trim();
  return { reply, handoff };
}

const EMAIL_RE = /[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/gi;
const PHONE_RE = /(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b/g;

// Contact details never reach the model or the log.
export function redactContact(text) {
  return String(text).replace(EMAIL_RE, "[email removed]").replace(PHONE_RE, "[phone removed]");
}

export class BadRequest extends Error {
  constructor(code) {
    super(code);
    this.code = code;
  }
}

// Validates the browser's payload and returns { messages, userTurns, page,
// sessionId }. `messages` is the last HISTORY_SENT turns, starting on a user
// turn and ending on the new user message, contact details redacted.
export function parseBody(body) {
  if (!body || typeof body !== "object" || !Array.isArray(body.messages)) throw new BadRequest("bad_request");
  const all = body.messages;
  if (!all.length || all.length > 200) throw new BadRequest("bad_request");
  for (const m of all) {
    if (!m || (m.role !== "user" && m.role !== "assistant") || typeof m.content !== "string" || !m.content.trim()) {
      throw new BadRequest("bad_request");
    }
    if (m.role === "user" && m.content.length > MAX_USER_CHARS) throw new BadRequest("message_too_long");
    if (m.role === "assistant" && m.content.length > MAX_ASSISTANT_CHARS) throw new BadRequest("bad_request");
  }
  if (all[all.length - 1].role !== "user") throw new BadRequest("bad_request");
  const userTurns = all.filter((m) => m.role === "user").length;
  let messages = all.slice(-HISTORY_SENT);
  while (messages.length && messages[0].role !== "user") messages = messages.slice(1);
  messages = messages.map((m) => ({ role: m.role, content: m.role === "user" ? redactContact(m.content) : m.content }));
  const page = typeof body.page === "string" && body.page.startsWith("/") ? body.page.slice(0, 200) : "";
  const sessionId =
    typeof body.sessionId === "string" && /^[A-Za-z0-9-]{8,64}$/.test(body.sessionId)
      ? body.sessionId
      : crypto.randomUUID();
  return { messages, userTurns, page, sessionId };
}

export async function sha256Hex(text) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function randomHex(bytes) {
  return [...crypto.getRandomValues(new Uint8Array(bytes))].map((b) => b.toString(16).padStart(2, "0")).join("");
}

// A random salt per UTC day, kept in D1 and deleted after two days, so a
// visitor key cannot be linked across days and no raw IP is ever stored.
export async function dailySalt(db, now) {
  const day = now.toISOString().slice(0, 10);
  await db.prepare("INSERT OR IGNORE INTO assistant_salt (day, salt) VALUES (?1, ?2)").bind(day, randomHex(32)).run();
  const row = await db.prepare("SELECT salt FROM assistant_salt WHERE day = ?1").bind(day).first();
  return row.salt;
}

export async function visitorKey(db, request, now) {
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  return sha256Hex(ip + "|" + (await dailySalt(db, now)));
}

// Fixed one-hour windows. Returns true when this message is over the limit.
export async function overRateLimit(db, key, now) {
  const windowStart = Math.floor(now.getTime() / 3600000) * 3600;
  const row = await db
    .prepare(
      "INSERT INTO assistant_rate (visitor, window_start, count) VALUES (?1, ?2, 1) " +
        "ON CONFLICT (visitor, window_start) DO UPDATE SET count = count + 1 RETURNING count",
    )
    .bind(key, windowStart)
    .first();
  return row.count > RATE_LIMIT_PER_HOUR;
}

export async function loggedTurns(db, sessionId) {
  const row = await db.prepare("SELECT COUNT(*) AS n FROM assistant_log WHERE session_id = ?1").bind(sessionId).first();
  return row ? Number(row.n) : 0;
}

export async function logTurn(db, { now, page, sessionId, userMessage, reply, handoff }) {
  await db
    .prepare(
      "INSERT INTO assistant_log (ts, page_path, session_id, user_message, reply, handoff) VALUES (?1, ?2, ?3, ?4, ?5, ?6)",
    )
    .bind(now.toISOString(), page, sessionId, userMessage, reply, handoff || "")
    .run();
}

export async function cleanup(db, now) {
  const cutoff = new Date(now.getTime() - LOG_RETENTION_DAYS * 86400000).toISOString();
  const yesterday = new Date(now.getTime() - 86400000).toISOString().slice(0, 10);
  const oldWindow = Math.floor(now.getTime() / 3600000) * 3600 - 7200;
  await db.prepare("DELETE FROM assistant_log WHERE ts < ?1").bind(cutoff).run();
  await db.prepare("DELETE FROM assistant_rate WHERE window_start < ?1").bind(oldWindow).run();
  await db.prepare("DELETE FROM assistant_salt WHERE day < ?1").bind(yesterday).run();
}

// One non-streaming Messages API call. Returns the reply text, or throws.
export async function callClaude(env, system, messages, fetchImpl = fetch) {
  const model = env.ASSISTANT_MODEL || DEFAULT_MODEL;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), UPSTREAM_TIMEOUT_MS);
  try {
    const res = await fetchImpl(API_URL, {
      method: "POST",
      signal: controller.signal,
      headers: {
        "content-type": "application/json",
        "x-api-key": env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model,
        max_tokens: MAX_TOKENS,
        system: [{ type: "text", text: system, cache_control: { type: "ephemeral" } }],
        messages,
        ...(MODEL_PARAMS[model] || {}),
      }),
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    if (data.stop_reason === "refusal") throw new Error("upstream refusal");
    const text = (data.content || [])
      .filter((b) => b.type === "text")
      .map((b) => b.text)
      .join("")
      .trim();
    if (!text) throw new Error("upstream empty reply");
    return text;
  } finally {
    clearTimeout(timer);
  }
}

// Spreadsheet-safe CSV cell: quoted, quotes doubled, and a leading = + - @
// neutralised so a logged message cannot run as a formula when opened.
export function csvCell(value) {
  let s = value == null ? "" : String(value);
  if (/^[=+\-@\t\r]/.test(s)) s = "'" + s;
  return '"' + s.replace(/"/g, '""') + '"';
}

export async function safeEqual(a, b) {
  const [x, y] = await Promise.all([sha256Hex(String(a)), sha256Hex(String(b))]);
  let diff = 0;
  for (let i = 0; i < x.length; i++) diff |= x.charCodeAt(i) ^ y.charCodeAt(i);
  return diff === 0;
}
