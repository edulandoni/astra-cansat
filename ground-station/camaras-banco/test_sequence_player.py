import json
import tempfile
import unittest
from pathlib import Path
from sequence_player import Archive,Playback
from test_sequence_verify import fixture


class PlayerTests(unittest.TestCase):
    def test_irregular_timing_and_changed_image(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);obj=fixture(root)
            for f,stamp in zip(obj['frames'],[1000000,1500000,2700000,3000000]):f['capture_us']=stamp
            (root/'sequence.json').write_text(json.dumps(obj),encoding='utf-8')
            archive=Archive(root)
            with self.assertRaises(ValueError):Archive(root,'1111111111111111')
            self.assertEqual(archive.duration,2.)
            self.assertEqual([archive.index_at(t) for t in [0,.49,.5,1.6,1.7,2,9]],[0,0,1,1,2,3,3])
            self.assertEqual(archive.image(0).size,(640,480))
            (root/'frame_0001.jpg').write_bytes(b'changed')
            with self.assertRaises(ValueError):archive.image(0)

    def test_incomplete_archive_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);obj=fixture(root);obj['closed']=False
            (root/'sequence.json').write_text(json.dumps(obj),encoding='utf-8')
            with self.assertRaises(ValueError):Archive(root)

    def test_pause_resume_rewind(self):
        now=[100.];player=Playback(3,lambda:now[0])
        player.play();now[0]=101.;self.assertEqual(player.elapsed(),1)
        player.pause();now[0]=105.;self.assertEqual(player.elapsed(),1)
        player.play();now[0]=106.;self.assertEqual(player.elapsed(),2)
        now[0]=110.;self.assertEqual(player.elapsed(),3)
        player.rewind();self.assertEqual(player.elapsed(),0)
        player.play();now[0]=111.;self.assertEqual(player.elapsed(),1)

if __name__=='__main__':unittest.main()
