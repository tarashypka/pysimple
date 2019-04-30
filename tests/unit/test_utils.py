import unittest
from typing import *

import pandas as pd

from pysimple.utils import flatten_iter, df2dict, split_list


class FlattenIterTestCase(unittest.TestCase):
    """Test utils.flatten_iter() function"""

    def test_output_is_iterator(self):
        """Test if flatten_iter() returns iterator"""
        outp = flatten_iter([[1, 2]])
        self.assertTrue(isinstance(outp, Iterable))

    def test_output_is_valid(self):
        """Test if flatten_iter() returns expected output"""
        inp = [[1, 2], [3, 4]]
        expected = [1, 2, 3, 4]
        actual = list(flatten_iter(inp))
        self.assertEqual(expected, actual)

    def test_iter_input(self):
        """Test if flatten_iter() works with iterators as input"""
        inp = [range(1, 3), range(3, 5)]
        expected = set(range(1, 5))
        actual = set(flatten_iter(inp))
        self.assertEqual(expected, actual)

    def test_empty_input(self):
        """Test if flatten_iter() works with empty list as input"""
        inp = []
        expected = []
        actual = list(flatten_iter(inp))
        self.assertEqual(expected, actual)


class Df2DictTestCase(unittest.TestCase):
    """Test utils.df2dict() function"""

    def test_output_is_valid(self):
        """Test if df2dict() returns expected output"""
        expected = [{'a': 1, 'b': 2}, {'a': 2, 'b': 3}]
        inp = pd.DataFrame(expected)
        actual = df2dict(inp)
        self.assertEqual(expected, actual)

    def test_empty_input(self):
        """Test if df2dict() works with empty DataFrame as input"""
        expected = []
        inp = pd.DataFrame([])
        actual = df2dict(inp)
        self.assertEqual(expected, actual)


class SplitListTestCase(unittest.TestCase):
    """Test utils.split_list() function"""

    def test_output_is_iterator(self):
        """Test if split_list() returns iterator"""
        outp = split_list([1, 2, 3], split_size=1)
        self.assertTrue(isinstance(outp, Iterable))

    def test_splits_arg(self):
        """Test if split_list() returns expected output for splits arg"""
        inp = [1, 2, 3, 4, 5]
        # Split positions
        splits = [0, 2, 4]
        expected = [[], [1, 2], [3, 4], [5]]
        actual = list(split_list(items=inp, splits=splits))
        self.assertEqual(expected, actual)

    def test_empty_splits_arg(self):
        """Test if split_list() works with empty splits arg"""
        inp = [1, 2, 3, 4, 5]
        expected = [inp]
        actual = list(split_list(items=inp, splits=[]))
        self.assertEqual(expected, actual)

    def test_n_splits_arg(self):
        """Test if split_list() returns expected output for n_splits arg"""
        inp = [1, 2, 3, 4, 5]

        expected = [[1, 2, 3, 4, 5]]
        actual = list(split_list(items=inp, n_splits=1))
        self.assertEqual(expected, actual)

        expected = [[1, 2, 3], [4, 5]]
        actual = list(split_list(items=inp, n_splits=2))
        self.assertEqual(expected, actual)

        expected = [[1, 2], [3, 4], [5]]
        actual = list(split_list(items=inp, n_splits=3))
        self.assertEqual(expected, actual)

        inp = list(range(100))
        for n_splits in range(1, 10):
            # Check that there are exactly n splits
            actual = list(split_list(items=inp, n_splits=n_splits))
            self.assertEqual(n_splits, len(actual))
            # Check that splits are of expected equal size
            expected_size = len(actual[0])
            for split in actual[1:-1]:
                self.assertEqual(expected_size, len(split))

    def test_zero_n_splits_arg(self):
        """Test if split_list() returns expected output for n_splits=0"""
        inp = [1, 2, 3, 4, 5]
        expected = [[1, 2, 3, 4, 5]]
        actual = list(split_list(items=inp, n_splits=1))
        self.assertEqual(expected, actual)

    def test_split_size_arg(self):
        """Test if split_list() returns expected output for split_size arg"""
        inp = [1, 2, 3, 4, 5]
        expected = [[1, 2], [3, 4], [5]]
        actual = list(split_list(items=inp, split_size=2))
        self.assertEqual(expected, actual)

        inp = list(range(100))
        for split_size in range(1, 10):
            # Check that each split is of expected size
            actual = list(split_list(items=inp, split_size=split_size))
            for split in actual[:-1]:
                self.assertEqual(split_size, len(split))

    def test_empty_input(self):
        """Test if split_list() works with empty list as input"""
        expected = [[]]
        actual = list(split_list(items=[], n_splits=10))
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
