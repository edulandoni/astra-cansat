"""ASTRA-39/41: visor Qt del archivo validado; no captura ni abre USB."""
import sys
from PySide6.QtCore import Qt,QTimer
from PySide6.QtGui import QImage,QPixmap
from PySide6.QtWidgets import QDialog,QVBoxLayout,QHBoxLayout,QLabel,QPushButton
from runtime import AREA
sys.path.insert(0,str(AREA/'camaras-banco'))
from sequence_player import Archive,Playback


class SequenceDialog(QDialog):
    def __init__(self,parent,folder,expected_device=None,title='Secuencia conservada'):
        super().__init__(parent);self.archive=Archive(folder,expected_device);self.clock=Playback(self.archive.duration)
        self.index=None;self.failed=False;self.setWindowTitle('ASTRA · '+title);self.resize(780,680)
        layout=QVBoxLayout(self);origin='MUESTRA DE PC' if self.archive.report['origin']=='pc-fixture' else 'ARCHIVOS DE CÁMARA · NO ES EN VIVO'
        layout.addWidget(QLabel(origin));self.picture=QLabel();self.picture.setAlignment(Qt.AlignCenter);layout.addWidget(self.picture)
        self.status=QLabel();self.status.setWordWrap(True);layout.addWidget(self.status)
        actions=QHBoxLayout();self.buttons=[]
        for label,fn in [('Reproducir',self.clock.play),('Pausa',self.clock.pause),('Inicio',self.clock.rewind)]:
            b=QPushButton(label);b.clicked.connect(fn);actions.addWidget(b);self.buttons.append(b)
        layout.addLayout(actions)
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

    def closeEvent(self,event):self.timer.stop();event.accept()
