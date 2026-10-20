// Unit tests for the Ask OmniFit functions. No network: fetch is mocked, and
// D1 is stood in for by an in-memory SQLite database built from schema.sql.
//
//   node --test tests/
import { test, beforeEach } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { DatabaseSync } from "node:sqlite";

import { onRequestGet as askGet, onRequestPost as askPost } from "../functions/api/ask.js";
import { onRequestGet as logGet } from "../functions/api/assistant-log.js";
import {
  extractHandoff,
  redactContact,
  csvCell,
  cleanup,
  TURN_CAP_REPLY,
  RATE_LIMIT_PER_HOUR,
} from "../functions/_lib/assistant.js";
import { KNOWLEDGE } from "../functions/_lib/knowledge.js";

const SCHEMA = readFileSync(new URL("../schema.sql", import.meta.url), "utf8");
const ORIGIN = "https://www.omnifittraining.com";

// The subset of the D1 binding the functions use.
class FakeD1 {
  constructor() {
    this.db = new DatabaseSync(":memory:");
    this.db.exec(SCHEMA);
  }
  prepare(sql) {
    const db = this.db;
    let args = [];
    return {
      bind(...a) { args = a; return this; },
      async first() { return db.prepare(sql).get(...args) ?? null; },
      async run() { db.prepare(sql).run(...args); return { success: true }; },
      async all() { return { results: db.prepare(sql).all(...args) }; },
    };
  }
  rows(table) { return this.db.prepare(`SELECT * FROM ${table}`).all(); }
}

let calls;
function mockFetch(reply = "Studio Momentum on The Program is $640 per 4-week cycle. [[BOOK]]", status = 200) {
  calls = [];
  globalThis.fetch = async (url, init) => {
    calls.push({ url, init, body: JSON.parse(init.body) });
    if (status !== 200) return new Response(JSON.stringify({ type: "error" }), { status });
    return new Response(JSON.stringify({
      type: "message", role: "assistant", stop_reason: "end_turn",
      content: [{ type: "text", text: reply }],
    }), { status: 200, headers: { "content-type": "application/json" } });
  };
}

function env(extra = {}) {
  return { ANTHROPIC_API_KEY: "test-key", DB: new FakeD1(), ...extra };
}

function post(body, { origin = ORIGIN, ip = "203.0.113.7" } = {}) {
  const headers = { "content-type": "application/json", "CF-Connecting-IP": ip };
  if (origin) headers.Origin = origin;
  return new Request("https://www.omnifittraining.com/api/ask", {
    method: "POST", headers, body: typeof body === "string" ? body : JSON.stringify(body),
  });
}

function convo(n, last = "What does it cost?") {
  // n user turns, alternating with assistant replies, ending on a user turn.
  const m = [];
  for (let i = 1; i < n; i++) {
    m.push({ role: "user", content: `question ${i}` });
    m.push({ role: "assistant", content: `answer ${i}` });
  }
  m.push({ role: "user", content: last });
  return m;
}

async function ask(e, body, opts) {
  const res = await askPost({ request: post(body, opts), env: e });
  return { status: res.status, data: await res.json() };
}

beforeEach(() => mockFetch());

// ── token stripping ────────────────────────────────────────────────
test("extractHandoff strips [[BOOK]] and returns it as handoff", () => {
  assert.deepEqual(extractHandoff("Happy to help. [[BOOK]]"), { reply: "Happy to help.", handoff: "book" });
});
test("extractHandoff strips [[FIT_CHECK]] and returns it as handoff", () => {
  assert.deepEqual(extractHandoff("[[FIT_CHECK]] Not sure? Try this."), { reply: "Not sure? Try this.", handoff: "fit_check" });
});
test("extractHandoff: no token, null handoff; several tokens, all stripped, first wins", () => {
  assert.deepEqual(extractHandoff("Plain answer."), { reply: "Plain answer.", handoff: null });
  assert.deepEqual(extractHandoff("A [[FIT_CHECK]] b [[BOOK]]"), { reply: "A b", handoff: "fit_check" });
});
test("POST returns the reply without the token and handoff as a separate field", async () => {
  const { status, data } = await ask(env(), { messages: convo(1), page: "/", sessionId: "abcdef12-3456" });
  assert.equal(status, 200);
  assert.equal(data.reply, "Studio Momentum on The Program is $640 per 4-week cycle.");
  assert.equal(data.handoff, "book");
  assert.ok(!data.reply.includes("[["));
});

// ── 503 when unconfigured ──────────────────────────────────────────
test("503 when ANTHROPIC_API_KEY is missing", async () => {
  const { status } = await ask({ DB: new FakeD1() }, { messages: convo(1) });
  assert.equal(status, 503);
  assert.equal(calls.length, 0);
});
test("503 when the DB binding is missing", async () => {
  const { status } = await ask({ ANTHROPIC_API_KEY: "k" }, { messages: convo(1) });
  assert.equal(status, 503);
  assert.equal(calls.length, 0);
});
test("GET status probe: 503 unconfigured, 200 configured, 503 on an unlisted host", async () => {
  const at = (u) => new Request(u);
  assert.equal((await askGet({ request: at("https://www.omnifittraining.com/api/ask"), env: {} })).status, 503);
  const ok = await askGet({ request: at("https://www.omnifittraining.com/api/ask"), env: env() });
  assert.equal(ok.status, 200);
  assert.deepEqual(await ok.json(), { ok: true });
  assert.equal((await askGet({ request: at("https://preview.omnifit-site.pages.dev/api/ask"), env: env() })).status, 503);
});
test("GET status probe names what is missing, never a value", async () => {
  const at = new Request("https://omnifit-site.pages.dev/api/ask");
  assert.deepEqual(await (await askGet({ request: at, env: {} })).json(), { ok: false, missing: ["ANTHROPIC_API_KEY", "DB"] });
  assert.deepEqual(await (await askGet({ request: at, env: { DB: new FakeD1() } })).json(), { ok: false, missing: ["ANTHROPIC_API_KEY"] });
  const body = await (await askGet({ request: at, env: { ANTHROPIC_API_KEY: "sk-secret" } })).text();
  assert.deepEqual(JSON.parse(body), { ok: false, missing: ["DB"] });
  assert.ok(!body.includes("sk-secret"));
  assert.deepEqual(await (await askGet({ request: new Request("https://x.omnifit-site.pages.dev/api/ask"), env: env() })).json(),
    { ok: false, host_not_allowed: "x.omnifit-site.pages.dev" });
});
test("assistant-log: 503 without ADMIN_KEY or DB", async () => {
  const r = new Request("https://www.omnifittraining.com/api/assistant-log?key=x");
  assert.equal((await logGet({ request: r, env: { DB: new FakeD1() } })).status, 503);
  assert.equal((await logGet({ request: r, env: { ADMIN_KEY: "x" } })).status, 503);
});

// ── origin ─────────────────────────────────────────────────────────
test("rejects a missing or foreign Origin with 403", async () => {
  for (const origin of [null, "https://evil.example", "http://www.omnifittraining.com", "https://x.omnifit-site.pages.dev"]) {
    const { status } = await ask(env(), { messages: convo(1) }, { origin });
    assert.equal(status, 403, String(origin));
  }
  assert.equal(calls.length, 0);
});
test("accepts the three allowed origins", async () => {
  for (const origin of ["https://omnifittraining.com", "https://www.omnifittraining.com", "https://omnifit-site.pages.dev"]) {
    assert.equal((await ask(env(), { messages: convo(1) }, { origin })).status, 200, origin);
  }
});

// ── caps ───────────────────────────────────────────────────────────
test("rejects a user message over 600 characters", async () => {
  const { status, data } = await ask(env(), { messages: convo(1, "x".repeat(601)) });
  assert.equal(status, 400);
  assert.equal(data.error, "message_too_long");
  assert.equal((await ask(env(), { messages: convo(1, "x".repeat(600)) })).status, 200);
  assert.equal(calls.length, 1);
});
test("rejects malformed payloads", async () => {
  for (const body of ["not json", {}, { messages: [] }, { messages: [{ role: "assistant", content: "hi" }] },
    { messages: [{ role: "system", content: "hi" }] }, { messages: [{ role: "user", content: 5 }] }]) {
    assert.equal((await ask(env(), body)).status, 400, JSON.stringify(body));
  }
});
test("sends only the last 10 messages, starting on a user turn", async () => {
  await ask(env(), { messages: convo(8) }); // 15 messages
  const sent = calls[0].body.messages;
  assert.ok(sent.length <= 10);
  assert.equal(sent[0].role, "user");
  assert.equal(sent.at(-1).content, "What does it cost?");
  assert.equal(sent.length, 9); // last 10 began on an assistant turn, which is dropped
});
test("after 12 user turns, returns the fixed handoff reply without calling the API", async () => {
  assert.equal((await ask(env(), { messages: convo(12) })).status, 200);
  assert.equal(calls.length, 1);
  const { status, data } = await ask(env(), { messages: convo(13) });
  assert.equal(status, 200);
  assert.equal(data.reply, TURN_CAP_REPLY);
  assert.equal(data.handoff, "book");
  assert.equal(calls.length, 1);
});
test("the turn cap also counts turns already logged for the session", async () => {
  const e = env();
  for (let i = 0; i < 12; i++) await ask(e, { messages: convo(1), sessionId: "session-0001" });
  const { data } = await ask(e, { messages: convo(1), sessionId: "session-0001" });
  assert.equal(data.reply, TURN_CAP_REPLY);
  assert.equal(calls.length, 12);
});

// ── rate limit ─────────────────────────────────────────────────────
test(`rate limit: ${RATE_LIMIT_PER_HOUR} messages an hour per visitor, then 429`, async () => {
  const e = env();
  for (let i = 0; i < RATE_LIMIT_PER_HOUR; i++) {
    assert.equal((await ask(e, { messages: convo(1), sessionId: `sess-${1000 + i}` })).status, 200, `message ${i + 1}`);
  }
  const over = await ask(e, { messages: convo(1), sessionId: "sess-9999" });
  assert.equal(over.status, 429);
  assert.equal(over.data.error, "rate_limited");
  assert.equal((await ask(e, { messages: convo(1) }, { ip: "198.51.100.9" })).status, 200, "another visitor is unaffected");
});
test("never stores the raw IP", async () => {
  const e = env();
  await ask(e, { messages: convo(1) }, { ip: "203.0.113.77" });
  for (const t of ["assistant_log", "assistant_rate", "assistant_salt"]) {
    assert.ok(!JSON.stringify(e.DB.rows(t)).includes("203.0.113.77"), t);
  }
  const [rate] = e.DB.rows("assistant_rate");
  assert.match(rate.visitor, /^[0-9a-f]{64}$/);
});

// ── API request shape ──────────────────────────────────────────────
test("calls the Messages API with the required headers, model, max_tokens and cached system block", async () => {
  await ask(env(), { messages: convo(1) });
  const { url, init, body } = calls[0];
  assert.equal(url, "https://api.anthropic.com/v1/messages");
  assert.equal(init.headers["x-api-key"], "test-key");
  assert.equal(init.headers["anthropic-version"], "2023-06-01");
  assert.equal(body.model, "claude-sonnet-5-5");
  assert.equal(body.max_tokens, 400);
  assert.ok(!body.stream);
  assert.equal(body.system.length, 1);
  assert.deepEqual(body.system[0].cache_control, { type: "ephemeral" });
  assert.ok(body.system[0].text.startsWith("You are the AI assistant on omnifittraining.com"));
  assert.ok(body.system[0].text.includes(KNOWLEDGE.trim()));
});
test("ASSISTANT_MODEL overrides the model", async () => {
  await ask(env({ ASSISTANT_MODEL: "claude-opus-5-5" }), { messages: convo(1) });
  assert.equal(calls[0].body.model, "claude-opus-5-5");
});
test("upstream failure returns 502 and logs nothing", async () => {
  mockFetch("x", 500);
  const e = env();
  const { status } = await ask(e, { messages: convo(1) });
  assert.equal(status, 502);
  assert.equal(e.DB.rows("assistant_log").length, 0);
});

// ── logging ────────────────────────────────────────────────────────
test("logs timestamp, page, session, message, reply and handoff, with contact details removed", async () => {
  const e = env();
  await ask(e, { messages: convo(1, "Call me at 619-555-0100 or me@example.com"), page: "/training-rates-san-diego", sessionId: "abcd-1234-efgh" });
  const [row] = e.DB.rows("assistant_log");
  assert.equal(row.page_path, "/training-rates-san-diego");
  assert.equal(row.session_id, "abcd-1234-efgh");
  assert.equal(row.handoff, "book");
  assert.equal(row.reply, "Studio Momentum on The Program is $640 per 4-week cycle.");
  assert.ok(!Number.isNaN(Date.parse(row.ts)));
  assert.equal(row.user_message, "Call me at [phone removed] or [email removed]");
  assert.ok(!JSON.stringify(calls[0].body).includes("me@example.com"), "contact details never reach the API");
});
test("cleanup deletes log rows older than 90 days", async () => {
  const db = new FakeD1();
  const now = new Date("2026-10-19T12:00:00Z");
  for (const ts of ["2026-07-01T00:00:00Z", "2026-10-01T00:00:00Z"]) {
    db.db.prepare("INSERT INTO assistant_log (ts, page_path, session_id, user_message, reply, handoff) VALUES (?, '/', 's', 'q', 'a', '')").run(ts);
  }
  await cleanup(db, now);
  assert.deepEqual(db.rows("assistant_log").map((r) => r.ts), ["2026-10-01T00:00:00Z"]);
});
test("redactContact leaves ordinary text and prices alone", () => {
  assert.equal(redactContact("Is $1,250 per 4-week cycle right for 2 sessions?"), "Is $1,250 per 4-week cycle right for 2 sessions?");
});

// ── admin CSV ──────────────────────────────────────────────────────
test("assistant-log returns the last 30 days as CSV for the right key only", async () => {
  const db = new FakeD1();
  const recent = new Date(Date.now() - 2 * 86400000).toISOString();
  const old = new Date(Date.now() - 40 * 86400000).toISOString();
  const ins = db.db.prepare("INSERT INTO assistant_log (ts, page_path, session_id, user_message, reply, handoff) VALUES (?, ?, ?, ?, ?, ?)");
  ins.run(recent, "/", "s1", '=HYPERLINK("x")', 'He said "hi"', "book");
  ins.run(old, "/", "s2", "old question", "old answer", "");
  const e = { DB: db, ADMIN_KEY: "secret-key" };
  const wrong = await logGet({ request: new Request("https://www.omnifittraining.com/api/assistant-log?key=nope"), env: e });
  assert.equal(wrong.status, 403);
  const none = await logGet({ request: new Request("https://www.omnifittraining.com/api/assistant-log"), env: e });
  assert.equal(none.status, 403);
  const res = await logGet({ request: new Request("https://www.omnifittraining.com/api/assistant-log?key=secret-key"), env: e });
  assert.equal(res.status, 200);
  assert.match(res.headers.get("content-type"), /^text\/csv/);
  const csv = await res.text();
  const lines = csv.trim().split("\r\n");
  assert.equal(lines[0], "ts,page_path,session_id,user_message,reply,handoff");
  assert.equal(lines.length, 2, "the 40-day-old row is excluded");
  assert.ok(lines[1].includes(`"'=HYPERLINK(""x"")"`), "formula neutralised and quotes doubled");
  assert.equal(csvCell('a"b'), '"a""b"');
});
