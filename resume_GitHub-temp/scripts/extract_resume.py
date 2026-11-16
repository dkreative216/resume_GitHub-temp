#!/usr/bin/env python3
"""Print the plain text of an uploaded resume.

Usage:
    python3 extract_resume.py <resume.pdf|resume.docx|resume.txt|resume.md>
"""
import os
import sys


def from_pdf(path):
    from pypdf import PdfReader
    text = "\n".join((page.extract_text() or "") for page in PdfReader(path).pages)
    if not text.strip():
        print("No selectable text found. The PDF may be a scan: ask the user for a text version or paste.", file=sys.stderr)
    return text


def from_docx(path):
    try:
        import docx
    except ImportError:
        sys.exit("python-docx is not installed. Run: pip install python-docx")
    d = docx.Document(path)
    lines = [p.text for p in d.paragraphs]
    for table in d.tables:
        for row in table.rows:
            lines.append(" | ".join(cell.text for cell in row.cells))
    return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        text = from_pdf(path)
    elif ext == ".docx":
        text = from_docx(path)
    elif ext in (".txt", ".md", ".rtf", ""):
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
    else:
        sys.exit(f"Unsupported file type: {ext}. Use PDF, DOCX, TXT or MD, or paste the text.")
    print(text.strip())


if __name__ == "__main__":
    main()
