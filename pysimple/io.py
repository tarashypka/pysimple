import sys
import json
import gzip
import pickle
from collections import defaultdict
from logging import Logger
from pathlib import Path
from typing import *

import dill
import pandas as pd

from pysimple.logging import silent_logger


# Always represent NaN values with the same identifier
NAN_IDENTIFIER = 'NA'


def plain_path(path: Path) -> Path:
    """Flatten path"""
    return Path(path).expanduser().absolute()


def ensure_dir(dirpath: Path) -> Path:
    """Ensure that directory exists"""
    dirpath = plain_path(dirpath)
    dirpath.mkdir(parents=True, exist_ok=True)
    return dirpath


def ensure_filedir(filepath: Path) -> Path:
    """Ensure that file directory exists"""
    filepath = plain_path(filepath)
    ensure_dir(filepath.parent)
    return filepath


def read_lines(filepath: Path, logger: Logger=silent_logger(), **kwargs) -> Iterator[str]:
    """Read lines from text file"""
    filepath = plain_path(filepath)
    kwargs.setdefault('mode', 'r')
    kwargs.setdefault('encoding', 'utf-8')
    logger.info(f'Read lines from {filepath} ...')
    with filepath.open(**kwargs) as f:
        for line in f:
            yield line.rstrip()


def write_lines(filepath: Path, lines: List[str], logger: Logger=silent_logger(), **kwargs) -> None:
    """Write lines into text file"""
    filepath = ensure_filedir(filepath)
    kwargs.setdefault('mode', 'w')
    kwargs.setdefault('encoding', 'utf-8')
    logger.info(f'Write {len(lines)} lines into {filepath} ...')
    with filepath.open(**kwargs) as f:
        for line in lines:
            f.write(line + '\n')


def load_pickle(filepath: Path, use_dill: bool=False, logger: Logger=silent_logger()):
    """Deserialize object with pickle"""
    filepath = plain_path(filepath)
    logger.info(f'Load data from {filepath} ...')
    serializer = dill if use_dill else pickle
    compress = str(filepath).endswith('.gz')
    file = gzip.open(filepath, mode='rb') if compress else filepath.open(mode='rb')
    with file as f:
        return serializer.load(f)


def dump_pickle(filepath: Path, obj: "serializable object", use_dill: bool=False, logger: Logger=silent_logger()):
    """Serialize object with pickle"""
    filepath = ensure_filedir(filepath)
    logger.info(f'Dump data into {filepath} ...')
    protocol = 2 if sys.version_info[0] == 2 else 4
    serializer = dill if use_dill else pickle
    compress = str(filepath).endswith('.gz')
    file = gzip.open(filepath, mode='wb') if compress else filepath.open(mode='wb')
    with file as f:
        try:
            serializer.dump(obj, f, protocol=protocol)
        except RecursionError:
            logger.warning('Set recursion limit to 10000!')
            sys.setrecursionlimit(10000)
            serializer.dump(obj, f, protocol=protocol)


def from_json(filepath: Path, encoding='utf-8', logger: Logger=silent_logger(), **kwargs):
    """Load dictionary from json file"""
    filepath = plain_path(filepath)
    logger.info(f'Load data from {filepath} ...')
    with filepath.open(mode='r', encoding=encoding) as f:
        return json.load(f, **kwargs)


def to_json(filepath: Path, data: dict, encoding='utf-8', logger: Logger=silent_logger(), **kwargs):
    """Dump dictionary into json file"""
    filepath = ensure_filedir(filepath)
    logger.info(f'Dump data to {filepath} ...')
    kwargs.setdefault('indent', 4)
    kwargs.setdefault('ensure_ascii', False)
    with filepath.open(mode='w', encoding=encoding) as f:
        json.dump(data, f, **kwargs)


def count_lines(filepath: Path, **kwargs) -> int:
    """Count lines in file"""
    filepath = plain_path(filepath)
    kwargs.setdefault('mode', 'r')
    kwargs.setdefault('encoding', 'utf-8')
    with filepath.open(**kwargs) as f:
        return sum(1 for _ in f)


def from_tsv(filepath: Path, logger: Logger=silent_logger(), **kwargs) -> pd.DataFrame:
    """Load table from tsv file"""
    filepath = plain_path(filepath)
    kwargs.setdefault('sep', '\t')
    kwargs.setdefault('na_values', NAN_IDENTIFIER)
    kwargs.setdefault('keep_default_na', False)
    kwargs.setdefault('dtype', object)
    if str(filepath).endswith('.gz'):
        kwargs.setdefault('compression', 'gzip')
    logger.info(f'Load data from {filepath} ...')
    return pd.read_csv(filepath, **kwargs)


def to_tsv(filepath: Path, data: pd.DataFrame, logger: Logger=silent_logger(), **kwargs):
    """Write table into tsv file"""
    filepath = ensure_filedir(filepath)
    kwargs.setdefault('sep', '\t')
    kwargs.setdefault('na_rep', NAN_IDENTIFIER)
    kwargs.setdefault('encoding', 'utf-8')
    kwargs.setdefault('index', False)
    if str(filepath).endswith('.gz'):
        kwargs.setdefault('compression', 'gzip')
    logger.info(f'Dump {len(data)} rows into {filepath} ...')
    data.to_csv(filepath, **kwargs)


def suffix_filename(path: Path, suffix: str) -> Path:
    """Append suffix after filename"""
    path = plain_path(path)
    return path.with_name(path.stem + suffix + path.suffix)


# Mapping of unpickable attributes in shared memory
__SHARED__: Dict[int, Dict] = defaultdict(dict)


class Serializable:
    """May be used to pickle class with unpickable attributes, must be inherited"""

    def __init__(self, shared: Dict):
        global __SHARED__
        self.id_ = id(self)
        __SHARED__[self.id_].update(shared)

    def __getstate__(self):
        state = dict(self.__dict__)
        for attr_name, attr_val in __SHARED__[self.id_].items():
            del state[attr_name]
        return state

    def __setstate__(self, state: Dict):
        self.__dict__.update(state)
        self.__dict__.update(__SHARED__[self.id_])
