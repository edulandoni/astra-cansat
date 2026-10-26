"""ASTRA-39: fallas de transferencia y evidencia de foto, sin hardware."""
import io
import json
import unittest
import zlib
from PIL import Image
from camera_check import Decoder,ProtocolError,check_result,PROFILE,receive,restart_before_capture,validate_peer

ID='0123456789abcdef'
BOOT='abcdef0123456789'
DEVICE='0000000000000011'

def control(msg):
    return b'@CAM '+json.dumps({'v':1,**msg}).encode()+b'\n'

def fixture():
    out=io.BytesIO();Image.new('RGB',(640,480),(120,20,60)).save(out,format='JPEG')
    data=out.getvalue()
    header=dict(event='frame',id=ID,boot=BOOT,device=DEVICE,length=len(data),
                crc32=f'{zlib.crc32(data):08x}',width=640,height=480,
                request_us=100,capture_us=200,saved=True,sd_status='READBACK_OK',path='/prueba.jpg')
    info=dict(event='info',profile=PROFILE,camera_ready=True,boot=BOOT,device=DEVICE)
    wire=control(header)+data+b'\n'+control(dict(event='end',id=ID,boot=BOOT))
    return info,header,data,wire

class CameraTests(unittest.TestCase):
    def test_expected_camera_is_checked_before_capture_or_sd_request(self):
        info,_,_,_=fixture()
        validate_peer(info,DEVICE)
        with self.assertRaisesRegex(ProtocolError,'otra cámara'):
            validate_peer(info,'0000000000000022')
        not_ready={**info,'camera_ready':False}
        with self.assertRaisesRegex(ProtocolError,'no preparado'):validate_peer(not_ready,DEVICE)
        validate_peer(not_ready,DEVICE,require_ready=False)
        with self.assertRaisesRegex(ProtocolError,'otra cámara'):
            validate_peer(not_ready,'0000000000000022',require_ready=False)

    def test_fragmentation_and_burst_decode(self):
        info,h,data,wire=fixture()
        for chunk in (1,7,1024,len(wire)):
            d=Decoder();events=[]
            for i in range(0,len(wire),chunk):events+=d.feed(wire[i:i+chunk])
            d.finish();self.assertEqual(len(events),1)
            self.assertEqual(events[0]['payload'],data)
            self.assertTrue(check_result(info,events[0],True)['decoded'])

    def test_crc_corruption(self):
        _,h,data,_=fixture();bad=bytearray(data);bad[len(bad)//2]^=1
        with self.assertRaisesRegex(ProtocolError,'CRC distinto'):
            Decoder().feed(control(h)+bad+b'\n'+control(dict(event='end',id=ID,boot=BOOT)))

    def test_truncation_reset_and_wrong_order(self):
        _,h,data,wire=fixture()
        d=Decoder();d.feed(wire[:len(control(h))+100])
        with self.assertRaisesRegex(ProtocolError,'incompleta'):d.finish()
        for end in (dict(event='end',id='f'*16,boot=BOOT),dict(event='end',id=ID,boot='f'*16)):
            with self.assertRaisesRegex(ProtocolError,'otra captura'):
                Decoder().feed(control(h)+data+b'\n'+control(end))

    def test_oversize_header_and_payload_limits(self):
        _,h,_,_=fixture()
        for n in (-1,True,524289):
            with self.assertRaisesRegex(ProtocolError,'Tamaño'):Decoder().feed(control({**h,'length':n}))
        with self.assertRaisesRegex(ProtocolError,'demasiado largo'):Decoder().feed(b'x'*2048)
        with self.assertRaisesRegex(ProtocolError,'demasiado largo'):Decoder().feed(b'x'*1500+b'\n')

    def test_matching_crc_does_not_prove_jpeg(self):
        info,h,_,_=fixture();bad=b'not a photo'
        wire=control({**h,'length':len(bad),'crc32':f'{zlib.crc32(bad):08x}'})+bad+b'\n'+control(dict(event='end',id=ID,boot=BOOT))
        msg=Decoder().feed(wire)[0]
        with self.assertRaises(Exception):check_result(info,msg)

    def test_image_geometry_and_color(self):
        info,h,data,_=fixture()
        with self.assertRaisesRegex(ProtocolError,'Dimensiones'):check_result(info,{**h,'payload':data,'width':320})
        out=io.BytesIO();Image.new('L',(640,480)).save(out,format='JPEG')
        with self.assertRaisesRegex(ProtocolError,'color'):check_result(info,{**h,'payload':out.getvalue()})

    def test_freshness_identity_and_sd(self):
        info,h,data,_=fixture();frame={**h,'payload':data}
        for diff in ({'boot':'0'*16},{'device':'0'*16},{'capture_us':99}):
            with self.assertRaises(ProtocolError):check_result(info,{**frame,**diff},True)
        for status in ('MOUNT_FAILED','SHORT_WRITE','READBACK_MISMATCH','EXISTS_REFUSED'):
            f={**frame,'saved':False,'sd_status':status}
            with self.assertRaisesRegex(ProtocolError,'SD'):check_result(info,f,True)
            self.assertFalse(check_result(info,f,False)['sd_readback_verified_by_device'])

    def test_diagnostics_and_stale_response_ignored(self):
        _,_,_,wire=fixture()
        class Port:
            chunks=[b'Boot diagnostic\n'+control(dict(event='error',id='f'*16,reason='OLD'))+wire]
            def read(self,n):return self.chunks.pop(0) if self.chunks else b''
        msg=receive(Port(),io.BytesIO(),Decoder(),ID,'frame',.1)
        self.assertEqual(msg['id'],ID)

    def test_no_automatic_retry_on_timeout(self):
        class Port:
            def read(self,n):return b''
            def write(self,data):raise AssertionError('No debe reenviar')
        with self.assertRaises(TimeoutError):receive(Port(),io.BytesIO(),Decoder(),ID,'frame',.005)

    def test_download_mode_reports_boot_instead_of_generic_timeout(self):
        class Port:
            def read(self,n):return b'waiting for download\r\n'
            def write(self,data):raise AssertionError('No debe reenviar')
        with self.assertRaisesRegex(ProtocolError,'modo programación'):
            receive(Port(),io.BytesIO(),Decoder(),ID,'info',.1)

    def test_explicit_reset_keeps_old_boot_bytes_and_never_resends_order(self):
        class Port:
            in_waiting=len(b'waiting for download\r\n')
            def read(self,n):return b'waiting for download\r\n'[:n]
            def write(self,data):raise AssertionError('No debe enviar órdenes')
        port=Port();saved=io.BytesIO();delays=[]
        count=restart_before_capture(port,saved,delays.append)
        self.assertEqual(saved.getvalue(),b'waiting for download\r\n')
        self.assertEqual(count,Port.in_waiting);self.assertEqual(delays,[.1,1.5])
        self.assertFalse(port.rts);self.assertFalse(port.dtr)
        class Short(Port):
            def read(self,n):return b'partial'
        saved=io.BytesIO()
        with self.assertRaisesRegex(ProtocolError,'incompleta'):
            restart_before_capture(Short(),saved,delays.append)
        self.assertEqual(saved.getvalue(),b'partial')

if __name__=='__main__':unittest.main()
