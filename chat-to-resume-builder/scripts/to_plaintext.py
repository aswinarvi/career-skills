#!/usr/bin/env python3
"""to_plaintext.py - render resume.json as an ATS-safe plain-text .txt.

Usage:
    python3 to_plaintext.py resume.json [resume.txt]

For pasting into web application forms and plain-text-only ATS boxes: no bullet glyphs
(uses "- "), no columns, no special characters, standard section headings.
"""
import json
import sys

IN = sys.argv[1] if len(sys.argv) > 1 else "resume.json"
OUT = sys.argv[2] if len(sys.argv) > 2 else "resume.txt"

with open(IN, encoding="utf-8") as f:
    data = json.load(f)

KNOWN_TOP = {"basics", "target", "summary", "experience", "projects", "personal_projects",
             "education", "skills", "certifications", "soft_skills", "meta"}
for k in data:
    if k not in KNOWN_TOP:
        print(f'warning: unknown top-level key "{k}" - not rendered', file=sys.stderr)
for sec in ("experience", "projects", "personal_projects"):
    for item in data.get(sec, []) or []:
        if isinstance(item.get("bullets"), list):  # bare-string bullets are valid; coerce
            item["bullets"] = [{"text": b} if isinstance(b, str) else b for b in item["bullets"]]

lines = []
def blank():
    if lines and lines[-1] != "":
        lines.append("")
def head(t):
    blank()
    lines.append(t.upper())
    lines.append("-" * len(t))
def has(v):
    if isinstance(v, list):
        return len(v) > 0
    return v is not None and str(v).strip() != ""

b = data.get("basics", {})
if has(b.get("name")):
    lines.append(b["name"])
if has(b.get("title")):
    lines.append(b["title"])
contact = [b[k] for k in ("email", "phone", "location") if has(b.get(k))]
contact += [l["url"] for l in b.get("links", []) if has(l.get("url"))]
if contact:
    lines.append(" | ".join(contact))


def daterange(e):
    # no end date -> just the start; "Present" must be stated by the user, never assumed
    s = (e.get("start") or "").strip()
    end = (e.get("end") or "").strip()
    return " - ".join([x for x in (s, end) if x])


def render_experience(items):
    if not items:
        return
    head("Experience")
    for e in items:
        title = " - ".join([x for x in (e.get("title"), e.get("company")) if has(x)])
        dr = daterange(e)
        lines.append(f"{title}  ({dr})" if dr else title)
        if has(e.get("location")):
            lines.append(e["location"])
        for bl in e.get("bullets", []):
            if has(bl.get("text")):
                lines.append(f"- {bl['text']}")
        lines.append("")


def render_projects(items, label="Projects"):
    if not items:
        return
    head(label)
    for p in items:
        name = p.get("name", "")
        role = f" - {p['role']}" if has(p.get("role")) else ""
        link = f"  {p['link']}" if has(p.get("link")) else ""
        lines.append(f"{name}{role}{link}".rstrip())
        for bl in p.get("bullets", []):
            if has(bl.get("text")):
                lines.append(f"- {bl['text']}")
        lines.append("")


def render_skills(items):
    if not items:
        return
    head("Skills")
    for g in items:
        cat = f"{g['category']}: " if has(g.get("category")) else ""
        lines.append(cat + ", ".join(g.get("items", [])))


def render_education(items):
    if not items:
        return
    head("Education")
    for ed in items:
        deg = ", ".join([x for x in (ed.get("degree"), ed.get("field")) if has(x)])
        inst = ed.get("institution", "")
        left = " - ".join([x for x in (inst, deg) if x])
        dr = daterange(ed)
        lines.append(f"{left}  ({dr})" if dr else left)
        if has(ed.get("location")):
            lines.append(ed["location"])
        for d in ed.get("details", []):
            if has(d):
                lines.append(f"- {d}")


def render_certifications(items):
    if not items:
        return
    head("Certifications")
    for c in items:
        parts = " - ".join([x for x in (c.get("name"), c.get("issuer")) if has(x)])
        date = f"  ({c['date']})" if has(c.get("date")) else ""
        lines.append(parts + date)


def render_summary(_):
    if has(data.get("summary")):
        head("Summary")
        lines.append(data["summary"])


def render_soft_skills(items):
    items = [s for s in items if has(s)]
    if not items:
        return
    head("Soft Skills")
    lines.append(", ".join(items))


R = {
    "summary": lambda: render_summary(None),
    "experience": lambda: render_experience(data.get("experience", [])),
    "projects": lambda: render_projects(data.get("projects", [])),
    "personal_projects": lambda: render_projects(data.get("personal_projects", []), "Personal Projects"),
    "skills": lambda: render_skills(data.get("skills", [])),
    "education": lambda: render_education(data.get("education", [])),
    "certifications": lambda: render_certifications(data.get("certifications", [])),
    "soft_skills": lambda: render_soft_skills(data.get("soft_skills", [])),
}

order = data.get("meta", {}).get("section_order") or \
    ["summary", "experience", "projects", "personal_projects", "skills", "education", "certifications", "soft_skills"]
for s in order:
    if s in R:
        R[s]()
    else:
        print(f'warning: unknown section "{s}" in section_order - skipped', file=sys.stderr)

text = "\n".join(lines).rstrip() + "\n"
# force plain ASCII where trivially possible
text = (text.replace("\u2013", "-").replace("\u2014", "-").replace("\u00b7", "-")
            .replace("\u2019", "'").replace("\u2022", "-").replace("\u00a0", " "))
with open(OUT, "w", encoding="utf-8") as f:
    f.write(text)
print(f"wrote {OUT} ({len(text)} chars)")
