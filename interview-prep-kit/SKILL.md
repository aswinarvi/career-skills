---
name: interview-prep-kit
description: >-
  Generate a comprehensive, company- and resume-personalized interview preparation document —
  maximum interview questions WITH fully written suggested answers — from a job description,
  company name, and (optionally) the candidate's resume, delivered as .md, .docx, or .pdf.
  Use this whenever the user wants to prepare for a job interview, asks for interview questions
  for a role or company, wants likely or past interview questions, mock-interview material, STAR
  answer prep, says "help me prep for my {company} interview", or shares a JD and asks what they
  will be asked — even if they never say the words "interview prep". Also triggers when referenced
  by name. The skill researches the company and reported past interview questions online, explains
  the technical topics highlighted in the JD and generates questions from them, and can delegate
  resume tailoring to the chat-to-resume-builder skill.
---

# Interview Prep Kit

Mission: walk into the interview having already seen every question. This skill turns a JD +
company + resume into one polished prep document: the maximum realistic set of questions the
candidate will face, each with a fully written suggested answer personalized to *their* real
experience — and **never invents experience they don't have**.

Scripts live in **this skill's own directory** (the one containing this SKILL.md) — call them by
absolute path; `$SKILL` below means that directory. Data files (`master.md`, `jd.txt`, outputs)
live in the working directory, inside an output folder `<Company>-interview-prep/`.

## Step 0 — Intake (ask ONCE, only for what's missing)

Scan the user's message and any attached files first. If `/mnt/user-data/uploads/` exists
(claude.ai containers), check it. **Never re-ask something the input already answers.** If
anything is missing, stop and ask **one consolidated bulleted batch** covering every gap — never
drip-feed questions:

- **Job description** — paste, URL, or file. (`skip` → generic prep for the role title alone)
- **Company + role title** — e.g. "Zerodha — Senior Flutter Engineer".
- **Resume** — attach, path, or paste. Needed to personalize answers. (`skip` → answers become
  clearly labeled templates with `[your project]`-style placeholders)
- **Also tailor the resume to this JD?** — yes/no. If yes, the resume is required.
- **Output format** — `md` / `docx` / `pdf` (default `md`).
- **Depth** — show this table and default to `standard`:

| Mode | Q&A pairs | Topic explainers | Typical docx/pdf size |
|---|---|---|---|
| `quick` | ~30–35 | 1–2 lines each | ~15–25 pages |
| `standard` | ~65–75 | ~150 words each | ~35–50 pages |
| `max` | ~110–130 | 250–400 words each | ~60–90 pages |

File handling: `.pdf` → Read directly (the Read tool renders PDF pages). `.docx` →
`pandoc -t markdown`; fallback `unzip -p <file> word/document.xml`. `.txt`/`.md` → Read directly.
A JD given as a URL → fetch it. Save the JD text to `jd.txt` in the working directory.

Confirm with a one-line plan ("Standard-depth prep for Senior Flutter Engineer @ Zerodha, docx,
with resume tailoring — proceeding"), then run the whole pipeline without further questions.

## Step 1 — Parse the JD

Read **`references/topic-explainers.md`** and **`references/seniority-tuning.md`**, then extract:

1. **Highlighted technical topics** — the concrete skills/technologies the JD names, ranked
   P0 (explicitly required) / P1 (mentioned) / P2 (implied by responsibilities).
2. **Seniority level** — from title, years required, and scope language.
3. **Competencies** — 5–6 behavioral competencies the responsibilities imply (ownership,
   collaboration, ambiguity, leadership, learning, delivery under pressure).

If the JD was skipped, infer topics and competencies from the role title and say so in the doc.

## Step 2 — Company research (WebSearch)

Read **`references/company-research.md`** (Part A) and research: mission/values, products,
engineering blog, recent news, team scale, tech stack signals. Only cite URLs actually fetched.

## Step 3 — Past-questions recon (WebSearch)

Read **`references/company-research.md`** (Part B). Search Glassdoor, AmbitionBox, LeetCode
Discuss, Reddit, Blind, GeeksforGeeks interview experiences, and Indeed for questions candidates
*actually reported* for this company and role. Collect with attribution
(`(reported — Glassdoor, 2025)`), deduplicate, note round and frequency. These findings also
**re-weight the question plan** — if reports show a DSA-heavy loop, raise the DSA count; if
system-design-heavy, raise that.

## Step 4 — Build the question plan

Read **`references/question-taxonomy.md`**. Produce a per-category target count from: the depth
mode baseline × seniority weighting (Step 1) × recon re-weighting (Step 3). Write the plan as a
short table at the top of your working notes before generating anything.

## Step 5 — Write the master document incrementally

Read **`references/document-structure.md`** (exact section template) and
**`references/answer-frameworks.md`** (STAR / CAR / PAR / SOAR / Present–Past–Future rules).

Write `master.md` **section by section, appending one section per pass** — never attempt the
whole document in one generation. Recommended pass order: cover + primer → company snapshot →
reported past questions → screening → behavioral (split into 2 passes at `max` depth) →
situational → technical-by-topic (one pass per 2–3 topics) → system design → DSA plan → resume
deep-dive → culture fit → reverse questions → story bank → checklist. After each pass, re-read
the last ~20 lines written to keep numbering and tone continuous.

Answer rules (non-negotiable):

- Every suggested answer for behavioral/resume/culture questions must be built from **real resume
  artifacts** — named projects, technologies, metrics the resume actually contains. Mark anything
  the user should confirm with `(verify)`. If no resume was given, write template answers with
  explicit placeholders — never fake specifics.
- Tag each answer with its framework: `[STAR]`, `[CAR]`, `[SOAR]`, `[PPF]`.
- Technical answers: correct, concise, at the seniority level detected — include the "why",
  trade-offs, and 1–2 follow-up probes an interviewer would drill into.
- Never invent LeetCode problem numbers, URLs, salary figures, or company facts. Label
  `(inferred)` where reasoning fills a gap and `(reported — source, year)` where recon found it.

## Step 6 — Optional resume tailoring (delegate)

If the user opted in: invoke the `chat-to-resume-builder` skill if it's among your available
skills (on the CLI, equivalently, read `~/.claude/skills/chat-to-resume-builder/SKILL.md` and
follow it). Run it in the **same working directory** (it will reuse `jd.txt`). It produces
`resume.json` + a tailored
ATS-linted `resume.docx`. Then **use `resume.json` as the source of truth** when personalizing
answers in Step 5, so the story bank and the tailored resume never contradict each other. Copy
the tailored resume into the output folder. If that skill is not installed, say so and continue
with the original resume.

## Step 7 — Convert, verify, deliver

```bash
python3 $SKILL/scripts/build_output.py master.md --format docx \
    --out "<Company>-interview-prep/Interview-Prep-<Company>.docx" --page a4
```

`--format` is `md`, `docx`, or `pdf`; `--page` is `a4` (default) or `letter` (US/Canada). The
script is pure-Python (python-docx / reportlab) and falls back to pandoc if a library is missing.

Then **look at it** — never ship unseen:
- `pdf` → Read the PDF directly (the Read tool renders pages). Check the cover, one Q&A section,
  and the final page.
- `docx` → `soffice --headless --convert-to pdf <file>.docx`, Read that PDF, then delete it.
- `md` → Read the first and last 60 lines.

Deliver the absolute paths of everything in `<Company>-interview-prep/` (prep doc, master.md,
tailored resume if produced). Offer — don't force — a follow-up: "want a `quick`-mode 1-page
cheat sheet from the same material?"

## Interaction style

Terse and answer-first. Lead with the result. One consolidated question batch at intake, then
zero questions until delivery. No filler, no recaps of what you're about to do.
