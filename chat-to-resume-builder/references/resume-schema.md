# resume.json schema

The working file. JSON is used (not YAML) so the build/lint scripts parse it with zero dependencies.
All fields are optional except `basics.name`; omit what you don't have rather than inventing it. Empty
arrays and empty strings are fine and are simply skipped by the builder.

`assets/resume.example.json` is a complete, valid instance — copy it as a starting scaffold.

## Top-level shape

```json
{
  "basics":         { ... },
  "target":         { ... },
  "summary":        "string",
  "experience":     [ { ... } ],
  "projects":       [ { ... } ],
  "personal_projects": [ { ... } ],
  "education":      [ { ... } ],
  "skills":         [ { ... } ],
  "soft_skills":    [ "string" ],
  "certifications": [ { ... } ],
  "meta":           { ... }
}
```

Only these keys are rendered — the builders warn on stderr about any unknown top-level key or
unknown `section_order` entry instead of silently dropping content.

## `basics` — header block

| Field | Type | Notes |
|---|---|---|
| `name` | string | **Required.** Full name as it should appear at the top. |
| `title` | string | Optional headline under the name, e.g. "Senior Mobile Engineer". Keep it factual, not a slogan. |
| `email` | string | |
| `phone` | string | |
| `location` | string | "City, Country" or "City, ST". No street address (ATS doesn't need it; privacy). |
| `links` | array | `[{ "label": "GitHub", "url": "github.com/…" }]`. Show the bare URL text, not "click here". |

## `target` — tailoring context (optional)

| Field | Type | Notes |
|---|---|---|
| `role` | string | Role being applied for. |
| `company` | string | |
| `jd_keywords` | array of strings | Keywords/skills pulled from the job description. Drives emphasis and the ATS keyword-coverage check. Populate this from the JD; never copy the JD prose into the resume. |

## `summary` — string (optional)

2–3 lines, factual, front-loaded with the strongest real signal. Omit entirely rather than writing a
generic objective ("Seeking a challenging role…") — those lower the ATS score and waste the top of page 1.

## `experience[]` — reverse-chronological roles

| Field | Type | Notes |
|---|---|---|
| `company` | string | |
| `title` | string | |
| `location` | string | Optional. |
| `start` | string | Use a **consistent** format across all entries, e.g. `"Jan 2023"`. |
| `end` | string | Same format, or `"Present"` — but only write `"Present"` when the role is actually current. An empty `end` renders as just the start date; the builders never assume "Present". |
| `bullets` | array | See below. |

Each bullet:

```json
{ "text": "Cut cold-start time 38% by lazy-loading feature modules",
  "metrics": ["38%"],
  "keywords": ["performance", "Android"] }
```

- `text` — one achievement, past tense, strong verb first. Follow the XYZ/STAR guidance in
  `writing-rules.md`. **Do not fabricate the number in `metrics`** — it must come from the user.
- `metrics` / `keywords` — optional hints used by the ATS check (quantification rate, keyword coverage).
  They are not rendered separately; the number just lives inside `text`.
- A bare string is also accepted as a bullet (coerced to `{ "text": ... }` by all scripts), but prefer
  the object form so `metrics`/`keywords` can feed the ATS check.

## `projects[]` (optional — useful for early-career, portfolio, or open-source)

```json
{ "name": "logstream", "role": "Creator", "link": "github.com/…",
  "bullets": [ { "text": "…" } ] }
```

## `personal_projects[]` (optional)

Same shape as `projects[]`, rendered as its own "Personal Projects" section. Use it to keep
personal/open-source work separate when `projects` holds employer work (navy labels that section
"Key Projects"). Default order places it right after `projects`.

## `education[]`

| Field | Type | Notes |
|---|---|---|
| `institution` | string | |
| `degree` | string | e.g. "B.E." |
| `field` | string | e.g. "Computer Science". |
| `location` | string | Optional, "City, Country". |
| `start` / `end` | string | Optional; consistent format. |
| `details` | array of strings | Optional: honors, relevant coursework, GPA if strong. |

## `skills[]` — grouped, not one flat blob

```json
[ { "category": "Languages",  "items": ["Dart", "Kotlin", "Swift"] },
  { "category": "Frameworks", "items": ["Flutter", "Jetpack Compose"] } ]
```

Grouping parses cleanly and reads fast. Only list skills the user actually has.

## `soft_skills` — array of strings (optional)

```json
["Effective Communication", "Mentorship & Coaching", "Cross-functional Collaboration"]
```

Rendered as its own short section (one `·`-separated line). Use sparingly — hard skills and
quantified bullets carry far more weight.

## `certifications[]` (optional)

```json
{ "name": "AWS Solutions Architect – Associate", "issuer": "AWS", "date": "2024" }
```

## `meta` — build + session state

| Field | Type | Notes |
|---|---|---|
| `format` | string | `"docx"` (default), `"pdf"`, or `"txt"`. `.docx` is the primary deliverable; PDF is produced with the same converter used for the visual check (SKILL.md Step 3). |
| `page` | string | `"a4"` (default) or `"letter"`. Pick by the user's region — A4 everywhere except the US/Canada. |
| `theme` | string | `"navy"` (default): navy caps headings, company-first role lines, justified body, "Core Competencies" naming — matches the George reference template. `"classic"`: the original plain monochrome look. Both single-column, ATS-safe. |
| `section_order` | array of strings | Render order. Default depends on theme — navy: `["summary","skills","experience","projects","personal_projects","education","soft_skills","certifications"]`; classic: `["summary","experience","projects","personal_projects","skills","education","certifications","soft_skills"]`. Reorder on request (e.g. skills-first for a career-changer). |
| `length_target` | string | `"1-page"` or `"2-page"`. Guides how aggressively to trim. |
| `decisions_log` | array of strings | Append every accepted edit ("removed Objective", "1-page target", "moved Skills above Experience"). Consulted on rebuild so user choices persist across iterations. |

## Editing during the conversational loop

Make the smallest edit that satisfies the request:

- "punch up bullet 2 of the current job" → rewrite that one `text`, leave the rest untouched.
- "cut the summary" → set `summary` to `""` and append `"removed summary"` to `decisions_log`.
- "tailor to this JD" → fill `target`, reorder `experience`/bullets by relevance, adjust emphasis — add nothing false.
- "one page" → set `length_target` to `"1-page"`, trim oldest/weakest bullets first, note it in `decisions_log`.

Then rebuild with `build_docx.js`. The document reflects the data; the data reflects the user's decisions.
