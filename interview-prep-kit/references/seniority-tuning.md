# Seniority Tuning

## Detect the level

Signals, in priority order:
1. **JD title keywords** — intern/graduate/junior/associate → *junior*; no modifier or "II" →
   *mid*; senior/lead/staff/principal → *senior+*; manager/head/director/VP → *manager/exec*.
2. **Years required** — 0–2 junior, 2–5 mid, 5–9 senior, 9+ staff/lead territory.
3. **Scope language** — "own", "drive", "architect", "mentor", "across teams" pushes up a level.
4. **Resume years** — if resume and JD disagree by more than one level, prep at the JD's level
   but note the mismatch in the cover block (it *will* come up in screening).

State the detected level in the document's cover block, e.g. "Prepared at: Senior (JD asks 5+
yrs, resume shows 6)".

## Weighting multipliers (apply to taxonomy baseline counts)

| Category | Junior | Mid | Senior/Staff | Manager/Exec |
|---|---|---|---|---|
| Screening/HR | 1.0 | 1.0 | 1.0 | 1.0 |
| Behavioral | 0.7 | 1.0 | 1.2 | 1.5 |
| Situational | 0.7 | 1.0 | 1.2 | 1.5 |
| Technical by topic | 1.2 | 1.0 | 1.0 | 0.5 |
| System design | 0 (omit) | 0.7 | 1.5 | 1.0 (org/architecture strategy) |
| Coding/DSA | 1.5 | 1.0 | 0.7 | 0 (omit unless recon says otherwise) |
| Resume deep-dive | 0.7 | 1.0 | 1.2 | 1.2 |
| Culture fit | 1.0 | 1.0 | 1.0 | 1.2 |
| Reverse questions | 1.0 | 1.0 | 1.2 | 1.5 |

Round to integers, then trim or pad the largest categories to stay inside the mode's total band.

## Difficulty scaling within a category

- **Junior** — fundamentals, definitions, "have you used X", potential and learning speed.
  Behavioral questions accept academic/internship/side-project stories; say so in the primer.
- **Mid** — real project depth, "walk me through how you built/debugged X", situational
  judgment, ownership of a feature end-to-end.
- **Senior/Staff** — trade-off reasoning ("why X over Y, and when would you reverse it"),
  system design, cross-team influence, mentoring, incidents they owned, the strategic *why*
  behind architecture choices. Every technical answer should carry at least one trade-off.
- **Manager/Exec** — team building, delivery strategy, stakeholder conflict, hiring bar,
  motivation-to-join, org design. Technical questions shrink to architecture judgment.

## Role-type adaptation

The taxonomy is role-agnostic; the *topics* come from the JD (see `topic-explainers.md`). For
non-engineering roles (PM, design, data, sales), rename "Technical by topic" to the craft
equivalent (product sense / portfolio / SQL & metrics / methodology) and replace the DSA plan
with the role's standard exercise (case study, portfolio review, analytics take-home) — recon
in Step 3 usually reveals which one the company uses.
