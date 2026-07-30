---
name: chat-to-resume-builder
description: >-
  Create, tailor, and iteratively edit resumes/CVs through conversation, producing a polished
  single-column ATS-friendly .docx. Use this whenever the user wants to build a resume or CV, rewrite
  or update an existing one, tailor a resume to a specific job description, or turn raw material
  (pasted notes, an old resume, a LinkedIn export) into a real resume — even if they don't say the
  word "resume" (e.g. "help me apply for this job", "make my work history look better", "punch up
  these bullets for a job app"). Also triggers when the user references this skill by name. Handles
  both pasted text and uploaded files as input, asks for missing info in one consolidated batch (never
  drip-feed questions), then works like a chat-based resume editor. Self-contained: ships its own
  deterministic docx builder, ATS linter, and plain-text exporter.
---

# Chat to Resume Builder

Mission: a person's chances should rest on their real experience, not their formatting skills. This
skill turns whatever the user has into a clean, parseable resume — and **never invents experience they
don't have**.

## Core model: data first, document second

The single source of truth is a JSON file, **`resume.json`**, in the working directory. The `.docx` is
generated *from* it, deterministically. This is what makes conversational editing clean: a user
reaction like "cut the summary" or "punch up bullet 2" becomes a small edit to `resume.json` followed
by a rebuild — never a from-scratch regeneration that silently changes unrelated sections.

Schema and field definitions: **`references/resume-schema.md`**. Read it before first populating the file.

Scripts live in **this skill's own directory** (the one containing this SKILL.md) — call them by
absolute path; `$SKILL` below means that directory. Data files (`resume.json`, `jd.txt`, output)
live in the working directory.

## Step 0 — Collect input (two entry modes)

Accept both, and combine if both are present:

- **Pasted text** in the prompt (work history, notes, an old resume, a job description).
- **Files** the user points at (a path or @-mention). If `/mnt/user-data/uploads/` exists
  (claude.ai containers), check it too. By type:
  - `.pdf` → **Read the file directly** — the Read tool renders PDF pages natively. LinkedIn
    "Save to PDF" exports are just PDFs.
  - `.docx` → `pandoc -t markdown` if installed; on macOS without pandoc,
    `textutil -convert txt <file>.docx -stdout`; last resort `unzip -p <file> word/document.xml`.
  - `.txt` / `.md` → Read directly.

A job description supplied as input is a **tailoring target**, not resume content. Save its text to
**`jd.txt`** (the ATS check takes `--jd jd.txt`) and record its keywords under `target.jd_keywords` —
never paste JD prose into the resume.

## Step 1 — Sufficiency check (decide: build now, or ask once)

**Build immediately, skip questions**, when the input already contains enough to populate a real
Experience section: at least one role with a title, an employer, and some indication of what the person
did there. An uploaded existing resume or a reasonably complete LinkedIn export always clears this bar.

**Otherwise, stop and ask ONE consolidated question block** — a single message, bulleted, covering every
gap at once. Do not ask questions one at a time. Use the template and the sufficiency rubric in
**`references/intake-questions.md`**. At minimum the batch must cover: target role/industry (and any JD to
tailor to), work history (roles/companies/dates/achievements), education, skills to highlight, format and
paper size (.docx / PDF / plain text; A4 / US Letter), and whether an existing resume or template should
be the base.

Ask only for what's genuinely missing — never re-ask something the input already answered.

## Step 2 — Populate `resume.json`

Map the gathered material into the schema. While writing bullets and summary, apply
**`references/writing-rules.md`**:

- **Anti-fabrication is absolute.** Never invent employers, titles, dates, metrics, degrees, or skills. If a
  bullet would be stronger with a number the user didn't give, either ask for it or leave it out — do not
  make one up. Respect **verb discipline**: don't upgrade "contributed to" into "led/owned/built" unless
  it's true. The builders never assume anything either: an empty `end` date renders as just the start —
  write `"Present"` only when the user says the role is current.
- **Avoid the AI fingerprint.** Run the banned-word / tic scan in the writing rules so the output reads as
  human-written, not model-generated.
- **If a JD is present**, tailor: reorder and re-emphasize real experience toward the JD's keywords, note
  honest gaps, but add nothing fictional.

## Step 3 — Generate and verify the `.docx`

```bash
node $SKILL/scripts/build_docx.js resume.json resume.docx
```

Two data-driven knobs (see the schema):

- **`meta.theme`** — `"navy"` (default): navy caps headings, company-first role lines, justified body,
  "Core Competencies" naming; matches the George reference template. `"classic"`: plain monochrome.
  Both are single-column and ATS-safe.
- **`meta.page`** — `"a4"` (default) or `"letter"`. Pick by the user's region (A4 everywhere except
  the US/Canada); ask at intake if unclear.

Then **look at it** — never ship a `.docx` unseen. In order of preference:

1. `soffice --headless --convert-to pdf resume.docx`, then **Read `resume.pdf` directly** (the Read
   tool renders PDF pages — no rasterizing needed).
2. macOS without LibreOffice: export via Pages —
   `osascript -e 'tell app "Pages" to open POSIX file "<abs>/resume.docx"' ...export...as PDF`.
   If it errors "Not authorised to send Apple events", the user must grant automation permission
   (System Settings → Privacy & Security → Automation) — or suggest `brew install --cask libreoffice`.
3. Last resort: `qlmanage -t -s 1400 -o . resume.docx`, then Read the generated `.png`. First page
   only, and QuickLook substitutes fonts and mis-renders right tab stops — use it to check layout and
   content order, not typography or date alignment.

If none of these worked, say so explicitly when delivering — don't imply the render was checked.
Delete intermediate preview files (the preview PDF, `.png` thumbnails) once checked, unless the PDF
*is* the deliverable.

And lint it for ATS:

```bash
python3 $SKILL/scripts/ats_check.py resume.json            # add --jd jd.txt if tailoring
```

This prints a 0–100 score with a checklist and specific fixes (rubric: **`references/ats-rules.md`**),
and exits non-zero below the pass threshold of 85 — expected while iterating. If the render exceeds
`meta.length_target` (1 page under ~10 years' experience, 2 pages maximum), tighten content.

## Step 4 — Conversational editing loop

After the first draft, act as a chat-based resume editor:

- Take the user's reaction ("make this punchier", "drop the objective", "move skills up", "tailor to this
  JD", "shorten to one page") and make a **targeted edit to `resume.json`**, then rebuild via Step 3.
- Change only what was asked. Don't rewrite untouched sections.
- Record each accepted change in `meta.decisions_log` (e.g. "removed Objective section", "1-page target")
  so later rebuilds don't silently reintroduce something the user already cut.
- Re-run `ats_check.py` after edits that could affect parseability.

## Step 5 — Deliver

- Tell the user the absolute path of the finished file. If `meta.format` is `"pdf"`, produce
  `resume.pdf` with the same converter used for the preview and deliver that instead of (or alongside)
  the `.docx`.
- Offer, don't force, a plain-text ATS-safe version:

  ```bash
  python3 $SKILL/scripts/to_plaintext.py resume.json resume.txt
  ```

  This is the copy-paste-into-a-web-form version: no bullet glyphs, no columns, plain ASCII.

## Interaction style

Terse and answer-first. Lead with the draft or the result, not preamble. When you must ask for missing
info, use a single bulleted batch. No filler, no "I'd be happy to", no recapping what you're about to do.
