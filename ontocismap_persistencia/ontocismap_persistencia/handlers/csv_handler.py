from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
FILES_DIR = BASE_DIR / "files"

def read_csv(file_name: str) -> pd.DataFrame:
    """Lê CSVs do projeto, que usam ponto e vírgula como separador."""
    path = FILES_DIR / file_name
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    return pd.read_csv(path, sep=";", dtype=str, keep_default_na=False).apply(
        lambda col: col.str.strip() if col.dtype == "object" else col
    )
