"""ASTRA-22/21: variables completas, series, control, almacenamiento y diagnóstico."""
from collections import deque
from datetime import datetime,timezone
import json
import math
from pathlib import Path
from PySide6.QtCore import Qt,QPointF,QUrl
from PySide6.QtGui import QPainter,QPen,QColor,QPainterPath,QDesktopServices
from PySide6.QtWidgets import (QWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QTabWidget,
    QScrollArea,QLabel,QPushButton,QComboBox,QTableWidget,QTableWidgetItem,QHeaderView,
    QAbstractItemView,QPlainTextEdit,QFileDialog)
from engine import display
from ui_model import FIELDS_INFO,controls,OPS,command_text,interruption_text

SPECS=[('Altura barométrica · m',('ALTITUDE',)),('Presión · kPa',('PRESSURE',)),
       ('Temperatura · °C',('TEMPERATURE',)),('Tensión de batería · V',('VOLTAGE',)),
       ('Corriente · A',('CURRENT',)),('Velocidad angular · rad/s',('GYRO_R','GYRO_P','GYRO_Y')),
       ('Aceleración · m/s²',('ACCEL_R','ACCEL_P','ACCEL_Y')),('Altura GPS · m s. n. m.',('GPS_ALTITUDE',)),
       ('Satélites GPS',('GPS_SATS',)),('Latitud · °',('GPS_LATITUDE',)),('Longitud · °',('GPS_LONGITUDE',))]


def text(value=''):
    w=QLabel(value);w.setWordWrap(True);w.setTextFormat(Qt.PlainText);return w


def grid_table(headers):
    w=QTableWidget(0,len(headers));w.setHorizontalHeaderLabels(headers)
    w.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);w.verticalHeader().hide()
    w.setEditTriggers(QAbstractItemView.NoEditTriggers);w.setAlternatingRowColors(True);w.setShowGrid(False)
    w.setSelectionBehavior(QAbstractItemView.SelectRows);return w


def rows(table,values):
    table.setRowCount(len(values))
    for i,row in enumerate(values):
        for j,value in enumerate(row):table.setItem(i,j,QTableWidgetItem(str(value)))


class SeriesPlot(QWidget):
    COLORS=('#087F73','#4976CC','#C47B20')
    def __init__(self,title,keys):
        super().__init__();self.title=title;self.keys=keys;self.points=deque(maxlen=180);self.old=True
        self.setMinimumHeight(230);self.setMinimumWidth(270)

    def add(self,segment,count,data):
        values=[]
        for key in self.keys:
            value=data.get(key)
            if key.startswith('GPS_') and key!='GPS_SATS' and data.get('GPS_SATS')=='0':value=None
            try:value=float(value) if value is not None else None
            except (TypeError,ValueError):value=None
            values.append(value if value is None or math.isfinite(value) else None)
        self.points.append((segment,count,values))

    def paintEvent(self,event):
        p=QPainter(self);p.setRenderHint(QPainter.Antialiasing);p.fillRect(self.rect(),QColor('white'))
        p.setPen(QColor('#24334B'));p.drawText(12,22,self.title)
        all_values=[v for _,_,values in self.points for v in values if v is not None]
        if not all_values:p.setPen(QColor('#7D8BA0'));p.drawText(self.rect(),Qt.AlignCenter,'Sin muestras válidas');return
        lo=min(all_values);hi=max(all_values);span=hi-lo
        if span<1e-9:span=max(abs(hi)*.02,.01)
        lo-=span*.08;hi+=span*.08
        left=68;right=self.width()-18;top=42;bottom=self.height()-36
        for i in range(3):
            y=top+i*(bottom-top)/2;value=hi-i*(hi-lo)/2
            p.setPen(QColor('#EDF0F5'));p.drawLine(left,int(y),right,int(y))
            p.setPen(QColor('#65758D'));p.drawText(2,int(y)-8,60,20,Qt.AlignRight,f'{value:.4g}')
        first=min(v[1] for v in self.points);last=max(v[1] for v in self.points)
        p.drawText(left,bottom+22,f'contador {first}–{last}')
        for series,key in enumerate(self.keys):
            color=QColor('#9BA7B8' if self.old else self.COLORS[series%3]);p.setPen(QPen(color,2))
            path=QPainterPath();previous=None
            for segment,count,values in self.points:
                value=values[series]
                if value is None:previous=None;continue
                point=QPointF(left+(count-first)/max(last-first,1)*(right-left),bottom-(value-lo)/(hi-lo)*(bottom-top))
                if previous and previous==(segment,count-1):path.lineTo(point)
                else:path.moveTo(point)
                previous=(segment,count)
            p.drawPath(path)
            p.drawText(12+series*90,self.height()-4,key.split('_')[-1] if len(self.keys)>1 else ('histórico' if self.old else 'actual'))


class TelemetryWorkspace(QTabWidget):
    def __init__(self,owner):
        super().__init__();self.owner=owner;self.segment=None;self.last_variables=None;self.last_commands=None;self.last_seq=None
        self.setMinimumHeight(620)
        self.variables=grid_table(['Variable','Valor','Condición']);self.variables.setRowCount(len(FIELDS_INFO))
        for i,(key,(name,unit,help_text)) in enumerate(FIELDS_INFO.items()):
            self.variables.setItem(i,0,QTableWidgetItem(name));self.variables.item(i,0).setToolTip(key+'\n'+help_text)
        self.addTab(self.variables,'Variables (22)')
        scroll=QScrollArea();scroll.setWidgetResizable(True);graph_page=QWidget();graph_grid=QGridLayout(graph_page)
        graph_grid.addWidget(text('Últimas 180 muestras del segmento actual. Los cortes no se unen. El registro completo queda en los archivos de la sesión.'),0,0,1,2)
        self.plots=[]
        for i,(title,keys) in enumerate(SPECS):
            plot=SeriesPlot(title,keys);self.plots.append(plot);graph_grid.addWidget(plot,1+i//2,i%2)
        scroll.setWidget(graph_page);self.addTab(scroll,'Gráficos (11)')
        command_page=QWidget();c=QVBoxLayout(command_page)
        c.addWidget(text('Comandos del perfil de banco. La reproducción de registros no envía órdenes.'))
        self.scenario=QComboBox()
        for name,value in [('Nominal','NOMINAL'),('Pérdidas','PACKET_LOSS'),('Datos corruptos','CORRUPTED_PACKET'),('GPS sin solución','GPS_LOSS'),('Omisión lógica','RESET')]:self.scenario.addItem(name,value)
        c.addWidget(self.scenario);bar=QHBoxLayout();self.command_buttons={}
        for op,title in [('RUN','Iniciar'),('STOP','Detener emisión'),('CAL_ZERO','Altura cero'),('SET_TIME','Hora UTC'),('POWER_STATUS','Batería y solar')]:
            b=QPushButton(title);b.clicked.connect(lambda checked=False,operation=op:self.send(operation));bar.addWidget(b);self.command_buttons[op]=b
        c.addLayout(bar);self.power=text('Sin respuesta de energía.');c.addWidget(self.power)
        self.commands=grid_table(['Identificador','Orden','Resultado']);c.addWidget(self.commands)
        self.repeat=QPushButton('Repetir identificador seleccionado · banco');self.repeat.clicked.connect(self.repeat_selected);c.addWidget(self.repeat)
        c.addWidget(text('Repetir usa el mismo ID para ensayar deduplicación. No hay reintentos automáticos. Enviar, aceptar y ejecutar son estados diferentes.'))
        self.addTab(command_page,'Comandos')
        storage_page=QWidget();st=QVBoxLayout(storage_page)
        self.backup=text('Segundo destino: no configurado.');st.addWidget(self.backup)
        self.backup_button=QPushButton('Seleccionar segundo destino…');self.backup_button.clicked.connect(self.choose_backup);st.addWidget(self.backup_button)
        self.no_backup=QPushButton('Usar sólo destino principal');self.no_backup.clicked.connect(self.clear_backup);st.addWidget(self.no_backup)
        st.addWidget(text('Dos carpetas no prueban soportes independientes. El destino se aplica a la próxima sesión; nunca se formatea ni se reemplazan archivos anteriores.'))
        self.storage=grid_table(['Destino','Registro','Guardados','Pendientes','Descartados','Error']);st.addWidget(self.storage)
        self.open_folder=QPushButton('Abrir archivos de la sesión');self.open_folder.clicked.connect(self.open_session);st.addWidget(self.open_folder)
        self.paths=text();st.addWidget(self.paths);self.addTab(storage_page,'Guardado')
        diag_page=QWidget();dg=QVBoxLayout(diag_page);self.identity=text();dg.addWidget(self.identity)
        self.quality=text();dg.addWidget(self.quality);self.interruptions=grid_table(['Corte','Estado y resultado']);dg.addWidget(self.interruptions)
        self.addTab(diag_page,'Diagnóstico')
        self.raw=QPlainTextEdit();self.raw.setReadOnly(True);self.raw.setMaximumBlockCount(300);self.addTab(self.raw,'Tramas')

    def reset(self):
        self.segment=None;self.last_variables=None;self.last_commands=None;self.last_seq=None
        for plot in self.plots:plot.points.clear();plot.update()
        self.raw.clear()

    def add_packet(self,segment,packet):
        if self.segment is not None and self.segment!=segment:
            for plot in self.plots:plot.points.clear()
        self.segment=segment;values=display(packet.data)
        for plot in self.plots:plot.add(segment,packet.count,values)

    def send(self,op):
        args={}
        if op=='RUN':args=dict(scenario=self.scenario.currentData(),samples=131)
        if op=='SET_TIME':
            now=datetime.now(timezone.utc);args=dict(utc_seconds=now.hour*3600+now.minute*60+now.second)
        self.owner.order(op,**args)

    def repeat_selected(self):
        source=self.owner.source;row=self.commands.currentRow()
        if source and row>=0 and self.commands.item(row,0):
            ident=self.commands.item(row,0).data(Qt.UserRole)
            self.owner.guarded(lambda:source.engine.repeat(ident))

    def choose_backup(self):
        folder=QFileDialog.getExistingDirectory(self,'Segundo destino de la próxima sesión')
        if folder:self.owner.backup_path=Path(folder);self.backup.setText('Segundo destino: '+folder)

    def clear_backup(self):self.owner.backup_path=None;self.backup.setText('Segundo destino: no configurado.')

    def open_session(self):
        if self.owner.source:QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.owner.source.store.roots[0])))

    def refresh(self,view):
        s=view['snapshot'];source=self.owner.source;active=bool(source and not source.closed)
        self.backup_button.setEnabled(not active);self.no_backup.setEnabled(not active);self.open_folder.setEnabled(source is not None)
        values=view['values'];signature=(tuple(values.items()),view['old'],view['mode'])
        if signature!=self.last_variables:
            self.last_variables=signature
            raw=(s.get('latest') or s.get('last_sample') or {}) if s else {}
            for i,key in enumerate(FIELDS_INFO):
                value=values.get(key,'—');condition='Sin muestra' if not raw else ('Histórica' if view['old'] else 'Actual')
                if view['mode']=='replay' and raw:condition='Registro reproducido'
                if key.startswith('GPS_') and key!='GPS_SATS' and raw.get('GPS_SATS')=='0':condition='Sin solución · última válida'
                self.variables.setItem(i,1,QTableWidgetItem(value));self.variables.setItem(i,2,QTableWidgetItem(condition))
        flags=controls(s) if s else {}
        for op,b in self.command_buttons.items():b.setEnabled(bool(active and not source.stopping and flags.get(op)))
        self.repeat.setEnabled(bool(active and not source.stopping and view['mode']!='replay' and s.get('peer')))
        for plot in self.plots:
            plot.old=view['old'] or bool(s and (s.get('latest') or {}).get('GPS_SATS')=='0' and plot.keys[0].startswith('GPS_') and plot.keys!=('GPS_SATS',))
            plot.update()
        if not s:return
        power=s.get('power') or {}
        self.power.setText('Batería: '+str(power.get('voltage','—'))+' V · Solar: '+str(power.get('solar_voltage','—'))+' V · respuesta sintética de banco')
        commands=s['commands'];signature=json.dumps(commands,sort_keys=True,default=str)
        if signature!=self.last_commands:
            self.last_commands=signature;rows(self.commands,[(c['id'].rsplit(':',1)[-1],OPS.get(c['op'],c['op']),command_text(c,s['epoch'])) for c in commands])
            for i,c in enumerate(commands):self.commands.item(i,0).setData(Qt.UserRole,c['id']);self.commands.item(i,0).setToolTip(c['id'])
        rows(self.storage,[(('Principal' if w['destination']==0 else 'Copia'),('Original' if w['kind']=='raw' else 'CSV'),w['saved'],w['pending'],w['dropped'],w['error'] or '—') for w in s['storage']])
        self.paths.setText('\n'.join(str(p) for p in source.store.roots))
        self.identity.setText(f"Sesión PC: {s['session']}\nArranque / misión: {s['epoch'] or 'sin confirmar'}\nSegmento: {s['segment']}")
        self.quality.setText(f"Edad de muestra: {view['age']} · Edad GPS: {s.get('gps_age')} s\nDuplicados: {s['duplicates']} · Conflictos: {s['conflicts']} · Rechazados: {s['invalid']} · Hora sin avanzar: {'sí' if s['clock_warning'] else 'no'}\nFuente: {view['badge']}")
        rows(self.interruptions,[(c['number'],interruption_text(c)) for c in s['interruptions']])
        events=source.event_snapshot()
        if events and events[-1]['seq']!=self.last_seq:
            self.last_seq=events[-1]['seq'];lines=[]
            for event in events:
                line=dict(event)
                if event['kind']=='wire':line['ascii']=bytes.fromhex(event['raw_hex']).decode('ascii',errors='replace')
                lines.append(json.dumps(line,ensure_ascii=False,default=str))
            self.raw.setPlainText('\n'.join(lines));bar=self.raw.verticalScrollBar();bar.setValue(bar.maximum())
