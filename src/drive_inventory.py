from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable

import pandas as pd

SUPPORTED = {'.csv', '.json', '.jsonl', '.xlsx', '.xls', '.txt', '.parquet'}


def iter_files(root: str | Path) -> Iterable[Path]:
    root = Path(root)
    yield from (p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in SUPPORTED)


def sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            h.update(chunk)
    return h.hexdigest()


def inspect_file(path: Path) -> dict:
    row = {
        'path': str(path),
        'name': path.name,
        'suffix': path.suffix.lower(),
        'bytes': path.stat().st_size,
        'sha256': sha256(path),
        'rows': None,
        'columns': None,
        'error': None,
    }
    try:
        suffix = path.suffix.lower()
        if suffix == '.csv':
            df = pd.read_csv(path, nrows=5000)
        elif suffix in {'.xlsx', '.xls'}:
            df = pd.read_excel(path, nrows=5000)
        elif suffix == '.parquet':
            df = pd.read_parquet(path)
        elif suffix == '.jsonl':
            df = pd.read_json(path, lines=True)
        elif suffix == '.json':
            obj = json.loads(path.read_text(encoding='utf-8'))
            df = pd.json_normalize(obj if isinstance(obj, list) else [obj])
        else:
            row['rows'] = len(path.read_text(encoding='utf-8', errors='replace').splitlines())
            return row
        row['rows'] = len(df)
        row['columns'] = list(map(str, df.columns))
    except Exception as exc:
        row['error'] = f'{type(exc).__name__}: {exc}'
    return row


def build_inventory(root: str | Path) -> pd.DataFrame:
    return pd.DataFrame(inspect_file(p) for p in iter_files(root))
