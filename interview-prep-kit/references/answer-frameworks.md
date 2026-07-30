# Answer Frameworks — When and How

Tag every suggested answer with exactly one framework. The document's primer section (§1)
teaches the reader these same rules in ~half a page.

## [STAR] — Situation, Task, Action, Result
Default for behavioral questions. Budget inside a 150–250-word answer:
- **S** 2–3 sentences max — just enough context to make the stakes clear.
- **T** 1 sentence — the candidate's specific responsibility, not the team's.
- **A** ~half the answer — first person singular, concrete decisions, name the technologies.
- **R** 2–3 sentences — quantified where the resume gives numbers; add one line of "what I'd do
  differently" for senior roles.
Never use STAR for "tell me about yourself" or "why us".

## [CAR] / [PAR] — Challenge/Problem, Action, Result
Condensed STAR without the S/T split. Use for screening rounds, rapid-fire panels, and any
question where the full STAR would drag. 60–120 words.

## [SOAR] — Situation, Obstacle, Action, Result
Use when the *obstacle* is the interesting part (production incident, hard deadline, blocked
dependency, disagreement with a senior). The O gets its own vivid sentence; otherwise same
budgets as STAR. Down-converts to STAR trivially if the candidate prefers.

## [PPF] — Present, Past, Future
Only for "tell me about yourself" and "walk me through your resume". Present role and scope →
the 2–3 past beats most relevant to *this* JD → why this opportunity is the logical next step.
Target ≤90 seconds spoken (~130 words). End pointing at the company, not at the candidate.

## [SBI] — Situation, Behavior, Impact
For feedback/leadership questions ("tell me about a time you gave hard feedback", "how do you
handle underperformance"). Emphasizes observed behavior over judgment.

## Technical answers (no story framework)
Structure: direct answer → why / how it works → trade-offs or when-not-to → 1–2 follow-up
probes. Match depth to seniority (see `seniority-tuning.md`): juniors define and apply; seniors
compare alternatives and justify choices they made in real projects (pull those from the resume
when possible — a technical answer that cites the candidate's own project is twice as strong).

## System design answers
Fixed skeleton: 1) clarify requirements + constraints (list the questions to ask), 2) high-level
architecture (components + data flow, described in prose the candidate can sketch), 3) deep dive
one component, 4) trade-offs + scaling/failure modes. Keep each answer ≤350 words; it's a
rehearsal script, not a textbook.

## Personalization discipline
- Pull Situation/Action material only from the resume (or `resume.json` if Step 6 ran).
- Every claim a candidate might be pressed on gets `(verify)` if the skill inferred it.
- If two questions would naturally use the same story, the second answer must open with
  "Reuse story from B{n}, shifting emphasis to …" instead of duplicating text — this keeps the
  doc shorter and trains the candidate to flex stories.
- No resume → placeholders in square brackets (`[the payments app you shipped]`), and the doc's
  primer must tell the reader to fill them in before rehearsing.
