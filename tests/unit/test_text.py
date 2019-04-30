import unittest

import pandas as pd

from pysimple.text import flatten_text


class FlattenTextTestCase(unittest.TestCase):
    """Test text.flatten_text() function"""

    def test_output_is_valid(self):
        """Test if flatten_text() returns expected flattened texts"""

        inp2outp = {
            '    ': '',
            '\n': '',
            '\t': '',
            '\r': '',
            '\n\t': '',
            '\nabc': 'abc',
            '\n\tAbC\n': 'AbC',
            '\n    AbC\t\rDeF    \nGJk\r': 'AbC DeF GJk'
        }

        data = pd.DataFrame(dict(inp=list(inp2outp.keys()), expected=list(inp2outp.values())))
        data['actual'] = flatten_text(t=data['inp'])

        data['valid'] = data['expected'].eq(data['actual'])

        if not data['valid'].all():
            print('\n\nTest failed for next cases:\n', data.loc[~data['valid'], ['inp', 'expected', 'actual']])

        self.assertTrue(data['valid'].all())


if __name__ == '__main__':
    unittest.main()
