import unittest

import numpy as np

from pysimple.stats import bootstrap


class StatsTestCase(unittest.TestCase):
    """Test functions in stats module"""

    def setUp(self):
        np.random.seed(37)

    def tearDown(self):
        np.random.seed()

    def test_bootstrap_output(self):
        """Test if bootstrap function returns mean and percentiles as expected"""
        x = np.random.random(size=10_000)
        x_mean, x_percentile1, x_percentile2 = bootstrap(x=x, samples=100, percent=10)
        self.assertAlmostEqual(x_mean, 0.500, delta=0.001)
        self.assertAlmostEqual(x_percentile1, 0.496, delta=0.001)
        self.assertAlmostEqual(x_percentile2, 0.504, delta=0.001)
