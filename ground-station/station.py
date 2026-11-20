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
from ui_model import FIELDS_INFO
from serial.tools.list_ports import comports
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import (
    QApplication, QComboBox, QDialog, QFileDialog, QFrame, QGridLayout, QHBoxLayout,
    QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget,
)


def configure_font(app):
    fonts = Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts'
    for name in ('segoeui.ttf', 'segoeuib.ttf'):
        if (fonts / name).is_file():
            QFontDatabase.addApplicationFont(str(fonts / name))
    font = QFont('Segoe UI') if 'Segoe UI' in QFontDatabase.families() else app.font()
    font.setPointSize(14)
    app.setFont(font)


class Station(QMainWindow):
    def __init__(self, output):
        super().__init__()
        self.source = None
        self.output = Path(output)
        self.backup_path = None
        self.setWindowTitle('ASTRA | Estación de tierra')
        self.resize(1600, 1000)
        self.setStyleSheet("""
            QMainWindow, QWidget#shell {background:#edf2f6;color:#172c43}
            QLabel {color:#172c43;font-size:14pt}
            QFrame#mast {background:#102b43;border-radius:8px}
            QLabel#brand {color:white;font-size:22pt;font-weight:700}
            QLabel#signal {color:#acf2e5;font-weight:700;font-size:14pt}
            QFrame#card {background:white;border:1px solid #d0dce5;border-radius:7px}
            QPushButton {padding:8px 13px;background:white;border:1px solid #a8bbc9;border-radius:4px}
            QPushButton:disabled {color:#6c7982;background:#e3e9ee}
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
        self.button(bar, 'Herramientas de banco…', self.show_bench_tools)
        layout.addLayout(bar)
        self.operation_page = QFrame(objectName='card')
        layout.addWidget(self.operation_page, 1)
        operation = QVBoxLayout(self.operation_page)
        operation.setContentsMargins(14, 12, 14, 12)
        operation.setSpacing(12)
        self.detail = text()
        operation.addWidget(self.detail)
        status = QHBoxLayout()
        self.counts = text()
        self.primary = text()
        self.backup = text()
        for label in (self.counts, self.primary, self.backup):
            status.addWidget(label, 1)
        operation.addLayout(status)

        readings = QGridLayout()
        self.readings = {}
        for index, (key, (title, _, description)) in enumerate(FIELDS_INFO.items()):
            name = text(title)
            value = text('—')
            value.setToolTip(description)
            value.setStyleSheet('color:#09524c;font-weight:700')
            row, col = divmod(index, 4)
            pair = QHBoxLayout()
            pair.addWidget(name)
            pair.addWidget(value, 1)
            readings.addLayout(pair, row, col)
            readings.setColumnStretch(col, 1)
            self.readings[key] = value
        operation.addLayout(readings)

        charts = QGridLayout()
        self.mission_plots = []
        for index, (title, keys) in enumerate((
            ('Altura relativa · m', ('ALTITUDE',)),
            ('Batería · V', ('VOLTAGE',)),
            ('Corriente · A', ('CURRENT',)),
            ('Aceleración · m/s²', ('ACCEL_R', 'ACCEL_P', 'ACCEL_Y')),
            ('Vel. angular · rad/s', ('GYRO_R', 'GYRO_P', 'GYRO_Y')),
        )):
            plot = SeriesPlot(title, keys)
            plot.setMinimumHeight(166)
            row, col = divmod(index, 3)
            charts.addWidget(plot, row, col)
            self.mission_plots.append(plot)
        operation.addLayout(charts, 1)
        self.mission_segment = None
        self.bench_tools = QDialog(self)
        self.bench_tools.setWindowTitle('ASTRA | Herramientas de banco')
        self.bench_tools.resize(1120, 740)
        self.telemetry = TelemetryWorkspace(self)
        QVBoxLayout(self.bench_tools).addWidget(self.telemetry)
        self.scan_ports()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(200)
        self.refresh()

    def show_bench_tools(self):
        self.bench_tools.show()
        self.bench_tools.raise_()
        self.bench_tools.activateWindow()

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
        self.mission_segment = None
        for plot in self.mission_plots:
            plot.points.clear()
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
        valid = snapshot.get('total_valid', '—')
        self.counts.setText(f"RX válidos: {valid} · Huecos: {view['gaps']}")
        raw = snapshot.get('latest') or snapshot.get('last_sample') or {}
        for key, label in self.readings.items():
            value = view['values'].get(key, '—')
            if raw.get('GPS_SATS') == '0' and key.startswith('GPS_') and key != 'GPS_SATS':
                value = 'Sin solución'
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
                if segment != self.mission_segment:
                    self.mission_segment = segment
                    for plot in self.mission_plots:
                        plot.points.clear()
                values = display(packet.data)
                for plot in self.mission_plots:
                    plot.add(segment, packet.count, values)
                self.telemetry.add_packet(segment, packet)
        for plot in self.mission_plots:
            plot.old = view['old'] or view['mode'] == 'replay'
            plot.update()
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
