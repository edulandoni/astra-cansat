import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from test_sequence_verify import fixture
from sequence_video import export_video


@unittest.skipUnless(importlib.util.find_spec('av'),'Exportación requiere PyAV')
class VideoTests(unittest.TestCase):
    def test_irregular_times_frame_count_and_originals(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);source=root/'source';source.mkdir();obj=fixture(source)
            for f,t in zip(obj['frames'],[1000000,1345678,2198765,3024680]):f['capture_us']=t
            (source/'sequence.json').write_text(json.dumps(obj),encoding='utf-8')
            before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.iterdir()}
            r=export_video(source,None,root/'output')
            self.assertEqual(r['frames'],4);self.assertFalse(r['audio']);self.assertEqual(r['source_origin'],'pc-fixture')
            self.assertLessEqual(r['max_timestamp_error_us'],1000);self.assertTrue(r['originals_unchanged'])
            self.assertEqual(before,{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.iterdir()})
            again=export_video(source,None,root/'output');self.assertNotEqual(r['video'],again['video'])

    def test_incomplete_source_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);obj=fixture(root);obj['closed']=False
            (root/'sequence.json').write_text(json.dumps(obj),encoding='utf-8')
            with self.assertRaises(ValueError):export_video(root,None,root/'output')


if __name__=='__main__':unittest.main()
