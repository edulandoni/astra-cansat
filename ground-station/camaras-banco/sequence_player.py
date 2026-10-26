"""ASTRA-39/41: reproducción local con tiempos declarados; nunca captura."""
from bisect import bisect_right
import hashlib
import io
import math
from pathlib import Path
import time
from PIL import Image
from sequence_verify import verify,MAX_JPEG


class Archive:
    def __init__(self,folder,expected_device=None):
        self.root=Path(folder).resolve(strict=True)
        self.report=verify(self.root,expected_device)
        if expected_device and self.report['origin']!='camera':raise ValueError('Esta carpeta es una muestra de PC, no una secuencia de la cámara seleccionada')
        if not self.report['complete']:raise ValueError('Secuencia incompleta o contradictoria: '+ '; '.join(e['reason'] for e in self.report['errors'][:5]))
        self.frames=self.report['frames']
        if not self.frames:raise ValueError('La secuencia no tiene imágenes comprobadas')
        first=self.frames[0]['capture_us']
        self.times=[(f['capture_us']-first)/1e6 for f in self.frames]
        self.duration=self.times[-1]

    def index_at(self,seconds):
        if not math.isfinite(seconds) or seconds<0:raise ValueError('Instante inválido')
        return max(0,min(len(self.times)-1,bisect_right(self.times,seconds)-1))

    def image(self,index):
        frame=self.frames[index];path=self.root/frame['file']
        if path.is_symlink() or path.resolve().parent!=self.root:raise ValueError('La ruta de imagen cambió')
        with path.open('rb') as h:data=h.read(MAX_JPEG+1)
        if len(data)!=frame['bytes'] or hashlib.sha256(data).hexdigest()!=frame['sha256']:raise ValueError('La imagen cambió después de verificarla; detengo la reproducción')
        with Image.open(io.BytesIO(data)) as picture:
            picture.load();return picture.copy()


class Playback:
    def __init__(self,duration,clock=time.monotonic):
        if not math.isfinite(duration) or duration<0:raise ValueError('Duración inválida')
        self.duration=duration;self.clock=clock;self.position=0.;self.started=None

    def elapsed(self):
        return min(self.duration,self.position+(self.clock()-self.started if self.started is not None else 0))

    def play(self):
        if self.elapsed()>=self.duration:self.position=0.;self.started=None
        if self.started is None:self.started=self.clock()

    def pause(self):self.position=self.elapsed();self.started=None
    def rewind(self):self.position=0.;self.started=None


def open_player(parent,folder,expected_device,label):
    # Sólo se llama por acción explícita. La importación no crea ventanas.
    import tkinter as tk
    from tkinter import ttk
    from PIL import ImageTk
    archive=Archive(folder,expected_device)
    window=tk.Toplevel(parent);window.title('ASTRA — Secuencia conservada — '+label)
    window.geometry('760x690');window.minsize(700,620)
    origin='SIMULACIÓN DE PC' if archive.report['origin']=='pc-fixture' else 'ARCHIVOS DE CÁMARA · NO ES EN VIVO'
    ttk.Label(window,text=origin,font=('Segoe UI',13,'bold')).pack(pady=10)
    ttk.Label(window,text='Reproduzco imágenes guardadas con sus tiempos declarados. No envío órdenes ni abro puertos.',wraplength=700).pack(padx=12)
    picture_label=ttk.Label(window);picture_label.pack(pady=10)
    status=tk.StringVar();ttk.Label(window,textvariable=status,wraplength=700).pack(padx=12,pady=5)
    buttons=ttk.Frame(window);buttons.pack(pady=7)
    clock=Playback(archive.duration)
    state=dict(index=None,photo=None,timer=None,closed=False,failed=False)

    def close():
        state['closed']=True
        if state['timer'] is not None:window.after_cancel(state['timer'])
        window.destroy()

    def update():
        if state['closed']:return
        elapsed=clock.elapsed();index=archive.index_at(elapsed)
        if index!=state['index']:
            try:
                state['photo']=ImageTk.PhotoImage(archive.image(index),master=window)
                picture_label.configure(image=state['photo']);state['index']=index
            except (OSError,ValueError) as exc:
                clock.pause();state['failed']=True;status.set(str(exc));return
        end=elapsed>=archive.duration
        if end:clock.pause()
        status.set(f'Cuadro {index+1} de {len(archive.frames)} · instante guardado {archive.times[index]:.3f} s · intervalo primero–último {archive.duration:.3f} s. '+('Fin de secuencia.' if end else 'Tiempos relativos desde la primera imagen.'))
        state['timer']=window.after(40,update)

    def play():
        if not state['failed']:clock.play()
    def rewind():
        if not state['failed']:clock.rewind();state['index']=None
    ttk.Button(buttons,text='Reproducir',command=play).pack(side='left',padx=5)
    ttk.Button(buttons,text='Pausa',command=clock.pause).pack(side='left',padx=5)
    ttk.Button(buttons,text='Volver al inicio',command=rewind).pack(side='left',padx=5)
    ttk.Label(window,text='Sin audio. El último cuadro no tiene duración final declarada. Si la pantalla se demora, puede saltar cuadros al reproducir; los archivos no cambian.',wraplength=700).pack(padx=12,pady=8)
    window.protocol('WM_DELETE_WINDOW',close);update()
    return window
