"""ASTRA-41: integración con el receptor y límites de la presentación."""
import json
import tempfile
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from runtime import Simulation, packet_at, radio_rows, recovery_demo, chart_runs


class LaboratoryTests(unittest.TestCase):
    def test_recovery_and_conflicts(self):
        with tempfile.TemporaryDirectory() as folder:
            complete=recovery_demo(folder)
            partial=recovery_demo(folder,'ausente_en_ambas')
            conflict=recovery_demo(folder,'conflicto')
            self.assertTrue(complete['written']); self.assertEqual(complete['candidates'],10)
            self.assertTrue(partial['written']); self.assertEqual(partial['candidates'],9)
            self.assertFalse(conflict['written']); self.assertEqual(conflict['conflicts'],1)
            self.assertFalse(list(Path(conflict['root']).rglob('*.csv')))
            for result in (complete,partial,conflict):self.assertTrue(result['originals_unchanged'])
            csv_file=next(Path(complete['root']).rglob('*.csv'))
            self.assertEqual(len(csv_file.read_text().splitlines()),11)
            self.assertEqual(len((csv_file.parents[2]/'provenance.jsonl').read_text().splitlines()),10)

    def test_graph_does_not_join_gaps_or_sessions(self):
        points=[('a',1,0),('a',2,5),('a',4,10),('b',5,15)]
        self.assertEqual([len(run) for run in chart_runs(points)],[2,1,1])

    def test_packet_and_airtime(self):
        raw, rows=packet_at(0)
        self.assertEqual(len(rows),22)
        self.assertEqual(len(raw),124)
        self.assertTrue(raw.endswith(b'\r'))
        self.assertAlmostEqual(radio_rows(55)[0]['airtime_seconds'],.107776)
        self.assertEqual([r['sf'] for r in radio_rows(100)],list(range(7,13)))
        self.assertGreater(next(r for r in radio_rows(100) if r['sf']==10)['airtime_seconds'],1)

    def test_scenarios_saved_by_real_engine(self):
        def run(scenario):
            with tempfile.TemporaryDirectory() as folder:
                sim=Simulation(folder,scenario,10)
                try:
                    until=time.monotonic()+24
                    while not sim.engine.snapshot()['done'] and time.monotonic()<until: time.sleep(.05)
                    snap=sim.engine.snapshot()
                    self.assertTrue(snap['done'],scenario)
                    self.assertGreater(snap['total_valid'],100,scenario)
                    if scenario=='NOMINAL':
                        self.assertEqual(snap['total_valid'],131)
                        self.assertEqual(snap['invalid'],0)
                        self.assertEqual(snap['observed_gaps'],0)
                    if scenario=='PACKET_LOSS':self.assertGreater(snap['observed_gaps'],0)
                    if scenario=='CORRUPTED_PACKET':self.assertGreater(snap['invalid'],0)
                    if scenario=='RESET':self.assertEqual(snap['observed_gaps'],3)
                finally:sim.close()
                self.assertFalse(sim.thread.is_alive())
                self.assertTrue(all(not w.thread.is_alive() for w in sim.store.writers))
                journal=sim.store.roots[0]/'journal.jsonl'
                events=[json.loads(line) for line in journal.read_text().splitlines()]
                self.assertTrue(any(e['kind']=='packet' for e in events))
                self.assertTrue(all(w['pending']==0 and w['dropped']==0 for w in sim.store.status()))
                return scenario, snap['total_valid'], snap['invalid'], snap['observed_gaps']
        with ThreadPoolExecutor(max_workers=5) as executor:
            results=list(executor.map(run,['NOMINAL','PACKET_LOSS','CORRUPTED_PACKET','GPS_LOSS','RESET']))
        print('Resultados de integración:', results)

if __name__=='__main__':unittest.main()
