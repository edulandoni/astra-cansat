import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from sequence_session import record


class SequenceSessionTests(unittest.TestCase):
    def result(self,folder,result,code=0):
        calls=[]
        def run(args,**kwargs):
            calls.append(args);out=Path(args[args.index('--output')+1])/'result';out.mkdir()
            (out/'request-result.json').write_text(json.dumps(result),encoding='utf-8')
            return SimpleNamespace(returncode=code)
        output=record('camera1','1111111111111111','COM7',folder,runner=run)
        return output,calls

    def closed(self):
        return dict(state='reported_closed',response=dict(device='1111111111111111',boot='2222222222222222',id='3333333333333333',closed=True,frames=12,expected_frames=12,reason='COMPLETE',path='/ASTRA_SEQ_2222222222222222_3333333333333333'))

    def test_closed_report_is_not_independent_readback(self):
        with tempfile.TemporaryDirectory() as folder:
            result,calls=self.result(folder,self.closed())
            self.assertTrue(result['reported_closed']);self.assertFalse(result['independent_readback_verified'])
            self.assertEqual(len(calls),1);self.assertNotIn('--reset-once',calls[0])

    def test_unsupported_timeout_and_partial_do_not_approve(self):
        with tempfile.TemporaryDirectory() as folder:
            for obj in [dict(state='unknown_or_not_sent',error='Sin CLIP'),dict(state='unknown_or_not_sent',error='Timeout'),dict(state='reported_partial',response=dict(frames=2,reason='FRAME_FAILED'))]:
                result,calls=self.result(folder,obj,1);self.assertFalse(result['reported_closed']);self.assertEqual(len(calls),1)

    def test_contradictory_closed_result_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            for field,value in [('frames',1),('device','4444444444444444'),('path','/wrong')]:
                obj=self.closed();obj['response'][field]=value
                with self.assertRaises(ValueError):self.result(folder,obj)

    def test_explicit_port_and_device_required(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):record('camera1','1111111111111111','',folder)
            with self.assertRaises(ValueError):record('camera1','wrong','COM7',folder)


if __name__=='__main__':unittest.main()
