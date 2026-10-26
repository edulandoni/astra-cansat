"""ASTRA-41/22: origen explícito; USB nunca se sustituye por simulación."""
import threading
from pathlib import Path
from runtime import Engine, Store
from sources import PCBench, serial_loop, replay_loop
from ui_model import presentation


class Source:
    def __init__(self,output,mode,port=None,scenario='NOMINAL',speed=1,replay=None):
        if mode not in ('usb','pc','replay'):raise ValueError('Elegir placa, simulación o grabación')
        if mode=='usb' and not port:raise ValueError('Seleccioná explícitamente el puerto de la placa')
        if mode=='replay' and (not replay or not Path(replay).is_file()):raise ValueError('Elegí un registro existente')
        if speed not in (1,5,10):raise ValueError('Velocidad no admitida')
        self.mode=mode;self.port=port;self.error='';self.stopping=False;self.closed=False
        self.store=Store(output)
        self.engine=Engine(self.store,source={'usb':'USB_BENCH','pc':'PC_BENCH','replay':'REPLAY'}[mode])
        def work():
            try:
                if mode=='usb':serial_loop(self.engine,port,reset_once=False)
                elif mode=='replay':replay_loop(self.engine,replay,speed)
                else:PCBench(self.engine).run_loop(1/speed)
            except Exception as exc:
                self.error=str(exc);self.engine.disconnected(self.error)
        self.worker=threading.Thread(target=work,daemon=True);self.worker.start()
        if mode=='pc':self.engine.command('RUN',scenario=scenario,samples=131)

    def stop(self):
        if self.stopping or self.closed:return
        self.stopping=True;self.engine.stop.set()
        def finish():
            try:
                self.worker.join(3)
                if self.worker.is_alive():
                    # Espero su salida antes de cerrar los archivos que utiliza.
                    self.worker.join()
                self.store.close()
            except Exception as exc:self.error=str(exc)
            finally:self.closed=True
        self.closer=threading.Thread(target=finish,daemon=True);self.closer.start()


def source_view(source):
    if source is None:return dict(mode='idle',badge='SIN FUENTE DE DATOS',title='Sin fuente seleccionada',
        detail='Adquisición detenida. Selección disponible: USB, simulación PC o reproducción.',
        old=True,values={},snapshot=None,gaps='—',age='—')
    s=source.engine.snapshot();p=presentation(s)
    age=s.get('last_sample_age');age_text='sin muestras' if age is None else f'{age:.1f} s'
    has_data=bool(s.get('latest'));connected=s.get('transport_connected',False)
    old=not has_data or not connected or source.closed or bool(s.get('paused') or s.get('done') or s.get('ambiguous') or s.get('waiting_identity')) or (age is not None and age>3)
    if source.mode=='usb':
        badge='ESP32 POR USB · DATOS DE BANCO'
        if source.closed:title='Conexión cerrada'
        elif not connected:title='Placa desconectada' if s.get('ever_connected') else 'Esperando conexión con la placa'
        elif s.get('waiting_identity') or s.get('ambiguous'):title='Puerto abierto · verificando el emisor'
        elif not has_data:title='Puerto abierto · esperando mediciones'
        elif s.get('done') or s.get('paused'):title='La placa dejó de emitir este ensayo'
        elif old:title='Conectada · sin mediciones nuevas'
        else:title='Recibiendo desde el ESP32'
        detail='Estos datos llegan por el cable USB. El firmware de banco genera valores ficticios; no son sensores de vuelo.'
        if not connected:detail='Sin la placa no entran mediciones nuevas. Los valores conservados se muestran como históricos. No activo una simulación de reemplazo.'
    elif source.mode=='pc':
        badge='SIMULACIÓN EN LA PC · SIN PLACA'
        title='Simulación terminada' if source.closed or s.get('done') else 'Simulación de telemetría'
        detail='Origen: emisor sintético de PC. Estos datos no provienen del ESP32.'
    else:
        badge='REPRODUCCIÓN · ARCHIVO GUARDADO'
        title='Fin de la grabación' if not source.worker.is_alive() else 'Reproduciendo una prueba guardada'
        detail='Leemos una captura anterior. No estamos recibiendo datos nuevos ni enviando órdenes a una placa.'
        old=not source.worker.is_alive()
    if source.stopping and not source.closed:title='Conservando registros y cerrando…'
    if source.error:detail+=' '+source.error
    return dict(mode=source.mode,badge=badge,title=title,detail=detail,old=old,values=p['values'],snapshot=s,
                gaps=p['gap_value'],age=age_text)
