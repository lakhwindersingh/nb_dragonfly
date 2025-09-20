#!/usr/bin/env python3
"""
Prettify Markdown and text files in the sdlc-pipeline directory.

Rules applied (conservative):
- Normalize tabs to 4 spaces
- Trim trailing whitespace
- Ensure a single blank line between blocks (collapse 2+ blank lines to 1)
- Ensure a single newline at end of file
- Ensure a space after Markdown heading hashes (e.g., '##Heading' -> '## Heading')
- Standardize unordered list bullets to '- ' when lines start with '* ' or '+ '
- Preserve fenced code blocks verbatim (``` ... ``` and ~~~ fences)

Additional enhancements for readability:
- Normalize code fences to backticks with consistent language aliases (e.g., yml→yaml, sh/shell→bash)
- Ensure a blank line before and after fenced code blocks
- Auto-wrap ASCII folder tree sections (├──, │, └──, +--, etc.) into fenced blocks as ```text

This script is idempotent and safe to run multiple times.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[3]  # project root
PIPELINE_DIR = ROOT / "sdlc-pipeline"

HEADING_RE = re.compile(r"^( {0,3})(#{1,6})([^#\s`].*)$")
BULLET_RE = re.compile(r"^(\s*)([\*\+])\s+(.*)$")
FENCE_RE = re.compile(r"^([ \t]*)(`{3,}|~{3,})(.*)$")

# Detect a line that looks like part of a folder tree (ASCII art)
TREE_LINE_RE = re.compile(r"(?:[├└│])|(?:\+--)|(?:\|\s)|(?:`--)|(?:-- )")

LANG_ALIASES = {
    "yml": "yaml",
    "sh": "bash",
    "shell": "bash",
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "tf": "hcl",
    "docker": "dockerfile",
}

def _normalize_fence_info(info: str) -> str:
    info = (info or "").strip()
    if not info:
        return ""
    parts = info.split()
    if parts:
        lang = parts[0].lower()
        lang = LANG_ALIASES.get(lang, lang)
        parts[0] = lang
    return " ".join(parts)

def _ensure_blank_around_blocks(lines: list[str]) -> list[str]:
    out: list[str] = []
    in_code = False
    for i, line in enumerate(lines):
        m = FENCE_RE.match(line)
        if m:
            indent, marker, rest = m.groups()
            info = _normalize_fence_info(rest)
            # normalize marker to backticks
            opener = f"{indent}```{info}".rstrip()
            if not in_code:
                # ensure blank line before opener if previous is non-blank and not beginning
                if out and out[-1].strip() != "":
                    out.append("")
                out.append(opener)
                in_code = True
            else:
                # closer
                out.append(f"{indent}```")
                # ensure blank line after closer if next is non-blank (handled in next iteration peek)
                in_code = False
            continue
        out.append(line)
    # Ensure single blank line after closing fence if last added was a closer followed by text already handled by collapse step
    return out

def _wrap_tree_sections(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    in_code = False
    n = len(lines)
    while i < n:
        line = lines[i]
        if FENCE_RE.match(line):
            # passthrough fences untouched; normalization happens later
            out.append(line)
            # toggle in_code
            in_code = not in_code
            i += 1
            continue
        if not in_code:
            # detect start of a tree block: current line and next line match TREE_LINE_RE
            if TREE_LINE_RE.search(line):
                # collect contiguous tree-like lines
                block: list[str] = [line]
                j = i + 1
                while j < n and lines[j].strip() != "" and TREE_LINE_RE.search(lines[j]):
                    block.append(lines[j])
                    j += 1
                # Only wrap if at least 2 lines or single line with obvious tree glyphs
                if block:
                    # ensure blank before
                    if out and out[-1].strip() != "":
                        out.append("")
                    out.append("```text")
                    out.extend([b.rstrip() for b in block])
                    out.append("```")
                    # ensure blank after
                    if j < n and lines[j].strip() != "":
                        out.append("")
                    i = j
                    continue
        out.append(line)
        i += 1
    return out


def is_markup_file(p: Path) -> bool:
    if not p.is_file():
        return False
    ext = p.suffix.lower()
    if ext in {".md", ".markdown", ".txt"}:
        return True
    # Also prettify top-level README files without extension (rare)
    return p.name.lower() in {"readme"}


def prettify_lines(lines: Iterable[str]) -> list[str]:
    # First pass: basic normalization outside code fences
    out: list[str] = []
    in_code = False

    def emit(line: str):
        out.append(line)

    for raw in lines:
        line = raw.rstrip("\n\r")

        # Detect fences (start or end). Keep code blocks verbatim for now
        m = FENCE_RE.match(line)
        if m:
            in_code = not in_code
            emit(line.rstrip())
            continue

        if in_code:
            # Preserve verbatim inside code blocks
            emit(line.rstrip())
            continue

        # Normalize tabs to 4 spaces
        line = line.replace("\t", "    ")
        # Trim trailing whitespace
        line = line.rstrip()

        # Ensure a space after heading hashes (if any)
        hm = HEADING_RE.match(line)
        if hm:
            indent, hashes, rest = hm.groups()
            rest = rest.lstrip()
            emit(f"{indent}{hashes} {rest}".rstrip())
            continue

        # Standardize bullet markers for unordered lists
        bm = BULLET_RE.match(line)
        if bm:
            lead_ws, _bullet, content = bm.groups()
            emit(f"{lead_ws}- {content}".rstrip())
            continue

        emit(line)

    # Collapse multiple blank lines to single blank line
    collapsed: list[str] = []
    blank = False
    for line in out:
        if line.strip() == "":
            if not blank:
                collapsed.append("")
            blank = True
        else:
            collapsed.append(line)
            blank = False

    # Remove leading/trailing blank lines
    while collapsed and collapsed[0].strip() == "":
        collapsed.pop(0)
    while collapsed and collapsed[-1].strip() == "":
        collapsed.pop()

    # Second pass: wrap ASCII folder tree sections outside code fences
    wrapped = _wrap_tree_sections(collapsed)

    # Third pass: normalize fences to backticks, normalize language info, and ensure blank lines around code blocks
    fenced = _ensure_blank_around_blocks(wrapped)

    # Final collapse to clean up any extra blank lines introduced
    final: list[str] = []
    blank = False
    for line in fenced:
        if line.strip() == "":
            if not blank:
                final.append("")
            blank = True
        else:
            final.append(line.rstrip())
            blank = False

    # Trim leading/trailing blanks again
    while final and final[0].strip() == "":
        final.pop(0)
    while final and final[-1].strip() == "":
        final.pop()

    return final


def process_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    pretty = prettify_lines(original)
    new_content = "\n".join(pretty) + "\n"
    old_content = "\n".join(original)
    if new_content != old_content + ("\n" if not old_content.endswith("\n") else ""):
        path.write_text(new_content, encoding="utf-8")
        return True
    return False


def main(argv: list[str]) -> int:
    base = PIPELINE_DIR
    if not base.exists():
        print(f"sdlc-pipeline directory not found at {base}")
        return 2

    changed = 0
    files: list[Path] = []
    for p in base.rglob('*'):
        if is_markup_file(p):
            files.append(p)
    files.sort()

    for f in files:
        try:
            if process_file(f):
                changed += 1
                print(f"[prettified] {f.relative_to(ROOT)}")
        except Exception as e:
            print(f"[warn] failed to prettify {f}: {e}")

    print(f"Done. Files updated: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
