# interview-prep-kit

A [Claude skill](https://docs.claude.com/en/docs/claude-code/skills) that turns a **job description + company + (optionally) your resume** into one polished interview-prep document: the maximum realistic set of questions you'll face, each with a fully written suggested answer built from your *real* experience — never invented.

## What it does

- Researches the company and **questions candidates actually reported** (Glassdoor, Blind, Reddit, LeetCode Discuss…), cited with source and year, and re-weights the question mix to match the company's real loop.
- Parses the JD into ranked technical topics and behavioral competencies, explains each topic at the right seniority level, and generates questions per a category taxonomy.
- Writes answers tagged with their framework (`[STAR]`, `[CAR]`, `[SOAR]`, `[PPF]`), personalized from resume artifacts; anything unverifiable is marked `(verify)`, inferences `(inferred)`.
- Three depth modes: `quick` (~30 Q&A), `standard` (~70), `max` (~120).
- Delivers `.md`, `.docx`, or `.pdf` (A4 or letter) via `scripts/build_output.py` (python-docx / reportlab, pandoc fallback), plus a reusable `master.md`.
- Optionally delegates resume tailoring to the [chat-to-resume-builder](../chat-to-resume-builder/) skill and keeps the answers consistent with the tailored resume.

## Usage

Install (see [root README](../README.md)), then just ask:

> help me prep for my Zerodha interview — here's the JD and my resume

The skill asks one consolidated batch of intake questions (format, depth, tailoring), then runs the whole pipeline without further questions.

## Requirements

- Web search access (company + past-question recon).
- Python 3 for the output builder; `python-docx` (docx) / `reportlab` (pdf), with pandoc as fallback.
