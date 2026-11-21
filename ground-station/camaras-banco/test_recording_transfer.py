import json,tempfile,unittest,zlib
from pathlib import Path
from recording_transfer import FileReader,download_recording
from test_recording_verify import setup,DEVICE


class Port:
    def __init__(self,root,corrupt=False,wrong=False):self.root=root;self.corrupt=corrupt;self.wrong=wrong;self.buffer=bytearray();self.sent=[]
    def write(self,data):
        self.sent.append(data);cmd,ident,*args=data.decode().split();boot='a'*16
        if cmd=='INFO':self.buffer+=b'@CAM '+json.dumps(dict(v=1,event='info',id=ident,profile='camera-usb-0.1',camera_ready=True,device=DEVICE,boot=boot,commands=['REC_READ'])).encode()+b'\n';return
        _,origin,run,kind,segment,index=args;segment=int(segment);index=int(index)
        if kind in ('S','R'):p=self.root/('session-start.json' if kind=='S' else 'session-result.json')
        else:p=self.root/f'segment_{segment:04}'/('sequence.json' if kind=='M' else f'frame_{index:04}.'+('jpg' if kind=='J' else 'json'))
        payload=p.read_bytes();crc=f'{zlib.crc32(payload)&0xffffffff:08x}'
        header=dict(v=1,event='file',id=ident,boot=boot,device='2'*16 if self.wrong else DEVICE,length=len(payload),crc32='00000000' if self.corrupt else crc)
        end=dict(v=1,event='file_end',id=ident,boot=boot,sent=len(payload))
        self.buffer+=b'@CAM '+json.dumps(header).encode()+b'\n'+payload+b'\n@CAM '+json.dumps(end).encode()+b'\n'
    def flush(self):pass
    def read(self,n):
        data=bytes(self.buffer[:min(n,37)]);del self.buffer[:len(data)];return data


class TransferTests(unittest.TestCase):
    def test_full_fragmented_copy_verifies_and_does_not_change_source(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'card';source.mkdir();setup(source)
            before={p.relative_to(source):p.read_bytes() for p in source.rglob('*') if p.is_file()}
            reader=FileReader(Port(source),DEVICE,'0123456789abcdef','b'*16);reader.identify()
            progress=[]
            result=download_recording(reader,Path(folder)/'copy',progress=progress.append)
            self.assertEqual([x['segment'] for x in progress],[1,2])
            self.assertTrue(result['complete']);self.assertFalse(result['independent_reader'])
            self.assertEqual(result['verification']['checked_frames'],8)
            self.assertEqual(before,{p.relative_to(source):p.read_bytes() for p in source.rglob('*') if p.is_file()})

    def test_crc_error_keeps_partial_and_does_not_retry(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder);source=p/'card';source.mkdir();setup(source);port=Port(source,corrupt=True)
            reader=FileReader(port,DEVICE,'0123456789abcdef','b'*16);reader.identify()
            with self.assertRaises(ValueError):reader.fetch('S',0,0,p/'partial.json')
            self.assertTrue((p/'partial.json').exists());self.assertEqual(len(port.sent),2)

    def test_identity_size_budget_and_selector(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder);source=p/'card';source.mkdir();setup(source)
            reader=FileReader(Port(source,wrong=True),DEVICE,'0123456789abcdef','b'*16);reader.identify()
            with self.assertRaises(ValueError):reader.fetch('S',0,0,p/'bad.json')
            self.assertFalse((p/'bad.json').exists())
            reader=FileReader(Port(source),DEVICE,'0123456789abcdef','b'*16);reader.identify()
            with self.assertRaises(ValueError):reader.fetch('SR',0,0,p/'bad.json')
            with self.assertRaises(ValueError):reader.fetch('S',0,0,p/'bad.json',max_total=1)

    def test_sensor_failure_does_not_prevent_reading_existing_sd_files(self):
        class SensorFailed(Port):
            def write(self,data):
                super().write(data)
                if data.startswith(b'INFO '):self.buffer=self.buffer.replace(b'"camera_ready": true',b'"camera_ready": false')
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder);source=p/'card';source.mkdir();setup(source)
            reader=FileReader(SensorFailed(source),DEVICE,'0123456789abcdef','b'*16);reader.identify()
            reader.fetch('S',0,0,p/'start.json')
            self.assertTrue((p/'start.json').exists())

    def test_cancel_preserves_partial_copy_and_card(self):
        import threading
        class CancelOnHeader(FileReader):
            def message(self,ident,event,until):
                value=super().message(ident,event,until)
                if event=='file':self.cancel.set()
                return value
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder);source=p/'card';source.mkdir();setup(source)
            original=(source/'session-start.json').read_bytes()
            reader=CancelOnHeader(Port(source),DEVICE,'0123456789abcdef','b'*16,cancel=threading.Event());reader.identify()
            with self.assertRaises(InterruptedError):reader.fetch('S',0,0,p/'partial.json')
            self.assertTrue((p/'partial.json').exists());self.assertEqual((source/'session-start.json').read_bytes(),original)


if __name__=='__main__':unittest.main()
