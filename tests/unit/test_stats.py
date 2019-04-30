import unittest

import numpy as np

from pysimple.stats import bootstrap


class BootstrapTestCase(unittest.TestCase):
    """Test stats.bootstrap() function"""

    def setUp(self):
        np.random.seed(37)

    def tearDown(self):
        np.random.seed()

    def test_output_is_valid(self):
        """Test if bootstrap() returns expected mean and percentiles"""
        x = np.random.random(size=10_000)
        x_mean, x_percentile1, x_percentile2 = bootstrap(x=x, samples=100, percent=10)
        self.assertAlmostEqual(x_mean, 0.500, delta=0.001)
        self.assertAlmostEqual(x_percentile1, 0.496, delta=0.001)
        self.assertAlmostEqual(x_percentile2, 0.504, delta=0.001)


if __name__ == '__main__':
    unittest.main()
