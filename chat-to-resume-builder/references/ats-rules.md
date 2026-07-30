# ATS rules: formatting, anti-patterns, and the 0–100 score

Guiding principle, in priority order: **ATS-parseable first, human-readable second, visually fancy never.**
The best-written resume is worthless if the tracking system shreds it before a person sees it.

## Formatting rules (the builder enforces these; keep them if hand-editing)

- **Single column.** No side-by-side layouts, no text boxes, no multi-column sections. `build_docx.js`
  produces single-column output and uses no tables for layout — in both themes (`navy` and `classic`);
  color accents and justified text do not affect parsing.
- **Standard fonts** only: Calibri, Arial, Helvetica, Georgia, Times New Roman. The builder defaults to Calibri.
- **Standard section headings**, spelled the ordinary way: Summary, Experience (or Work Experience), Projects,
  Skills, Education, Certifications. Don't get creative ("Where I've Made Dents") — parsers match on the
  standard words.
- **Real bullet lists** via the document's list feature — never a literal "•" typed into a line, never a table
  used to fake bullets.
- **Consistent dates** in one format throughout, e.g. `Jan 2023 – Present`.
- **Reverse-chronological** within Experience and Education.
- **No images, logos, icons, headshots, charts, or skill-rating bars.** ATS can't read them; some parsers choke.
- **Critical info in the body, not the header/footer.** Some parsers ignore headers/footers — keep name and
  contact in the document body (the builder does).
- **File type: `.docx`** for submission. Offer `.txt` for plain web-form paste boxes.

## Anti-patterns (why common "designer" resumes fail ATS)

| Looks like | Why it breaks | Do instead |
|---|---|---|
| Two-column layout, sidebar | Parser reads across columns and scrambles order | Single column, top-to-bottom |
| Infographic / skill bars / photo | Not machine-readable; visual noise | Plain text; list skills as words |
| Generic objective ("Seeking a challenging role…") | Wastes the top of page 1, scores nothing | Omit, or a 2–3 line factual summary |
| Mixed date formats / bullet styles / fonts | Reads as sloppy; confuses parsers | Strict consistency |
| Fancy section names | Parser can't map them to standard sections | Standard headings |
| 3+ pages | Rarely read; dilutes signal | 1 page (<10 yrs), 2 pages max |

## The 0–100 score (`scripts/ats_check.py`)

The script checks what's verifiable from `resume.json` and prints a score, a checklist, and specific fixes.
Weighting (100 total):

| Bucket | Points | What it checks |
|---|---:|---|
| Contact completeness | 15 | name + email + phone present; location present |
| Standard sections | 15 | has Experience (or Projects) and at least one of Education/Skills; recognized section names |
| Dates (presence/format/order) | 15 | every experience role has a start date (8); one month-level format throughout (4); experience is reverse-chronological (3) |
| Quantification | 15 | share of experience bullets containing a real number/metric |
| Action verbs | 10 | bullets start with a strong verb — weak openers ("Responsible for"/"Worked on"/"Helped with") never count |
| Length sanity | 10 | total bullet/section volume fits the `length_target` (rough estimate; confirm on the rendered PDF) |
| AI-fingerprint / banned words | 10 | flags overused LLM words and empty intensifiers from `writing-rules.md` |
| JD keyword coverage | 10 | (only if `--jd` given) fraction of `target.jd_keywords` found anywhere in the resume — bullet text and keyword hints, summary, titles, skills, soft skills, certifications — with word-boundary matching (so "Go"/"R" can't match inside other words) |

When `--jd` is not provided, its 10 points are redistributed proportionally so the score still tops out at 100.

**Pass threshold: 85.** The script exits 0 at or above 85, 1 below — a failing exit while iterating is
expected. Below threshold, apply the printed fixes and re-run. The score is a lint, not a guarantee —
always also *look at the rendered PDF* (Step 3 in SKILL.md) to catch anything visual the data-level check can't
see, especially true page count.

## Length guidance

- Under ~10 years of experience → target 1 page. Trim oldest and weakest bullets first.
- Senior/extensive → 2 pages maximum. Never 3.
- If the rendered PDF spills a few lines onto an extra page, tighten wording before cutting whole
  achievements — often removing filler words (`writing-rules.md`) reclaims the space.
