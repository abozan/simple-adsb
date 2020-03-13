import unittest
import decoder

class TestDecoder(unittest.TestCase):
    msg = "8D4840D6202CC371C32CE0576098"
    msg_pos1 = "8D40621D58C382D690C8AC2863A7"
    msg_pos2 = "8D40621D58C386435CC412692AD6"
    msg_vel = "8D485020994409940838175B284F"

    def test_df(self):
        self.assertEqual(decoder.df(TestDecoder.msg), 17)

    def test_ca(self):
        self.assertEqual(decoder.ca(TestDecoder.msg), 5)

    def test_icao(self):
        self.assertEqual(decoder.icao(TestDecoder.msg), "010010000100000011010110")

    def test_typecode(self):
        self.assertEqual(decoder.typecode(TestDecoder.msg), 4)

    def test_ec(self):
        self.assertEqual(decoder.ec(TestDecoder.msg), 0)

    def test_callsign(self):
        self.assertEqual(decoder.callsign(TestDecoder.msg), "KLM1023")

    def test_cprNL(self):
        self.assertEqual(decoder.cprNL(87), 2)
        self.assertEqual(decoder.cprNL(0), 59)
        self.assertEqual(decoder.cprNL(-88), 1)
        self.assertEqual(decoder.cprNL(30), 51)

    def test_oeFlag(self):
        self.assertEqual(decoder.oeFlag(TestDecoder.msg_pos1), 0)
        self.assertEqual(decoder.oeFlag(TestDecoder.msg_pos2), 1)

    def test_cprlat(self):
        self.assertEqual(decoder.cprlat(TestDecoder.msg_pos1), 93000)
        self.assertEqual(decoder.cprlat(TestDecoder.msg_pos2), 74158)

    def test_cprlon(self):
        self.assertEqual(decoder.cprlon(TestDecoder.msg_pos1), 51372)
        self.assertEqual(decoder.cprlon(TestDecoder.msg_pos2), 50194)

    def test_airborne_position(self):
        self.assertEqual(decoder.airborne_position(TestDecoder.msg_pos1, TestDecoder.msg_pos2,1,0), (52.25720, 3.91937))

    def test_altitude(self):
        self.assertEqual(decoder.altitude(TestDecoder.msg_pos1), 38000)

    def test_velocity(self):
        self.assertEqual(decoder.velocity(TestDecoder.msg_vel), (159, 182.9, -832, 'GS'))

if __name__ == '__main__':
    unittest.main()
