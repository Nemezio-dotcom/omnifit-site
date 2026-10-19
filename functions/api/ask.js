// POST /api/ask - the "Ask OmniFit" assistant.
// GET  /api/ask - status probe the widget uses to decide whether to show itself.
//
// Harmless until configured: without the ANTHROPIC_API_KEY secret and the D1
// binding DB, both methods return 503 and the widget never appears.
import { SYSTEM_PROMPT } from "../_lib/system-prompt.js";
import { KNOWLEDGE } from "../_lib/knowledge.js";
import {
  ALLOWED_HOSTS,
  BadRequest,
  MAX_USER_TURNS,
  TURN_CAP_REPLY,
  callClaude,
  cleanup,
  extractHandoff,
  isConfigured,
  json,
  logTurn,
  loggedTurns,
  originAllowed,
  overRateLimit,
  parseBody,
  visitorKey,
} from "../_lib/assistant.js";

const SYSTEM = SYSTEM_PROMPT + "\n\nKNOWLEDGE:\n\n" + KNOWLEDGE;

function later(context, promise) {
  const p = promise.catch((e) => console.error("assistant cleanup failed", e));
  if (context.waitUntil) context.waitUntil(p);
  return p;
}

export async function onRequestGet({ request, env }) {
  if (!isConfigured(env) || !ALLOWED_HOSTS.has(new URL(request.url).hostname)) {
    return json({ ok: false }, 503);
  }
  return json({ ok: true });
}

export async function onRequestPost(context) {
  const { request, env } = context;
  if (!isConfigured(env)) return json({ error: "unavailable" }, 503);
  if (!originAllowed(request)) return json({ error: "forbidden_origin" }, 403);

  let parsed;
  try {
    parsed = parseBody(await request.json());
  } catch (e) {
    return json({ error: e instanceof BadRequest ? e.code : "bad_request" }, 400);
  }
  const { messages, userTurns, page, sessionId } = parsed;
  const db = env.DB;
  const now = new Date();
  const userMessage = messages[messages.length - 1].content;

  try {
    if (await overRateLimit(db, await visitorKey(db, request, now), now)) {
      return json({ error: "rate_limited" }, 429);
    }
    const turns = Math.max(userTurns, (await loggedTurns(db, sessionId)) + 1);
    let reply, handoff;
    if (turns > MAX_USER_TURNS) {
      reply = TURN_CAP_REPLY;
      handoff = "book";
    } else {
      ({ reply, handoff } = extractHandoff(await callClaude(env, SYSTEM, messages)));
      if (!reply) throw new Error("reply was only a handoff token");
    }
    await logTurn(db, { now, page, sessionId, userMessage, reply, handoff });
    later(context, cleanup(db, now));
    return json({ reply, handoff, sessionId });
  } catch (e) {
    console.error("assistant error", e && e.message);
    return json({ error: "upstream_error" }, 502);
  }
}
