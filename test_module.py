import unittest
from decoder import df, ca

class TestDecoder(unittest.TestCase):
    msg = "8D4840D6202CC371C32CE0576098"

    def test_df(self):
        self.assertEqual(df(TestDecoder.msg), 17)

    def test_ca(self):
        self.assertEqual(ca(TestDecoder.msg), 5)

if __name__ == '__main__':
    unittest.main()
