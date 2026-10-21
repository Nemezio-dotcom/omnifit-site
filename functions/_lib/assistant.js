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
// Messages per hour across every visitor together (ASSISTANT_GLOBAL_LIMIT_PER_HOUR
// overrides). Caps what the API key can spend however many addresses send.
export const GLOBAL_LIMIT_PER_HOUR = 300;
export const GLOBAL_RATE_KEY = "global"; // visitor keys are 64 hex chars, so this cannot collide
export const LOG_RETENTION_DAYS = 90;
export const CLEANUP_INTERVAL_MS = 10 * 60000;
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

// A reply cut off at max_tokens: drop a half-written handoff token ("[[BO"),
// then cut back to the last complete sentence (or line) so it reads as
// finished. Complete tokens in the dropped tail are kept, so a hand-off the
// model already wrote still shows its button. A reply with no sentence end at
// all is cut at the last word and given an ellipsis.
const PARTIAL_TOKEN_RE = /\[(?:\[[A-Z_]*\]?)?\s*$/;
const SENTENCE_END_RE = /[.!?…]["'”’)\]]*(?=\s|$)|\n/g;
export function tidyTruncated(text) {
  const s = String(text || "").replace(PARTIAL_TOKEN_RE, "").replace(/\s+$/, "");
  let cut = -1;
  for (const m of s.matchAll(SENTENCE_END_RE)) {
    // A cut inside a complete token is impossible: tokens hold no . ! ? or newline.
    // A digit and a period at the very end may be a figure cut mid-decimal
    // ("4." of "4.98"), so that is not trusted as a sentence end.
    if (m[0] === "." && m.index + 1 === s.length && /\d/.test(s[m.index - 1] || "")) continue;
    cut = m[0] === "\n" ? m.index : m.index + m[0].length;
  }
  let head = cut > 0 ? s.slice(0, cut) : "";
  if (!head.replace(TOKEN_RE, "").trim()) {
    // No usable sentence end: keep whole words and mark the cut.
    head = s.replace(/\s*\S*$/, "").replace(/[\s,;:–—-]+$/, "");
    head = head.replace(TOKEN_RE, "").trim() ? head + "…" : "";
  }
  const tail = s.slice(head.replace(/…$/, "").length);
  const tokens = tail.match(TOKEN_RE) || [];
  return (head.trimEnd() + (tokens.length ? " " + tokens.join(" ") : "")).trim();
}

// ── contact redaction ──────────────────────────────────────────────
// Emails: literal ("a@b.com", "a @ b.com"), bracketed ("a [at] b [dot] com",
// "a(at)b.com") and spelled out ("a dot b at c dot com"). The bare-word form
// with real dots ("john at gmail.com") is only treated as an email when the
// domain is a common mail provider or the name part looks like one (has a
// dot, digit, underscore or plus), so "I found you at yelp.com" survives.
const LOCAL_CH = "[A-Z0-9_%+-]";
const DOT_OBF = "(?:\\s*(?:\\[dot\\]|\\(dot\\)|\\{dot\\}|<dot>)\\s*|\\s+dot\\s+)";
const DOT_ANY = `(?:${DOT_OBF}|\\s+\\.\\s+|\\.)`;
const LOCAL = `${LOCAL_CH}+(?:${DOT_ANY}${LOCAL_CH}+)*`;
const AT_BRACKET = "\\s*(?:\\[at\\]|\\(at\\)|\\{at\\}|<at>)\\s*";
const AT_SYM = "\\s*@\\s*";
const AT_WORD = "\\s+at\\s+";
const LABEL = "[A-Z0-9-]+";
const TLD = "[A-Z]{2,24}";
const DOMAIN_ANY = `(?:${LABEL}${DOT_ANY})+${TLD}`;
const DOMAIN_OBF = `(?:${LABEL}${DOT_ANY})*${LABEL}${DOT_OBF}(?:${LABEL}${DOT_ANY})*${TLD}`;
const END = "(?![A-Z0-9-])";
const EMAIL_RES = [
  // Any "at" with a spelled-out dot in the domain.
  new RegExp(`${LOCAL}(?:${AT_SYM}|${AT_BRACKET}|${AT_WORD})${DOMAIN_OBF}${END}`, "gi"),
  // "@" or a bracketed at, with any dots.
  new RegExp(`${LOCAL}(?:${AT_SYM}|${AT_BRACKET})${DOMAIN_ANY}${END}`, "gi"),
];
const WORD_AT_RE = new RegExp(`(${LOCAL})${AT_WORD}(${DOMAIN_ANY})${END}`, "gi");
const MAIL_PROVIDERS =
  /^(?:gmail|googlemail|yahoo|ymail|hotmail|outlook|live|msn|icloud|me|mac|aol|proton|protonmail|pm|gmx|mail|zoho|comcast|att|sbcglobal|cox|verizon|charter|earthlink|fastmail|hey|yandex)$/i;

// Phones: 10 to 15 digits in one run, separated only by spaces, dots, dashes
// or brackets, with an optional leading "+" ("+52 664 123 4567", "0061 412
// 345 678", "(619) 555-0100"). Not preceded by a letter, digit, "$", "." or
// ",", and not followed by a digit or a decimal/thousands part, so prices,
// dates, ZIP codes, street numbers and times are left alone.
const PHONE_RE = /(?<![A-Za-z0-9$.,\/])\+?\(?\d(?:[ \t\u00a0.\-()]{0,3}\d){9,14}(?![0-9]|[.,]\d)/g;

// Contact details never reach the model or the log.
export function redactContact(text) {
  let s = String(text);
  for (const re of EMAIL_RES) s = s.replace(re, "[email removed]");
  s = s.replace(WORD_AT_RE, (all, local, domain) => {
    const looksLikeEmail = /[._+0-9]|\bdot\b/i.test(local) || MAIL_PROVIDERS.test(domain.split(".")[0].trim());
    return looksLikeEmail ? "[email removed]" : all;
  });
  // A run made only of years ("2024 2025 2026") is not a phone number.
  return s.replace(PHONE_RE, (all) =>
    all.split(/[^0-9]+/).every((g) => /^(?:19|20)\d\d$/.test(g)) ? all : "[phone removed]",
  );
}

export class BadRequest extends Error {
  constructor(code) {
    super(code);
    this.code = code;
  }
}

// Validates the browser's payload and returns { userMessage, userTurns, page,
// sessionId }. Only the new (last) user message is used: earlier turns are
// rebuilt from the log for the session (sessionHistory), so assistant text
// the browser sends back is never trusted. The browser may keep sending its
// history; it is checked for shape and its user-turn count only ever raises
// the turn count.
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
  const userMessage = redactContact(all[all.length - 1].content);
  const page = typeof body.page === "string" && body.page.startsWith("/") ? body.page.slice(0, 200) : "";
  const sessionId =
    typeof body.sessionId === "string" && /^[A-Za-z0-9-]{8,64}$/.test(body.sessionId)
      ? body.sessionId
      : crypto.randomUUID();
  return { userMessage, userTurns, page, sessionId };
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

// The address a visitor is rate-limited by: IPv4 as is, IPv6 by its /64
// prefix (one household or device usually holds a whole /64, so keying on the
// full address would let it rotate through 2^64 keys). Unparseable input is
// used as is.
export function rateSubject(ip) {
  const raw = String(ip || "").trim().toLowerCase();
  if (!raw.includes(":")) return raw || "unknown";
  const addr = raw.replace(/^\[|\]$/g, "").replace(/%.*$/, "");
  const halves = addr.split("::");
  if (halves.length > 2) return raw;
  const groups = (part) => {
    if (!part) return [];
    const out = [];
    for (const g of part.split(":")) {
      if (/^\d+\.\d+\.\d+\.\d+$/.test(g)) {
        const b = g.split(".").map(Number);
        if (b.some((n) => n > 255)) return null;
        out.push(((b[0] << 8) | b[1]).toString(16), ((b[2] << 8) | b[3]).toString(16));
      } else if (/^[0-9a-f]{1,4}$/.test(g)) out.push(parseInt(g, 16).toString(16));
      else return null;
    }
    return out;
  };
  const head = groups(halves[0]);
  const tail = halves.length === 2 ? groups(halves[1]) : [];
  if (!head || !tail) return raw;
  const fill = 8 - head.length - tail.length;
  if (halves.length === 2 ? fill < 1 : fill !== 0) return raw;
  const full = [...head, ...Array(fill).fill("0"), ...tail];
  return full.slice(0, 4).join(":") + "::/64";
}

export async function visitorKey(db, request, now) {
  const ip = rateSubject(request.headers.get("CF-Connecting-IP"));
  return sha256Hex(ip + "|" + (await dailySalt(db, now)));
}

export function globalLimit(env) {
  const n = Number.parseInt(env && env.ASSISTANT_GLOBAL_LIMIT_PER_HOUR, 10);
  return Number.isFinite(n) && n > 0 ? n : GLOBAL_LIMIT_PER_HOUR;
}

// Fixed one-hour windows. Returns true when this message is over the limit.
// Used per visitor (key = visitor hash) and site-wide (key = GLOBAL_RATE_KEY).
export async function overRateLimit(db, key, now, limit = RATE_LIMIT_PER_HOUR) {
  const windowStart = Math.floor(now.getTime() / 3600000) * 3600;
  const row = await db
    .prepare(
      "INSERT INTO assistant_rate (visitor, window_start, count) VALUES (?1, ?2, 1) " +
        "ON CONFLICT (visitor, window_start) DO UPDATE SET count = count + 1 RETURNING count",
    )
    .bind(key, windowStart)
    .first();
  return row.count > limit;
}

export async function loggedTurns(db, sessionId) {
  const row = await db.prepare("SELECT COUNT(*) AS n FROM assistant_log WHERE session_id = ?1").bind(sessionId).first();
  return row ? Number(row.n) : 0;
}

// The conversation so far, rebuilt from what this server logged for the
// session (visitor messages already redacted, replies as returned): the last
// few exchanges, oldest first, as Messages API turns. With the new message
// appended this stays within HISTORY_SENT messages.
export async function sessionHistory(db, sessionId, pairs = Math.floor((HISTORY_SENT - 1) / 2)) {
  const { results } = await db
    .prepare("SELECT user_message, reply FROM assistant_log WHERE session_id = ?1 ORDER BY id DESC LIMIT ?2")
    .bind(sessionId, pairs)
    .all();
  const out = [];
  for (const r of (results || []).reverse()) {
    if (!String(r.user_message || "").trim() || !String(r.reply || "").trim()) continue;
    out.push({ role: "user", content: String(r.user_message) }, { role: "assistant", content: String(r.reply) });
  }
  return out;
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

// Retention without relying on any one request type: every /api/ask and
// /api/assistant-log request calls this, and at most once per
// CLEANUP_INTERVAL_MS one of them claims the assistant_meta row and runs
// cleanup(). The daily worker in workers/assistant-cleanup calls cleanup()
// directly. If assistant_meta does not exist yet (schema.sql not re-run), it
// cleans on every call instead. Returns true when it cleaned.
export async function maybeCleanup(db, now = new Date()) {
  try {
    const claimed = await db
      .prepare(
        "INSERT INTO assistant_meta (key, value) VALUES ('last_cleanup', ?1) " +
          "ON CONFLICT (key) DO UPDATE SET value = excluded.value WHERE assistant_meta.value < ?2 RETURNING value",
      )
      .bind(now.toISOString(), new Date(now.getTime() - CLEANUP_INTERVAL_MS).toISOString())
      .first();
    if (!claimed) return false;
  } catch (e) {
    console.error("assistant_meta unavailable; cleaning anyway", e && e.message);
  }
  await cleanup(db, now);
  return true;
}

// One non-streaming Messages API call. Returns the reply text, or throws. A
// reply cut off at max_tokens is tidied (tidyTruncated) rather than shown
// mid-sentence.
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
    let text = (data.content || [])
      .filter((b) => b.type === "text")
      .map((b) => b.text)
      .join("")
      .trim();
    if (data.stop_reason === "max_tokens") text = tidyTruncated(text);
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
