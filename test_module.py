import unittest
from decoder import df, ca, icao, tc, ec, callsign, cprNL


class TestDecoder(unittest.TestCase):
    msg = "8D4840D6202CC371C32CE0576098"

    def test_df(self):
        self.assertEqual(df(TestDecoder.msg), 17)

    def test_ca(self):
        self.assertEqual(ca(TestDecoder.msg), 5)

    def test_icao(self):
        self.assertEqual(icao(TestDecoder.msg), "010010000100000011010110")

    def test_tc(self):
        self.assertEqual(tc(TestDecoder.msg), 4)

    def test_ec(self):
        self.assertEqual(ec(TestDecoder.msg), 0)

    def test_callsign(self):
        self.assertEqual(callsign(TestDecoder.msg), "KLM1023")

    def test_cprNL(self):
        self.assertEqual(cprNL(87), 2)
        self.assertEqual(cprNL(0), 59)
        self.assertEqual(cprNL(-88), 1)
        self.assertEqual(cprNL(30), 51)

if __name__ == '__main__':
    unittest.main()
