"""Fixtures de PC con formato simulado de cámara; no representan una captura física."""
import json,tempfile,unittest
from pathlib import Path
from test_sequence_verify import fixture
from recording_verify import verify_recording

DEVICE='1'*16


def setup(root):
    total=0
    for n in range(1,3):
        folder=root/f'segment_{n:04}';folder.mkdir();obj=fixture(folder)
        obj.update(origin='camera',device=DEVICE)
        for f in obj['frames']:
            f['capture_us']+=(n-1)*2000000
            (folder/f['file'].replace('.jpg','.json')).write_text(json.dumps({k:f[k] for k in ('index','boot','capture_us','bytes','crc32')}),encoding='utf-8')
            total+=f['bytes']
        (folder/'sequence.json').write_text(json.dumps(obj),encoding='utf-8')
    base=dict(v=1,profile='camera-recording-0.1',origin='camera',device=DEVICE,boot='0123456789abcdef',run='b'*16,started_us=0)
    start=dict(base,requested_seconds=5,segment_limit=60)
    end=dict(base,closed=True,reason='DURATION_LIMIT',segments_closed=2,frames_captured=8,frames_written=8,bytes_written=total,finished_us=5000000)
    (root/'session-start.json').write_text(json.dumps(start),encoding='utf-8');(root/'session-result.json').write_text(json.dumps(end),encoding='utf-8')


class RecordingTests(unittest.TestCase):
    def test_two_segments_and_originals_unchanged(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder);setup(p);before={f.relative_to(p):f.read_bytes() for f in p.rglob('*') if f.is_file()}
            r=verify_recording(p,DEVICE)
            self.assertTrue(r['complete']);self.assertEqual(r['checked_frames'],8);self.assertEqual(r['mean_interval_fps'],2)
            self.assertEqual(before,{f.relative_to(p):f.read_bytes() for f in p.rglob('*') if f.is_file()})

    def test_partial_missing_and_conflicting_sidecar(self):
        for mode in ['partial','missing','conflict','time','total']:
            with tempfile.TemporaryDirectory() as folder:
                p=Path(folder);setup(p)
                if mode=='missing':(p/'segment_0002/frame_0001.jpg').unlink()
                elif mode=='conflict':
                    f=p/'segment_0001/frame_0001.json';o=json.loads(f.read_text());o['capture_us']=99;f.write_text(json.dumps(o))
                elif mode=='time':
                    f=p/'segment_0002/sequence.json';o=json.loads(f.read_text());o['frames'][0]['capture_us']=1;f.write_text(json.dumps(o))
                else:
                    f=p/'session-result.json';o=json.loads(f.read_text());o.update(closed=False) if mode=='partial' else o.update(frames_written=9);f.write_text(json.dumps(o))
                self.assertFalse(verify_recording(p,DEVICE)['complete'])

    def test_identity_and_unclosed_extra_segment(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder);setup(p)
            with self.assertRaises(ValueError):verify_recording(p,'2'*16)
            (p/'segment_0003').mkdir();self.assertFalse(verify_recording(p,DEVICE)['complete'])

    def test_complete_recording_plays_and_exports_without_filling_gaps(self):
        from sequence_player import Archive
        from sequence_video import export_video
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'source';p.mkdir();setup(p)
            a=Archive(p,DEVICE)
            self.assertEqual(len(a.frames),8);self.assertEqual(a.image(7).size,(640,480))
            result=export_video(p,DEVICE,Path(folder)/'exports')
            self.assertEqual(result['state'],'verified');self.assertEqual(result['frames'],8)
            self.assertEqual(result['source_timestamps_us'],[i*500000 for i in range(8)])


if __name__=='__main__':unittest.main()
