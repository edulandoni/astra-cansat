import json
import tempfile
import unittest
import zlib
from pathlib import Path
from PIL import Image
from sequence_verify import verify, PROFILE


def fixture(root):
    frames=[]
    for index in range(1,5):
        name=f'frame_{index:04d}.jpg'
        Image.new('RGB',(640,480),(index*40,80,150)).save(root/name,'JPEG')
        data=(root/name).read_bytes()
        frames.append(dict(index=index,file=name,boot='0123456789abcdef',capture_us=index*500000,
                           bytes=len(data),crc32=f'{zlib.crc32(data)&0xffffffff:08x}'))
    obj=dict(v=1,profile=PROFILE,origin='pc-fixture',boot='0123456789abcdef',expected_frames=4,closed=True,frames=frames)
    return obj


class SequenceTests(unittest.TestCase):
    def run_case(self,change):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); obj=fixture(root); change(obj,root)
            (root/'sequence.json').write_text(json.dumps(obj),encoding='utf-8')
            return verify(root)

    def test_nominal_and_timing(self):
        result=self.run_case(lambda o,p:None)
        self.assertTrue(result['complete']);self.assertTrue(result['originals_unchanged'])
        self.assertEqual(result['origin'],'pc-fixture');self.assertEqual(result['mean_interval_fps'],2)

    def test_bad_crc_and_missing_file(self):
        bad=self.run_case(lambda o,p:o['frames'][0].update(crc32='00000000'))
        self.assertFalse(bad['complete'])
        missing=self.run_case(lambda o,p:(p/'frame_0002.jpg').unlink())
        self.assertFalse(missing['complete']);self.assertEqual(missing['checked_frames'],3)

    def test_incomplete_and_reset(self):
        for mutate in (lambda o,p:o.update(closed=False),lambda o,p:o['frames'].pop(),
                       lambda o,p:o['frames'][2].update(boot='ffffffffffffffff')):
            self.assertFalse(self.run_case(mutate)['complete'])

    def test_duplicate_and_time(self):
        for mutate in (lambda o,p:o['frames'][1].update(file='frame_0001.jpg'),
                       lambda o,p:o['frames'][2].update(capture_us=1),
                       lambda o,p:o['frames'][0].update(file='../frame_0001.jpg')):
            self.assertFalse(self.run_case(mutate)['complete'])

    def test_camera_requires_independent_expected_identity(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); obj=fixture(root)
            obj.update(origin='camera',device='1111111111111111')
            (root/'sequence.json').write_text(json.dumps(obj),encoding='utf-8')
            with self.assertRaises(ValueError):verify(root)
            with self.assertRaises(ValueError):verify(root,'2222222222222222')
            self.assertTrue(verify(root,'1111111111111111')['complete'])

if __name__=='__main__':unittest.main()
