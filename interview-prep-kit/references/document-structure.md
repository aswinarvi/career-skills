# Master Document Structure

`master.md` follows this exact skeleton. The build script maps `#`→Heading 1, `##`→Heading 2,
`###`→Heading 3, `####`→Heading 4; supports **bold**, *italic*, `code`, fenced code blocks,
`- ` bullets (2-space indent per level), `1. ` numbered lists, `- [ ]` checkboxes, pipe tables,
`> ` blockquotes, `---` rules, and `[text](url)` links. Stay inside that subset.

```
# Interview Prep — {Role} @ {Company}
{Cover block: prepared date · depth mode · detected seniority (+ mismatch note) ·
 recon-driven plan adjustments · question-count table by category}

## 1. How to Use This Doc & Answer Frameworks
{Half-page primer: reading order for the time available, framework cheat table
 (STAR/CAR/SOAR/PPF/SBI in one row each), the (verify)/(reported)/(inferred) legend,
 placeholder instructions if no resume was provided}

## 2. Company Snapshot & Interview Process
{Part A output: about, values, recent facts w/ dates, tech signals,
 process-overview table: Round | Format | Evaluates | Prep section}

## 3. Reported Past Interview Questions
{Part B output, grouped by round, every item attributed; answered inline or
 "→ answered as {ID}" pointers}

## 4. Screening / HR Round          {IDs S1…}
## 5. Behavioral                    {IDs B1…, grouped by competency as #### headers}
## 6. Situational                   {IDs SI1…}
## 7. Technical Deep-Dive by JD Topic
### T1. {Topic} — Explainer  [P0]
#### T1 Questions                   {IDs T1.1…}
### T2. {Topic} — Explainer  [P0]
...
## 8. System Design                 {IDs SD1…; omit at junior level}
## 9. Coding / DSA Plan             {priority matrix table + named problems per topic +
                                     "what the interviewer checks"; omit if recon says no DSA}
## 10. Resume Deep-Dive             {IDs R1…}
## 11. Company & Culture Fit        {IDs C1…}
## 12. Questions to Ask Them        {grouped by round: recruiter / hiring manager / peer / senior}
## 13. Story Bank                   {table: Story # | Resume artifact | One-line summary |
                                     Competencies it proves | Used in (question IDs)}
## 14. Day-Before & Day-Of Checklist
{- [ ] checkbox lists: 48h (re-read §2, §3, rehearse top-10), 24h (logistics, questions to ask
 printed), day-of (PPF warm-up, water, links/IDE ready for remote)}
```

## Incremental writing protocol

- One `##` section (or 2–3 technical topics) per generation pass; append to `master.md`.
- Before each pass, re-read the last ~20 lines of the file — continue numbering, don't repeat.
- Keep a running scratch tally of Q&A count per category; stop a category when its plan target
  is hit, and reconcile the cover-block table at the end (edit it to actuals).
- At `max` depth the full write is ~12–15 passes; that's expected. Don't compress to fit fewer.

## Length calibration (words → pages)

Rendered docx/pdf at 10.5–11pt lands ≈450–500 words/page. Section budgets that hit the mode's
page band: answered Q&A pairs at 150–250 words each (60–100 quick), explainers per
`topic-explainers.md`, §1–§3 together ≤4 pages standard / ≤6 max, checklist ≤1 page. If the
running total tracks over the band, trim answer verbosity before cutting questions.
