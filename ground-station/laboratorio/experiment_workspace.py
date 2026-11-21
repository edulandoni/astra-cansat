"""ASTRA-41: cálculos existentes y archivo completo de evidencia local."""
import csv
import importlib.util
import io
import json
from pathlib import Path
import uuid
from datetime import datetime,timezone
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget,QTabWidget,QVBoxLayout,QHBoxLayout,QFormLayout,
    QLineEdit,QDoubleSpinBox,QPushButton,QLabel,QTreeWidget,QTreeWidgetItem,QSplitter,
    QPlainTextEdit,QComboBox,QTableWidget,QTableWidgetItem,QHeaderView,QAbstractItemView)
from runtime import AREA
from link_budget import evaluate as link_evaluate,FIELDS as LINK_FIELDS


def load_rotor():
    spec=importlib.util.spec_from_file_location('astra_rotor_net',AREA/'experiments/2026-10-24-rotor-neto/evaluar.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module.evaluate


def software_campaign():
    def load(name,path):
        spec=importlib.util.spec_from_file_location(name,AREA/path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
    quality=load('astra_quality_campaign','experiments/2026-10-24-calidad/evaluar.py')
    policy=load('astra_destination_campaign','experiments/2026-10-24-destinos/politica.py')
    results=[];traces=[]
    for case in quality.CASES:
        result,trace=quality.run_case(*case);results.append(result);traces.extend(trace)
    return dict(origin='Reloj virtual y metadatos ficticios; sin USB ni RF',quality=results,traces=traces,
                destination=policy.run(),limits='No mide latencia física, confiabilidad estadística ni autenticación de radio.')


class ExperimentWorkspace(QTabWidget):
    def __init__(self,owner):
        super().__init__();self.owner=owner;self.setMinimumHeight(650);self.current_result=None
        link=QWidget();l=QVBoxLayout(link);l.addWidget(QLabel('Referencia de espacio libre. Las entradas vacías permanecen TBD. No configura RF.'))
        form=QFormLayout();self.link_inputs={}
        labels=['Frecuencia · MHz','Distancia · m','Potencia TX · dBm','Ganancia TX · dBi','Ganancia RX · dBi','Pérdida cable TX · dB','Pérdida cable RX · dB','Pérdida polarización · dB','Otras pérdidas · dB','Sensibilidad RX · dBm','Margen requerido · dB']
        for key,label in zip(LINK_FIELDS,labels):
            field=QLineEdit();field.setPlaceholderText('TBD');form.addRow(label,field);self.link_inputs[key]=field
        l.addLayout(form);actions=QHBoxLayout()
        b=QPushButton('Calcular presupuesto de enlace');b.clicked.connect(lambda:owner.guarded(self.calculate_link));actions.addWidget(b)
        ex=QPushButton('Cargar ejemplo hipotético');ex.clicked.connect(self.example_link);actions.addWidget(ex);l.addLayout(actions)
        self.link_result=QLabel('Sin cálculo ejecutado.');self.link_result.setWordWrap(True);l.addWidget(self.link_result);self.addTab(link,'Presupuesto de enlace')
        rotor=QWidget();r=QVBoxLayout(rotor);r.addWidget(QLabel('MODELO HIPOTÉTICO · No valida aerodinámica, despliegue ni generación eléctrica física.'))
        rf=QFormLayout();self.rotor_inputs={}
        for key,label,value,maximum in [('mass_kg','Masa total · kg',.5,100),('height_m','Tramo de descenso · m',400,10000),('descent_m_s','Velocidad de descenso · m/s',5,1000),('efficiency','Eficiencia global · fracción',.1,1),('extra_load_w','Carga adicional · W',.2,1000),('standby_s','Espera con carga adicional · s',0,1000000)]:
            spin=QDoubleSpinBox();spin.setDecimals(4);spin.setRange(0,maximum);spin.setValue(value);rf.addRow(label,spin);self.rotor_inputs[key]=spin
        r.addLayout(rf);calc=QPushButton('Calcular balance incremental');calc.clicked.connect(lambda:owner.guarded(self.calculate_rotor));r.addWidget(calc)
        self.rotor_result=QLabel('Sin cálculo ejecutado.');self.rotor_result.setWordWrap(True);r.addWidget(self.rotor_result);r.addStretch();self.addTab(rotor,'Rotor y energía')
        archive=QWidget();a=QVBoxLayout(archive);a.addWidget(QLabel('Archivos completos de evidencia, configuración y documentación. Sólo lectura.'))
        self.search=QLineEdit();self.search.setPlaceholderText('Filtrar por nombre o ruta');self.search.textChanged.connect(self.filter_files);a.addWidget(self.search)
        split=QSplitter();self.files=QTreeWidget();self.files.setHeaderLabel('Archivo del proyecto');split.addWidget(self.files)
        right=QWidget();rr=QVBoxLayout(right);self.collection=QComboBox();self.collection.currentIndexChanged.connect(self.show_records);rr.addWidget(self.collection)
        self.record_table=QTableWidget();self.record_table.setEditTriggers(QAbstractItemView.NoEditTriggers);self.record_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents);rr.addWidget(self.record_table)
        self.raw=QPlainTextEdit();self.raw.setReadOnly(True);rr.addWidget(self.raw);split.addWidget(right);split.setStretchFactor(1,2);a.addWidget(split)
        self.files.itemDoubleClicked.connect(lambda item,col:self.owner.guarded(lambda:self.read_file(item)))
        self.addTab(archive,'Resultados y fuentes');self.populate_files();self.collections={}
        campaign=QWidget();cl=QVBoxLayout(campaign)
        description=QLabel('Ensayo de software: seis casos de calidad con reloj virtual y once decisiones de destino. Se prueban altura constante, GPS ausente, relojes congelados y enlace activo sin mediciones. No abre puertos ni transmite radio.');description.setWordWrap(True);cl.addWidget(description)
        self.campaign_button=QPushButton('Ejecutar campaña de software');self.campaign_button.clicked.connect(self.run_campaign);cl.addWidget(self.campaign_button)
        self.campaign_status=QLabel('Sin campaña ejecutada en esta sesión.');self.campaign_status.setWordWrap(True);cl.addWidget(self.campaign_status)
        self.campaign_table=QTableWidget(0,4);self.campaign_table.setHorizontalHeaderLabels(['Caso','Resultado','Demora · s virtuales','Observaciones fuera del fallo'])
        self.campaign_table.setEditTriggers(QAbstractItemView.NoEditTriggers);self.campaign_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);cl.addWidget(self.campaign_table)
        cl.addWidget(QLabel('Conservo el detalle completo, las trazas temporales y los once vectores en un archivo nuevo.'))
        self.addTab(campaign,'Calidad y direccionamiento')

    def run_campaign(self):
        if any(kind=='experiment' for _,kind,_ in self.owner.jobs):return
        self.campaign_button.setEnabled(False);self.campaign_status.setText('Ejecutando casos de software…')
        def done(result):
            path=self.save_result('calidad-destinos',result);quality=result['quality'];vectors=result['destination']['vectors']
            data=[(r['case'],'Correcto' if r['passed'] else 'Revisar',r['detection_delay_from_first_fault_s'],r['unexpected_positive_observations']) for r in quality]
            data.extend((r['case'],'Correcto' if r['passed'] else 'Revisar','—',r['actual']) for r in vectors)
            self.campaign_table.setRowCount(len(data))
            for i,row in enumerate(data):
                for j,value in enumerate(row):self.campaign_table.setItem(i,j,QTableWidgetItem('—' if value is None else str(value)))
            self.campaign_status.setText(f"Calidad: {sum(r['passed'] for r in quality)}/6 · Destino: {sum(r['passed'] for r in vectors)}/11.\nArchivo: {path}")
            self.campaign_button.setEnabled(True)
        self.owner.submit(software_campaign,'experiment',done)

    def filter_files(self,query):
        query=query.casefold().strip()
        def visit(item,prefix=''):
            path=prefix+'/'+item.text(0);own=query in path.casefold()
            matches=[visit(item.child(i),path) for i in range(item.childCount())]
            visible=own or any(matches);item.setHidden(not visible)
            if query and matches:item.setExpanded(visible)
            return visible
        for i in range(self.files.topLevelItemCount()):visit(self.files.topLevelItem(i))

    def save_result(self,kind,result):
        result=dict(result,recorded_utc=datetime.now(timezone.utc).isoformat(),experiment=kind,origin='Cálculo hipotético; no medición física')
        folder=self.owner.output/'calculos';folder.mkdir(parents=True,exist_ok=True)
        path=folder/(kind+'_'+uuid.uuid4().hex+'.json')
        with path.open('x',encoding='utf-8') as h:json.dump(result,h,ensure_ascii=False,indent=2)
        self.current_result=result;return path

    def example_link(self):
        for key,value in zip(LINK_FIELDS,[915,1000,10,2,2,1,1,3,2,-120,6]):self.link_inputs[key].setText(str(value))
        self.link_result.setText('Ejemplo hipotético cargado. Ningún valor es una medición ni un perfil aprobado.')

    def calculate_link(self):
        values={k:float(w.text().replace(',','.')) if w.text().strip() else None for k,w in self.link_inputs.items()}
        result=link_evaluate(dict(label='Hipótesis de laboratorio',example_only=True,values=values,sources={k:'Hipótesis ingresada manualmente; no parámetro aprobado' for k,v in values.items() if v is not None}))
        path=self.save_result('enlace',result)
        fmt=lambda key:'TBD' if result[key] is None else f'{result[key]:.3f}'
        self.link_result.setText(f"Pérdida de espacio libre: {fmt('fspl_db')} dB\nPotencia recibida calculada: {fmt('received_power_dbm')} dBm\nMargen: {fmt('margin_db')} dB\nEntradas pendientes: {', '.join(result['missing']) or 'ninguna'}\nArchivo nuevo: {path.name}")

    def calculate_rotor(self):
        result=load_rotor()(**{k:w.value() for k,w in self.rotor_inputs.items()});path=self.save_result('rotor',result)
        self.rotor_result.setText(f"Duración del tramo: {result['active_seconds']:.2f} s\nGeneración hipotética: {result['generated_wh']:.6f} Wh\nConsumo adicional: {result['incremental_consumption_wh']:.6f} Wh\nBalance incremental: {result['net_incremental_wh']:.6f} Wh\nArchivo nuevo: {path.name}")

    def populate_files(self):
        self.files.clear()
        for folder in ('evidence','config','docs'):
            root=AREA/folder;node=QTreeWidgetItem([folder]);self.files.addTopLevelItem(node);parents={root:node}
            for path in sorted(root.rglob('*')):
                if path.is_file() and path.suffix.lower() in ('.json','.jsonl','.csv','.md','.txt'):
                    for parent in reversed(path.parent.parents):
                        if parent!=root and root not in parent.parents:continue
                        if parent not in parents:parents[parent]=QTreeWidgetItem(parents[parent.parent],[parent.name])
                    if path.parent not in parents:parents[path.parent]=QTreeWidgetItem(parents[path.parent.parent],[path.parent.name])
                    item=QTreeWidgetItem(parents[path.parent],[path.name]);item.setData(0,Qt.UserRole,str(path))

    def read_file(self,item):
        name=item.data(0,Qt.UserRole)
        if not name:return
        path=Path(name).resolve()
        if AREA.resolve() not in path.parents:raise ValueError('Archivo fuera del proyecto')
        if path.stat().st_size>8*1024*1024:raise ValueError('Archivo mayor de 8 MiB; abrir desde la carpeta para conservar lectura completa.')
        source=path.read_text(encoding='utf-8-sig');self.raw.setPlainText(source);self.collections={};self.collection.clear()
        if path.suffix=='.json':
            obj=json.loads(source)
            def visit(value,prefix='raíz'):
                if isinstance(value,list) and value and all(isinstance(row,dict) for row in value):self.collections[prefix]=value
                elif isinstance(value,dict):
                    for k,v in value.items():visit(v,prefix+'/'+k)
            visit(obj)
        elif path.suffix=='.csv':self.collections['CSV']=list(csv.DictReader(io.StringIO(source)))
        elif path.suffix=='.jsonl':self.collections['JSONL']=[json.loads(line) for line in source.splitlines() if line.strip()]
        for key in self.collections:self.collection.addItem(key)
        if not self.collections:self.record_table.setRowCount(0)

    def show_records(self,*_):
        data=getattr(self,'collections',{}).get(self.collection.currentText(),[])
        keys=list(dict.fromkeys(k for row in data if isinstance(row,dict) for k in row))
        self.record_table.setColumnCount(len(keys));self.record_table.setHorizontalHeaderLabels(keys);self.record_table.setRowCount(len(data))
        for i,row in enumerate(data):
            for j,k in enumerate(keys):
                value=row.get(k,'') if isinstance(row,dict) else row
                self.record_table.setItem(i,j,QTableWidgetItem(json.dumps(value,ensure_ascii=False) if isinstance(value,(dict,list)) else str(value)))
