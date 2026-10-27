import io
import json
import unittest
from preview_control import exchange


class Port:
    def __init__(self,device='a'*16,capable=True,change_boot=False):
        self.device=device;self.capable=capable;self.change_boot=change_boot
        self.lines=[];self.sent=[]
    def write(self,data):
        self.sent.append(data);verb,ident,*rest=data.decode().split()
        info=dict(event='info',profile='camera-usb-0.1',camera_ready=True,device=self.device,boot='b'*16,commands=['WIFI_ON','WIFI_OFF'] if self.capable else [])
        result=info if verb=='INFO' else dict(event='wifi_ready' if verb=='WIFI_ON' else 'wifi_off',boot=('c' if self.change_boot else 'b')*16)
        self.lines.append(b'@CAM '+json.dumps(dict(result,id=ident)).encode()+b'\n')
    def flush(self):pass
    def read_until(self,*args):return self.lines.pop(0)


class ControlTests(unittest.TestCase):
    def test_identity_and_capability_before_activation(self):
        for port in [Port(device='d'*16),Port(capable=False)]:
            with self.assertRaises(ValueError):exchange(port,'WIFI_ON','a'*16,'1'*16)
            self.assertEqual(len(port.sent),1)
    def test_activation_and_stop(self):
        port=Port();self.assertEqual(exchange(port,'WIFI_ON','a'*16,'1'*16)['event'],'wifi_ready')
        self.assertEqual(len(port.sent),2)
        port=Port();self.assertEqual(exchange(port,'WIFI_OFF','a'*16)['event'],'wifi_off')
    def test_reset_and_bad_key_not_retried(self):
        port=Port(change_boot=True)
        with self.assertRaises(ValueError):exchange(port,'WIFI_ON','a'*16,'1'*16)
        self.assertEqual(len(port.sent),2)
        port=Port()
        with self.assertRaises(ValueError):exchange(port,'WIFI_ON','a'*16,'short')
        self.assertEqual(port.sent,[])


if __name__=='__main__':unittest.main()
