from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import pandas as pd


def iter_pdfs(root: str | Path) -> Iterable[Path]:
    root = Path(root)
    yield from (p for p in root.rglob('*.pdf') if '_analysis_outputs' not in p.parts)


def extract_pdf_text(path: str | Path, max_pages: int | None = None) -> tuple[str, int]:
    """Extract selectable text from a PDF with PyMuPDF. No OCR is attempted."""
    import fitz  # pymupdf

    path = Path(path)
    chunks: list[str] = []
    with fitz.open(path) as doc:
        pages = len(doc)
        limit = pages if max_pages is None else min(pages, max_pages)
        for i in range(limit):
            chunks.append(doc[i].get_text('text'))
    return '\n'.join(chunks).strip(), pages


def parse_filename(path: str | Path) -> dict:
    """Best-effort metadata from names like 0122_Name_Name_999999999.pdf.

    It deliberately keeps the original filename and does not assume the final
    numeric token is always a phone number; that remains a candidate field.
    """
    p = Path(path)
    stem = p.stem
    tokens = stem.split('_')
    first_numeric = tokens[0] if tokens and tokens[0].isdigit() else None
    trailing_numeric = tokens[-1] if tokens and re.fullmatch(r'\d{6,15}', tokens[-1]) else None
    middle = tokens[1:-1] if trailing_numeric else tokens[1:]
    lead_name_candidate = ' '.join(middle).strip() or None
    return {
        'source_file': p.name,
        'source_path': str(p),
        'file_sequence_candidate': first_numeric,
        'lead_name_candidate': lead_name_candidate,
        'lead_numeric_candidate': trailing_numeric,
    }


def build_pdf_text_index(root: str | Path, max_files: int | None = None, max_pages: int | None = None) -> pd.DataFrame:
    rows = []
    for i, path in enumerate(iter_pdfs(root)):
        if max_files is not None and i >= max_files:
            break
        meta = parse_filename(path)
        try:
            text, pages = extract_pdf_text(path, max_pages=max_pages)
            meta.update({
                'pages': pages,
                'text_chars': len(text),
                'text_extractable': bool(text.strip()),
                'text_preview': text[:3000],
                'error': None,
            })
        except Exception as exc:
            meta.update({
                'pages': None,
                'text_chars': 0,
                'text_extractable': False,
                'text_preview': '',
                'error': f'{type(exc).__name__}: {exc}',
            })
        rows.append(meta)
    return pd.DataFrame(rows)


def normalize_text(text: str) -> str:
    text = text.replace('\u00a0', ' ')
    text = re.sub(r'\r\n?', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()
