#!/usr/bin/env node
/*
 * build_docx.js — render resume.json into a single-column, ATS-friendly .docx.
 *
 * Usage:  node build_docx.js [resume.json] [out.docx]
 * Deps:   `docx` — from node_modules if present, else the self-contained bundle in
 *         scripts/vendor/docx.js (regenerate: npm install, then
 *         npx esbuild <entry requiring "docx"> --bundle --minify --platform=node --format=cjs --outfile=vendor/docx.js)
 *
 * Layout rules (all themes):
 *   - real bullet lists via a numbering config (never a literal "•" in text, never layout tables)
 *   - separate Paragraphs instead of "\n"; right-aligned dates via a RIGHT tab stop
 *   - one column; no images, headers, or footers
 *
 * meta.page:  "a4" (default) or "letter".
 * meta.theme: "navy" (default) — navy caps headings, company-first role lines, justified body,
 *             "Core Competencies" naming; matches the George reference template.
 *             "classic" — the original plain monochrome layout.
 */

const fs = require("fs");
let docxLib;
try { docxLib = require("docx"); }
catch { docxLib = require("./vendor/docx.js"); }   // single-file esbuild bundle, for environments without node_modules
const {
  Document, Packer, Paragraph, TextRun,
  AlignmentType, BorderStyle, LevelFormat, TabStopType,
} = docxLib;

const IN = process.argv[2] || "resume.json";
const OUT = process.argv[3] || "resume.docx";

const data = JSON.parse(fs.readFileSync(IN, "utf8"));
const warn = (msg) => console.error(`warning: ${msg}`);

// ---- normalize + validate ---------------------------------------------------

const KNOWN_TOP = new Set(["basics", "target", "summary", "experience", "projects", "personal_projects",
  "education", "skills", "certifications", "soft_skills", "meta"]);
Object.keys(data).forEach((k) => {
  if (!KNOWN_TOP.has(k)) warn(`unknown top-level key "${k}" — it will NOT be rendered`);
});

// bullets may arrive as bare strings; coerce to { text }
["experience", "projects", "personal_projects"].forEach((sec) => {
  (data[sec] || []).forEach((item) => {
    if (Array.isArray(item?.bullets)) {
      item.bullets = item.bullets.map((b) => (typeof b === "string" ? { text: b } : b));
    }
  });
});

const has = (v) => Array.isArray(v) ? v.length > 0 : (v !== undefined && v !== null && String(v).trim() !== "");

// ---- page geometry (DXA) ----------------------------------------------------

const PAGES = { a4: { width: 11906, height: 16838 }, letter: { width: 12240, height: 15840 } };
const pageKey = String(data?.meta?.page || "a4").toLowerCase();
if (!PAGES[pageKey]) warn(`unknown meta.page "${pageKey}" — using "a4"`);
const PAGE = PAGES[pageKey] || PAGES.a4;
const MARGIN = { top: 720, bottom: 720, left: 864, right: 864 };
const RIGHT_TAB = PAGE.width - MARGIN.left - MARGIN.right;   // dates sit flush to the right margin

// ---- themes (sizes are half-points) ----------------------------------------

const THEMES = {
  classic: {
    font: "Calibri",
    body: 20, name: 36, head: 22, sub: 18,
    ink: "1A1A1A", grey: "555555", accent: "1A1A1A", rule: "AAAAAA",
    nameCaps: false, titleItalic: false, justify: false, companyFirst: false, linkAccent: false,
    headerRule: { style: BorderStyle.SINGLE, size: 4, color: "AAAAAA", space: 4 },
    headingRule: { style: BorderStyle.SINGLE, size: 6, color: "AAAAAA", space: 2 },
    labels: { summary: "Summary", experience: "Experience", projects: "Projects", personal_projects: "Personal Projects", skills: "Skills",
      education: "Education", certifications: "Certifications", soft_skills: "Soft Skills" },
    order: ["summary", "experience", "projects", "personal_projects", "skills", "education", "certifications", "soft_skills"],
  },
  navy: {
    font: "Calibri",
    body: 20, name: 44, head: 23, sub: 20,
    ink: "262626", grey: "595959", accent: "1F4E79", rule: "BFBFBF",
    nameCaps: true, titleItalic: true, justify: true, companyFirst: true, linkAccent: true,
    headerRule: { style: BorderStyle.SINGLE, size: 12, color: "1F4E79", space: 6 },
    headingRule: { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF", space: 2 },
    labels: { summary: "Professional Summary", experience: "Professional Experience", projects: "Key Projects",
      personal_projects: "Personal Projects", skills: "Core Competencies", education: "Education",
      certifications: "Certifications", soft_skills: "Soft Skills" },
    order: ["summary", "skills", "experience", "projects", "personal_projects", "education", "soft_skills", "certifications"],
  },
};
const themeKey = String(data?.meta?.theme || "navy").toLowerCase();
if (!THEMES[themeKey]) warn(`unknown meta.theme "${themeKey}" — using "navy"`);
const T = THEMES[themeKey] || THEMES.navy;

// ---- small builders ---------------------------------------------------------

function sectionHeading(text) {
  return new Paragraph({
    spacing: { before: 240, after: 80 },
    keepNext: true,
    border: { bottom: T.headingRule },
    children: [ new TextRun({ text: text.toUpperCase(), bold: true, size: T.head, color: T.accent, characterSpacing: 12 }) ],
  });
}

// A line with left content and (optionally) a right-aligned string on the same row,
// via an explicit RIGHT tab stop at the right margin (renders correctly in Word, Google Docs, LibreOffice).
function twoSided(leftRuns, rightText, opts = {}) {
  const children = [...leftRuns];
  const para = { spacing: { before: opts.before ?? 120, after: opts.after ?? 20 }, children };
  if (opts.keepNext) para.keepNext = true;
  if (has(rightText)) {
    children.push(new TextRun({ text: "\t", size: T.sub }));
    children.push(new TextRun({ text: rightText, size: T.sub, color: T.grey, italics: !!opts.rightItalic }));
    para.tabStops = [ { type: TabStopType.RIGHT, position: RIGHT_TAB } ];
  }
  return new Paragraph(para);
}

function bullet(text) {
  const para = {
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 20 },
    children: [ new TextRun({ text, size: T.body, color: T.ink }) ],
  };
  if (T.justify) para.alignment = AlignmentType.JUSTIFIED;
  return new Paragraph(para);
}

// No end date → render just the start. "Present" must be stated by the user, never assumed.
function dateRange(start, end) {
  const s = has(start) ? String(start).trim() : "";
  const e = has(end) ? String(end).trim() : "";
  return [s, e].filter(Boolean).join(" – ");   // en dash
}

// ---- header -----------------------------------------------------------------

const children = [];
const rawName = data?.basics?.name || "Your Name";

children.push(new Paragraph({
  spacing: { after: has(data?.basics?.title) ? 20 : 60 },
  children: [ new TextRun({ text: T.nameCaps ? rawName.toUpperCase() : rawName, bold: true, size: T.name, color: T.accent }) ],
}));

if (has(data?.basics?.title)) {
  children.push(new Paragraph({
    spacing: { after: 60 },
    children: [ new TextRun({ text: data.basics.title, size: T.head, italics: T.titleItalic, color: T.titleItalic ? T.accent : T.grey }) ],
  }));
}

const contact = [];
["location", "email", "phone"].forEach((k) => { if (has(data?.basics?.[k])) contact.push({ text: data.basics[k], link: false }); });
(data?.basics?.links || []).forEach((l) => { if (has(l?.url)) contact.push({ text: l.url, link: true }); });
if (contact.length) {
  const runs = [];
  contact.forEach((c, i) => {
    if (i) runs.push(new TextRun({ text: "  •  ", size: T.sub, color: T.grey }));
    runs.push(new TextRun({ text: c.text, size: T.sub, color: (c.link && T.linkAccent) ? T.accent : T.grey }));
  });
  children.push(new Paragraph({
    spacing: { after: 40 },
    border: { bottom: T.headerRule },
    children: runs,
  }));
}

// ---- section renderers ------------------------------------------------------

function projectList(list, label) {
  const items = (list || []).filter((p) => has(p?.name));
  if (!items.length) return;
  children.push(sectionHeading(label));
  items.forEach((p) => {
    const left = [ new TextRun({ text: p.name, bold: true, size: T.body, color: T.accent }) ];
    if (has(p.role)) left.push(new TextRun({ text: `  —  ${p.role}`, size: T.sub, color: T.grey }));
    if (has(p.link)) left.push(new TextRun({ text: `  ${p.link}`, size: T.sub, color: T.grey }));
    children.push(twoSided(left, dateRange(p.start, p.end), { keepNext: true }));
    (p.bullets || []).forEach((b) => { if (has(b?.text)) children.push(bullet(b.text)); });
  });
}

const renderers = {
  summary() {
    if (!has(data.summary)) return;
    children.push(sectionHeading(T.labels.summary));
    const para = { spacing: { after: 40 }, children: [ new TextRun({ text: data.summary, size: T.body, color: T.ink }) ] };
    if (T.justify) para.alignment = AlignmentType.JUSTIFIED;
    children.push(new Paragraph(para));
  },

  experience() {
    const items = (data.experience || []).filter((e) => has(e?.company) || has(e?.title));
    if (!items.length) return;
    children.push(sectionHeading(T.labels.experience));
    items.forEach((e) => {
      if (T.companyFirst) {
        // line 1: Company … dates    line 2: Title · Location (italic grey)
        const first = has(e.company) ? e.company : e.title;
        children.push(twoSided([ new TextRun({ text: first, bold: true, size: T.body, color: T.ink }) ], dateRange(e.start, e.end), { keepNext: true }));
        const second = [has(e.company) ? e.title : "", e.location].filter(has).join(" · ");
        if (second) {
          children.push(new Paragraph({
            spacing: { before: 0, after: 40 },
            keepNext: true,
            children: [ new TextRun({ text: second, size: T.sub, italics: true, color: T.grey }) ],
          }));
        }
      } else {
        const left = [];
        if (has(e.title)) left.push(new TextRun({ text: e.title, bold: true, size: T.body, color: T.ink }));
        if (has(e.company)) left.push(new TextRun({ text: (left.length ? "  —  " : "") + e.company, size: T.body, color: T.ink }));
        if (has(e.location)) left.push(new TextRun({ text: `  (${e.location})`, size: T.sub, color: T.grey }));
        children.push(twoSided(left, dateRange(e.start, e.end), { keepNext: true }));
      }
      (e.bullets || []).forEach((b) => { if (has(b?.text)) children.push(bullet(b.text)); });
    });
  },

  projects() { projectList(data.projects, T.labels.projects); },

  personal_projects() { projectList(data.personal_projects, T.labels.personal_projects); },

  skills() {
    const items = (data.skills || []).filter((g) => has(g?.items));
    if (!items.length) return;
    children.push(sectionHeading(T.labels.skills));
    items.forEach((g) => {
      const runs = [];
      if (has(g.category)) runs.push(new TextRun({ text: `${g.category}: `, bold: true, size: T.body, color: T.accent }));
      runs.push(new TextRun({ text: (g.items || []).join(", "), size: T.body, color: T.ink }));
      children.push(new Paragraph({ spacing: { after: 24 }, children: runs }));
    });
  },

  education() {
    const items = (data.education || []).filter((ed) => has(ed?.institution) || has(ed?.degree));
    if (!items.length) return;
    children.push(sectionHeading(T.labels.education));
    items.forEach((ed) => {
      const degree = [ed.degree, ed.field].filter(has).join(" – ");
      if (T.companyFirst) {
        // line 1: Degree – Field … dates    line 2: Institution · Location (italic grey)
        const first = degree || ed.institution;
        children.push(twoSided([ new TextRun({ text: first, bold: true, size: T.body, color: T.ink }) ], dateRange(ed.start, ed.end), { keepNext: true }));
        const second = [degree ? ed.institution : "", ed.location].filter(has).join(" · ");
        if (second) {
          children.push(new Paragraph({
            spacing: { before: 0, after: 40 },
            children: [ new TextRun({ text: second, size: T.sub, italics: true, color: T.grey }) ],
          }));
        }
      } else {
        const left = [];
        if (has(ed.institution)) left.push(new TextRun({ text: ed.institution, bold: true, size: T.body, color: T.ink }));
        if (degree) left.push(new TextRun({ text: (left.length ? "  —  " : "") + degree, size: T.body, color: T.ink }));
        if (has(ed.location)) left.push(new TextRun({ text: `  (${ed.location})`, size: T.sub, color: T.grey }));
        children.push(twoSided(left, dateRange(ed.start, ed.end)));
      }
      (ed.details || []).forEach((d) => { if (has(d)) children.push(bullet(d)); });
    });
  },

  certifications() {
    const items = (data.certifications || []).filter((c) => has(c?.name));
    if (!items.length) return;
    children.push(sectionHeading(T.labels.certifications));
    items.forEach((c) => {
      const parts = [c.name, c.issuer].filter(has).join(" — ");
      children.push(twoSided([ new TextRun({ text: parts, size: T.body, color: T.ink }) ], has(c.date) ? c.date : ""));
    });
  },

  soft_skills() {
    const items = (data.soft_skills || []).filter(has);
    if (!items.length) return;
    children.push(sectionHeading(T.labels.soft_skills));
    children.push(new Paragraph({
      spacing: { after: 24 },
      children: [ new TextRun({ text: items.join(" · "), size: T.body, color: T.ink }) ],
    }));
  },
};

const order = (data?.meta?.section_order && data.meta.section_order.length)
  ? data.meta.section_order
  : T.order;

order.forEach((s) => {
  if (renderers[s]) renderers[s]();
  else warn(`unknown section "${s}" in meta.section_order — skipped`);
});

// ---- document ---------------------------------------------------------------

const doc = new Document({
  creator: "chat-to-resume-builder",
  styles: { default: { document: { run: { font: T.font, size: T.body, color: T.ink } } } },
  numbering: { config: [ {
    reference: "bullets",
    levels: [ { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 300, hanging: 160 } } } } ],
  } ] },
  sections: [ {
    properties: { page: {
      size: { width: PAGE.width, height: PAGE.height },
      margin: MARGIN,
    } },
    children,
  } ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log(`wrote ${OUT} (${buf.length} bytes, ${children.length} paragraphs, theme=${themeKey in THEMES ? themeKey : "navy"}, page=${pageKey in PAGES ? pageKey : "a4"})`);
}).catch((err) => { console.error("build failed:", err); process.exit(1); });
