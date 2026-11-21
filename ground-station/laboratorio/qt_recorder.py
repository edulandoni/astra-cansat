"""ASTRA-39/41: control explícito y progreso reportado; no es lectura independiente de SD."""
import queue
import threading
import time
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QSpinBox,QPushButton
from camera_health import RecordingHealth


class RecorderPanel(QWidget):
    def __init__(self,begin,parent=None,copy=None):
        super().__init__(parent)
        self.begin=begin;self.events=queue.Queue(maxsize=32)
        self.stop_event=threading.Event();self.detach_event=threading.Event()
        self.health=None;self.active=False;self.last=None
        layout=QVBoxLayout(self);layout.addWidget(QLabel('Grabación en microSD · seguimiento USB'))
        note=QLabel('La duración límite se ejecuta en la cámara. Cerrar el seguimiento no detiene la grabación. Wi-Fi debe estar desactivado. No retires la tarjeta ni cortes alimentación mientras graba.')
        note.setWordWrap(True);layout.addWidget(note)
        row=QHBoxLayout();self.unit=QComboBox();self.unit.addItems(['Cámara 1','Cámara 2']);row.addWidget(self.unit)
        self.duration=QSpinBox();self.duration.setRange(1,3600);self.duration.setValue(30);self.duration.setSuffix(' s de duración límite');row.addWidget(self.duration)
        self.start_button=QPushButton('Iniciar grabación');self.start_button.clicked.connect(lambda:self.begin(True,self.unit.currentIndex()+1,self.duration.value()));row.addWidget(self.start_button)
        self.watch_button=QPushButton('Consultar grabación');self.watch_button.clicked.connect(lambda:self.begin(False,self.unit.currentIndex()+1,self.duration.value()));row.addWidget(self.watch_button)
        self.stop_button=QPushButton('Detener y cerrar');self.stop_button.clicked.connect(self.request_stop);self.stop_button.setEnabled(False);row.addWidget(self.stop_button)
        self.detach_button=QPushButton('Cerrar seguimiento USB');self.detach_button.clicked.connect(self.detach_event.set);self.detach_button.setEnabled(False);row.addWidget(self.detach_button)
        layout.addLayout(row)
        self.copy_button=QPushButton('Copiar grabación a PC por USB');self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(lambda:copy(self.unit.currentIndex()+1,self.last) if copy else None);layout.addWidget(self.copy_button)
        self.status=QLabel('SIN CONSULTAR · no hay reporte de grabación');self.status.setWordWrap(True);layout.addWidget(self.status)
        self.timer=QTimer(self);self.timer.timeout.connect(self.refresh);self.timer.start(250)

    def prepare(self,device):
        self.stop_event.clear();self.detach_event.clear();self.health=RecordingHealth(device);self.last=None
        while not self.events.empty():self.events.get_nowait()
        self.active=True;self.set_busy(True);self.status.setText('Solicitando estado de la cámara…')
        self.copy_button.setEnabled(False)

    def set_busy(self,busy):
        for w in [self.unit,self.duration,self.start_button,self.watch_button]:w.setEnabled(not busy)
        self.stop_button.setEnabled(busy);self.detach_button.setEnabled(busy)

    def request_stop(self):
        self.stop_event.set();self.stop_button.setEnabled(False)

    def refresh(self):
        while not self.events.empty():
            event=self.events.get_nowait()
            try:self.health.accept(event['report'],event['received_at']);self.last=event['report']
            except (ValueError,TypeError) as exc:
                self.detach_event.set();self.status.setText('ESTADO DESCONOCIDO · '+str(exc));return
        if not self.active or not self.health:return
        states={'UNKNOWN':'ESTADO DESCONOCIDO','START_UNCONFIRMED':'INICIO SIN GUARDADO CONFIRMADO','PROGRESS_UNCONFIRMED':'ESPERANDO PROGRESO','WRITING_REPORTED':'GUARDADO EN PROGRESO · REPORTADO','WRITE_STALLED':'ESCRITURA SIN PROGRESO RECIENTE','ERROR':'ERROR REPORTADO','NOT_RECORDING':'GRABACIÓN DETENIDA · REPORTADA'}
        code=self.health.view(time.monotonic());r=self.last or {}
        age=max(0,(r.get('uptime_ms',0)-r.get('last_write_ms',0))/1000+time.monotonic()-(self.health.received_at or time.monotonic()))
        self.status.setText(states[code]+f"\nCuadros capturados: {r.get('frames_captured',0)} · guardados y leídos por cámara: {r.get('frames_written',0)} · bytes: {r.get('bytes_written',0)} · segmentos cerrados: {r.get('segments_closed',0)}\nÚltima escritura hace {age:.1f} s según reporte y tiempo transcurrido · espacio libre reportado: {r.get('free_bytes',0)/1048576:.1f} MiB\nLa comprobación independiente de archivos se realiza desde el lector.")

    def finished(self,result):
        self.refresh();self.active=False;self.set_busy(False)
        state=result['state'];r=result.get('last') or {}
        text={'COMPLETE':'GRABACIÓN CERRADA · REPORTADA','FAILED':'GRABACIÓN FALLIDA · REPORTADA','IDLE':'SIN GRABACIÓN INICIADA','DETACHED':'SEGUIMIENTO CERRADO · la cámara podría continuar hasta su límite','UNKNOWN':'ESTADO DESCONOCIDO · no puedo confirmar cierre','REJECTED':'ORDEN RECHAZADA · consultá el estado de la grabación'}.get(state,state)
        self.status.setText(text+f"\nCuadros guardados reportados: {r.get('frames_written',0)} · segmentos cerrados: {r.get('segments_closed',0)}\n"+str(result.get('error') or r.get('error') or r.get('reason') or '')+'\nFalta lectura independiente de la SD.')
        self.last=r;self.copy_button.setEnabled(state=='COMPLETE')
