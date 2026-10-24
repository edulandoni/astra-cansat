"""Contrastes numéricos y restricciones del modelo; no ensayos RF."""
import unittest
from airtime_lora import airtime

class AirtimeTests(unittest.TestCase):
    def test_known_arithmetic(self):
        # SF7/125k: 88 símbolos de payload +12,25 preámbulo; 1,024ms/símbolo.
        self.assertAlmostEqual(airtime(51,7,125000,1,8,1,0)['airtime_seconds'],.102656)
        self.assertAlmostEqual(airtime(134,7,125000,1,8,1,0)['airtime_seconds'],.220416)
        self.assertAlmostEqual(airtime(134,12,125000,1,8,1,0)['airtime_seconds'],5.087232)
    def test_constraints_and_optimization(self):
        for n in [0,256]:
            with self.assertRaises(ValueError):airtime(n,7,125000,1,8,1,0)
        with self.assertRaises(ValueError):airtime(20,6,125000,1,8,1,0)
        with self.assertRaises(ValueError):airtime(20,12,125000,1,8,1,0,de=0)
        self.assertEqual(airtime(20,12,125000,1,8,1,0)['de'],1)
        self.assertEqual(airtime(20,7,125000,1,8,1,0)['de'],0)
        self.assertGreater(airtime(134,9,125000,4,8,1,0)['airtime_seconds'],airtime(134,9,125000,1,8,1,0)['airtime_seconds'])

if __name__=='__main__':unittest.main()
