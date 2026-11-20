"""ASTRA operator console. Reuses the validated bench acquisition engine."""
import argparse
import os
import queue
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'laboratorio'))
from qt_model import Source, source_view
from telemetry_workspace import SeriesPlot, TelemetryWorkspace, text
from engine import display
from serial.tools.list_ports import comports
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QFrame, QHBoxLayout, QMainWindow,
    QMessageBox, QPushButton, QTabWidget, QVBoxLayout, QWidget,
)


def configure_font(app):
    fonts = Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts'
    for name in ('segoeui.ttf', 'segoeuib.ttf'):
        if (fonts / name).is_file():
            QFontDatabase.addApplicationFont(str(fonts / name))
    if 'Segoe UI' in QFontDatabase.families():
        app.setFont(QFont('Segoe UI', 10))


class Station(QMainWindow):
    def __init__(self, output):
        super().__init__()
        self.source = None
        self.output = Path(output)
        self.backup_path = None
        self.setWindowTitle('ASTRA | Estación de tierra')
        self.resize(1360, 850)
        self.setStyleSheet("""
            QMainWindow, QWidget#shell {background:#edf2f6;color:#172c43}
            QLabel {color:#172c43;font-size:15px}
            QFrame#mast {background:#102b43;border-radius:8px}
            QLabel#brand {color:white;font-size:27px;font-weight:700}
            QLabel#signal {color:#acf2e5;font-weight:700;font-size:16px}
            QLabel#metric {color:#0e574f;font-size:24px;font-weight:700}
            QFrame#card {background:white;border:1px solid #d0dce5;border-radius:7px}
            QPushButton {padding:8px 13px;background:white;border:1px solid #a8bbc9;border-radius:4px}
            QPushButton:disabled {color:#6c7982;background:#e3e9ee}
            QTabBar::tab {padding:10px 18px}
            QTabBar::tab:selected {background:white;color:#086c60}
        """)
        shell = QWidget(objectName='shell')
        self.setCentralWidget(shell)
        layout = QVBoxLayout(shell)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)
        mast = QFrame(objectName='mast')
        header = QHBoxLayout(mast)
        header.setContentsMargins(18, 14, 18, 14)
        brand = text('ASTRA  /  Estación de tierra')
        brand.setObjectName('brand')
        self.signal = text()
        self.signal.setObjectName('signal')
        header.addWidget(brand, 1)
        header.addWidget(self.signal)
        layout.addWidget(mast)
        bar = QHBoxLayout()
        self.port = QComboBox()
        self.port.setMinimumWidth(220)
        bar.addWidget(self.port)
        self.scan = self.button(bar, 'Buscar puertos', self.scan_ports)
        self.usb = self.button(bar, 'Abrir USB de banco', self.open_usb)
        self.replay = self.button(bar, 'Reproducir registro', self.open_replay)
        self.stop_button = self.button(bar, 'Cerrar sesión', self.stop)
        bar.addStretch()
        layout.addLayout(bar)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs, 1)
        page = QWidget()
        operation = QVBoxLayout(page)
        operation.setSpacing(12)
        self.detail = text()
        operation.addWidget(self.detail)
        metrics = QHBoxLayout()
        self.metrics = {}
        for key, title in [('STATE', 'Etapa'), ('ALTITUDE', 'Altura relativa · m'),
                           ('VOLTAGE', 'Batería · V'), ('VALID', 'Muestras válidas'),
                           ('GAPS', 'Huecos observados')]:
            card = QFrame(objectName='card')
            column = QVBoxLayout(card)
            column.addWidget(text(title))
            value = text('—')
            value.setObjectName('metric')
            column.addWidget(value)
            metrics.addWidget(card, 1)
            self.metrics[key] = value
        operation.addLayout(metrics)
        row = QHBoxLayout()
        self.plot = SeriesPlot('Altura relativa · m', ('ALTITUDE',))
        row.addWidget(self.plot, 3)
        health = QFrame(objectName='card')
        side = QVBoxLayout(health)
        side.addWidget(text('REGISTRO DE SESIÓN'))
        self.primary = text()
        self.backup = text()
        side.addWidget(self.primary)
        side.addWidget(self.backup)
        side.addStretch()
        row.addWidget(health, 1)
        operation.addLayout(row, 1)
        self.tabs.addTab(page, 'Operación')
        self.telemetry = TelemetryWorkspace(self)
        self.tabs.addTab(self.telemetry, 'Telemetría y registros')
        self.scan_ports()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(200)
        self.refresh()

    def button(self, layout, title, action):
        button = QPushButton(title)
        button.clicked.connect(action)
        layout.addWidget(button)
        return button

    def scan_ports(self):
        previous = self.port.currentData()
        self.port.clear()
        self.port.addItem('Seleccioná el puerto', None)
        for port in sorted(comports()):
            self.port.addItem(port.device, port.device)
        if previous and self.port.findData(previous) >= 0:
            self.port.setCurrentIndex(self.port.findData(previous))

    def guarded(self, action):
        try:
            action()
        except (OSError, ValueError, RuntimeError) as error:
            QMessageBox.warning(self, 'Operación interrumpida', str(error))

    def order(self, operation, **arguments):
        if self.source and self.source.mode == 'usb' and not self.source.stopping:
            self.guarded(lambda: self.source.engine.command(operation, **arguments))

    def open_usb(self):
        self.guarded(lambda: self.start('usb', port=self.port.currentData()))

    def open_replay(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Abrir diario', '', 'Diario (*.jsonl)')
        if file:
            self.guarded(lambda: self.start('replay', replay=file))

    def start(self, mode, **options):
        if self.source and not self.source.closed:
            raise ValueError('Cerrá la sesión activa antes de abrir otra.')
        self.source = Source(self.output, mode, backup=self.backup_path, **options)
        self.telemetry.reset()
        self.plot.points.clear()
        self.refresh()

    def stop(self):
        if self.source:
            self.source.stop()

    def refresh(self):
        view = source_view(self.source)
        snapshot = view['snapshot'] or {}
        self.signal.setText(view['badge'])
        condition = 'Última muestra conservada' if view['old'] else 'Edad de la muestra'
        self.detail.setText(f"{view['title']}  ·  {condition}: {view['age']}")
        for key, label in self.metrics.items():
            value = view['values'].get(key, '—')
            if key == 'VALID':
                value = snapshot.get('total_valid', '—')
            elif key == 'GAPS':
                value = view['gaps']
            label.setText(str(value))
        active = bool(self.source and not self.source.closed)
        for widget in (self.port, self.scan, self.usb, self.replay):
            widget.setEnabled(not active)
        self.stop_button.setEnabled(active and not self.source.stopping)
        if self.source:
            for _ in range(500):
                try:
                    segment, packet = self.source.engine.updates.get_nowait()
                except queue.Empty:
                    break
                self.plot.add(segment, packet.count, display(packet.data))
                self.telemetry.add_packet(segment, packet)
        self.plot.old = view['old']
        self.plot.update()
        self.telemetry.refresh(view)
        for index, label, name in ((0, self.primary, 'Principal'), (1, self.backup, 'Segundo destino')):
            writers = [w for w in snapshot.get('storage', []) if w['destination'] == index]
            if not writers:
                label.setText(f'{name} · Sin sesión' if index == 0 else f'{name} · Sin registro activo')
                continue
            csv = next(w for w in writers if w['kind'] == 'csv')
            errors = sum(bool(w['error'] or w['dropped']) for w in writers)
            status = 'REVISAR GUARDADO' if errors else 'Registro CSV'
            label.setText(f"{name} · {status}\n{csv['saved']} guardadas · {csv['pending']} pendientes")

    def closeEvent(self, event):
        if self.source and not self.source.closed:
            self.stop()
            event.ignore()
            QTimer.singleShot(250, self.close)
        else:
            event.accept()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path.home() / 'ASTRA-Station')
    args = parser.parse_args()
    app = QApplication([])
    configure_font(app)
    station = Station(args.output)
    station.show()
    sys.exit(app.exec())
