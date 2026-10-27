"""ASTRA-39: copia SD→USB→PC, sin borrar, sobrescribir o pedir extracción de tarjeta."""
import hashlib,json,re,secrets,time,zlib
from pathlib import Path
from camera_check import validate_peer


class FileReader:
    def __init__(self,port,device,origin_boot,run,clock=time.monotonic,cancel=None):
        for value in (device,origin_boot,run):
            if not re.fullmatch('[a-f0-9]{16}',value):raise ValueError('Identificadores de lectura inválidos.')
        self.port,self.device,self.origin,self.run,self.clock=port,device,origin_boot,run,clock
        self.buffer=bytearray();self.boot=None;self.files=[];self.total=0
        self.cancel=cancel

    def check_cancel(self):
        if self.cancel and self.cancel.is_set():raise InterruptedError('Copia cancelada; originales y archivos parciales conservados.')

    def line(self,until):
        while self.clock()<until:
            self.check_cancel()
            if b'\n' in self.buffer:
                line,_,rest=self.buffer.partition(b'\n');self.buffer=bytearray(rest)
                if len(line)>4096:raise ValueError('Cabecera de archivo excesiva.')
                return bytes(line)
            if len(self.buffer)>4096:raise ValueError('Cabecera incompleta excesiva.')
            data=self.port.read(512)
            if data:self.buffer.extend(data)
        raise TimeoutError('Sin respuesta de archivo; no reintento ni descarto la copia parcial.')

    def message(self,ident,event,until):
        while self.clock()<until:
            line=self.line(until)
            if b'waiting for download' in line:raise ValueError('La cámara está en modo programación.')
            if not line.startswith(b'@CAM '):continue
            obj=json.loads(line[5:])
            if not isinstance(obj,dict) or obj.get('v')!=1:raise ValueError('Control inválido.')
            if obj.get('id')!=ident:continue
            if self.boot and obj.get('boot')!=self.boot:raise ValueError('Cambió el arranque durante la transferencia.')
            if obj.get('event')=='error':raise ValueError('Lectura rechazada: '+str(obj.get('reason')))
            if obj.get('event')!=event:raise ValueError('Control de archivo incompatible.')
            return obj
        raise TimeoutError('Sin control de archivo.')

    def identify(self):
        ident=secrets.token_hex(8);self.port.write(f'INFO {ident}\n'.encode());self.port.flush()
        info=self.message(ident,'info',self.clock()+10);validate_peer(info,self.device,require_ready=False)
        if 'REC_READ' not in info.get('commands',[]):raise ValueError('El firmware no anuncia lectura de grabaciones.')
        if not re.fullmatch('[a-f0-9]{16}',info.get('boot','')):raise ValueError('Arranque inválido.')
        self.boot=info['boot']

    def fetch(self,kind,segment,index,destination,max_total=512*1024*1024):
        if kind not in ('S','R','M','J','I') or type(segment) is not int or type(index) is not int or not 0<=segment<=600 or not 0<=index<=60:
            raise ValueError('Selector de archivo inválido.')
        if (kind in ('S','R') and (segment or index)) or (kind not in ('S','R') and not segment) or (kind=='M' and index) or (kind in ('J','I') and not index):
            raise ValueError('Índice incompatible con el archivo pedido.')
        ident=secrets.token_hex(8)
        self.port.write(f'REC_READ {ident} {self.boot} {self.origin} {self.run} {kind} {segment} {index}\n'.encode());self.port.flush()
        header=self.message(ident,'file',self.clock()+10)
        length=header.get('length');crc=header.get('crc32')
        if header.get('device')!=self.device or type(length) is not int or not 1<=length<=(512*1024 if kind=='J' else 128*1024) or not re.fullmatch('[a-f0-9]{8}',str(crc)):
            raise ValueError('Identidad, longitud o CRC de archivo inválidos.')
        if self.total+length>max_total:raise ValueError('La copia supera el límite configurado; conservo lo recibido.')
        target=Path(destination);digest=hashlib.sha256();sum_crc=0;count=0;until=self.clock()+length/8000+10
        with target.open('xb') as out:
            while count<length and self.clock()<until:
                self.check_cancel()
                if not self.buffer:
                    block=self.port.read(min(4096,length-count))
                    if not block:continue
                    self.buffer.extend(block)
                n=min(length-count,len(self.buffer));block=bytes(self.buffer[:n]);del self.buffer[:n]
                out.write(block);digest.update(block);sum_crc=zlib.crc32(block,sum_crc);count+=n
        if count!=length or f'{sum_crc&0xffffffff:08x}'!=crc:raise ValueError('Copia incompleta o CRC diferente; archivo parcial conservado.')
        end=self.message(ident,'file_end',self.clock()+5)
        if end.get('sent')!=length:raise ValueError('Cierre de transferencia incompatible.')
        self.total+=length;self.files.append(dict(file=str(target),bytes=length,sha256=digest.hexdigest(),crc32=crc))
        return target


def download_recording(reader,destination,progress=None):
    root=Path(destination);root.mkdir(parents=True,exist_ok=False)
    result=dict(complete=False,source='camera-sd-over-usb',independent_reader=False)
    try:
        for kind,name in [('S','session-start.json'),('R','session-result.json')]:reader.fetch(kind,0,0,root/name)
        start=json.loads((root/'session-start.json').read_text());end=json.loads((root/'session-result.json').read_text())
        for obj in [start,end]:
            if obj.get('device')!=reader.device or obj.get('boot')!=reader.origin or obj.get('run')!=reader.run or obj.get('profile')!='camera-recording-0.1':raise ValueError('Metadatos de otra grabación.')
        n=end.get('segments_closed')
        if type(n) is not int or not 1<=n<=600:raise ValueError('Cantidad de segmentos inválida.')
        for segment in range(1,n+1):
            folder=root/f'segment_{segment:04}';folder.mkdir()
            reader.fetch('M',segment,0,folder/'sequence.json');meta=json.loads((folder/'sequence.json').read_text())
            frames=meta.get('frames')
            if not isinstance(frames,list) or not 1<=len(frames)<=60:raise ValueError('Índice de segmento inválido.')
            for index,frame in enumerate(frames,1):
                if frame.get('index')!=index or frame.get('file')!=f'frame_{index:04}.jpg':raise ValueError('Nombres o índices no consecutivos.')
                reader.fetch('J',segment,index,folder/frame['file'])
                reader.fetch('I',segment,index,folder/f'frame_{index:04}.json')
                if progress and index%20==0:progress(dict(segment=segment,segments=n,frames_in_segment=index,bytes_received=reader.total))
            if progress:progress(dict(segment=segment,segments=n,bytes_received=reader.total))
        from recording_verify import verify_recording
        report=verify_recording(root,reader.device)
        result.update(complete=report['complete'],verification=report,files=reader.files,bytes_received=reader.total)
        return result
    except Exception as exc:
        result.update(error=str(exc),files=reader.files,bytes_received=reader.total);raise
    finally:
        (root/'usb-copy-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')


def copy_from_camera(port_name,device,origin_boot,run,output,cancel=None):
    from datetime import datetime,timezone
    import serial
    destination=Path(output)/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_')+secrets.token_hex(4))/f'ASTRA_REC_{origin_boot}_{run}'
    try:
        port=serial.Serial(port=None,baudrate=115200,timeout=.2,write_timeout=3)
        port.dtr=False;port.rts=False;port.port=port_name
        with port:
            reader=FileReader(port,device,origin_boot,run,cancel=cancel);reader.identify()
            result=download_recording(reader,destination)
        return dict(result,folder=str(destination))
    except Exception as exc:return dict(complete=False,error=str(exc),folder=str(destination),independent_reader=False)
