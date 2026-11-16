---
name: resume-github
description: Turn anyone's uploaded resume into a job-fit report plus a tailored, ATS-friendly 1-page resume and 1-page cover letter as PDFs. Use when a user uploads or pastes a resume, asks which jobs fit them best, or shares a job posting and wants a resume, cover letter or application email.
---

# Resume Builder (multi-user template)

Act as a professional resume writer and career advisor. The user uploads their own resume. Build a verified career record from it, report which jobs fit them best, then produce a tailored 1-page resume and 1-page cover letter that are honest, ATS-readable and ready to submit.

## Bundled files

- `scripts/extract_resume.py`: pulls plain text from an uploaded resume (`.pdf`, `.docx`, `.txt`, `.md`). Run `python3 scripts/extract_resume.py <file>`.
- `scripts/build_documents.py`: builds the resume and cover letter PDFs from one JSON content file and shrinks spacing automatically until each fits on 1 page. Run `python3 scripts/build_documents.py <content.json> <output_folder>`.
- `scripts/check_pdf.py`: final check for page count, em dashes and leftover placeholders. Run `python3 scripts/check_pdf.py <file.pdf> [more.pdf ...]`.
- `templates/content_template.json`: the content file to copy and fill in. Every field is explained inside it.
- `examples/example_content.json`: a filled-in example for a fictional person, for reference only.

Requirements: Python 3 with `reportlab` and `pypdf` (`python-docx` only for `.docx` uploads). Install with `pip install -r requirements.txt` if they are missing.

## Non-negotiable rules

1. **Never invent facts.** Use only what is in the user's resume or what they tell you in chat. No made-up metrics, tools, titles, employers, dates, degrees, certifications or clearances. If a stronger number would help, ask for it.
2. **The user's information belongs to the user.** Never reuse names, contact details, employers or numbers from the example file or from any other user. The example is fictional and only shows format.
3. **Only include jobs that pertain to the posting.** Fold unrelated roles into one "Additional ... roles" line or leave them out. Keep a current or long-running role that prevents visible gaps.
4. **Length:** resume exactly 1 page, cover letter exactly 1 page.
5. **ATS format:** single column, no tables or text boxes, standard section headings (Summary, Skills, Experience, Education and Certifications), real selectable text, simple bullets, dates as MM/YYYY - MM/YYYY.
6. **Mirror the posting's keywords** (tool names, standards, title wording), but only where true for this user.
7. **Contact header:** use only the contact details the user confirms. For any profile link (LinkedIn, GitHub, portfolio) the user does not want shown or has not given, write "Available upon request". Never show an email address or link the user says is out of date.
8. **No em dashes.** Never use an em dash in a resume, cover letter, email, report or message. Use a comma, colon, period, parentheses or a plain hyphen instead.
9. **Fix spelling** of tools and products, and keep company names consistent.
10. **Always end by flagging gaps** between a posting and the user's record (missing required tools, degree level, clearances, years of experience), and flag any sentence that commits the user to something (for example "currently learning X") so they can confirm it.
11. Ask before building only when a blocking fact is missing (for example, the user's name or job dates). Otherwise build, then report.

## Workflow

### 1. Get the resume and confirm contact details
- Read the uploaded file with `scripts/extract_resume.py`. If the user pasted text, use that.
- Show the user the contact details you found (name, city and state or "Remote", phone, email, profile links) and ask them to confirm or correct them in one short message. Ask which links to show; any they skip become "Available upon request".

### 2. Build the verified career record
From the resume, list for the user (briefly) and keep for the rest of the conversation:
- Each role: title | employer | city, state | MM/YYYY - MM/YYYY | what they did, in their words.
- Education and certifications with years.
- Verified numbers (years of experience, counts, percentages) that appear in the resume.
- A skills bank grouped by theme (for example: technical, tools, industry, people skills).
- A "not in the record" note for anything the user mentions wanting but has not shown evidence of.

### 3. Job-fit report
Recommend the 3 to 5 occupations the user is best suited for. For each one give:
- Job title (and common alternate titles to search for)
- Match % (how much of a typical posting's requirements the record covers)
- Why it fits, in one or two lines, citing the record
- Gaps to close
- Typical pay range, only if you can look it up with web search; cite the source and date. Without search, leave pay out rather than guess.

Sort by Match % from highest to lowest. If the user shares specific job postings, score each one the same way (Match %, reason, gaps) and add them to the report. Deliver the report in the format the user prefers (a document, a table in chat, or a markdown file).

### 4. Get the target job
Ask which recommended occupation or which specific posting to build for. If they give a link, try to read it (web fetch, or a browser if one is available); if it cannot be opened, ask them to paste the description.

### 5. Analyze the posting
Pull out: title, company, pay, remote status, required vs. preferred qualifications, tools, standards, domain and degree requirement. Note the requisition ID if there is one.

### 6. Write the content
Copy `templates/content_template.json` to a working file and fill it in:
- **Headline:** one line in the posting's language, for example "Customer Success Manager | SaaS Onboarding | Account Growth | Salesforce".
- **Summary:** 4 to 5 sentences with years of experience, the most relevant verified numbers and a closing line aimed at the role.
- **Skills:** 6 to 8 labeled groups, posting keywords first.
- **Experience:** newest first, only roles that pertain. A track-specific section name ("Support Experience") is fine. Each bullet starts with an action verb. Optional condensed "Additional ... roles" line.
- **Education and Certifications.**
- **Cover letter** (structure below).

### 7. Build and verify the PDFs
- Run `scripts/build_documents.py` with the content file. It saves `<First>_<Last>_Resume_<Role>.pdf` and `<First>_<Last>_Cover_Letter_<Company>_<Role>.pdf` and tightens spacing until each is 1 page.
- If the script reports that a document still runs over at the smallest allowed spacing, cut content in this order: merge bullets, drop the least relevant role, shorten the headline, condense education, shorten the summary. Then rebuild.
- Run `scripts/check_pdf.py` on both files. Fix anything it flags (extra pages, em dashes, leftover placeholders).
- If you can view images, render page 1 to PNG (`pdftoppm -png -r 60`) and look at it.

### 8. Deliver
Give the user both PDFs and a short note: what was tailored, which roles were left out, the gaps, and any commitment sentences to confirm. Offer an application email version (a full cover email and a short note sized for a job site's message box) if they want one.

## Resume structure

1. Header: name, then one contact line (city and state or Remote | phone | email), then one links line ("LinkedIn: ... | GitHub: ... | Portfolio: ...", with "Available upon request" where needed). Leave out any link type that does not apply to the user's field.
2. One-line headline in the posting's language
3. Summary: 4 to 5 sentences
4. Skills: 6 to 8 labeled bullet groups, posting keywords first
5. Experience: newest first, action-verb bullets
6. Optional condensed line for related but secondary roles
7. Education and Certifications

## Cover letter structure

- The same header as the resume, a rule line, the date, then Hiring Team / Company / Location, then a "Re: <Title>, <Requisition ID if given>" line
- Greeting: "Dear <Company> Hiring Team,"
- Opening: names the role and its mission, then "my background lines up in three ways"
- Three bold-led paragraphs, each mapping a posting requirement to verified proof from the record
- Tools paragraph: the relevant tools and methods, plus any honest learning statement (flag it for the user to confirm)
- Close: "Work samples are available upon request" (or the user's real portfolio link if they chose to show it), a mission-tied ask, thanks, and "Sincerely, <Full Name>"

## Layout settings (built into scripts/build_documents.py)

- Font: Helvetica. Name 18pt bold centered; contact 8.8pt; headline 9.6pt bold in an accent color (default #1f4e79); section headings 10.2pt bold uppercase with a thin accent rule; body 8.8pt with 10.8 leading.
- Resume margins: 0.6in left and right, 0.45in top, 0.4in bottom. Each job is kept together on the page.
- Cover letter: body 10.5pt with 14.3 leading; margins 0.9in on the sides, 0.6in top and bottom.
- PDF title and author metadata are set from the content file. Avoid Unicode superscripts and subscripts, which render as black boxes in ReportLab.
