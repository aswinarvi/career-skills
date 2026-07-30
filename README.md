# career-skills

[Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) for Claude — work in Claude Code (CLI) and the Claude Desktop / claude.ai apps.

| Skill | What it does |
|---|---|
| [chat-to-resume-builder](chat-to-resume-builder/) | Creates, tailors, and iteratively edits resumes/CVs through conversation, producing a polished single-column ATS-friendly `.docx` — with a 0–100 ATS lint score and a plain-text export. Never invents experience. |
| [interview-prep-kit](interview-prep-kit/) | Turns a job description + company + (optionally) your resume into one polished prep document — the maximum realistic set of interview questions with fully written answers personalized to your real experience — as `.md`, `.docx`, or `.pdf`. |

The two compose: interview-prep-kit can delegate resume tailoring to chat-to-resume-builder when both are installed.

## Install — Claude Code (CLI)

```bash
git clone <this-repo-url>
cp -R career-skills/chat-to-resume-builder career-skills/interview-prep-kit ~/.claude/skills/
```

New sessions pick the skills up automatically.

## Install — Claude Desktop / claude.ai

Zip the skill folder and upload it in **Settings → Capabilities → Skills**:

```bash
cd career-skills
zip -r interview-prep-kit.zip interview-prep-kit -x "*.DS_Store"
```

## License

[MIT](LICENSE)
