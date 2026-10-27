"""ASTRA-39/41: servidor PC identificado, nunca una prueba física de cámara."""
import os
os.environ['QT_QPA_PLATFORM']='offscreen'
import io
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from PIL import Image
from PySide6.QtWidgets import QApplication
from qt_camera_live import CameraLive
from test_camera_stream import part


class LiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app=QApplication.instance() or QApplication([])

    def wait_for(self,predicate,seconds=3):
        until=time.monotonic()+seconds
        while time.monotonic()<until:
            self.app.processEvents()
            if predicate():return
            time.sleep(.01)
        self.fail('No llegó el estado esperado.')

    def test_native_network_image_identity_stale_and_shutdown(self):
        out=io.BytesIO();Image.new('RGB',(320,240),'red').save(out,format='JPEG')
        jpeg=out.getvalue();closed=threading.Event()
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-Type','multipart/x-mixed-replace; boundary=astra-frame')
                self.end_headers()
                data=part(jpeg=jpeg)+part(2,200,jpeg=jpeg)
                try:
                    for start in range(0,len(data),37):
                        self.wfile.write(data[start:start+37]);self.wfile.flush()
                    closed.wait(3)
                except OSError:pass
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        w=CameraLive(lambda n:'camera1')
        try:
            self.assertIsNone(w.reply)
            w.address.setText(f'http://127.0.0.1:{server.server_port}/stream');w.start()
            self.wait_for(lambda:w.received==2)
            self.assertFalse(w.picture.pixmap().isNull())
            self.assertIn('RECIBIENDO IMÁGENES',w.status.text())
            w.received_at-=3;w.refresh()
            self.assertIn('SIN IMAGEN RECIENTE',w.status.text())
            w.stop();self.app.processEvents()
            self.assertIsNone(w.reply);self.assertIn('DESCONECTADA',w.status.text())
        finally:
            w.stop();w.timer.stop();w.close();closed.set();server.shutdown();server.server_close();thread.join()


if __name__=='__main__':unittest.main()
