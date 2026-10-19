# The OmniFit Journal — run playbook

Every scheduled Journal run follows this file. CANON.md wins wherever the two
disagree. The owner (Nemezio) approves every post: nothing reaches `main`
until he replies "publish".

## 1. Start of run

1. Attach and clone the repo with push access (owner `Nemezio-dotcom`, repo
   `omnifit-site`), then `git fetch --depth=200 origin main` so git dates in
   the sitemap are right.
2. Read `CANON.md` (compliance screen, KEYWORD OWNERSHIP, THE JOURNAL),
   this file, and `editorial/CALENDAR.md`.
3. Pending-draft check: list remote branches named `blog-NN`. If one exists
   that is not merged into `main`, a post is still waiting for approval. Do
   NOT write another post. Send the owner one short reminder with that
   draft's preview link and stop.
4. Otherwise take the first `queued` row in the calendar. Next branch number
   = highest existing `blog-NN` (merged or not, or the calendar's #) + 1.

## 2. Writing standards

Audience: busy professionals and executives 30+ who are researching, not yet
buying. Tone: calm, precise, executive consultant. No hype, no influencer
voice, no bootcamp or challenge language.

- 1,200 to 1,800 words. Open with a `post-lede` paragraph that answers the
  reader's question in two or three sentences. Then H2 sections a skimmer
  can follow on their own.
- Pair the physical stage with the behavioral stage named in the calendar.
  That pairing is the Journal's point of view; make it visible.
- One `post-quotable` block: a self-contained 40 to 70 word paragraph an AI
  assistant could quote, naming OmniFit Performance once.
- A `post-faq` section with 3 or 4 questions in the reader's own words, each
  answered in 2 to 4 sentences. (The FAQ schema is generated from these.)
- 3 to 5 internal links to the owner pages in the calendar row, with
  descriptive anchor text in body copy. Never link with cost wording
  (CANON: no cost-anchor links until the cost page exists).
- Use the H2 for the FAQ heading and keep every H2 free of owned keywords.

Hard rules (CANON compliance screen; certify.py enforces most of them):
- No outcome guarantees and no "guarantee" outside the 30-Day Fit Guarantee.
- No pounds, inches or body fat tied to a timeframe. No projections ("you
  will lose..."). No population clinical claims.
- Not a medical provider: never diagnose, treat, cure, fix a condition or
  replace a clinician. Say "coaching", "training", "refer to a licensed
  clinician". Coaching, not therapy.
- Never "free" near consultation, assessment, screen, session or diagnostic.
  No "clinical-grade" or "medical-grade".
- Numbers about OmniFit clients only if they are on /outcomes, quoted
  exactly, with a link to /outcomes and "coach-rated" where it applies.
- No invented studies, statistics, quotes or citations. General principles
  are fine; if a specific finding matters, describe it without numbers or
  leave it out.
- No client names or client stories in posts (case studies cover those).
- Canon spellings: OmniFit Performance; Nemezio LopezPerez; 190+ reviews as
  "4.98 average across 190+ reviews"; Performance Assessment ($150 in
  person, $75 virtual). Prices only if needed, only from CANON's October
  card, and prefer linking to the rates page.
- No emoji. No prenatal or postpartum content.

## 3. Build the draft

1. `git checkout -b blog-NN origin/main`.
2. Write `pages/blog/<slug>.html` in the format documented at the top of
   `site/blog.py`. `published` and `updated` = today (Pacific time); they
   are reset on the publish day.
3. Set the calendar row status to `draft (blog-NN)`.
4. Run `python3 build.py --strict`, `python3 tools/certify.py` and
   `python3 tools/ownership.py`. All three must pass. Fix the post, never
   the checks.
5. Commit (post + calendar + rebuilt `public/`) and push the branch only.
   Preview: `https://blog-NN.omnifit-site.pages.dev/blog/<slug>` (Cloudflare
   needs a few minutes after the push; previews are noindexed).

## 4. Message the owner

One message, in this order:
- Title and a two-sentence summary.
- The preview link.
- A LinkedIn companion post (under 1,300 characters, first-person in
  Nemezio's voice, no hashtags wall, ends with the post's live URL
  `https://www.omnifittraining.com/blog/<slug>`), ready to paste after
  publishing.
- "Reply **publish** to put it live, or tell me what to change."

Changes requested: edit, re-run the three checks, push to the same branch,
send the preview link again.

## 5. On "publish"

1. Set `published` and `updated` to today (Pacific time). Calendar status:
   `published YYYY-MM-DD`.
2. Rebuild, re-run the three checks, commit.
3. Merge `blog-NN` into `main` (fast-forward if possible), push `main`,
   then delete the remote branch.
4. Tell the owner the live URL, and that it is ready for "Request indexing"
   in Search Console (the sitemap already lists it).
