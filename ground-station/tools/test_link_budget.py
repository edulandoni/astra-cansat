import unittest
from link_budget import evaluate,FIELDS


def example():
    return dict(label='EJEMPLO, NO ASTRA',example_only=True,
                values=dict(zip(FIELDS,[915,1000,10,0,5,1,1,3,2,-110,10])),
                sources={k:'HipÃ³tesis deliberada de prueba, no mediciÃ³n' for k in FIELDS})


class BudgetTests(unittest.TestCase):
    def test_missing_is_not_zero(self):
        result=evaluate({'values':{k:None for k in FIELDS}})
        self.assertIsNone(result['margin_db']);self.assertEqual(len(result['missing']),len(FIELDS))
    def test_six_db_per_distance_doubling_and_explicit_losses(self):
        p=example();r=evaluate(p)
        self.assertAlmostEqual(r['fspl_db'],91.6762051032,places=8)
        self.assertAlmostEqual(r['received_power_dbm'],8-r['fspl_db'])
        self.assertAlmostEqual(r['margin_db'],r['received_power_dbm']+110)
        p['values']['distance_m']*=2
        self.assertAlmostEqual(evaluate(p)['fspl_db']-r['fspl_db'],6.0205999,places=6)
        self.assertAlmostEqual(r['additional_loss_sweep'][-1]['margin_db'],r['margin_db']-10)
    def test_sensitivity_cannot_be_invented_and_invalid_inputs_fail(self):
        p=example();p['values']['rx_sensitivity_dbm']=None
        self.assertIsNone(evaluate(p)['margin_db'])
        for key,value in [('frequency_mhz',0),('other_loss_db',-1),('tx_power_dbm',True),('distance_m',float('inf'))]:
            p=example();p['values'][key]=value
            with self.assertRaises(ValueError):evaluate(p)
        p=example();p['sources']['tx_power_dbm']='TBD'
        with self.assertRaises(ValueError):evaluate(p)


if __name__=='__main__':unittest.main(verbosity=2)
