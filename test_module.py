import unittest
from decoder import df, ca, icao, typecode, ec, callsign, cprNL, oeFlag, cprlat, cprlon, airborne_position, altitude, velocity

class TestDecoder(unittest.TestCase):
    msg = "8D4840D6202CC371C32CE0576098"
    msg_pos1 = "8D40621D58C382D690C8AC2863A7"
    msg_pos2 = "8D40621D58C386435CC412692AD6"
    msg_vel = "8D485020994409940838175B284F"

    def test_df(self):
        self.assertEqual(df(TestDecoder.msg), 17)

    def test_ca(self):
        self.assertEqual(ca(TestDecoder.msg), 5)

    def test_icao(self):
        self.assertEqual(icao(TestDecoder.msg), "010010000100000011010110")

    def test_typecode(self):
        self.assertEqual(typecode(TestDecoder.msg), 4)

    def test_ec(self):
        self.assertEqual(ec(TestDecoder.msg), 0)

    def test_callsign(self):
        self.assertEqual(callsign(TestDecoder.msg), "KLM1023")

    def test_cprNL(self):
        self.assertEqual(cprNL(87), 2)
        self.assertEqual(cprNL(0), 59)
        self.assertEqual(cprNL(-88), 1)
        self.assertEqual(cprNL(30), 51)

    def test_oeFlag(self):
        self.assertEqual(oeFlag(TestDecoder.msg_pos1), 0)
        self.assertEqual(oeFlag(TestDecoder.msg_pos2), 1)

    def test_cprlat(self):
        self.assertEqual(cprlat(TestDecoder.msg_pos1), 93000)
        self.assertEqual(cprlat(TestDecoder.msg_pos2), 74158)

    def test_cprlon(self):
        self.assertEqual(cprlon(TestDecoder.msg_pos1), 51372)
        self.assertEqual(cprlon(TestDecoder.msg_pos2), 50194)

    def test_airborne_position(self):
        self.assertEqual(airborne_position(TestDecoder.msg_pos1, TestDecoder.msg_pos2,1,0), (52.25720, 3.91937))

    def test_altitude(self):
        self.assertEqual(altitude(TestDecoder.msg_pos1), 38000)

    def test_velocity(self):
        self.assertEqual(velocity(TestDecoder.msg_vel), (159, 182.9, -832, 'GS'))

if __name__ == '__main__':
    unittest.main()
