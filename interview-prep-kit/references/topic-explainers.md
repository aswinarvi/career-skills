# JD Topic Extraction & Explainers

The technical section of the document is organized **by the JD's own highlighted topics**, each
with an explainer followed by questions generated *from that explainer*. This is what makes the
prep feel custom instead of a generic question bank.

## Extracting topics

Scan the JD's requirements, responsibilities, and "nice to have" lines for concrete technical
nouns — languages, frameworks, patterns, tools, domains ("Flutter", "BLoC", "platform channels",
"CI/CD", "PCI-DSS", "GraphQL", "offline sync"). Then rank:

- **P0** — explicitly required ("must have", "strong experience in", appears in the title, or in
  the first three requirement bullets).
- **P1** — mentioned once, or "nice to have" / "familiarity with".
- **P2** — implied by responsibilities but never named ("work with the payments team" → payment
  flows, idempotency; "ship weekly" → release engineering).

Cluster near-duplicates (Bloc + Cubit + state management → one topic). Target: 4–6 topics at
`quick`, 6–8 at `standard`, 8–10 at `max` — all P0s always in; fill with P1, then P2.
Cross-check against the resume: a P0 topic **missing from the resume** gets flagged in the
explainer ("expect extra scrutiny here — the JD requires it and your resume doesn't show it")
and one extra question.

## Explainer template (per topic)

```
### T{n}. {Topic} — Explainer  `[P0]`
{What it is — 1–2 sentences, plain language.}
**Core concepts:** {5–8 comma-separated or bulleted items an interviewer expects fluency in}
**In this role:** {1–2 sentences connecting the topic to THIS company/JD — use Step 2 research
and JD responsibilities; e.g. "Zerodha's order pad is latency-sensitive, so expect rendering
and isolate questions rather than trivia."}
**Pitfalls & gotchas:** {2–4 bullets — the mistakes that reveal shallow knowledge}
```

Length budget: `max` 250–400 words, `standard` 120–180, `quick` 1–2 lines (skip pitfalls).

## Questions from the explainer

Immediately after each explainer: 3–6 questions (per the plan's technical count ÷ topics),
ordered fundamentals → depth → trade-off, each in the standard Q&A format. At least one
question per P0 topic must be a *trade-off* question at mid+ seniority, and at least one should
tie to the candidate's resume when it plausibly can ("You used Riverpod at <employer> — defend
that choice against BLoC for this team").

Accuracy discipline: explainers must be technically correct and current-as-known; where an
ecosystem moves fast (framework versions, deprecations), avoid version-specific claims unless
recon/JD pins a version, and prefer "as of the JD" phrasing. Never bluff an unfamiliar
proprietary tool — say it's company-internal and generate questions about the *category* it
belongs to instead.
