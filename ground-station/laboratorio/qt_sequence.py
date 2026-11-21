"""ASTRA-39/41: visor Qt del archivo validado; no captura ni abre USB."""
import sys
from PySide6.QtCore import Qt,QTimer,QUrl
from PySide6.QtGui import QImage,QPixmap,QDesktopServices
from PySide6.QtWidgets import QDialog,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QFileDialog
from runtime import AREA
sys.path.insert(0,str(AREA/'camaras-banco'))
from sequence_player import Archive,Playback


class SequenceDialog(QDialog):
    def __init__(self,parent,folder,expected_device=None,title='Secuencia conservada'):
        super().__init__(parent);self.archive=Archive(folder,expected_device);self.clock=Playback(self.archive.duration)
        self.index=None;self.failed=False;self.expected_device=expected_device;self.exporting=False;self.close_pending=False;self.exported=None
        self.setWindowTitle('ASTRA · '+title);self.resize(780,760)
        layout=QVBoxLayout(self);origin='MUESTRA DE PC' if self.archive.report['origin']=='pc-fixture' else 'ARCHIVOS DE CÁMARA · NO ES EN VIVO'
        layout.addWidget(QLabel(origin));self.picture=QLabel();self.picture.setAlignment(Qt.AlignCenter);layout.addWidget(self.picture)
        self.status=QLabel();self.status.setWordWrap(True);layout.addWidget(self.status)
        actions=QHBoxLayout();self.buttons=[]
        for label,fn in [('Reproducir',self.clock.play),('Pausa',self.clock.pause),('Inicio',self.clock.rewind)]:
            b=QPushButton(label);b.clicked.connect(fn);actions.addWidget(b);self.buttons.append(b)
        layout.addLayout(actions)
        exports=QHBoxLayout();self.export_button=QPushButton('Exportar MP4…');self.export_button.setEnabled(hasattr(parent,'submit'));self.export_button.clicked.connect(self.choose_export);exports.addWidget(self.export_button)
        self.open_export=QPushButton('Abrir MP4');self.open_export.setEnabled(False);self.open_export.clicked.connect(lambda:QDesktopServices.openUrl(QUrl.fromLocalFile(self.exported)));exports.addWidget(self.open_export);layout.addLayout(exports)
        self.export_status=QLabel('MP4 derivado con tiempos conservados, sin interpolación ni audio. Los JPEG originales permanecen intactos.');self.export_status.setWordWrap(True);layout.addWidget(self.export_status)
        note=QLabel('Sin audio. Los tiempos son relativos al primer cuadro; no declaran duración final del último. Si la pantalla demora puede omitir cuadros al mostrar, conservando los archivos.');note.setWordWrap(True);layout.addWidget(note)
        self.timer=QTimer(self);self.timer.timeout.connect(self.refresh);self.timer.start(40);self.refresh()

    def refresh(self):
        if self.failed:return
        elapsed=self.clock.elapsed();index=self.archive.index_at(elapsed)
        try:
            if index!=self.index:
                image=self.archive.image(index).convert('RGB');data=image.tobytes()
                qim=QImage(data,image.width,image.height,image.width*3,QImage.Format_RGB888).copy()
                self.picture.setPixmap(QPixmap.fromImage(qim));self.index=index
            self.status.setText(f'Cuadro {index+1} de {len(self.archive.frames)} · instante {self.archive.times[index]:.3f} s · primero–último {self.archive.duration:.3f} s')
            if elapsed>=self.archive.duration:self.clock.pause()
        except (OSError,ValueError) as exc:
            self.failed=True;self.clock.pause();self.status.setText('Reproducción detenida: '+str(exc));self.timer.stop()
            for b in self.buttons:b.setEnabled(False)

    def choose_export(self):
        output=QFileDialog.getExistingDirectory(self,'Destino del MP4 · crea una carpeta nueva')
        if output:self.start_export(output)

    def start_export(self,output):
        if self.exporting:return
        from sequence_video import export_video
        self.exporting=True;self.export_button.setEnabled(False);self.export_status.setText('Exportando y volviendo a decodificar el MP4 para comprobar cuadros y tiempos…')
        def work():
            try:return export_video(self.archive.root,self.expected_device,output)
            except Exception as exc:return dict(state='failed',error=str(exc))
        def done(result):
            self.exporting=False;self.export_button.setEnabled(True)
            if result['state']=='verified':
                self.exported=result['video'];self.open_export.setEnabled(True)
                self.export_status.setText(f"MP4 verificado · {result['frames']} cuadros · tramo {result['first_to_last_seconds']:.3f} s · error temporal máximo {result['max_timestamp_error_us']} µs.\n{self.exported}")
            else:self.export_status.setText('No pude verificar el MP4: '+result['error'])
            if self.close_pending:self.close()
        self.parent().submit(work,'video',done)

    def closeEvent(self,event):
        if self.exporting:self.close_pending=True;self.export_status.setText('Espero el cierre y verificación del MP4 antes de salir…');event.ignore();return
        self.timer.stop();event.accept()
