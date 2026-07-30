# Intake: sufficiency rubric + the consolidated question batch

The goal is to ask **once**, or not at all. Drip-feeding questions one at a time is the main failure mode
to avoid.

## Sufficiency rubric — do I have enough to build?

Build immediately, without questions, if **all** of these hold:

- **Work history exists**: at least one role with a *title*, an *employer*, and some hint of *what they did*
  (a responsibility or achievement). Dates can be approximate or missing.
- The material is the user's *own* experience (pasted notes, an old resume, a LinkedIn export) — not just a
  job description with nothing about the candidate.

If a role's dates or metrics are missing but the role itself is clear, **build first, then ask the few
specifics inline** while showing the draft — don't block the whole resume on a start date.

A **job description alone** (no candidate info) is never sufficient — you have a target but nothing to tailor.

## The consolidated batch (use when insufficient)

Send as a single message. Terse, bulleted. Only include lines for gaps the input didn't already fill.
Adapt wording; keep it scannable.

> Need a few things to build this. The more you give, the less you'll have to fix after:
>
> - **Target** — what role/industry is this for? Paste the job description if you have one and I'll tailor to it.
> - **Work history** — for each role (most recent first): title, company, dates, and 2–4 things you did or
>   achieved there (numbers help — %, $, scale, time saved).
> - **Education** — degree, institution, year. (Skip if not relevant to your field.)
> - **Skills** — the ones you want front-and-center.
> - **Format & paper** — .docx (default), PDF, or plain text for pasting into web forms? A4 (default
>   outside the US/Canada) or US Letter?
> - **Existing resume or template?** — attach it and I'll build on it instead of starting cold.
> - **Contact** — name, email, phone, location, and any links (GitHub/LinkedIn/portfolio) — if not already above.

## After the batch comes back

- Fill `resume.json` from the answers (`references/resume-schema.md`).
- If the user answered some but not all lines, proceed with what you have; ask for any remaining specifics
  *inline alongside the first draft*, not as a fresh gate.
- Don't re-ask anything the batch already answered.

## Reading uploaded material before asking

Always parse uploads first (Step 0 in SKILL.md) — an uploaded resume usually answers most of the batch on its
own, so the only questions left are the target role and format. Asking for information that's sitting in an
attached file is the fastest way to annoy the user.
