#!/usr/bin/env python3
"""ats_check.py - lint resume.json for ATS compatibility and print a 0-100 score.

Usage:
    python3 ats_check.py resume.json [--jd job_description.txt]

Checks only what is verifiable from the data. Always also LOOK at the rendered PDF
(see SKILL.md Step 3) for true page count and any visual issue. Rubric: references/ats-rules.md
Pass threshold: 85. Exit code: 0 if score >= 85, else 1.
"""
import argparse
import json
import re
import sys

BANNED = [
    "spearheaded", "leveraged", "leveraging", "utilized", "utilize", "delve", "showcase",
    "robust", "seamless", "seamlessly", "cutting-edge", "best-in-class", "synergy", "holistic",
    "tapestry", "myriad", "plethora", "passionate about", "results-driven", "detail-oriented",
    "proven track record", "team player", "go-getter", "wear many hats",
    "significantly", "successfully", "effectively", "various", "numerous",
]
WEAK_STARTS = ["responsible for", "worked on", "helped with", "involved in", "tasked with", "duties included"]
# Recognized strong openers: regular "-ed" verbs are caught by suffix; these cover common irregulars + the verb bank.
STRONG_VERBS = set("""
built rebuilt cut drove set reset led ran grew won wrote rewrote spun drew made took brought taught sought
sent kept held met began chose rose spoke broke oversaw forecast spread split shipped
launched owned migrated added reduced improved created designed developed implemented engineered automated
integrated accelerated optimized streamlined hardened refactored stabilized resolved diagnosed profiled
instrumented measured benchmarked delivered scaled mentored coordinated spearheaded established negotiated
secured generated increased decreased saved boosted expanded architected orchestrated overhauled revamped
consolidated deployed maintained managed directed produced initiated pioneered transformed unified
standardized modernized containerized dockerized tested validated debugged fixed patched released published
presented authored drafted analyzed evaluated forecasted modeled prototyped
""".split())
# Date formats that pin down a MONTH. Year-only ("YYYY") is compatible with any of these (common for education).
MONTH_FORMATS = {"Mon YYYY", "MM/YYYY", "YYYY-MM"}
DATE_PATTERNS = {
    "Mon YYYY":   re.compile(r"^[A-Z][a-z]{2,8}\s+\d{4}$"),        # Jan 2023
    "MM/YYYY":    re.compile(r"^\d{1,2}/\d{4}$"),                   # 01/2023
    "YYYY":       re.compile(r"^\d{4}$"),                          # 2023
    "YYYY-MM":    re.compile(r"^\d{4}-\d{2}$"),                    # 2023-01
}
PRESENT = {"present", "current", "now", "ongoing", ""}


def strong_open(text):
    """True if the bullet opens with a plausible action verb. Weak openers never count,
    even though 'worked'/'helped'/'tasked' end in -ed."""
    t = text.strip().lower()
    if any(t.startswith(w) for w in WEAK_STARTS):
        return False
    first = re.split(r"[\s,]+", t, 1)[0].strip(".:;")
    if not first:
        return False
    return first in STRONG_VERBS or (first.endswith("ed") and len(first) > 3)


MONTHS = {m: i for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}


def date_key(v):
    """(year, month) sort key for a date string, or None if unparseable."""
    v = (v or "").strip()
    m = re.match(r"^([A-Za-z]{3,9})\s+(\d{4})$", v)
    if m:
        return (int(m.group(2)), MONTHS.get(m.group(1)[:3].lower(), 0))
    m = re.match(r"^(\d{1,2})/(\d{4})$", v)
    if m:
        return (int(m.group(2)), int(m.group(1)))
    m = re.match(r"^(\d{4})-(\d{2})$", v)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    m = re.match(r"^(\d{4})$", v)
    if m:
        return (int(m.group(1)), 0)
    return None


def mentions(kw, text):
    """Word-boundary containment, so short keywords ('Go', 'R') don't match inside other words."""
    return re.search(r"(?<![a-z0-9])" + re.escape(kw.lower()) + r"(?![a-z0-9])", text) is not None


def searchable_text(data):
    """Everything a JD keyword could legitimately live in: bullet text + keyword hints,
    summary, titles, companies, skills, soft skills, certifications."""
    parts = [str((data.get("basics") or {}).get("title") or ""), str(data.get("summary") or "")]
    for sec in ("experience", "projects"):
        for e in data.get(sec, []) or []:
            parts += [str(e.get(k) or "") for k in ("title", "company", "name")]
            for b in e.get("bullets", []) or []:
                if isinstance(b, str):
                    parts.append(b)
                    continue
                parts.append(str(b.get("text") or ""))
                parts += [str(k) for k in (b.get("keywords") or [])]
    for g in data.get("skills", []) or []:
        parts.append(str(g.get("category") or ""))
        parts += [str(i) for i in (g.get("items") or [])]
    parts += [str(s) for s in (data.get("soft_skills") or [])]
    for c in data.get("certifications", []) or []:
        parts += [str(c.get("name") or ""), str(c.get("issuer") or "")]
    return " \n ".join(p for p in parts if p).lower()


def date_fmt(v):
    v = (v or "").strip()
    if v.lower() in PRESENT:
        return None
    for name, pat in DATE_PATTERNS.items():
        if pat.match(v):
            return name
    return "OTHER"


def all_bullets(data):
    out = []
    for sec in ("experience", "projects"):
        for e in data.get(sec, []) or []:
            for b in e.get("bullets", []) or []:
                if isinstance(b, str):          # bare-string bullets are valid; coerce
                    b = {"text": b}
                if isinstance(b, dict) and b.get("text", "").strip():
                    out.append(b)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("resume")
    ap.add_argument("--jd", help="path to a job-description text file for keyword coverage")
    args = ap.parse_args()

    with open(args.resume, encoding="utf-8") as f:
        data = json.load(f)

    checks = []   # (label, earned, possible, list_of_fixes)
    b = data.get("basics", {})
    bullets = all_bullets(data)

    # 1. contact completeness (15)
    pts, fixes = 0, []
    for field, val in (("name", 5), ("email", 4), ("phone", 3), ("location", 3)):
        if str(b.get(field, "")).strip():
            pts += val
        else:
            fixes.append(f"add basics.{field}")
    checks.append(("Contact completeness", pts, 15, fixes))

    # 2. standard sections (15)
    pts, fixes = 0, []
    has_core = bool(data.get("experience")) or bool(data.get("projects"))
    has_support = bool(data.get("education")) or bool(data.get("skills"))
    if has_core:
        pts += 9
    else:
        fixes.append("add at least one Experience or Projects entry")
    if has_support:
        pts += 6
    else:
        fixes.append("add a Skills or Education section")
    checks.append(("Standard sections", pts, 15, fixes))

    # 3. dates: presence (8) + one format (4) + reverse-chronological (3)
    pts, fixes = 0, []
    exp = data.get("experience", []) or []
    entries = exp + (data.get("education", []) or [])
    if not entries:
        pts = 8  # nothing to check; the sections check already penalizes the gap
    else:
        # presence: every experience role needs a start date (education dates are optional)
        if exp:
            with_start = sum(1 for e in exp if str(e.get("start") or "").strip())
            pts += round(8 * with_start / len(exp))
            if with_start < len(exp):
                fixes.append(f"{len(exp) - with_start} experience role(s) missing a start date - parsers need dates")
        else:
            pts += 8
        # consistency: one month-level format, no unrecognized formats
        month_fmts, other = set(), 0
        for e in entries:
            for key in ("start", "end"):
                fmt = date_fmt(e.get(key))
                if fmt == "OTHER":
                    other += 1
                elif fmt in MONTH_FORMATS:
                    month_fmts.add(fmt)
                # None (empty/Present) and bare "YYYY" are compatible with anything
        if other == 0 and len(month_fmts) <= 1:
            pts += 4
        elif len(month_fmts) <= 1:
            pts += 2
            fixes.append("normalize the odd date(s) to match the rest")
        else:
            fixes.append(f"unify month-level date formats (found: {', '.join(sorted(month_fmts))})")
        # order: experience start dates must not increase down the page
        keys = [k for k in (date_key(e.get("start")) for e in exp) if k]
        if all(a >= b for a, b in zip(keys, keys[1:])):
            pts += 3
        else:
            fixes.append("order Experience most-recent-first (reverse-chronological)")
    checks.append(("Dates (presence/format/order)", pts, 15, fixes))

    # 4. quantification (15)
    pts, fixes = 0, []
    if bullets:
        quant = sum(1 for x in bullets if x.get("metrics") or re.search(r"\d", x.get("text", "")))
        frac = quant / len(bullets)
        pts = round(frac * 15)
        if frac < 0.5:
            fixes.append(f"only {quant}/{len(bullets)} bullets have a number - add real metrics (%, $, time, scale) where you have them")
    else:
        fixes.append("no bullets to quantify")
    checks.append(("Quantification", pts, 15, fixes))

    # 5. action verbs (10)
    pts, fixes = 0, []
    if bullets:
        weak = [x for x in bullets if any(x.get("text", "").lower().lstrip().startswith(w) for w in WEAK_STARTS)]
        strong = sum(1 for x in bullets if strong_open(x.get("text", "")))
        frac = strong / len(bullets)
        pts = round(frac * 10)
        if weak:
            fixes.append(f"{len(weak)} bullet(s) start weakly (e.g. 'Responsible for') - lead with a strong past-tense verb")
        elif frac < 1:
            fixes.append(f"{len(bullets) - strong} bullet(s) don't open with an action verb - start with the verb, not a noun")
    else:
        fixes.append("no bullets found")
    checks.append(("Action verbs", pts, 10, fixes))

    # 6. length sanity (10)
    pts, fixes = 0, []
    target = (data.get("meta", {}).get("length_target") or "1-page").lower()
    n = len(bullets)
    cap = 22 if "1" in target else 40
    if n <= cap:
        pts = 10
    elif n <= cap * 1.3:
        pts = 6
        fixes.append(f"~{n} bullets is a lot for a {target} resume - trim the oldest/weakest")
    else:
        pts = 2
        fixes.append(f"~{n} bullets will overflow a {target} resume - cut aggressively")
    fixes.append("confirm true page count on the rendered PDF")
    checks.append(("Length sanity", pts, 10, fixes))

    # 7. AI-fingerprint / banned words (10)
    pts, fixes = 10, []
    blob = " ".join(x.get("text", "") for x in bullets).lower() + " " + (data.get("summary") or "").lower()
    hits = sorted({w for w in BANNED if w in blob})
    if hits:
        pts = max(0, 10 - 2 * len(hits))
        fixes.append("remove/replace AI-cliché or filler words: " + ", ".join(hits[:8]))
    checks.append(("AI-fingerprint / banned words", pts, 10, fixes))

    # 8. JD keyword coverage (10, only if --jd) - scans the WHOLE resume (skills, keyword
    # hints, titles, certs), word-boundary matched
    jd_used = False
    if args.jd:
        jd_used = True
        with open(args.jd, encoding="utf-8") as f:
            jd = f.read().lower()
        hay = searchable_text(data)
        kws = data.get("target", {}).get("jd_keywords") or []
        pts, fixes = 0, []
        if not kws:
            # fallback: derive a rough keyword set from the JD (stopword-filtered tokens)
            kws = sorted({w for w in re.findall(r"[A-Za-z][A-Za-z0-9+.#/-]{2,}", jd)
                          if w not in _STOP})[:20]
            fixes.append("populate target.jd_keywords for a sharper match")
        covered = sum(1 for k in kws if mentions(k, hay))
        frac = covered / len(kws) if kws else 0
        pts = round(frac * 10)
        missing = [k for k in kws if not mentions(k, hay)][:10]
        if missing:
            fixes.append("JD terms not reflected (add only if true to your experience): " + ", ".join(missing))
        checks.append(("JD keyword coverage", pts, 10, fixes))

    # ---- score ----
    earned = sum(c[1] for c in checks)
    possible = sum(c[2] for c in checks)
    if not jd_used:
        # redistribute the missing 10 so the scale still tops at 100
        earned = earned / possible * 100 if possible else 0
        possible = 100
    score = round(earned)

    verdict = "PASS" if score >= 85 else ("CLOSE" if score >= 70 else "NEEDS WORK")
    print(f"ATS score: {score}/100  [{verdict}]  (threshold 85)\n")
    for label, e, p, fx in checks:
        mark = "OK " if e == p else ("~  " if e >= p * 0.6 else "X  ")
        print(f"  {mark}{label}: {e}/{p}")
        for fix in fx:
            print(f"        - {fix}")
    if score < 85:
        print("\nApply the fixes above, rebuild, and re-run. Never fabricate to raise the score.")
    sys.exit(0 if score >= 85 else 1)


_STOP = set("""a an the and or of to in for with on at by from as is are be will you your we our they their this that
role position company team work experience skills years ability strong excellent good must have should would about
including etc using use used help support looking seeking join responsibilities requirements qualifications preferred
plus new all any who what which will can may""".split())


if __name__ == "__main__":
    main()
