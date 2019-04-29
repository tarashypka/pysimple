import pandas as pd


def flatten_text(t: pd.Series, fillna: str='') -> pd.Series:
    """Replace whitespace characters in text column with spaces"""
    return t \
        .fillna(fillna).astype(str) \
        .str.strip() \
        .str.rstrip() \
        .str.replace(r'\s+', ' ')
