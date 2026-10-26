import io
import json
import unittest
from sequence_request import request,Controls,ProtocolError,receive

BOOT='0123456789abcdef';DEVICE='1111111111111111'
def control(**obj):return b'@CAM '+json.dumps(dict(v=1,**obj)).encode()+b'\n'

class Port:
    def __init__(self,capability=True,device=DEVICE):self.pending=bytearray();self.writes=[];self.capability=capability;self.device=device
    def write(self,data):
        self.writes.append(data);op,ident=data.decode().strip().split()
        if op=='INFO':self.pending.extend(control(event='info',id=ident,profile='camera-usb-0.1',camera_ready=True,device=self.device,boot=BOOT,commands=['INFO','CLIP'] if self.capability else ['INFO']))
        else:self.pending.extend(control(event='sequence',id=ident,boot=BOOT,device=self.device,path=f'/ASTRA_SEQ_{BOOT}_{ident}',frames=12,expected_frames=12,closed=True,reason='COMPLETE'))
    def read(self,n):data=self.pending[:7];del self.pending[:7];return bytes(data)
    def flush(self):pass

class RequestTests(unittest.TestCase):
    def test_fragmented_report_is_not_independent_proof(self):
        port=Port();ids=iter(['aaaaaaaaaaaaaaaa','bbbbbbbbbbbbbbbb'])
        result=request(port,io.BytesIO(),DEVICE,lambda:next(ids))
        self.assertEqual(result['state'],'reported_closed')
        self.assertFalse(result['independent_readback_verified'])
        self.assertEqual(len(port.writes),2)

    def test_wrong_unit_and_old_firmware_prevent_clip(self):
        for port in (Port(device='2222222222222222'),Port(capability=False)):
            with self.assertRaises(ProtocolError):request(port,io.BytesIO(),DEVICE)
            self.assertEqual(len(port.writes),1)

    def test_timeout_does_not_send_any_retry(self):
        port=Port(); times=iter([0,0,2])
        with self.assertRaises(TimeoutError):receive(port,io.BytesIO(),Controls(),'a','sequence',1,clock=lambda:next(times))
        self.assertEqual(port.writes,[])

    def test_bounded_decoder_and_unexpected_frame(self):
        with self.assertRaises(ProtocolError):Controls().feed(b'x'*1025)
        with self.assertRaises(ProtocolError):Controls().feed(control(event='frame'))

    def test_partial_reset_and_contradictory_result(self):
        class Altered(Port):
            def __init__(self,alter):super().__init__();self.alter=alter
            def write(self,data):
                super().write(data)
                if data.startswith(b'CLIP '):
                    msg=json.loads(self.pending[5:]);self.alter(msg)
                    self.pending=bytearray(control(**{k:v for k,v in msg.items() if k!='v'}))
        partial=Altered(lambda m:m.update(frames=3,closed=False,reason='FRAME_FAILED'))
        self.assertEqual(request(partial,io.BytesIO(),DEVICE)['state'],'reported_partial')
        for alter in (lambda m:m.update(boot='ffffffffffffffff'),lambda m:m.update(frames=3),
                      lambda m:m.update(path='/OTHER_FOLDER'),lambda m:m.update(device='2222222222222222')):
            port=Altered(alter)
            with self.assertRaises(ProtocolError):request(port,io.BytesIO(),DEVICE)
            self.assertEqual(len(port.writes),2)

if __name__=='__main__':unittest.main()
