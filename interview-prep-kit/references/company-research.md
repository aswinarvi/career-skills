# Company Research & Past-Questions Recon

Two web-research passes. Budget ~4–8 searches for Part A and ~5–10 for Part B (`max` mode uses
the upper end). Only cite URLs actually fetched. Every fact in the document that came from the
web carries a source; every guess carries `(inferred)`.

## Part A — Company research

Search targets, in order of value:
1. `<company> about mission values` → official site. Extract mission, values (verbatim value
   names — culture-fit answers should echo them), founding facts.
2. `<company> products` / the site's product pages → what they build, who the customers are.
3. `<company> engineering blog` → tech stack signals, engineering culture, named systems
   (these seed technical and reverse questions that impress).
4. `<company> news 2025 2026` → funding, launches, leadership changes, controversies. One
   recent-news reference inside a "why us" answer is a strong differentiator.
5. `<company> interview process <role>` → rounds, timeline, format.

Synthesize into the document's **Company Snapshot** section: 1 short paragraph (what they do),
values list, 3–5 recent facts with dates, tech-stack signals, and an **interview process
overview table** (round → format → what's evaluated → prep pointer to a section of this doc).
Mark the process table `(reported)` or `(inferred)` per row.

## Part B — Past-questions recon

Goal: questions candidates *actually reported* being asked at this company for this role (or
nearest role). Query patterns — run several, vary phrasing:

- `<company> <role> interview questions`
- `<company> interview experience` (GeeksforGeeks & personal blogs use this phrasing heavily)
- `<company> interview questions site:glassdoor.com` — and without the site filter if blocked
- `<company> <role> interview ambitionbox` (strong for India-based companies)
- `<company> leetcode discuss` (company tag threads list real coding questions)
- `<company> interview reddit` / `<company> interview blind`
- `<company> hiring process rounds`

Rules of evidence:
- **Attribute every reported question**: `(reported — Glassdoor, 2025)`,
  `(reported — GfG interview experience, 2024)`. No source → it isn't "reported", drop it or
  mark `(inferred)`.
- **Prefer recent** (≤2–3 years). Older reports: keep only if multiple sources agree; tag the
  year honestly.
- **Deduplicate** near-identical questions; note frequency instead ("asked in 3 of 5 reports").
- **Never fabricate** a Glassdoor/LeetCode listing, problem number, or URL. If recon finds
  little (small/stealth companies), say exactly that in the section intro and lean on
  role-generic patterns instead.
- Aggregators and SEO listicles ("Top 50 <company> questions") are weak evidence — use only to
  corroborate, never as sole source.

Output: the document's **Reported Past Questions** section — grouped by round, each question
with attribution, each with either a written answer (if it fits an answered category) or a
pointer to the section where an equivalent question is answered ("→ answered as T7").

Re-weighting: after recon, adjust the Step 4 plan — e.g. reports show 2 DSA rounds → DSA ×1.5
and say so in the cover block ("recon shows a DSA-heavy loop; plan adjusted"). Reports show
take-home + no live coding → shrink DSA, add a take-home strategy note.
