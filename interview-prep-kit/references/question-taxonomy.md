# Question Taxonomy — 9 Categories with Counts

Baseline counts per depth mode. Adjust with seniority weighting (`seniority-tuning.md`) and
recon re-weighting (SKILL.md Step 3) — but keep the grand total inside the mode's band:
`quick` 30–35 · `standard` 65–75 · `max` 110–130.

| # | Category | quick | standard | max | Notes |
|---|---|---|---|---|---|
| 1 | Screening / HR round | 4 | 8 | 10 | logistics, motivation, salary/notice, resume walk-through |
| 2 | Behavioral | 8 | 16 | 24 | ≥3 per competency across 5–6 competencies |
| 3 | Situational | 3 | 8 | 12 | hypotheticals drawn from JD responsibilities |
| 4 | Technical by JD topic | 8 | 18 | 25 | 3–6 per P0/P1 topic, from the topic explainers |
| 5 | System design | 2 | 6 | 10 | mid-level and above only; mobile-flavored for app roles |
| 6 | Coding / DSA plan | 3 | 6 | 12 | curated topic-priority list, not prose Q&A (see below) |
| 7 | Resume deep-dive | 3 | 8 | 12 | project probes, tech-choice justifications, gaps, transitions |
| 8 | Company / culture fit | 3 | 6 | 10 | built from Step 2 research; map to candidate stories |
| 9 | Reverse questions | 6 | 12 | 18 | grouped by round; not counted as Q&A pairs — no answers needed |

Category 9 and the DSA list don't get written answers, so the *answered* Q&A pairs land at
roughly: quick ~31, standard ~70, max ~113 — inside band.

## What each category must contain

**1. Screening / HR.** "Walk me through your resume", why-this-company, why-leaving, notice
period, salary expectation (give a *strategy*, not a number, unless recon found ranges — then
cite), work authorization/location if the JD implies it. Short answers, [CAR] or [PPF].

**2. Behavioral.** Map every question to a competency from Step 1. Premise: past behavior
predicts future behavior. Each answer is a named, real story from the resume ([STAR] default,
[SOAR] when the obstacle is the point). No two answers may reuse the same story unless the doc
says "reuse story #N with a different emphasis".

**3. Situational.** "How would you handle…" scenarios lifted from the JD's actual
responsibilities (a migration, a production incident, a conflicting-stakeholder feature).
Answer = a decision framework plus one concrete illustration.

**4. Technical by JD topic.** Generated from the topic explainers (`topic-explainers.md`).
Order questions within a topic from fundamentals → depth → trade-offs. Each answer ends with
*Follow-ups:* 1–2 probes an interviewer would push on.

**5. System design.** Scale to the platform: for mobile roles use offline-first sync, caching,
push/notification fan-out, modularization, feed/chat design; for backend use the classic
load-balancer → service → data-layer ladder. Answer = requirements-clarification checklist,
high-level design, deep dive on one component, trade-offs.

**6. Coding / DSA plan.** Not prose Q&A. Emit a topic-priority matrix (P0/P1/P2 topics for this
company per recon) and named, well-known problems per topic (e.g. "Two Sum", "LRU Cache") —
**never invent problem numbers or URLs**. Include per-topic "what the interviewer checks".
Skip or shrink this category if recon shows the company doesn't run DSA rounds.

**7. Resume deep-dive.** Read the resume like a hostile interviewer: every project gets a "tell
me more", every technology a "why that one", every gap or short stint a direct question. Answers
rehearse honest, confident framings — never spin that contradicts the resume.

**8. Company / culture fit.** Connect the company's stated values/products/news (Step 2) to the
candidate's real stories. Include at least one "what do you know about us" and one
"why us over competitors" with specifics from research.

**9. Reverse questions.** Grouped by round: recruiter (4–5), hiring manager (4–6), peer/tech
(4–5), senior/leadership (3–4). Favor insight-revealing questions ("what would I need to
accomplish in the first 90 days to be a clear success?") over anything Googleable.

## Per-question format (all answered categories)

```
**Q{n}. {question}** `[STAR]` `(reported — Glassdoor, 2025)`   ← tags only when applicable
*Why they ask:* {one line — max mode only}
**Suggested answer:** {150–250 words standard/max; 60–100 quick}
*Follow-ups:* {1–2 bullets}
```

Number questions continuously within a category, restarting per category (S1…, B1…, T1…).
