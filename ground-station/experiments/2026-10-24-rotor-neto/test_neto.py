import unittest
from evaluar import evaluate,scenarios


class NetEnergyTests(unittest.TestCase):
    def test_original_scale_and_negative_benefit_are_preserved(self):
        cases=scenarios()
        self.assertAlmostEqual(cases['sin_carga_extra']['net_incremental_wh'],.05448138888889)
        self.assertAlmostEqual(cases['sin_generacion_con_auxiliar']['net_incremental_wh'],-.00444444444444)
        self.assertLess(cases['auxiliar_dos_horas_previas']['net_incremental_wh'],0)
        self.assertGreater(cases['auxiliar_solo_en_descenso']['net_incremental_wh'],0)
    def test_invalid_efficiency_and_cost_fail(self):
        p=dict(mass_kg=.5,height_m=400.,descent_m_s=5.,efficiency=.1,extra_load_w=.2,standby_s=0.)
        for key,value in [('efficiency',1.1),('standby_s',-1),('descent_m_s',0),('extra_load_w',float('nan'))]:
            with self.assertRaises(ValueError):evaluate(**{**p,key:value})


if __name__=='__main__':unittest.main(verbosity=2)
