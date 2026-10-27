"""ASTRA-39/41: vista previa Qt explícita; no activa radio ni declara SD verificada."""
import time
from PySide6.QtCore import QByteArray, QBuffer, QIODevice, Qt, QTimer, QUrl
from PySide6.QtGui import QImageReader, QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkProxy
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from camera_stream import StreamParser, stream_url


class CameraLive(QWidget):
    def __init__(self, identity_for, parent=None, control=None):
        super().__init__(parent)
        self.identity_for = identity_for
        self.network = QNetworkAccessManager(self)
        self.network.setProxy(QNetworkProxy(QNetworkProxy.NoProxy))
        self.reply = None
        self.parser = None
        self.received_at = None
        self.received = 0
        self.started = None
        self.detail = ''
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Vista previa Wi-Fi · mantenimiento local'))
        explanation = QLabel('La PC debe estar conectada a la red de mantenimiento de la cámara. La conexión es manual y no inicia grabación. La imagen no confirma escritura en SD.')
        explanation.setWordWrap(True)
        layout.addWidget(explanation)
        power = QHBoxLayout()
        for enabled, text in [(True,'Activar Wi-Fi por USB'),(False,'Desactivar Wi-Fi por USB')]:
            action = QPushButton(text)
            action.setEnabled(control is not None)
            action.clicked.connect(lambda checked=False,on=enabled:control(on,self.unit.currentIndex()+1))
            power.addWidget(action)
        layout.addLayout(power)
        row = QHBoxLayout()
        self.unit = QComboBox()
        self.unit.addItems(['Cámara 1', 'Cámara 2'])
        row.addWidget(self.unit)
        self.address = QLineEdit('http://192.168.4.1:81/stream')
        row.addWidget(self.address)
        self.connect_button = QPushButton('Conectar vista previa')
        self.connect_button.clicked.connect(self.start)
        row.addWidget(self.connect_button)
        stop = QPushButton('Desconectar vista previa')
        stop.clicked.connect(self.stop)
        row.addWidget(stop)
        layout.addLayout(row)
        self.picture = QLabel('Sin imagen de la red')
        self.picture.setAlignment(Qt.AlignCenter)
        self.picture.setMinimumHeight(240)
        layout.addWidget(self.picture)
        self.status = QLabel('DESCONECTADA · no se abrió ninguna conexión')
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(250)

    def start(self):
        self.stop()
        try:
            url = stream_url(self.address.text())
            identity = self.identity_for(self.unit.currentIndex() + 1)
            self.parser = StreamParser(identity)
        except (ValueError, KeyError, OSError) as exc:
            self.detail = str(exc)
            self.refresh()
            return
        self.received_at = None
        self.received = 0
        self.started = time.monotonic()
        self.detail = 'Esperando una imagen nueva e identidad válida'
        request = QNetworkRequest(QUrl(url))
        request.setAttribute(QNetworkRequest.RedirectPolicyAttribute, QNetworkRequest.ManualRedirectPolicy)
        request.setAttribute(QNetworkRequest.CacheLoadControlAttribute, QNetworkRequest.AlwaysNetwork)
        request.setTransferTimeout(5000)
        reply = self.network.get(request)
        reply.setReadBufferSize(128 * 1024)
        self.reply = reply
        reply.readyRead.connect(lambda: self.consume(reply))
        reply.finished.connect(lambda: self.finished(reply))
        self.connect_button.setEnabled(False)
        self.unit.setEnabled(False)
        self.address.setEnabled(False)
        self.refresh()

    def consume(self, reply):
        if reply is not self.reply:
            return
        try:
            if reply.attribute(QNetworkRequest.HttpStatusCodeAttribute) != 200:
                raise ValueError('La cámara no respondió HTTP 200; no sigo redirecciones.')
            if bytes(reply.rawHeader('Content-Type')).split(b';')[0].strip().lower() != b'multipart/x-mixed-replace':
                raise ValueError('La respuesta no es un flujo de cámara compatible.')
            latest = None
            while reply.bytesAvailable():
                for meta, jpeg in self.parser.feed(bytes(reply.read(65536))):
                    data = QByteArray(jpeg)
                    source = QBuffer(data)
                    source.open(QIODevice.ReadOnly)
                    reader = QImageReader(source, b'JPEG')
                    size = reader.size()
                    if not (0 < size.width() <= 1600 and 0 < size.height() <= 1200):
                        raise ValueError('Dimensiones de imagen fuera de límites.')
                    image = reader.read()
                    if image.isNull():
                        raise ValueError('La imagen recibida no se puede decodificar.')
                    latest = image
                    self.received += 1
                    self.received_at = time.monotonic()
            if latest is not None:
                self.picture.setPixmap(QPixmap.fromImage(latest).scaled(640, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.detail = 'Imagen recibida y decodificada · grabación en SD no supervisada por este visor'
            self.refresh()
        except Exception as exc:
            self.stop(str(exc))

    def finished(self, reply):
        if reply is self.reply:
            self.stop('Conexión terminada: ' + reply.errorString())

    def stop(self, reason='Vista previa desconectada; la imagen conservada no es actual'):
        reply, self.reply = self.reply, None
        if reply is not None:
            reply.abort()
            reply.deleteLater()
        self.detail = reason
        self.connect_button.setEnabled(True)
        self.unit.setEnabled(True)
        self.address.setEnabled(True)
        self.refresh()

    def refresh(self):
        now = time.monotonic()
        age = None if self.received_at is None else now - self.received_at
        live = self.reply is not None and age is not None and age <= 2
        state = 'RECIBIENDO IMÁGENES' if live else ('SIN IMAGEN RECIENTE' if self.reply is not None else 'DESCONECTADA')
        stats = f' · última imagen recibida hace {age:.1f} s' if age is not None else ''
        if self.started and self.received:
            stats += f' · {self.received / max(now-self.started, .001):.1f} cuadros/s promedio recibido'
        self.status.setText(state + stats + '\n' + self.detail)
        self.status.setStyleSheet('color: #246B4A;' if live else 'color: #925017;')
