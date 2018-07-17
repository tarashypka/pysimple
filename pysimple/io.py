import os
import pickle
from pathlib import Path
from typing import *

import pandas as pd

from pysimple.utils import silent
from pysimple.utils import is_hash


# Always represent NaN values with the same identifier
__NAN_IDENTIFIER__ = 'NA'


def plain_path(path: os.PathLike) -> Path:
    return Path(path).expanduser().absolute()


def ensure_dir(dirpath: os.PathLike) -> os.PathLike:
    dirpath = plain_path(dirpath)
    dirpath.mkdir(parents=True, exist_ok=True)
    return dirpath


def ensure_filedir(filepath: os.PathLike) -> os.PathLike:
    filepath = plain_path(filepath)
    ensure_dir(filepath.parent)
    return filepath


def safe_dir(dirpath: os.PathLike):
    dirpath = plain_path(dirpath)
    dirpath.mkdir(parents=True, exist_ok=True)
    return dirpath


def read_lines(filepath: os.PathLike, report: Callable=silent, **kwargs) -> Generator[str, None, None]:
    filepath = plain_path(filepath)
    kwargs.setdefault('mode', 'r')
    kwargs.setdefault('encoding', 'utf-8')
    report('Read lines from', filepath, '...')
    with open(filepath, **kwargs) as f:
        for line in f:
            yield line.rstrip()


def write_lines(filepath: os.PathLike, lines: List[str], report: Callable=silent, **kwargs) -> None:
    filepath = ensure_filedir(filepath)
    kwargs.setdefault('mode', 'w')
    kwargs.setdefault('encoding', 'utf-8')
    report('Write', len(lines), 'lines into', filepath, '...')
    with open(filepath, **kwargs) as f:
        for line in lines:
            f.write(line + '\n')


def to_tsv(filepath: str, data: pd.DataFrame, report: Callable=silent, **kwargs) -> None:
    ensure_filedir(filepath=filepath)
    kwargs.setdefault('sep', '\t')
    kwargs.setdefault('na_rep', __NAN_IDENTIFIER__)
    kwargs.setdefault('encoding', 'utf-8')
    kwargs.setdefault('index', False)
    report('Dump', data.shape[0], 'rows into', filepath, '...')
    data.to_csv(filepath, **kwargs)


def from_tsv(filepath: os.PathLike, report: Callable=silent, **kwargs) -> pd.DataFrame:
    filepath = plain_path(filepath)
    kwargs.setdefault('sep', '\t')
    kwargs.setdefault('na_values', __NAN_IDENTIFIER__)
    kwargs.setdefault('keep_default_na', False)
    kwargs.setdefault('dtype', object)
    report('Load data from', filepath, '...')
    return pd.read_csv(filepath, **kwargs)


def to_tsv(filepath: os.PathLike, data: pd.DataFrame, report: Callable=silent, **kwargs) -> None:
    filepath = ensure_filedir(filepath)
    kwargs.setdefault('sep', '\t')
    kwargs.setdefault('na_rep', __NAN_IDENTIFIER__)
    kwargs.setdefault('encoding', 'utf-8')
    kwargs.setdefault('index', False)
    report('Dump', len(data), 'rows into', filepath, '...')
    data.to_csv(filepath, **kwargs)


def load_pickle(filepath: os.PathLike, report: Callable=silent) -> Any:
    filepath = plain_path(filepath)
    report('Load object from', filepath, '...')
    with open(filepath, mode='rb') as f:
        return pickle.load(f)


def dump_pickle(filepath: os.PathLike, obj: Any, report: Callable=silent) -> None:
    filepath = ensure_filedir(filepath)
    report('Dump object into', filepath, '...')
    with open(filepath, mode='wb') as f:
        pickle.dump(obj, f)


def list_hashes(dirpath: os.PathLike) -> List[str]:
    return [d for d in os.listdir(dirpath) if is_hash(d)]


def suffix_filename(filepath: os.PathLike, suffix: str) -> str:
    filepath, fileext = os.path.splitext(filepath)
    return filepath + suffix + fileext


def count_lines(filepath: os.PathLike, **kwargs) -> int:
    return sum(1 for _ in open(filepath, **kwargs))
