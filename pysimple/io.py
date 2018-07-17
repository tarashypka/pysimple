import os
import pickle
from typing import *

import pandas as pd

from pysimple.utils import silent
from pysimple.utils import is_hash


# Always represent NaN values with the same identifier
__NAN_IDENTIFIER__ = 'NA'


def plain_path(path: str) -> str:
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return path


def _ensure_filedir(filepath: str) -> None:
    filedir, _ = plain_path(path=filepath).rsplit(os.sep, maxsplit=1)
    if not os.path.isdir(filedir):
        os.makedirs(filedir)


def read_lines(filepath: str, report: Callable=silent, **kwargs) -> Generator[str, None, None]:
    kwargs.setdefault('mode', 'r')
    kwargs.setdefault('encoding', 'utf-8')
    report('Read lines from', filepath, '...')
    with open(filepath, **kwargs) as f:
        for line in f:
            yield line


def write_lines(filepath: str, lines: List[str], report: Callable=silent, **kwargs) -> None:
    _ensure_filedir(filepath=filepath)
    kwargs.setdefault('mode', 'w')
    kwargs.setdefault('encoding', 'utf-8')
    report('Write lines into', filepath, '...')
    with open(filepath, **kwargs) as f:
        for line in lines:
            f.write(line + '\n')


def to_tsv(filepath: str, data: pd.DataFrame, report: Callable=silent, **kwargs) -> None:
    _ensure_filedir(filepath=filepath)
    kwargs.setdefault('sep', '\t')
    kwargs.setdefault('na_rep', __NAN_IDENTIFIER__)
    kwargs.setdefault('encoding', 'utf-8')
    kwargs.setdefault('index', False)
    report('Dump', data.shape[0], 'rows into', filepath, '...')
    data.to_csv(filepath, **kwargs)


def from_tsv(filepath: str, report: Callable=silent, **kwargs) -> pd.DataFrame:
    kwargs.setdefault('sep', '\t')
    kwargs.setdefault('na_values', __NAN_IDENTIFIER__)
    kwargs.setdefault('keep_default_na', False)
    kwargs.setdefault('dtype', object)
    report('Load data from', filepath, '...')
    return pd.read_csv(filepath, **kwargs)


def dump_pickle(filepath: str, obj: Any, report: Callable=silent) -> None:
    _ensure_filedir(filepath=filepath)
    report('Dump object into', filepath, '...')
    with open(filepath, mode='wb') as f:
        pickle.dump(obj, f)


def load_pickle(filepath: str, report: Callable=silent) -> Any:
    report('Load object from', filepath, '...')
    with open(filepath, mode='rb') as f:
        return pickle.load(f)


def list_hashes(dirpath: str) -> List[str]:
    return [d for d in os.listdir(dirpath) if is_hash(d)]


def prefix_filename(filepath: str, prefix: str) -> str:
    filepath, fileext = os.path.splitext(filepath)
    return filepath + prefix + fileext


def count_lines(filepath: str, **kwargs) -> int:
    return sum(1 for _ in open(filepath, **kwargs))
