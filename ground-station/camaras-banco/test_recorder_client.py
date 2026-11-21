import io,json,queue,tempfile,threading,unittest
from pathlib import Path
from recorder_client import RecorderLink,monitor

DEVICE='1'*16;BOOT='a'*16


class Port:
    def __init__(self,*args,device=DEVICE,capable=True,**kwargs):
        self.device=device;self.capable=capable;self.boot=BOOT;self.buffer=bytearray();self.sent=[];self.seq=0;self.run='';self.frames=0;self.active=False
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def write(self,data):
        self.sent.append(data);cmd,ident,*args=data.decode().split()
        if cmd=='INFO':r=dict(v=1,event='info',profile='camera-usb-0.1',device=self.device,boot=self.boot,camera_ready=True,commands=['REC_START','REC_STOP','REC_STATUS'] if self.capable else [])
        else:
            if cmd=='REC_START':self.run=ident;self.active=True
            if cmd=='REC_STOP':self.active=False
            if self.active:self.frames+=1
            self.seq+=1
            r=dict(v=1,event='recorder',profile='camera-recorder-0.1',device=self.device,boot=self.boot,run=self.run,segment='segment1',state='RECORDING' if self.active else ('COMPLETE' if self.run else 'IDLE'),recording=self.active,report_seq=self.seq,frames_captured=self.frames,frames_written=self.frames,frames_readback=self.frames,bytes_written=self.frames*1000,uptime_ms=5000,last_write_ms=4000,free_bytes=100000,segments_closed=0,error='',reason='')
        self.buffer+=b'@CAM '+json.dumps(dict(r,id=ident)).encode()+b'\n'
    def flush(self):pass
    def read(self,n):data=bytes(self.buffer[:13]);del self.buffer[:13];return data


class RecorderTests(unittest.TestCase):
    def test_fragmented_protocol_start_status_stop(self):
        p=Port();link=RecorderLink(p,DEVICE,io.BytesIO());link.identify()
        r=link.start(30,ident='b'*16);self.assertTrue(r['recording'])
        self.assertGreater(link.status()['frames_written'],r['frames_written'])
        self.assertFalse(link.stop(r['run'])['recording'])
        self.assertEqual(len(p.sent),4)

    def test_wrong_identity_or_capability_prevents_start(self):
        for p in [Port(device='2'*16),Port(capable=False)]:
            with self.assertRaises(ValueError):RecorderLink(p,DEVICE).identify()
            self.assertEqual(len(p.sent),1)

    def test_reboot_conflict_and_timeout_no_retry(self):
        p=Port();link=RecorderLink(p,DEVICE);link.identify();p.boot='c'*16
        with self.assertRaises(ValueError):link.status()
        self.assertEqual(len(p.sent),2)
        class Silent(Port):
            def write(self,data):self.sent.append(data)
            def read(self,n):return b''
        t=[0]
        def clock():t[0]+=.1;return t[0]
        p=Silent();link=RecorderLink(p,DEVICE,clock=clock)
        with self.assertRaises(TimeoutError):link.request('REC_STATUS',budget=1)
        self.assertEqual(len(p.sent),1)

    def test_report_contradiction_rejected(self):
        p=Port();link=RecorderLink(p,DEVICE);link.identify();r=link.start(5)
        r=dict(r,report_seq=r['report_seq']+1,frames_readback=999)
        with self.assertRaises(ValueError):link.validate_status(r)

    def test_detach_does_not_send_stop_and_preserves_journal(self):
        p=Port();detach=threading.Event();detach.set()
        with tempfile.TemporaryDirectory() as folder:
            result=monitor('COM7',DEVICE,folder,5,True,threading.Event(),detach,queue.Queue(maxsize=4),serial_factory=lambda **k:p)
            self.assertEqual(result['state'],'DETACHED')
            self.assertFalse(any(b'REC_STOP' in cmd for cmd in p.sent))
            self.assertTrue((Path(result['folder'])/'monitor-result.json').exists())

    def test_rejection_is_distinct_from_unknown(self):
        class Reject(Port):
            def write(self,data):
                if data.startswith(b'REC_START'):
                    self.sent.append(data);ident=data.decode().split()[1]
                    self.buffer+=b'@CAM '+json.dumps(dict(v=1,event='error',id=ident,boot=BOOT,reason='WIFI_MUST_BE_OFF')).encode()+b'\n'
                else:super().write(data)
        p=Reject()
        with tempfile.TemporaryDirectory() as folder:
            result=monitor('COM7',DEVICE,folder,5,True,threading.Event(),threading.Event(),queue.Queue(maxsize=4),serial_factory=lambda **k:p)
            self.assertEqual(result['state'],'REJECTED');self.assertIn('Desactivá',result['error'])
            self.assertEqual(len(p.sent),2)


if __name__=='__main__':unittest.main()
