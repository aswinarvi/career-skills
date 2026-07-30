# chat-to-resume-builder

A [Claude Code skill](https://docs.claude.com/en/docs/claude-code/skills) that creates, tailors, and iteratively edits resumes/CVs through conversation, producing a polished single-column, ATS-friendly `.docx`.

## What it does

- Turns raw material — pasted notes, an old resume, a LinkedIn export, uploaded `.docx`/`.pdf` files — into a clean, parseable resume.
- Tailors a resume to a specific job description (reorders and re-emphasizes real experience toward the JD's keywords — never invents anything).
- Works like a chat-based resume editor: "punch up bullet 2", "drop the objective", "shorten to one page" become targeted edits followed by a deterministic rebuild.
- Lints the result with a 0–100 ATS score and specific fixes, and can emit a plain-text ATS-safe version for web forms.
- Two ATS-safe looks via `meta.theme`: **navy** (default — navy caps headings, company-first role lines, justified body) and **classic** (plain monochrome). Page size via `meta.page`: **a4** (default) or **letter**.

**Anti-fabrication is absolute**: the skill never invents employers, titles, dates, metrics, degrees, or skills.

## How it works

The single source of truth is a `resume.json` file (schema in [`references/resume-schema.md`](references/resume-schema.md)). The `.docx` is generated *from* it deterministically, so conversational edits are small JSON changes plus a rebuild — never a from-scratch regeneration that silently changes unrelated sections.

```
input (text / files) → resume.json → build_docx.js → resume.docx
                                   → ats_check.py  → ATS score + fixes
                                   → to_plaintext.py → resume.txt
```

## Installation

Copy this folder into your Claude Code skills directory:

```bash
# personal (all projects)
git clone https://github.com/<your-username>/chat-to-resume-builder.git \
  ~/.claude/skills/chat-to-resume-builder

# or project-scoped
git clone https://github.com/<your-username>/chat-to-resume-builder.git \
  .claude/skills/chat-to-resume-builder
```

It works out of the box — the `docx` dependency ships pre-bundled in `scripts/vendor/docx.js`
(`npm install` in `scripts/` is only needed if you want to regenerate that bundle). Optionally verify:

```bash
bash ~/.claude/skills/chat-to-resume-builder/scripts/smoke_test.sh
```

Then just ask Claude Code to build or edit a resume — the skill triggers automatically (e.g. "help me apply for this job", "tailor my resume to this JD").

## Requirements

- **Node.js** (for `scripts/build_docx.js`; the [`docx`](https://www.npmjs.com/package/docx) package is pre-bundled in `scripts/vendor/docx.js` — regenerate via `npm install` + `npx esbuild`, see the header of `build_docx.js`)
- **Python 3** (for `scripts/ats_check.py` and `scripts/to_plaintext.py`)
- Optional: **LibreOffice** (`soffice`) for the .docx→PDF visual check and PDF delivery — on macOS, Pages (AppleScript) or QuickLook (`qlmanage`) work as fallbacks; **pandoc** for reading uploaded `.docx` files — on macOS, `textutil` works instead. PDFs are read natively by Claude Code's Read tool; no `pdftotext`/`pdftoppm` needed.

## Repo layout

| Path | Purpose |
|---|---|
| `SKILL.md` | The skill definition Claude Code loads |
| `references/resume-schema.md` | `resume.json` schema and field definitions |
| `references/writing-rules.md` | Bullet/summary writing rules, anti-fabrication, AI-tic scan |
| `references/ats-rules.md` | ATS scoring rubric |
| `references/intake-questions.md` | Consolidated intake-question template |
| `scripts/build_docx.js` | Deterministic `resume.json` → `.docx` builder |
| `scripts/vendor/docx.js` | Self-contained esbuild bundle of the `docx` npm package (generated) |
| `scripts/ats_check.py` | ATS linter (0–100 score, `--jd jd.txt` for tailoring) |
| `scripts/to_plaintext.py` | Plain-text ATS-safe export |
| `scripts/smoke_test.sh` | End-to-end check of all three scripts (`bash scripts/smoke_test.sh`) |
| `assets/resume.example.json` | Example `resume.json` |

## License

MIT
