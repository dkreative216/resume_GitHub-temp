# resume-github: a Claude skill for job-fit reports, resumes and cover letters

Upload your resume and Claude will:

1. Build a verified record of your experience (nothing invented).
2. Give you a **job-fit report**: the 3 to 5 roles you fit best, with a match %, why you fit, gaps to close and (when web search is on) typical pay.
3. Score any job postings you share the same way.
4. Write a tailored, ATS-friendly **1-page resume** and **1-page cover letter** for the job you pick, and generate them as PDFs.

## What's in this folder

| Path | What it does |
|---|---|
| `SKILL.md` | The instructions Claude follows (required). |
| `scripts/extract_resume.py` | Reads your uploaded resume (PDF, DOCX, TXT or MD). |
| `scripts/build_documents.py` | Builds the resume and cover letter PDFs from one JSON file and auto-fits each to 1 page. |
| `scripts/check_pdf.py` | Final check: 1 page, no em dashes, no leftover placeholders. |
| `templates/content_template.json` | The blank content file Claude fills in for you. |
| `examples/example_content.json` | A filled-in example for a fictional person. |
| `requirements.txt` | Python packages the scripts need. |

## Install

**Claude apps (web, desktop):** download `resume-github.zip` from this repository's Releases (or zip the `resume-github` folder yourself so `SKILL.md` sits inside a top-level `resume-github/` folder). In Claude, open Settings, go to the Skills section and upload the zip. Code execution needs to be turned on for the PDF scripts to run.

**Claude Code:** copy the `resume-github` folder into `~/.claude/skills/` (for all projects) or `.claude/skills/` inside a project.

**Claude API / Agent SDK:** upload the folder as a custom skill. See Anthropic's skills documentation at https://docs.claude.com for the current steps.

If the PDF scripts report a missing package, run `pip install -r requirements.txt`.

## Use it

Start a chat and say something like:

- "Here's my resume. Which jobs fit me best?" (attach your resume)
- "Build a resume and cover letter for this posting: <paste the job description or link>"
- "Score these three job postings against my resume."

Claude will confirm your contact details first. Any profile link you don't want shown (LinkedIn, GitHub, portfolio) appears as "Available upon request".

## Rules the skill follows

- Uses only facts from your resume or what you tell it. No invented numbers, titles, degrees or tools.
- Single-column, ATS-readable layout with standard headings.
- Resume and cover letter are each exactly 1 page.
- No em dashes anywhere.
- Flags gaps between you and each posting, and any sentence that commits you to something, so you can confirm it.

## Privacy

Your resume stays in your own Claude conversation. This repository contains no personal data. The example file uses a fictional person.

## License

MIT. See `LICENSE`.
