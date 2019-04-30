import pandas as pd


def flatten_text(t: pd.Series) -> pd.Series:
    """Replace whitespace characters in text column with spaces"""
    return t.astype(str).str.strip().str.rstrip().str.replace(r'\s+', ' ')
