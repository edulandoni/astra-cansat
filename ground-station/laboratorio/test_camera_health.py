import unittest
from camera_health import RecordingHealth


def report(n=1, frames=1, boot='boot1', segment='s1', uptime=1000, last=1000, recording=True, error=None):
    return dict(device='c1',boot=boot,segment=segment,report_seq=n,frames_written=frames,bytes_written=frames*100,uptime_ms=uptime,last_write_ms=last,recording=recording,error=error)


class HealthTests(unittest.TestCase):
    def test_progress_not_just_accepted_or_one_report(self):
        h=RecordingHealth('c1');self.assertEqual(h.view(0),'UNKNOWN')
        h.accept(report(frames=0),0);self.assertEqual(h.view(0),'START_UNCONFIRMED')
        h.accept(report(2),1);self.assertEqual(h.view(1),'WRITING_REPORTED')
        self.assertEqual(h.view(5),'UNKNOWN')

    def test_stalled_reports_and_duplicate_do_not_keep_green(self):
        h=RecordingHealth('c1');h.accept(report(),0)
        self.assertEqual(h.view(0),'PROGRESS_UNCONFIRMED')
        h.accept(report(2,2,uptime=2000,last=2000),1)
        self.assertEqual(h.view(1),'WRITING_REPORTED')
        h.accept(report(3,2,uptime=6000,last=2000),4)
        self.assertEqual(h.view(4),'WRITE_STALLED')
        with self.assertRaises(ValueError):h.accept(report(3,2,uptime=6000,last=2000),6)
        self.assertEqual(h.received_at,4)

    def test_reset_segment_error_and_invalid_identity(self):
        h=RecordingHealth('c1');h.accept(report(),0);h.accept(report(2,2),1)
        h.accept(report(boot='boot2'),2);self.assertEqual(h.view(2),'PROGRESS_UNCONFIRMED')
        h.accept(report(2,boot='boot2',error='SD_FULL'),3);self.assertEqual(h.view(3),'ERROR')
        bad=report();bad['device']='c2'
        with self.assertRaises(ValueError):h.accept(bad,4)
        with self.assertRaises(ValueError):h.accept(report(3,boot='boot2',uptime=0),4)

    def test_stop_and_regression(self):
        h=RecordingHealth('c1');h.accept(report(recording=False),0)
        self.assertEqual(h.view(0),'NOT_RECORDING')
        with self.assertRaises(ValueError):h.accept(report(2,0),1)


if __name__=='__main__':unittest.main()
