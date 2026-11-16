#!/usr/bin/env python3
"""Final check for generated resumes and cover letters.

Usage:
    python3 check_pdf.py <file.pdf> [more.pdf ...]

Flags: more than 1 page, em dashes, leftover template placeholders, and text that
cannot be extracted (which hurts ATS parsing). Exits 1 if anything is flagged.
"""
import re
import sys

from pypdf import PdfReader

PLACEHOLDER = re.compile(r"\[[A-Z][A-Za-z /_-]*\]|<[A-Z][A-Za-z /_-]*>|TODO|XXX|Lorem ipsum")


def check(path):
    reader = PdfReader(path)
    text = "\n".join((p.extract_text() or "") for p in reader.pages)
    problems = []
    if len(reader.pages) != 1:
        problems.append(f"{len(reader.pages)} pages (must be 1)")
    if "\u2014" in text:
        problems.append(f"{text.count(chr(0x2014))} em dash(es)")
    found = sorted(set(PLACEHOLDER.findall(text)))
    if found:
        problems.append("placeholders left: " + ", ".join(found[:10]))
    if len(text.strip()) < 200:
        problems.append("very little extractable text (ATS may not read it)")
    print(f"{path}: " + ("OK" if not problems else "FIX -> " + "; ".join(problems)))
    return not problems


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    results = [check(p) for p in sys.argv[1:]]
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
