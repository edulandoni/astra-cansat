"""ASTRA-39/41: fragmentación, identidad y ausencia de falsas imágenes nuevas."""
import unittest
from camera_stream import StreamParser, stream_url


def part(index=1, stamp=100, device='camera1', boot='a'*16, jpeg=b'\xff\xd8test\xff\xd9'):
    return (f'--astra-frame\r\nContent-Type: image/jpeg\r\nContent-Length: {len(jpeg)}\r\nX-Device: {device}\r\nX-Boot: {boot}\r\nX-Frame-Id: {index}\r\nX-Capture-Us: {stamp}\r\n\r\n'.encode()+jpeg+b'\r\n')


class StreamTests(unittest.TestCase):
    def test_fragmented_and_burst(self):
        data=part()+part(4,400)
        for width in [1,3,17,4096]:
            p=StreamParser('camera1');out=[]
            for n in range(0,len(data),width):out+=p.feed(data[n:n+width])
            self.assertEqual([f[0]['index'] for f in out],[1,4])
            self.assertEqual(p.skipped,2)

    def test_duplicate_does_not_refresh_image(self):
        p=StreamParser('camera1');self.assertEqual(len(p.feed(part())),1)
        self.assertEqual(p.feed(part()),[]);self.assertEqual(p.duplicates,1)

    def test_conflicts_and_reset_rejected(self):
        for message in [part(stamp=101),part(2,99),part(2,200,boot='b'*16),part(device='camera2')]:
            p=StreamParser('camera1');p.feed(part())
            with self.assertRaises(ValueError):p.feed(message)

    def test_corrupt_truncated_and_excessive(self):
        for data in [part(jpeg=b'notjpeg'),part().replace(b'Content-Length: 8',b'Content-Length: 999999'),b'x'*4097]:
            with self.assertRaises(ValueError):StreamParser('camera1').feed(data)
        p=StreamParser('camera1');self.assertEqual(p.feed(part()[:-5]),[])
        self.assertLess(len(p.buffer),p.MAX_FRAME)

    def test_only_explicit_local_url(self):
        self.assertEqual(stream_url('http://192.168.4.1:81/stream'),'http://192.168.4.1:81/stream')
        for url in ['https://192.168.4.1/stream','http://example.com/stream','http://8.8.8.8/stream','http://u:p@192.168.4.1/stream','http://192.168.4.1/stream?password=x','http://224.0.0.1/stream']:
            with self.assertRaises(ValueError):stream_url(url)


if __name__=='__main__':unittest.main()
