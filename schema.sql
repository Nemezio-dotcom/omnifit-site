-- D1 schema for the "Ask OmniFit" assistant (binding name: DB).
-- Safe to run more than once.

-- One row per visitor message. No IP address and no contact details are stored
-- (emails and phone numbers are removed before a message is logged).
-- Rows older than 90 days are deleted automatically. The server also rebuilds
-- each conversation's context from these rows (by session_id), so the reply
-- column is what the model sees as its own earlier answers.
CREATE TABLE IF NOT EXISTS assistant_log (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  ts           TEXT    NOT NULL,             -- ISO 8601 UTC timestamp
  page_path    TEXT    NOT NULL DEFAULT '',  -- page the visitor was on
  session_id   TEXT    NOT NULL,             -- random id made in the browser
  user_message TEXT    NOT NULL,
  reply        TEXT    NOT NULL,
  handoff      TEXT    NOT NULL DEFAULT ''   -- 'book', 'fit_check' or ''
);
CREATE INDEX IF NOT EXISTS assistant_log_ts ON assistant_log (ts);
CREATE INDEX IF NOT EXISTS assistant_log_session ON assistant_log (session_id);

-- Rate limits, in fixed one-hour windows: 30 messages per visitor, where the
-- visitor is a SHA-256 hash of the IP address (IPv6: its /64 prefix) and the
-- day's random salt, so the raw IP is never stored; plus one site-wide row,
-- visitor = 'global', capping all visitors together (default 300 an hour,
-- ASSISTANT_GLOBAL_LIMIT_PER_HOUR). Rows older than two hours are deleted.
CREATE TABLE IF NOT EXISTS assistant_rate (
  visitor      TEXT    NOT NULL,
  window_start INTEGER NOT NULL,             -- start of the hour, Unix seconds
  count        INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (visitor, window_start)
);

-- One random salt per UTC day; old salts are deleted, so hashes from
-- different days cannot be linked.
CREATE TABLE IF NOT EXISTS assistant_salt (
  day          TEXT    PRIMARY KEY,          -- YYYY-MM-DD
  salt         TEXT    NOT NULL
);

-- Bookkeeping for the throttled cleanup: key 'last_cleanup' holds the ISO time
-- of the last run, so requests clean at most once every ten minutes.
-- (Added Oct 20 2026; re-running this file adds it to an existing database.)
CREATE TABLE IF NOT EXISTS assistant_meta (
  key          TEXT    PRIMARY KEY,
  value        TEXT    NOT NULL
);
