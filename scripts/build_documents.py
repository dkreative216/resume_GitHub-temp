#!/usr/bin/env python3
"""Build a 1-page ATS-friendly resume and a 1-page cover letter from a JSON content file.

Usage:
    python3 build_documents.py <content.json> <output_folder>

The content file follows templates/content_template.json. Spacing and font sizes are
reduced in small steps (down to a floor) until each document fits on one page.
"""
import json
import os
import re
import sys
from io import BytesIO
from xml.sax.saxutils import escape

from pypdf import PdfReader
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate

INK = HexColor("#1a1a1a")
SCALES = [1.0, 0.97, 0.94, 0.91, 0.88, 0.85]  # smallest allowed = 85% of the base sizes


def esc(text):
    return escape(str(text or "").strip())


def slug(text):
    return re.sub(r"[^A-Za-z0-9]+", "_", str(text or "").strip()).strip("_") or "Document"


def styles(scale, accent):
    s = lambda v: round(v * scale, 2)
    return {
        "name": ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=s(18), leading=s(21), alignment=TA_CENTER, textColor=INK),
        "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=s(8.8), leading=s(11), alignment=TA_CENTER, textColor=INK),
        "headline": ParagraphStyle("headline", fontName="Helvetica-Bold", fontSize=s(9.6), leading=s(12), alignment=TA_CENTER, textColor=accent, spaceBefore=s(3)),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=s(10.2), leading=s(12), textColor=accent, spaceBefore=s(6), spaceAfter=s(1)),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=s(8.8), leading=s(10.8), textColor=INK),
        "job": ParagraphStyle("job", fontName="Helvetica", fontSize=s(8.9), leading=s(10.9), textColor=INK, spaceBefore=s(3)),
        "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=s(8.8), leading=s(10.8), textColor=INK, leftIndent=11, bulletIndent=2),
        "addl": ParagraphStyle("addl", fontName="Helvetica", fontSize=s(8.8), leading=s(10.8), textColor=INK, spaceBefore=s(3)),
        "cbody": ParagraphStyle("cbody", fontName="Helvetica", fontSize=s(10.5), leading=s(14.3), textColor=INK, spaceAfter=s(8.5)),
    }


def header(story, person, st):
    story.append(Paragraph(esc(person.get("full_name")), st["name"]))
    contact = [person.get("location"), person.get("phone"), person.get("email")]
    story.append(Paragraph(" | ".join(esc(c) for c in contact if c), st["contact"]))
    links = [f"{esc(l.get('label'))}: {esc(l.get('value') or 'Available upon request')}" for l in person.get("links", []) if l.get("label")]
    if links:
        story.append(Paragraph(" | ".join(links), st["contact"]))


def resume_story(c, st, accent):
    r = c["resume"]
    story = []
    header(story, c["person"], st)
    if r.get("headline"):
        story.append(Paragraph(esc(r["headline"]), st["headline"]))

    def section(title):
        story.append(Paragraph(esc(title).upper(), st["h2"]))
        story.append(HRFlowable(width="100%", thickness=0.6, color=accent, spaceBefore=0, spaceAfter=2))

    section("Summary")
    story.append(Paragraph(esc(r.get("summary")), st["body"]))
    section("Skills")
    for group in r.get("skills", []):
        story.append(Paragraph(f"<b>{esc(group.get('label'))}:</b> {esc(group.get('text'))}", st["bullet"], bulletText="•"))
    for sec in r.get("experience_sections", []):
        section(sec.get("title", "Experience"))
        for role in sec.get("roles", []):
            parts = [f"<b>{esc(role.get('title'))}</b>"] + [esc(role.get(k)) for k in ("employer", "location", "dates") if role.get(k)]
            items = [Paragraph(" | ".join(parts), st["job"])]
            items += [Paragraph(esc(b), st["bullet"], bulletText="•") for b in role.get("bullets", [])]
            story.append(KeepTogether(items))
        if sec.get("additional"):
            label, _, rest = sec["additional"].partition(":")
            text = f"<b>{esc(label)}:</b>{esc(':' + rest)[1:]}" if rest else esc(label)
            story.append(Paragraph(text, st["addl"]))
    section("Education and Certifications")
    for item in r.get("education", []):
        story.append(Paragraph(esc(item), st["bullet"], bulletText="•"))
    return story


def cover_story(c, st, accent):
    cl = c["cover_letter"]
    story = []
    header(story, c["person"], st)
    story.append(HRFlowable(width="100%", thickness=0.8, color=accent, spaceBefore=8, spaceAfter=14))
    story.append(Paragraph(esc(cl.get("date")), st["cbody"]))
    story.append(Paragraph("<br/>".join(esc(x) for x in cl.get("recipient_lines", [])), st["cbody"]))
    if cl.get("re_line"):
        story.append(Paragraph(f"<b>{esc(cl['re_line'])}</b>", st["cbody"]))
    story.append(Paragraph(esc(cl.get("greeting")), st["cbody"]))
    for p in cl.get("paragraphs", []):
        lead = f"<b>{esc(p['lead'])}</b> " if p.get("lead") else ""
        story.append(Paragraph(lead + esc(p.get("text")), st["cbody"]))
    story.append(Paragraph(f"{esc(cl.get('closing', 'Sincerely,'))}<br/><br/>{esc(c['person'].get('full_name'))}", st["cbody"]))
    return story


def render(make_story, margins, meta, accent, scale):
    buf = BytesIO()
    st = styles(scale, accent)
    doc = SimpleDocTemplate(buf, pagesize=letter, leftMargin=margins[0] * 72, rightMargin=margins[1] * 72,
                            topMargin=margins[2] * 72, bottomMargin=margins[3] * 72, title=meta, author=meta.split(" - ")[0])
    doc.build(make_story(st, accent))
    data = buf.getvalue()
    return data, len(PdfReader(BytesIO(data)).pages)


def fit_and_save(make_story, margins, meta, accent, path):
    for scale in SCALES:
        data, pages = render(make_story, margins, meta, accent, scale)
        if pages == 1:
            break
    with open(path, "wb") as f:
        f.write(data)
    status = "OK, 1 page" if pages == 1 else f"STILL {pages} PAGES at smallest spacing: cut content and rebuild"
    print(f"{path}: {status} (scale {scale})")
    return pages == 1


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        c = json.load(f)
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    accent = HexColor(c.get("accent_color", "#1f4e79"))
    name = c["person"]["full_name"]
    role = c.get("target", {}).get("role", "Role")
    company = c.get("target", {}).get("company", "Company")
    base = slug(name)
    ok = True
    if c.get("resume"):
        ok &= fit_and_save(lambda st, a: resume_story(c, st, a), (0.6, 0.6, 0.45, 0.4), f"{name} - {role} Resume", accent,
                           os.path.join(out, f"{base}_Resume_{slug(role)}.pdf"))
    if c.get("cover_letter"):
        ok &= fit_and_save(lambda st, a: cover_story(c, st, a), (0.9, 0.9, 0.6, 0.6), f"{name} - Cover Letter - {role}, {company}", accent,
                           os.path.join(out, f"{base}_Cover_Letter_{slug(company)}_{slug(role)}.pdf"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
