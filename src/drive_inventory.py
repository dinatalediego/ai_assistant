from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable

import pandas as pd

SUPPORTED = {'.csv', '.json', '.jsonl', '.xlsx', '.xls', '.txt', '.parquet'}
INVENTORY_COLUMNS = [
    'path', 'name', 'suffix', 'bytes', 'sha256', 'supported', 'rows', 'columns', 'error'
]


def iter_files(root: str | Path) -> Iterable[Path]:
    """Yield every file recursively.

    We inventory unsupported files too so the notebook can explain why a dataset
    was not parsed instead of returning an empty DataFrame with no columns.
    """
    root = Path(root)
    yield from (p for p in root.rglob('*') if p.is_file())


def sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            h.update(chunk)
    return h.hexdigest()


def inspect_file(path: Path) -> dict:
    suffix = path.suffix.lower()
    row = {
        'path': str(path),
        'name': path.name,
        'suffix': suffix or '[sin extensión]',
        'bytes': path.stat().st_size,
        'sha256': sha256(path),
        'supported': suffix in SUPPORTED,
        'rows': None,
        'columns': None,
        'error': None,
    }

    if suffix not in SUPPORTED:
        row['error'] = f'Formato todavía no soportado: {suffix or "sin extensión"}'
        return row

    try:
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
        else:  # .txt
            row['rows'] = len(path.read_text(encoding='utf-8', errors='replace').splitlines())
            return row

        row['rows'] = len(df)
        row['columns'] = list(map(str, df.columns))
    except Exception as exc:
        row['error'] = f'{type(exc).__name__}: {exc}'
    return row


def build_inventory(root: str | Path) -> pd.DataFrame:
    rows = [inspect_file(p) for p in iter_files(root)]
    return pd.DataFrame(rows, columns=INVENTORY_COLUMNS)
