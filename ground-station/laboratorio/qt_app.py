"""ASTRA-41/22 — Laboratorio nativo Qt Widgets. Sin navegador ni puertos automáticos."""
import argparse
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import queue
import time
import sys
from PySide6.QtCore import Qt,QTimer,QUrl,QPointF
from PySide6.QtGui import QColor,QPainter,QPen,QPainterPath,QFont,QPixmap,QDesktopServices,QFontDatabase
from PySide6.QtWidgets import (QApplication,QMainWindow,QWidget,QFrame,QLabel,QPushButton,
    QVBoxLayout,QHBoxLayout,QGridLayout,QStackedWidget,QScrollArea,QComboBox,QSpinBox,
    QTableWidget,QTableWidgetItem,QHeaderView,QFileDialog,QMessageBox,QDialog,QTextBrowser,
    QToolButton,QAbstractItemView)
from runtime import AREA,FIELDS,packet_at,radio_rows,recovery_demo,chart_runs
from qt_model import Source,source_view
from journey import STEPS
from content import REPORTS
from ui_model import controls,command_text,FIELDS_INFO,STATES
from telemetry_workspace import TelemetryWorkspace
from experiment_workspace import ExperimentWorkspace

STYLE='''
* {font-family: "Segoe UI"; font-size: 13px; color: #24334B;}
QMainWindow, QWidget#shell {background: #F4F6FA;}
QWidget#sidebar {background: #17273F;}
QWidget#sidebar QLabel {color: #A6B7D0; background: transparent;}
QWidget#sidebar QLabel#brand {color: white; font-size: 23px; font-weight: 700;}
QWidget#sidebar QPushButton {text-align: left; border: 0; padding: 13px 16px; border-radius: 8px; color: #B9C8DE; background: transparent;}
QWidget#sidebar QPushButton:hover {background: #223650; color: white;}
QWidget#sidebar QPushButton:checked {background: #2B415E; color: white; font-weight: 600;}
QLabel#eyebrow {color: #69788E; font-size: 11px; font-weight: 700;}
QLabel#heading {font-size: 24px; font-weight: 600; color: #17273F;}
QLabel#sub {font-size: 14px; color: #67758A;}
QLabel#cardTitle {font-size: 17px; font-weight: 600;}
QLabel#metricValue {font-size: 27px; font-weight: 600; color: #17273F;}
QLabel#muted {color: #6D7D93;}
QLabel#badge {border-radius: 7px; padding: 7px 11px; background: #E8EDF5; color: #495D78; font-size: 11px; font-weight: 700;}
QFrame#card {background: white; border: 1px solid #DDE3EC; border-radius: 4px;}
QFrame#hero {background: #F9FAFC; border: 1px solid #DDE3EC; border-radius: 4px;}
QFrame#hero QLabel {background: transparent;}
QPushButton {background: white; border: 1px solid #D9E1EC; border-radius: 4px; padding: 9px 14px; font-weight: 600;}
QPushButton:hover {background: #EFF3FA; border-color: #A9B9D1;}
QPushButton:disabled {color: #98A4B4; background: #EEF1F5; border-color: #E2E7EE;}
QPushButton#primary {background: #087F73; color: white; border: 1px solid #087F73;}
QPushButton#primary:hover {background: #06675E;}
QPushButton#primary:disabled {background: #A0C8C2; border-color: #A0C8C2;}
QComboBox,QSpinBox {background: white; border: 1px solid #D9E1EC; border-radius: 6px; padding: 8px; min-height: 20px;}
QComboBox::drop-down {border: 0; width: 24px;}
QScrollArea {background: transparent; border: 0;}
QScrollArea > QWidget > QWidget {background: transparent;}
QToolButton {text-align: left; background: #F5F7FA; border: 0; border-radius: 6px; padding: 10px; color: #526781;}
QTableWidget {background: white; alternate-background-color: #F5F7FA; border: 0; gridline-color: #EDF0F5; selection-background-color: #DCEFEA;}
QHeaderView::section {background: #F1F4F8; border: 0; border-bottom: 1px solid #DBE3EE; padding: 9px; color: #52647D; font-weight: 600;}
QTabWidget::pane {border: 1px solid #DDE3EC; background: white;}
QTabBar::tab {background: #E8EDF5; padding: 10px 12px; border: 0; margin-right: 2px;}
QTabBar::tab:selected {background: white; color: #087F73; border-bottom: 2px solid #087F73;}
QTextBrowser {background: white; border: 1px solid #E1E7EF; border-radius: 9px; padding: 18px; font-size: 14px;}
QScrollBar:vertical {background: transparent; width: 8px;}
QScrollBar::handle:vertical {background: #CBD5E3; border-radius: 4px; min-height: 30px;}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical {height: 0;}
'''


def label(text='',kind=None):
    w=QLabel(text);w.setTextFormat(Qt.PlainText);w.setWordWrap(True)
    if kind:w.setObjectName(kind)
    return w


def button(text,callback,primary=False):
    b=QPushButton(text);b.setCursor(Qt.PointingHandCursor)
    if primary:b.setObjectName('primary')
    b.clicked.connect(callback);return b


def card(title=None,description=None,hero=False):
    w=QFrame();w.setObjectName('hero' if hero else 'card');lay=QVBoxLayout(w)
    lay.setContentsMargins(22,20,22,20);lay.setSpacing(12)
    if title:lay.addWidget(label(title,'cardTitle'))
    if description:lay.addWidget(label(description,'sub'))
    return w,lay


def details(title,text):
    w=QWidget();lay=QVBoxLayout(w);lay.setContentsMargins(0,0,0,0)
    b=QToolButton();b.setText('+  '+title);b.setCheckable(True)
    body=label(text,'muted');body.hide();lay.addWidget(b);lay.addWidget(body)
    def toggle(checked):body.setVisible(checked);b.setText(('-  ' if checked else '+  ')+title)
    b.toggled.connect(toggle);return w


def table(headers):
    w=QTableWidget(0,len(headers));w.setHorizontalHeaderLabels(headers)
    w.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);w.verticalHeader().hide()
    w.setEditTriggers(QAbstractItemView.NoEditTriggers);w.setAlternatingRowColors(True)
    w.setSelectionBehavior(QAbstractItemView.SelectRows);w.setShowGrid(False)
    return w


class Plot(QWidget):
    def __init__(self):
        super().__init__();self.points=deque(maxlen=180);self.historical=False
        self.setMinimumHeight(210)

    def paintEvent(self,event):
        p=QPainter(self);p.setRenderHint(QPainter.Antialiasing)
        r=self.rect();left=48;right=r.width()-18;top=25;bottom=r.height()-30
        p.fillRect(r,QColor('white'));p.setPen(QColor('#7D8BA0'))
        for height in (0,250,500):
            y=bottom-height/550*(bottom-top);p.drawText(0,int(y)-8,40,20,Qt.AlignRight,str(height))
            p.setPen(QPen(QColor('#ECF0F5'),1));p.drawLine(left,int(y),right,int(y));p.setPen(QColor('#7D8BA0'))
        p.drawText(left,bottom+22,'contador de muestra')
        if not self.points:
            p.drawText(r,Qt.AlignCenter,'El gráfico aparece cuando llegan mediciones.');return
        low=min(x[1] for x in self.points);high=max(x[1] for x in self.points)
        p.setPen(QPen(QColor('#AAB4C3' if self.historical else '#078C7D'),2.7))
        for run in chart_runs(self.points):
            path=QPainterPath()
            for i,(_,count,height) in enumerate(run):
                point=QPointF(left+(count-low)/max(high-low,1)*(right-left),bottom-height/550*(bottom-top))
                if i:path.lineTo(point)
                else:path.moveTo(point)
            p.drawPath(path)


class Laboratory(QMainWindow):
    def __init__(self,config=None):
        super().__init__()
        # Registro la fuente local también en renderizado fuera de pantalla.
        if not getattr(Laboratory,'fonts_ready',False):
            for filename in ('segoeui.ttf','segoeuib.ttf','segoeuil.ttf'):
                path=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts'/filename
                if path.is_file():QFontDatabase.addApplicationFont(str(path))
            Laboratory.fonts_ready=True
        self.config=config or {};self.source=None;self.step=0
        self.output=Path(self.config.get('output',Path.home()/'ASTRA-Laboratorio'/'ensayos'))/'qt'
        self.backup_path=None
        self.pool=ThreadPoolExecutor(max_workers=2);self.jobs=[];self.closing=False;self.camera_results={};self.camera_busy=None;self.camera_started=None;self.camera_paths={};self.camera_operation='Foto'
        self.setWindowTitle('ASTRA · Laboratorio');self.resize(1280,850);self.setMinimumSize(1000,700)
        self.setStyleSheet(STYLE)
        shell=QWidget();shell.setObjectName('shell');self.setCentralWidget(shell)
        outer=QHBoxLayout(shell);outer.setContentsMargins(0,0,0,0);outer.setSpacing(0)
        side=QWidget();side.setObjectName('sidebar');side.setFixedWidth(218)
        nav=QVBoxLayout(side);nav.setContentsMargins(18,27,18,20);nav.setSpacing(7)
        nav.addWidget(label('A S T R A','brand'));nav.addWidget(label('LABORATORIO DE TIERRA'));nav.addSpacing(35)
        nav.addWidget(label('EXPLORAR'))
        self.nav={};self.stack=QStackedWidget();self.pages={}
        for key,title in [('recorrido','Avances del proyecto'),('datos','Telemetría'),('camaras','Cámaras'),('radio','Enlace RF'),('recuperacion','Recuperación de datos'),('ensayos','Ensayos y análisis'),('evidencias','Documentación')]:
            b=button(title,lambda checked=False,k=key:self.go(k));b.setCheckable(True);nav.addWidget(b);self.nav[key]=b
            scroll=QScrollArea();scroll.setWidgetResizable(True);page=QWidget();lay=QVBoxLayout(page)
            lay.setContentsMargins(32,28,32,28);lay.setSpacing(18);scroll.setWidget(page)
            self.pages[key]=(scroll,lay);self.stack.addWidget(scroll)
        nav.addStretch();nav.addWidget(label('CanSat universitario\nGroundstation y datos'))
        outer.addWidget(side)
        main=QWidget();body=QVBoxLayout(main);body.setContentsMargins(0,0,0,0);body.setSpacing(0)
        top=QWidget();top.setFixedHeight(60);toplay=QHBoxLayout(top);toplay.setContentsMargins(32,10,32,10)
        top_title=label('ESTACIÓN DE TIERRA   /   ASTRA','eyebrow');top_title.setWordWrap(False)
        toplay.addWidget(top_title);toplay.addStretch()
        self.origin=label('SIN FUENTE DE DATOS','badge');self.origin.setWordWrap(False);toplay.addWidget(self.origin)
        body.addWidget(top);body.addWidget(self.stack);outer.addWidget(main)
        self.build_journey();self.build_data();self.build_cameras();self.build_radio();self.build_recovery();self.build_experiments();self.build_evidence()
        self.go('recorrido');self.timer=QTimer(self);self.timer.timeout.connect(self.refresh);self.timer.start(150);self.refresh()
        self.port_timer=QTimer(self);self.port_timer.timeout.connect(self.refresh_camera_ports);self.port_timer.start(2000)

    def heading(self,key,title,subtitle):
        lay=self.pages[key][1];lay.addWidget(label(title,'heading'));lay.addWidget(label(subtitle,'sub'));return lay

    def go(self,key):
        self.stack.setCurrentWidget(self.pages[key][0])
        for k,b in self.nav.items():b.setChecked(k==key)

    def build_journey(self):
        lay=self.heading('recorrido','Avances del proyecto','Implementación, pruebas realizadas y pendientes por subsistema.')
        hero,h=card(hero=True);self.step_tag=label(kind='eyebrow');self.story_title=label(kind='heading');self.story_lead=label(kind='sub')
        h.addWidget(self.step_tag);h.addWidget(self.story_title);h.addWidget(self.story_lead);lay.addWidget(hero)
        grid=QHBoxLayout();built,bl=card('Implementación');proof,pl=card('Estado de verificación')
        self.story_built=label();self.story_proof=label();bl.addWidget(self.story_built);pl.addWidget(self.story_proof)
        grid.addWidget(built);grid.addWidget(proof);lay.addLayout(grid)
        say,sl=card('Prueba disponible');self.story_say=label();sl.addWidget(self.story_say)
        self.story_action=button('',self.story_demo,True);sl.addWidget(self.story_action,alignment=Qt.AlignLeft);lay.addWidget(say)
        self.story_detail=QVBoxLayout();lay.addLayout(self.story_detail)
        row=QHBoxLayout();self.previous=button('← Anterior',lambda:self.show_step(self.step-1));self.progress=label();self.next=button('Siguiente →',lambda:self.show_step(self.step+1),True)
        row.addWidget(self.previous);row.addStretch();row.addWidget(self.progress);row.addStretch();row.addWidget(self.next);lay.addLayout(row);lay.addStretch();self.show_step(0)

    def show_step(self,index):
        self.step=max(0,min(len(STEPS)-1,index));s=STEPS[self.step]
        for widget,key in [(self.step_tag,'tag'),(self.story_title,'title'),(self.story_lead,'lead'),(self.story_built,'built'),(self.story_proof,'proves'),(self.story_say,'say')]:widget.setText(s[key])
        self.story_action.setText(s['demo']);self.progress.setText(f'{self.step+1} de {len(STEPS)}')
        self.previous.setEnabled(self.step>0);self.next.setEnabled(self.step<len(STEPS)-1)
        while self.story_detail.count():self.story_detail.takeAt(0).widget().deleteLater()
        self.story_detail.addWidget(details('Fundamento técnico',s['technical']))

    def story_demo(self):self.go(STEPS[self.step]['page'])

    def build_data(self):
        lay=self.heading('datos','Telemetría','Una fuente activa por sesión: receptor USB, simulador de PC o registro guardado.')
        row=QHBoxLayout()
        usb,u=card('USB · ESP32','Adquisición desde el puerto seleccionado. Sin conexión no ingresan muestras nuevas.')
        self.usb_ports=QComboBox();self.usb_ports.setMinimumContentsLength(17);self.usb_ports.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon);u.addWidget(self.usb_ports)
        refresh=button('Actualizar puertos',self.refresh_ports);u.addWidget(refresh)
        self.connect_btn=button('Conectar ESP32',self.connect_usb,True);u.addWidget(self.connect_btn);row.addWidget(usb)
        pc,p=card('Simulación PC','Emisor sintético ejecutado en la computadora. No requiere conexión con el ESP32.')
        self.scenario=QComboBox()
        for title,value in [('Misión normal','NOMINAL'),('Mensajes que no llegan','PACKET_LOSS'),('Mensajes dañados','CORRUPTED_PACKET'),('GPS sin posición','GPS_LOSS'),('Omisión lógica','RESET')]:self.scenario.addItem(title,value)
        p.addWidget(self.scenario);self.pc_speed=QComboBox()
        for speed in (1,5,10):self.pc_speed.addItem(f'Velocidad ×{speed}',speed)
        self.pc_speed.setCurrentIndex(1);p.addWidget(self.pc_speed)
        self.pc_btn=button('Comenzar simulación',self.start_pc,True);p.addWidget(self.pc_btn);p.addWidget(label('Valores ficticios · no usa USB','muted'));row.addWidget(pc)
        replay,r=card('Reproducción','Lectura temporal de un registro guardado. No es adquisición en vivo.')
        self.replay_speed=QComboBox()
        for speed in (1,5,10):self.replay_speed.addItem(f'Velocidad ×{speed}',speed)
        r.addWidget(self.replay_speed)
        self.replay_btn=button('Elegir grabación…',self.pick_replay);r.addWidget(self.replay_btn);r.addStretch();row.addWidget(replay)
        self.sources_panel=QWidget();self.sources_panel.setLayout(row);lay.addWidget(self.sources_panel)
        status,s=card();self.data_title=label('Sin fuente seleccionada','cardTitle');self.data_detail=label('Adquisición detenida.','sub')
        s.addWidget(self.data_title);s.addWidget(self.data_detail)
        self.phase=label('Sin etapa de misión','badge');s.addWidget(self.phase,alignment=Qt.AlignLeft)
        buttons=QHBoxLayout();self.run_btn=button('Iniciar ensayo en placa',lambda:self.order('RUN',scenario='NOMINAL',samples=131));self.stop_btn=button('Cerrar y conservar',self.stop_source)
        buttons.addWidget(self.run_btn);buttons.addWidget(self.stop_btn);buttons.addStretch();s.addLayout(buttons);lay.addWidget(status)
        measures=QHBoxLayout();self.metric_values={}
        for key,title,hint in [('ALTITUDE','Altura sobre el inicio','Metros por encima de la referencia inicial.'),('TEMPERATURE','Temperatura','Valor del ensayo, expresado en °C.'),('VOLTAGE','Batería','Tensión declarada; no mide autonomía.'),('GPS_SATS','GPS','Satélites declarados; cero indica sin solución.')]:
            c,cl=card();cl.addWidget(label(title,'muted'));value=label('—','metricValue');cl.addWidget(value);cl.addWidget(label(hint,'muted'));measures.addWidget(c);self.metric_values[key]=value
        lay.addLayout(measures);chart,c=card('Altura durante el ensayo','Los huecos de contador quedan sin unir. El gráfico no completa datos ausentes.');self.plot=Plot();c.addWidget(self.plot);lay.addWidget(chart)
        counters,c=card('Recepción y almacenamiento');self.counts=label('Recibidos: —   ·   Válidos: —   ·   Guardados: —   ·   Por guardar: —');self.freshness=label('Sin mediciones recibidas.','muted');c.addWidget(self.counts);c.addWidget(self.freshness)
        c.addWidget(details('Definición de contadores','Recibidos: líneas de datos; excluye controles y diagnósticos reconocidos. Válidos: muestras que pudimos interpretar. Guardados: filas confirmadas del CSV principal. Por guardar: filas que ya llegaron y esperan escritura. Los mensajes que no llegaron durante un corte no están en esa cola. Huecos de contador requieren continuidad e identidad suficientes.'))
        self.packet_btn=button('Ver el paquete y todas las mediciones',self.packet_dialog);c.addWidget(self.packet_btn,alignment=Qt.AlignLeft);lay.addWidget(counters)
        lay.removeWidget(counters);lay.insertWidget(lay.indexOf(chart),counters)
        lay.removeWidget(chart);chart.hide()
        lay.removeItem(measures);measures.setParent(None);lay.removeWidget(counters)
        overview=QWidget();overview_layout=QVBoxLayout(overview);overview_layout.addLayout(measures);overview_layout.addWidget(counters);overview_layout.addStretch()
        self.telemetry=TelemetryWorkspace(self);self.telemetry.addTab(overview,'Estado');lay.addWidget(self.telemetry)
        self.refresh_ports()

    def refresh_ports(self):
        from serial.tools import list_ports
        selected=self.usb_ports.currentData();self.usb_ports.clear();self.usb_ports.addItem('Seleccioná el puerto de telemetría…',None)
        for p in list_ports.comports():self.usb_ports.addItem(f'{p.device} · {p.description}',p.device)
        if selected:
            index=self.usb_ports.findData(selected)
            if index>=0:self.usb_ports.setCurrentIndex(index)

    def start_source(self,mode,**kwargs):
        if self.source and not self.source.closed:raise ValueError('Cerrá y conservá la fuente actual antes de elegir otra.')
        self.source=Source(self.output,mode,backup=self.backup_path,**kwargs);self.plot.points.clear();self.telemetry.reset();self.refresh()

    def connect_usb(self):self.guarded(lambda:self.start_source('usb',port=self.usb_ports.currentData()))
    def start_pc(self):self.guarded(lambda:self.start_source('pc',scenario=self.scenario.currentData(),speed=self.pc_speed.currentData()))
    def pick_replay(self):
        path,_=QFileDialog.getOpenFileName(self,'Elegir diario de una prueba','','Registro JSONL (*.jsonl)')
        if path:self.guarded(lambda:self.start_source('replay',replay=path,speed=self.replay_speed.currentData()))
    def stop_source(self):
        if self.source:self.source.stop()
    def order(self,op,**args):
        if self.source:self.guarded(lambda:self.source.engine.command(op,**args))

    def packet_dialog(self):
        view=source_view(self.source);s=view['snapshot'];data=(s.get('latest') or s.get('last_sample')) if s else None
        if not data:return self.notice('Todavía no hay una muestra','Primero recibí datos desde una fuente explícita. No genero una muestra de reemplazo.')
        w=QDialog(self);w.setWindowTitle('ASTRA · Una muestra, campo por campo');w.resize(950,650);lay=QVBoxLayout(w)
        lay.addWidget(label(view['badge'],'badge'));lay.addWidget(label('La línea original y lo que significa cada posición.','cardTitle'))
        original=','.join(str(data[k]) for k in FIELDS)+'\r';raw=original.replace('\r','<CR>')
        lay.addWidget(label(('Muestra conservada · ' if view['old'] else 'Última muestra recibida · ')+f'{len(original.encode("ascii"))} bytes','muted'))
        lay.addWidget(label(raw,'muted'));t=table(['Campo','Valor original','Significado'])
        t.setRowCount(len(FIELDS_INFO))
        for i,(key,(title,unit,help_text)) in enumerate(FIELDS_INFO.items()):
            for j,text in enumerate((key,str(data.get(key,'—')),title+' · '+('°/s original' if key.startswith('GYRO_') else unit))):t.setItem(i,j,QTableWidgetItem(text))
            if key.startswith('GYRO_'):help_text='El paquete conserva grados por segundo. La pantalla de mediciones del perfil conocido convierte explícitamente a rad/s. No es inclinación.'
            for j in range(3):t.item(i,j).setToolTip(help_text)
        lay.addWidget(t);lay.addWidget(label('Texto ASCII separado por comas. El empaquetado binario de vuelo sigue bajo definición de Edu.','muted'));w.setAttribute(Qt.WA_DeleteOnClose);w.show()

    def build_cameras(self):
        lay=self.heading('camaras','Cámaras ESP32-CAM','Una foto nueva por solicitud. La imagen aparece aquí al terminar su recepción USB; no es video continuo.')
        cards=QHBoxLayout();self.photo_widgets={};self.camera_notes={};self.photo_badges={};self.sequence_buttons={}
        for n in (1,2):
            c,l=card(f'Cámara {n}');badge=label('EVIDENCIA CONSERVADA','badge');self.photo_badges[n]=badge;l.addWidget(badge);pic=QLabel();pic.setAlignment(Qt.AlignCenter);pic.setMinimumHeight(170)
            entry=self.config.get('photos',{}).get(str(n),{});pix=QPixmap(entry.get('path',''))
            if pix.isNull():pic.setText('Sin foto local configurada')
            else:
                pic.setPixmap(pix.scaled(400,220,Qt.KeepAspectRatio,Qt.SmoothTransformation));self.camera_paths[n]=entry['path']
            l.addWidget(pic);note=label(entry.get('caption','No es una captura de esta sesión.'),'muted');l.addWidget(note)
            actions=QHBoxLayout()
            b=button('Sacar foto',lambda checked=False,number=n:self.capture_camera(number,False),True);actions.addWidget(b)
            sd_button=button('Foto + microSD',lambda checked=False,number=n:self.capture_camera(number,True));actions.addWidget(sd_button)
            l.addLayout(actions);self.photo_widgets[n]=(pic,b);self.camera_notes[n]=note
            l.addWidget(button('Abrir secuencia guardada…',lambda checked=False,number=n:self.open_sequence(number)))
            last=button('Ver última grabación',lambda checked=False,number=n:self.open_sequence(number,latest=True))
            last.setEnabled(bool(self.config.get('sequences',{}).get(str(n))));l.addWidget(last)
            seq=button('Grabar prueba · 12 cuadros en SD',lambda checked=False,number=n:self.record_sequence(number));self.sequence_buttons[n]=seq;l.addWidget(seq)
            l.addWidget(button('Ampliar foto',lambda checked=False,number=n:self.enlarge_camera(number)))
            if not hasattr(self,'camera_action_buttons'):self.camera_action_buttons=[]
            self.camera_action_buttons.extend((b,sd_button));cards.addWidget(c)
        lay.addLayout(cards)
        prep,p=card('Configuración del chequeo','Puerto de la cámara montada en su base USB. Foto + SD comprueba la lectura reportada por la cámara; la lectura independiente se realiza desde el lector.')
        self.camera_ports=QComboBox();self.camera_ports.addItem('Seleccioná el puerto de cámara…',None);p.addWidget(self.camera_ports)
        p.addWidget(button('Actualizar puertos de cámara',self.refresh_camera_ports),alignment=Qt.AlignLeft)
        self.camera_summary=label('Esta sesión todavía no comprobó ninguna cámara.','muted');p.addWidget(self.camera_summary);lay.addWidget(prep)
        from qt_camera_live import CameraLive
        def camera_identity(number):
            sys.path.insert(0,str(AREA/'camaras-banco'))
            from camera_session import read_registry
            return read_registry(self.config.get('camera_registry',''))[f'camera{number}']
        self.camera_live=CameraLive(camera_identity,self,control=self.control_camera_wifi)
        lay.addWidget(self.camera_live)
        self.refresh_camera_ports()
        lay.addWidget(details('Alcance del banco','Foto USB y chequeo de escritura/lectura SD por unidad. La vista previa Wi-Fi requiere activar el modo de mantenimiento y conectar la PC a la red local de la cámara. Una imagen recibida no confirma grabación. Arranque autónomo, grabación prolongada, energía y continuidad ante reset requieren sus ensayos. Los comandos de vuelo los define Edu.'))

    def control_camera_wifi(self,enabled,n):
        def begin():
            import secrets
            sys.path.insert(0,str(AREA/'camaras-banco'))
            from camera_session import read_registry
            from preview_control import activate
            port=self.camera_ports.currentData()
            if not port:raise ValueError('Elegí el puerto USB de la cámara para activar o desactivar su red.')
            if any(kind=='camera' for _,kind,_ in self.jobs):raise ValueError('Hay una operación de cámara en curso.')
            if self.source and not self.source.closed and self.source.mode=='usb' and self.source.port==port:raise ValueError('El puerto está ocupado por telemetría.')
            identity=read_registry(self.config.get('camera_registry',''))[f'camera{n}']
            password=secrets.token_hex(8) if enabled else None
            self.camera_live.stop()
            self.camera_busy=n;self.camera_started=time.monotonic();self.camera_operation='Configuración Wi-Fi local'
            def done(result):
                self.camera_busy=None;self.camera_started=None
                self.camera_summary.setText('Wi-Fi de mantenimiento activado; no se inició grabación.' if enabled else 'Wi-Fi desactivado según la cámara.')
                if enabled:
                    self.camera_live.address.setText('http://'+result['ip']+':81/stream')
                    self.notice('Red local de cámara',f"Red: {result['ssid']}\nClave temporal: {password}\n\nConectá la PC a esta red desde Windows. Después pulsá Conectar vista previa. La clave sólo se muestra aquí; no se guarda en archivos.")
            self.submit(lambda:activate(port,identity,enabled,password),'camera',done)
        self.guarded(begin)

    def refresh_camera_ports(self):
        if self.camera_busy is not None:return
        from serial.tools import list_ports
        selected=self.camera_ports.currentData() or self.config.get('camera_port')
        ports=[(p.device,p.description) for p in list_ports.comports()]
        if getattr(self,'camera_port_list',None)==ports:return
        self.camera_port_list=ports
        self.camera_ports.clear();self.camera_ports.addItem('Seleccioná el puerto de cámara…',None)
        for device,description in ports:self.camera_ports.addItem(f'{device} · {description}',device)
        if selected:
            index=self.camera_ports.findData(selected)
            if index>=0:self.camera_ports.setCurrentIndex(index)

    def enlarge_camera(self,n):
        path=self.camera_paths.get(n)
        if not path:return self.notice('Sin imagen','Todavía no hay una foto para ampliar.')
        pix=QPixmap(str(path))
        if pix.isNull():return self.notice('Imagen no disponible','No pude abrir el archivo conservado.')
        dialog=QDialog(self);dialog.setWindowTitle(f'ASTRA · Cámara {n}');dialog.resize(900,760)
        lay=QVBoxLayout(dialog);lay.addWidget(label(self.photo_badges[n].text(),'badge'));pic=QLabel();pic.setAlignment(Qt.AlignCenter)
        pic.setPixmap(pix.scaled(850,620,Qt.KeepAspectRatio,Qt.SmoothTransformation));lay.addWidget(pic);lay.addWidget(label(self.camera_notes[n].text(),'muted'))
        dialog.setAttribute(Qt.WA_DeleteOnClose);dialog.show()

    def open_sequence(self,n,latest=False):
        def show():
            sys.path.insert(0,str(AREA/'camaras-banco'))
            from camera_session import read_registry
            from qt_sequence import SequenceDialog
            identity=read_registry(self.config.get('camera_registry',''))[f'camera{n}']
            folder=self.config.get('sequences',{}).get(str(n)) if latest else QFileDialog.getExistingDirectory(self,f'Secuencia conservada de cámara {n}')
            if not folder:return
            dialog=SequenceDialog(self,folder,identity,f'Cámara {n} · secuencia conservada')
            dialog.setAttribute(Qt.WA_DeleteOnClose);dialog.show()
        self.guarded(show)

    def capture_camera(self,n,save_sd=False):
        def begin():
            sys.path.insert(0,str(AREA/'camaras-banco'))
            from camera_session import read_registry,capture
            port=self.camera_ports.currentData()
            if not port:raise ValueError('Elegí el puerto de cámara antes de pedir una foto.')
            if self.source and not self.source.closed and self.source.mode=='usb' and self.source.port==port:raise ValueError('Ese puerto está siendo usado por telemetría. Elegí la cámara correcta o cerrá esa conexión.')
            if any(kind=='camera' for _,kind,_ in self.jobs):raise ValueError('Ya hay una comprobación en curso. Esperá a que termine.')
            identity=read_registry(self.config.get('camera_registry',''))[f'camera{n}']
            self.camera_results.pop(n,None);self.camera_busy=n;self.camera_started=time.monotonic();self.camera_operation='Foto'
            self.photo_badges[n].setText('CAPTURANDO FOTO NUEVA')
            self.camera_summary.setText(f'Cámara {n} · solicitando foto por {port}…')
            for b in self.camera_action_buttons:b.setEnabled(False)
            self.submit(lambda:capture(f'camera{n}',identity,port,self.output/'camaras',save_sd), 'camera',lambda r:self.camera_finished(n,r))
        self.guarded(begin)

    def camera_finished(self,n,r):
        if r.get('photo'):
            pix=QPixmap(str(r['photo']))
            if pix.isNull():raise ValueError('La imagen recibida no se pudo abrir; no actualizo la vista con un archivo inválido.')
            self.camera_paths[n]=str(r['photo']);self.photo_widgets[n][0].setPixmap(pix.scaled(400,220,Qt.KeepAspectRatio,Qt.SmoothTransformation))
            self.photo_badges[n].setText('FOTO CAPTURADA EN ESTA SESIÓN')
        self.camera_busy=None;self.camera_started=None;self.camera_results[n]=r
        ok=bool(r.get('operation_ok'))
        if r.get('photo'):
            from datetime import datetime
            try:stamp=datetime.fromisoformat(r['finished_utc']).astimezone().strftime('%d/%m · %H:%M:%S')
            except (ValueError,KeyError,TypeError):stamp='fecha no confirmada'
            result_text='Foto USB validada · SD no solicitada' if ok and not r.get('sd_requested') else ('Foto y lectura SD reportadas' if ok and r.get('sd_ok') else 'Foto recibida · chequeo incompleto')
            self.camera_notes[n].setText(result_text+' · '+stamp)
        else:
            self.photo_badges[n].setText('FOTO ANTERIOR · CAPTURA NO CONFIRMADA');self.camera_notes[n].setText('No llegó una foto nueva. La imagen conservada no corresponde a esta solicitud.')
        count=sum(bool(x.get('operation_ok')) for x in self.camera_results.values())
        sd_count=sum(bool(x.get('operation_ok') and x.get('sd_ok')) for x in self.camera_results.values())
        self.camera_summary.setText(f'Fotos comprobadas: {count} de 2 · Lectura SD reportada: {sd_count} de 2 · por turnos. Lectura desde lector independiente: ensayo aparte.')
        if r.get('error'):self.camera_summary.setText(self.camera_summary.text()+'\n'+str(r['error']))

    def record_sequence(self,n):
        def begin():
            sys.path.insert(0,str(AREA/'camaras-banco'))
            from camera_session import read_registry
            from sequence_session import record
            port=self.camera_ports.currentData()
            if not port:raise ValueError('Elegí el puerto de la cámara.')
            if any(kind=='camera' for _,kind,_ in self.jobs):raise ValueError('Hay una captura en curso; espero su cierre.')
            if self.source and not self.source.closed and self.source.mode=='usb' and self.source.port==port:raise ValueError('El puerto está ocupado por telemetría.')
            identity=read_registry(self.config.get('camera_registry',''))[f'camera{n}']
            self.camera_busy=n;self.camera_started=time.monotonic();self.camera_operation='Secuencia SD'
            self.photo_badges[n].setText('GRABANDO SECUENCIA · FOTO ANTERIOR')
            self.submit(lambda:record(f'camera{n}',identity,port,self.output/'camaras'), 'camera',lambda r:self.sequence_finished(n,r))
        self.guarded(begin)

    def sequence_finished(self,n,result):
        self.camera_busy=None;self.camera_started=None;self.photo_badges[n].setText('FOTO CONSERVADA · NO ES VIDEO EN VIVO')
        if result['reported_closed']:
            message=f"Cámara {n} · {result['frames']} cuadros · cierre reportado.\nCarpeta SD: {result['path']}\nFalta verificar los archivos desde el lector; no retires la tarjeta con la cámara alimentada."
        else:message=f"Grabación sin confirmar: {result.get('error') or result['state']}. No reenvío la orden automáticamente."
        self.camera_summary.setText(message);self.camera_notes[n].setText(message)

    def build_radio(self):
        lay=self.heading('radio','Enlace RF · cálculo LoRa','Tiempo de aire según tamaño de paquete y configuración. Sin emisión ni ensayo RF.')
        c,l=card('CÁLCULO · SIN EMISIÓN');row=QHBoxLayout();row.addWidget(label('Tamaño del paquete'))
        self.payload=QSpinBox();self.payload.setRange(1,255);self.payload.setValue(55);self.payload.setSuffix(' bytes');row.addWidget(self.payload)
        row.addWidget(label('Ancho de banda'));self.bw=QComboBox()
        for value in (125,250,500):self.bw.addItem(f'{value} kHz',value*1000)
        row.addWidget(self.bw);self.cr=QComboBox()
        for cr in range(1,5):self.cr.addItem(f'CR 4/{cr+4}',cr)
        row.addWidget(self.cr);l.addLayout(row);self.radio_table=table(['Perfil','Tiempo transmitiendo','De cada segundo ocupa','Margen antes de otros mensajes']);self.radio_table.setMinimumHeight(230);l.addWidget(self.radio_table)
        self.radio_summary=label();l.addWidget(self.radio_summary);lay.addWidget(c)
        c,l=card('Criterios de selección','Tamaño de paquete, SF, margen para telecomandos y reintentos. La selección final requiere ensayos de pérdidas, alcance, antenas y consumo.')
        l.addWidget(details('Hipótesis y fórmula','Fórmula SX1276 de Semtech. CRC activo, cabecera explícita y preámbulo 8; CR según selector. Optimización de baja tasa automática. La ocupación a 1 Hz es aritmética: no incluye ACK, comandos, guardas o reintentos, ni autoriza potencia/régimen de emisión.'))
        l.addWidget(button('Consultar fuente de Semtech',lambda:QDesktopServices.openUrl(QUrl('https://www.semtech.com/design-support/faq/faq-lora'))),alignment=Qt.AlignLeft);lay.addWidget(c);lay.addStretch()
        self.payload.valueChanged.connect(self.update_radio);self.bw.currentIndexChanged.connect(self.update_radio);self.cr.currentIndexChanged.connect(self.update_radio);self.update_radio()

    def update_radio(self):
        rows=radio_rows(self.payload.value(),self.bw.currentData(),self.cr.currentData());self.radio_table.setRowCount(len(rows))
        for i,r in enumerate(rows):
            sec=r['airtime_seconds'];texts=(f"SF{r['sf']}",f'{1000*sec:.1f} ms',f'{sec*100:.1f} %',f'{1000*(1-sec):.1f} ms' if sec<1 else 'No entra a 1 Hz')
            for j,text in enumerate(texts):
                item=QTableWidgetItem(text)
                if sec>=1:item.setForeground(QColor('#A8582A'))
                self.radio_table.setItem(i,j,item)
        self.radio_summary.setText(f"Con {self.payload.value()} bytes y SF7, la radio transmitiría durante {rows[0]['airtime_seconds']*1000:.1f} ms. Es tiempo de transmisión, no de viaje por el espacio.")

    def build_recovery(self):
        lay=self.heading('recuperacion','Recuperación de registros','Casos de prueba sintéticos. Salida nueva, fuentes originales conservadas y procedencia por registro.')
        row=QHBoxLayout()
        for mode,title,text in [('complementarias','Fuentes complementarias','Las fuentes tienen faltantes diferentes. Resultado esperado: diez registros recuperados.'),('ausente_en_ambas','Registro ausente','Un registro no aparece en ninguna fuente. Resultado esperado: nueve registros recuperados.'),('conflicto','Versiones contradictorias','Dos registros con igual identidad difieren. Resultado esperado: reconstrucción bloqueada.')]:
            c,l=card(title,text);l.addWidget(button('Probar este caso',lambda checked=False,m=mode:self.recover(m),True));row.addWidget(c)
        lay.addLayout(row);c,l=card('Resultado de la prueba');self.recovery_result=label('Elegí uno de los tres casos para ver qué ocurre.','sub');l.addWidget(self.recovery_result);lay.addWidget(c)
        lay.addWidget(label('SIMULACIÓN DE ARCHIVOS · Son dos archivos en el mismo disco. No demuestra un respaldo en soportes independientes.','muted'));lay.addStretch()

    def recover(self,mode):
        if any(kind=='recovery' for _,kind,_ in self.jobs):return
        self.recovery_result.setText('Comprobando fuentes y creando una salida nueva…')
        def done(r):self.recovery_result.setText(('Reconstrucción completada' if r['written'] else 'Reconstrucción bloqueada')+f"\nDatos presentes: {r['candidates']} de 10 · conflictos: {r['conflicts']} · originales intactos: {'sí' if r['originals_unchanged'] else 'no'}.\n"+('No hay información para recuperar lo que falta en ambas fuentes.' if r['candidates']<10 else 'El resultado queda conservado con sus fuentes.'))
        self.submit(lambda:recovery_demo(self.output,mode),'recovery',done)

    def build_experiments(self):
        lay=self.heading('ensayos','Ensayos y análisis','Cálculos reproducibles y archivo de resultados, parámetros y fuentes.')
        self.experiments=ExperimentWorkspace(self);lay.addWidget(self.experiments)

    def build_evidence(self):
        lay=self.heading('evidencias','Documentación','Informes de ensayo, requisitos, decisiones de diseño y antecedentes.')
        c,l=card('Informes y decisiones');self.documents=QComboBox()
        for title,path in REPORTS:self.documents.addItem(title,path)
        l.addWidget(self.documents);l.addWidget(button('Leer informe',self.open_report,True),alignment=Qt.AlignLeft)
        l.addWidget(button('Archivo completo de resultados y documentos',lambda:(self.go('ensayos'),self.experiments.setCurrentIndex(2))),alignment=Qt.AlignLeft);lay.addWidget(c)
        c,l=card('Pendientes de validación','Radio y antenas en condiciones reales; interfaz de vuelo acordada; energía y autonomía; arranque estable, secuencias reales y grabación prolongada de cámaras.')
        l.addWidget(label('Los cálculos, la simulación y las fotos previas tienen alcances diferentes. Ninguno acredita por sí solo el cumplimiento completo del PDR.','muted'));lay.addWidget(c)
        c,l=card('Investigación y antecedentes','Revisión de otras estaciones: buffers, datos inválidos, conservación y recuperación. Comparación de antenas y evaluación de rotor con parámetros y ensayos pendientes.')
        l.addWidget(label('Ganar una competencia no valida cada función de un diseño. Una hélice girando no prueba energía útil.','muted'));lay.addWidget(c);lay.addStretch()

    def open_report(self):
        path=AREA/self.documents.currentData()
        def show():
            text=path.read_text(encoding='utf-8');w=QDialog(self);w.setWindowTitle(self.documents.currentText());w.resize(950,730)
            l=QVBoxLayout(w);view=QTextBrowser();view.setOpenExternalLinks(False);view.setOpenLinks(False);view.setMarkdown(text)
            current=[path]
            def follow(url):
                if url.scheme() in ('http','https'):QDesktopServices.openUrl(url);return
                if url.scheme() not in ('','file'):return
                target=Path(url.toLocalFile()) if url.isLocalFile() else current[0].parent/url.path()
                target=target.resolve()
                if AREA.resolve() not in target.parents or not target.is_file():return
                if target.suffix.lower() not in ('.md','.json','.py','.txt'):return
                content=target.read_text(encoding='utf-8');current[0]=target
                if target.suffix.lower()=='.md':view.setMarkdown(content)
                else:view.setPlainText(content)
                w.setWindowTitle(target.name)
            view.anchorClicked.connect(lambda url:self.guarded(lambda:follow(url)))
            l.addWidget(view);w.setAttribute(Qt.WA_DeleteOnClose);w.show()
        self.guarded(show)

    def submit(self,fn,kind,done):self.jobs.append((self.pool.submit(fn),kind,done))

    def guarded(self,fn):
        try:return fn()
        except Exception as exc:self.notice('No pude completar la acción',str(exc))

    def notice(self,title,text):QMessageBox.information(self,title,text)

    def refresh(self):
        v=source_view(self.source);self.origin.setText(v['badge']);self.data_title.setText(v['title']);self.data_detail.setText(v['detail'])
        color={'idle':'#E8EDF5','usb':'#DDF1EA','pc':'#FFF0D8','replay':'#E9E5F8'}[v['mode']]
        if v['mode']=='usb' and v['old']:color='#FBEBDD'
        self.origin.setStyleSheet('background:'+color+';')
        active=bool(self.source and not self.source.closed)
        self.sources_panel.setVisible(not active)
        self.connect_btn.setEnabled(not active);self.pc_btn.setEnabled(not active);self.replay_btn.setEnabled(not active);self.stop_btn.setEnabled(active and not self.source.stopping)
        self.run_btn.setEnabled(bool(self.source and self.source.mode=='usb' and not self.source.stopping and controls(v['snapshot'])['RUN']))
        for key,w in self.metric_values.items():w.setText(v['values'].get(key,'—'));w.setStyleSheet('color: #8A96A8;' if v['old'] else '')
        self.plot.historical=v['old']
        if self.source:
            while True:
                try:
                    segment,p=self.source.engine.updates.get_nowait();self.plot.points.append((segment,p.count,float(p.data['ALTITUDE'])));self.telemetry.add_packet(segment,p)
                except queue.Empty:break
        self.plot.update();s=v['snapshot']
        sample_data=(s.get('latest') or s.get('last_sample') or {}) if s else {}
        stage=STATES.get(sample_data.get('STATE'),sample_data.get('STATE','Sin etapa de misión'))
        self.phase.setText(('Etapa conservada · ' if v['old'] and sample_data else 'Etapa · ')+stage)
        if sample_data.get('GPS_SATS')=='0':self.metric_values['GPS_SATS'].setText('Sin posición')
        if s:
            csv=next((w for w in s['storage'] if w['kind']=='csv'),{})
            received=s['frames_received']-s['control_received']-s['diagnostics']
            self.counts.setText(f"Recibidos: {received}  ·  Válidos: {s['total_valid']}  ·  Guardados: {csv.get('saved',0)}  ·  Por guardar: {csv.get('pending',0)}  ·  Huecos: {v['gaps']}")
            self.freshness.setText(('ÚLTIMA MUESTRA CONSERVADA · ' if v['old'] else 'Último dato recibido hace ')+v['age']+(' · Durante el corte, faltantes por determinar.' if v['mode']=='usb' and not s['transport_connected'] else ''))
            errors=[w['error'] for w in s['storage'] if w['error']]
            if errors:self.freshness.setText(self.freshness.text()+' · Problema de guardado: '+'; '.join(errors))
            if s['commands']:self.freshness.setToolTip(command_text(s['commands'][-1],s['epoch']))
        self.packet_btn.setEnabled(bool(s and (s.get('latest') or s.get('last_sample'))))
        self.telemetry.refresh(v)
        for job in list(self.jobs):
            future,kind,done=job
            if future.done():
                self.jobs.remove(job)
                try:done(future.result())
                except Exception as exc:
                    if kind=='camera':
                        n=self.camera_busy;self.camera_busy=None;self.camera_started=None
                        if n:
                            self.photo_badges[n].setText('FOTO ANTERIOR · CAPTURA NO CONFIRMADA');self.camera_notes[n].setText('La solicitud falló. La imagen mostrada no es una foto nueva.')
                        self.camera_summary.setText('No pude confirmar la comprobación: '+str(exc))
                    elif kind=='experiment':
                        self.experiments.campaign_status.setText('Campaña incompleta: '+str(exc));self.experiments.campaign_button.setEnabled(True)
                    else:self.recovery_result.setText('No pude completar la prueba: '+str(exc))
        for b in [*self.camera_action_buttons,*self.sequence_buttons.values()]:b.setEnabled(not any(kind=='camera' for _,kind,_ in self.jobs))
        if self.camera_busy is not None and self.camera_started is not None:
            elapsed=time.monotonic()-self.camera_started
            self.camera_summary.setText(f'Cámara {self.camera_busy} · {self.camera_operation} en curso · {elapsed:.1f} s. No desconectes la placa ni retires la SD.')
        if self.closing and not self.jobs and (not self.source or self.source.closed):self.close()

    def closeEvent(self,event):
        if self.jobs or (self.source and not self.source.closed):
            self.closing=True
            if self.source:self.source.stop()
            self.data_title.setText('Conservando el trabajo antes de cerrar…');event.ignore();return
        self.camera_live.stop();self.camera_live.timer.stop()
        self.timer.stop();self.port_timer.stop();self.pool.shutdown(wait=False);event.accept()


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--config',type=Path);p.add_argument('--page',choices=['recorrido','datos','camaras','radio','recuperacion','ensayos','evidencias'],default='recorrido');args=p.parse_args()
    config=json.loads(args.config.read_text(encoding='utf-8-sig')) if args.config else {}
    app=QApplication(sys.argv);app.setFont(QFont('Segoe UI',10));w=Laboratory(config);w.go(args.page);w.show();sys.exit(app.exec())

if __name__=='__main__':main()
