import unittest

import pandas as pd

from pysimple.text import flatten_text


class TextTestCase(unittest.TestCase):
    """Test functions in text module"""

    def test_flatten_text_output(self):
        """Test if flatten_text function returns flattened texts as expected"""

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
