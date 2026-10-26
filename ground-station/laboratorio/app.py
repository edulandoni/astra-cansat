"""ASTRA-41 — Laboratorio nativo, sin acceso automático a hardware."""
import argparse
import json
import os
import subprocess
import sys
import threading
import queue
import tkinter as tk
import webbrowser
from collections import deque
from pathlib import Path
from tkinter import ttk, messagebox
from content import CHAPTERS, REPORTS
from runtime import AREA, Simulation, packet_at, radio_rows, recovery_demo, chart_runs
from ui_model import FIELDS_INFO, STATES


class Laboratory:
    def __init__(self, root, config=None):
        self.root = root
        self.config = config or {}
        self.output = Path(self.config.get('output', Path.home() / 'ASTRA-Laboratorio' / 'ensayos'))
        self.sim = None
        self.closing = False
        self.children = {}
        self.points = deque(maxlen=180)
        self.last_point = None
        self.images = []
        self.recovery_busy=False
        self.recovery_result=None
        root.title('ASTRA — Laboratorio')
        root.geometry('1180x850')
        root.minsize(1020, 720)
        root.configure(bg='#edf2f7')
        style = ttk.Style(root)
        style.theme_use('clam')
        style.configure('TFrame', background='#edf2f7')
        style.configure('TLabel', background='#edf2f7', foreground='#172a43', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10), padding=6)
        style.configure('TNotebook.Tab', font=('Segoe UI', 10), padding=(12, 9))
        ttk.Label(root, text='ASTRA  /  Laboratorio', font=('Segoe UI', 22, 'bold')).pack(anchor='w', padx=22, pady=(14, 3))
        ttk.Label(root, text='Demostrar • entender • comprobar     |     Sin conexiones automáticas a placas').pack(anchor='w', padx=24, pady=(0, 12))
        self.book = ttk.Notebook(root)
        self.book.pack(fill='both', expand=True, padx=18)
        self.frames = {}
        self.details = {}
        for key, title, simple, technical in CHAPTERS:
            frame = ttk.Frame(self.book, padding=12)
            self.book.add(frame, text=key)
            self.frames[key] = frame
            ttk.Label(frame, text=title, font=('Segoe UI', 16, 'bold')).pack(anchor='w', pady=(0, 8))
            # Cada explicación tiene desplazamiento propio y se puede seleccionar/copiar.
            explanation = self.text(frame, simple, height=8 if key != 'Recorrido' else 15)
            button = ttk.Button(frame, text='Ver fundamento, alcance y detalle técnico')
            button.configure(command=lambda box=explanation, b=button, s=simple, t=technical: self.toggle(box, b, s, t))
            button.pack(anchor='w', pady=5)
            self.details[key] = (explanation, button)
        self.build_tour()
        self.build_telemetry()
        self.build_packet()
        self.build_cameras()
        self.build_radio()
        self.build_evidence()
        self.build_recovery()
        self.footer = ttk.Label(root, text='Elegí una sección. Los botones de hardware abren bancos separados bajo demanda.')
        self.footer.pack(anchor='w', padx=22, pady=9)
        root.protocol('WM_DELETE_WINDOW', self.close)
        self.timer = root.after(200, self.refresh)

    def text(self, parent, content, height=8):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True)
        box = tk.Text(frame, height=height, wrap='word', font=('Segoe UI', 11), bg='white', fg='#20334b', relief='flat', padx=12, pady=10)
        bar = ttk.Scrollbar(frame, command=box.yview)
        box.configure(yscrollcommand=bar.set)
        bar.pack(side='right', fill='y')
        box.pack(fill='both', expand=True)
        box.insert('1.0', content)
        box.configure(state='disabled')
        return box

    def toggle(self, box, button, simple, technical):
        expanded=button.cget('text').startswith('Ocultar')
        box.configure(state='normal'); box.delete('1.0','end'); box.insert('1.0',simple)
        if not expanded:
            boundary=box.index('end-1c'); box.insert('end','\n\nFUNDAMENTO Y ALCANCE\n\n'+technical); box.see(boundary)
        else:box.yview_moveto(0)
        box.configure(state='disabled')
        button.configure(text='Ver fundamento, alcance y detalle técnico' if expanded else 'Ocultar detalle técnico')

    def build_tour(self):
        f = self.frames['Recorrido']
        row = ttk.Frame(f); row.pack(fill='x', pady=10)
        for key in ('Telemetría', 'Paquete', 'Cámaras', 'Radio LoRa', 'Recuperación', 'Evidencias'):
            ttk.Button(row, text=key, command=lambda k=key: self.book.select(self.frames[k])).pack(side='left', padx=3)
        ttk.Label(f, text='Las explicaciones y cálculos funcionan sin Internet. Las fotos requieren la evidencia local configurada.', wraplength=1000).pack(anchor='w')

    def build_telemetry(self):
        f = self.frames['Telemetría']
        row = ttk.Frame(f); row.pack(fill='x', pady=7)
        self.scenario = tk.StringVar(value='NOMINAL')
        ttk.Label(row, text='Escenario').pack(side='left')
        ttk.Combobox(row, textvariable=self.scenario, values=('NOMINAL', 'PACKET_LOSS', 'CORRUPTED_PACKET', 'GPS_LOSS', 'RESET'), state='readonly', width=22).pack(side='left', padx=6)
        self.speed = tk.StringVar(value='5')
        ttk.Label(row, text='Velocidad ×').pack(side='left')
        self.speed_box=ttk.Combobox(row, textvariable=self.speed, values=('1','5','10'), state='readonly', width=4)
        self.speed_box.pack(side='left', padx=6)
        self.start_button = ttk.Button(row, text='Iniciar misión de PC', command=self.start_sim)
        self.start_button.pack(side='left', padx=5)
        ttk.Button(row, text='Detener y conservar', command=self.stop_sim).pack(side='left')
        self.metrics = tk.StringVar(value='SIMULACIÓN DE PC • Sin misión iniciada')
        ttk.Label(f, textvariable=self.metrics, wraplength=1050, font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=7)
        self.measurements = tk.StringVar(value='Altura, temperatura y posición aparecerán al iniciar.')
        ttk.Label(f, textvariable=self.measurements, wraplength=1050).pack(anchor='w')
        self.graph = tk.Canvas(f, height=155, bg='white', highlightthickness=0)
        self.graph.pack(fill='x', pady=7)
        self.telemetry_note = tk.StringVar(value='PACKET_LOSS omite mensajes; CORRUPTED_PACKET invalida presión; GPS_LOSS retiene la última posición. RESET aquí es lógico.')
        ttk.Label(f, textvariable=self.telemetry_note, wraplength=1050).pack(anchor='w')
        launchers=ttk.Frame(f); launchers.pack(anchor='w',pady=5)
        ttk.Button(launchers, text='Abrir estación completa · PC', command=lambda: self.launch('telemetry')).pack(side='left',padx=(0,6))
        ttk.Button(launchers, text='Preparar recepción USB…', command=self.choose_usb).pack(side='left')

    def start_sim(self):
        if self.sim:
            messagebox.showinfo('Misión existente', 'Detené y conservá la misión antes de iniciar otra.'); return
        try:
            self.points.clear(); self.last_point=None
            self.sim = Simulation(self.output, self.scenario.get(), int(self.speed.get()))
            self.speed_box.configure(state='disabled')
            self.start_button.configure(state='disabled')
            self.footer.configure(text='Registros nuevos en: '+str(self.sim.store.roots[0]))
        except Exception as exc: messagebox.showerror('No se pudo iniciar', str(exc))

    def stop_sim(self):
        if not self.sim: return
        self.start_button.configure(state='disabled')
        self.telemetry_note.set('Conservando registros y cerrando escritores…')
        sim = self.sim
        def stop():
            try: sim.close(); self.stop_error=None
            except Exception as exc: self.stop_error=str(exc)
            self.stopped=True
        if getattr(self, 'stopping', False): return
        self.stopping=True; self.stopped=False
        threading.Thread(target=stop, daemon=True).start()

    def build_packet(self):
        f=self.frames['Paquete']
        self.packet_time=tk.DoubleVar(value=0)
        ttk.Label(f, text='Instante de misión simulado (0–130 segundos)').pack(anchor='w')
        ttk.Scale(f, from_=0, to=130, variable=self.packet_time, command=self.update_packet).pack(fill='x')
        self.packet_label=tk.StringVar()
        ttk.Label(f, textvariable=self.packet_label).pack(anchor='w')
        self.raw=self.text(f, '', height=2)
        self.fields=ttk.Treeview(f, columns=('field','value','meaning'), show='headings', height=5)
        for col,title,width in [('field','Campo',170),('value','Valor original',160),('meaning','Significado / unidad original',650)]:
            self.fields.heading(col,text=title); self.fields.column(col,width=width)
        scroll=ttk.Scrollbar(f, command=self.fields.yview); self.fields.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right',fill='y'); self.fields.pack(fill='both',expand=True)
        self.fields.bind('<<TreeviewSelect>>',self.explain_field)
        self.update_packet()

    def update_packet(self, *_):
        raw, rows=packet_at(self.packet_time.get())
        self.packet_label.set(f't = {int(self.packet_time.get())} s • {len(raw)} bytes / {len(raw)*8} bits • 22 campos • texto ASCII')
        self.raw.configure(state='normal'); self.raw.delete('1.0','end'); self.raw.insert('1.0',raw.decode().replace('\r','<CR>')); self.raw.configure(state='disabled')
        self.fields.delete(*self.fields.get_children())
        for key,value in rows:
            name,unit,_=FIELDS_INFO[key]
            if key.startswith('GYRO_'): unit='°/s (original)'
            self.fields.insert('', 'end', iid=key, values=(key,value,name+' — '+unit))

    def explain_field(self, _):
        selected=self.fields.selection()
        if selected:
            key=selected[0]; name,unit,explanation=FIELDS_INFO[key]
            if key.startswith('GYRO_'): explanation='El paquete conserva grados/s. La pantalla de telemetría los convierte explícitamente a rad/s. Describe velocidad de giro, no inclinación.'
            messagebox.showinfo(name, explanation)

    def build_cameras(self):
        f=self.frames['Cámaras']; row=ttk.Frame(f); row.pack(fill='both',expand=True)
        for number in (1,2):
            card=ttk.LabelFrame(row,text=f'Cámara {number} · evidencia conservada',padding=8)
            card.pack(side='left',fill='both',expand=True,padx=5)
            entry=self.config.get('photos',{}).get(str(number),{})
            path=Path(entry.get('path','__sin_evidencia__'))
            try:
                from PIL import Image, ImageTk
                with Image.open(path) as im:
                    im.load(); im.thumbnail((430,190)); picture=ImageTk.PhotoImage(im.copy())
                self.images.append(picture); ttk.Label(card,image=picture).pack()
                ttk.Label(card,text=entry.get('caption','Foto local conservada; no es captura nueva.'),wraplength=430).pack(anchor='w',pady=6)
            except (OSError,ValueError,ImportError): ttk.Label(card,text='Sin fotografía local configurada.\nEl informe de verificación sigue disponible.',wraplength=430).pack(pady=25)
        ttk.Button(f,text='Abrir chequeo físico de cámaras',command=lambda:self.launch('camera')).pack(anchor='w',pady=6)

    def build_radio(self):
        f=self.frames['Radio LoRa']; row=ttk.Frame(f); row.pack(fill='x',pady=6)
        self.payload=tk.StringVar(value='55'); self.bw=tk.StringVar(value='125'); self.cr=tk.StringVar(value='1')
        for label,var,values in [('Bytes propios',self.payload,('50','55','60','100','124','255')),('BW (kHz)',self.bw,('125','250','500')),('CR (1=4/5, 4=4/8)',self.cr,('1','2','3','4'))]:
            ttk.Label(row,text=label).pack(side='left',padx=5)
            combo=ttk.Combobox(row,textvariable=var,values=values,state='readonly',width=7); combo.pack(side='left'); combo.bind('<<ComboboxSelected>>',self.update_radio)
        self.radio_table=ttk.Treeview(f,columns=('sf','time','fraction','margin'),show='headings',height=5)
        for k,label in [('sf','SF'),('time','Tiempo transmitiendo'),('fraction','Ocupación a 1 Hz'),('margin','Margen dentro de 1 segundo')]: self.radio_table.heading(k,text=label); self.radio_table.column(k,width=240)
        self.radio_table.pack(fill='x',pady=8)
        self.radio_note=tk.StringVar()
        ttk.Label(f,textvariable=self.radio_note,wraplength=1050).pack(anchor='w')
        ttk.Button(f,text='Fuente: fabricante Semtech',command=lambda:webbrowser.open('https://www.semtech.com/design-support/faq/faq-lora')).pack(anchor='w',pady=6)
        self.update_radio()

    def update_radio(self,*_):
        self.radio_table.delete(*self.radio_table.get_children())
        for r in radio_rows(int(self.payload.get()),int(self.bw.get())*1000,int(self.cr.get())):
            seconds=r['airtime_seconds']
            self.radio_table.insert('', 'end', values=(r['sf'],f'{seconds*1000:.3f} ms',f'{seconds*100:.1f} %',f'{(1-seconds)*1000:.1f} ms' if seconds<1 else 'No entra a 1 Hz'))
        self.radio_note.set('CÁLCULO • Cabecera explícita, CRC, preámbulo 8. El margen es aritmético: todavía faltan guardas, comandos y reintentos. No mide pérdidas ni consumo y no configura radio.')

    def build_evidence(self):
        f=self.frames['Evidencias']
        for label,path in REPORTS:
            ttk.Button(f,text=label+' — abrir informe',command=lambda p=path:self.open_report(p)).pack(anchor='w',pady=2)
        ttk.Button(f,text='Abrir carpeta de ensayos del Laboratorio',command=self.open_output).pack(anchor='w',pady=5)

    def build_recovery(self):
        f=self.frames['Recuperación']; row=ttk.Frame(f); row.pack(fill='x',pady=8)
        self.recovery_mode=tk.StringVar(value='complementarias')
        ttk.Combobox(row,textvariable=self.recovery_mode,values=('complementarias','ausente_en_ambas','conflicto'),state='readonly',width=24).pack(side='left',padx=(0,10))
        self.recovery_button=ttk.Button(row,text='Probar reconstrucción',command=self.run_recovery)
        self.recovery_button.pack(side='left')
        self.recovery_status=tk.StringVar(value='SIMULACIÓN DE ARCHIVOS • Cada prueba crea dos fuentes ficticias nuevas en este disco.')
        ttk.Label(f,textvariable=self.recovery_status,wraplength=1000,font=('Segoe UI',11)).pack(anchor='w',pady=12)
        ttk.Button(f,text='Ver carpetas y originales de las pruebas',command=self.open_output).pack(anchor='w')

    def run_recovery(self):
        if self.recovery_busy:return
        self.recovery_busy=True; self.recovery_result=None
        self.recovery_button.configure(state='disabled')
        self.recovery_status.set('Creando fuentes sintéticas y ejecutando el recuperador…')
        mode=self.recovery_mode.get()
        def work():
            try:self.recovery_result=(True,recovery_demo(self.output,mode))
            except Exception as exc:self.recovery_result=(False,str(exc))
        threading.Thread(target=work,daemon=True).start()

    def open_report(self, relative):
        path=AREA/relative
        try: content=path.read_text(encoding='utf-8')
        except OSError as exc: messagebox.showerror('Informe no disponible',str(exc)); return
        window=tk.Toplevel(self.root); window.title(path.name); window.geometry('950x700')
        self.text(window,content,height=30)

    def open_output(self):
        self.output.mkdir(parents=True,exist_ok=True)
        os.startfile(self.output)

    def choose_usb(self):
        from serial.tools import list_ports
        ports=list(list_ports.comports())
        window=tk.Toplevel(self.root); window.title('Elegir placa de telemetría'); window.geometry('630x230')
        ttk.Label(window,text='Elegí explícitamente el ESP32 de telemetría. No selecciones una cámara.\nEste paso abrirá su puerto; no carga firmware ni pide reset.',wraplength=590).pack(padx=15,pady=15)
        labels={f'{p.device} — {p.description}':p.device for p in ports}
        choice=tk.StringVar()
        ttk.Combobox(window,textvariable=choice,values=list(labels),state='readonly',width=65).pack(padx=15,pady=10)
        def confirm():
            if choice.get() not in labels:return
            port=labels[choice.get()]; window.destroy(); self.launch('telemetry',port)
        ttk.Button(window,text='Abrir recepción de la placa seleccionada',command=confirm).pack()
        if not ports:ttk.Label(window,text='Sin puertos disponibles. Cerrá y volvé a intentar al conectar la placa.').pack(pady=8)

    def launch(self, kind, port=None):
        child=self.children.get(kind)
        if child and child.poll() is None:
            messagebox.showinfo('Banco abierto','La ventana del banco ya está abierta. Buscala en la barra de tareas.'); return
        args=[sys.executable]
        if kind=='telemetry':
            args += [str(AREA/'banco-usb-v0.2/app.py'),'--source','usb' if port else 'pc','--output',str(self.output/'estacion-completa')]
            if port:args += ['--port',port]
        else:
            registry=self.config.get('camera_registry')
            if not registry or not Path(registry).is_file():
                messagebox.showinfo('Preparación pendiente','Falta configurar el registro privado de cámaras. El recorrido y los informes funcionan sin conectar hardware.'); return
            args += [str(AREA/'camaras-banco/camera_panel.py'),'--registry',registry,'--output',str(self.output/'camaras')]
        try: self.children[kind]=subprocess.Popen(args,cwd=AREA)
        except OSError as exc: messagebox.showerror('No se pudo abrir el banco',str(exc))

    def refresh(self):
        if self.sim:
            s=self.sim.engine.snapshot(); values=s.get('latest') or {}
            storage=s['storage']; saved=next((w['saved'] for w in storage if w['kind']=='csv'),0)
            pending=sum(w['pending'] for w in storage); dropped=sum(w['dropped'] for w in storage)
            self.metrics.set(f"SIMULACIÓN DE PC ×{self.speed.get()}  |  Válidos: {s['total_valid']}  |  Inválidos: {s['invalid']}  |  Huecos de contador: {s['observed_gaps']}  |  CSV guardados: {saved}  |  Escrituras pendientes: {pending}  |  Descartes de escritura: {dropped}")
            if values:
                gps='sin solución; última posición retenida' if values['GPS_SATS']=='0' else values['GPS_SATS']+' satélites declarados'
                self.measurements.set(f"{STATES.get(values['STATE'],values['STATE'])}  •  Altura: {values['ALTITUDE']} m  •  Temperatura: {values['TEMPERATURE']} °C  •  Batería ficticia: {values['VOLTAGE']} V  •  GPS: {gps}")
                # Consumo todas las muestras de la cola; una actualización de GUI
                # puede incluir varias cuando la simulación está acelerada.
                while True:
                    try:
                        segment,packet=self.sim.engine.updates.get_nowait()
                        self.points.append((segment,packet.count,float(packet.data['ALTITUDE'])))
                    except queue.Empty:break
                self.graph.delete('all'); width=max(self.graph.winfo_width(),300)
                self.graph.create_text(10,12,text='Altura (m) • eje horizontal: contador • huecos sin unir',anchor='w',fill='#425873')
                self.graph.create_text(10,34,text='500',anchor='w'); self.graph.create_text(10,140,text='0',anchor='w')
                if self.points:
                    low=min(p[1] for p in self.points); high=max(p[1] for p in self.points)
                    for run in chart_runs(self.points):
                        coords=[]
                        for _,count,h in run:coords += [45+(count-low)*(width-65)/max(high-low,1),140-h/550*110]
                        if len(coords)>=4:self.graph.create_line(*coords,fill='#2379bd',width=3)
                        elif coords:self.graph.create_oval(coords[0]-2,coords[1]-2,coords[0]+2,coords[1]+2,fill='#2379bd',outline='')
            if s['done']: self.telemetry_note.set('Misión terminada. Los registros se conservan. Pulsá Detener y conservar para preparar otro escenario.')
            errors=[w['error'] for w in storage if w['error']]
            if errors:self.telemetry_note.set('Problema de escritura: '+'; '.join(errors))
        if getattr(self,'stopping',False) and self.stopped:
            self.sim=None; self.stopping=False; self.start_button.configure(state='normal')
            self.speed_box.configure(state='readonly')
            self.telemetry_note.set('Registros conservados.' if not self.stop_error else 'Cierre con error: '+self.stop_error)
        if self.recovery_busy and self.recovery_result is not None:
            ok,result=self.recovery_result
            self.recovery_busy=False; self.recovery_button.configure(state='normal')
            if ok:
                written='CSV nuevo creado' if result['written'] else 'RECONSTRUCCIÓN BLOQUEADA'
                missing=10-result['candidates']
                self.recovery_status.set(f"{written}. Datos presentes: {result['candidates']}/10. Ausentes en ambas fuentes: {missing}. Conflictos: {result['conflicts']}. Originales intactos: {'sí' if result['originals_unchanged'] else 'NO'}.\nSon archivos sintéticos en el mismo disco; no acredita respaldo independiente.")
                self.footer.configure(text='Resultado conservado en: '+result['root'])
            else:self.recovery_status.set('No pude completar la prueba: '+result)
        if self.closing and not self.sim and not self.recovery_busy: self.root.destroy(); return
        self.timer=self.root.after(200,self.refresh)

    def close(self):
        self.closing=True
        if self.sim:self.stop_sim()
        elif not self.recovery_busy:
            self.root.after_cancel(self.timer); self.root.destroy()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path)
    args=parser.parse_args()
    config={}
    if args.config:
        try: config=json.loads(args.config.read_text(encoding='utf-8-sig'))
        except (OSError,ValueError) as exc:
            root=tk.Tk(); root.withdraw(); messagebox.showerror('Configuración del Laboratorio',str(exc)); root.destroy(); return
    root=tk.Tk(); Laboratory(root,config); root.mainloop()

if __name__=='__main__':main()
