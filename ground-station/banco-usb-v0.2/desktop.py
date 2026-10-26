"""ASTRA-22: interfaz Tk de operación, sin modificar el contrato del emisor."""
import json,queue,threading,time
from collections import deque
from datetime import datetime,timezone
import tkinter as tk
from tkinter import ttk,messagebox
from engine import display
from sources import PCBench,serial_loop,replay_loop
from quality import quality_flags
from ui_model import (GROUPS,FIELDS_INFO,SCENARIO_NAMES,SCENARIO_HELP,OPS,STATES,age,
                      presentation,command_text,controls,interruption_text)

def run_window(e,store,a,source,started,memory_reader,memory_api):
    root=tk.Tk();root.title('ASTRA — Estación de tierra — '+e.source+' — datos de prueba')
    root.geometry(f'{min(1540,root.winfo_screenwidth()-20)}x{min(1000,root.winfo_screenheight()-60)}+0+0')
    root.minsize(1050,760);root.configure(bg='white');root.option_add('*Font','{Segoe UI} 11')
    if root.tk.call('tk','windowingsystem')=='win32':root.state('zoomed')
    style=ttk.Style(root);style.configure('TLabelframe',background='white');style.configure('TLabelframe.Label',font=('Segoe UI',11,'bold'))
    header=tk.Frame(root,bg='#eaf1f8');header.pack(fill='x')
    title=tk.StringVar();explanation=tk.StringVar();fresh=tk.StringVar();cut=tk.StringVar()
    tk.Label(header,textvariable=title,bg='#eaf1f8',fg='#123a60',font=('Segoe UI',17,'bold'),anchor='w').pack(fill='x',padx=10)
    tk.Label(header,textvariable=explanation,bg='#eaf1f8',anchor='w').pack(fill='x',padx=10)
    source_title={'usb':f'ESP32 por USB · {a.port}','pc':'Simulador en la PC · sin placa','replay':f'Grabación · velocidad {a.speed:g}×'}[source]
    tk.Label(header,text=f'{source_title} | Valores sintéticos · radio y sensores reales pendientes | Equipo {a.team} de banco',bg='#eaf1f8',fg='#41576f',anchor='w').pack(fill='x',padx=10)
    tools=tk.Frame(root,bg='white');tools.pack(fill='x',padx=8,pady=4)
    scenario=tk.StringVar(value=SCENARIO_NAMES['NOMINAL']);scenario_help=tk.StringVar()
    tk.Label(tools,text='Ensayo:',bg='white').pack(side='left')
    chooser=ttk.Combobox(tools,textvariable=scenario,values=list(SCENARIO_NAMES.values()),state='readonly',width=24);chooser.pack(side='left',padx=4)
    selected=lambda:next(k for k,v in SCENARIO_NAMES.items() if v==scenario.get())
    def explain_scenario(*_):scenario_help.set(SCENARIO_HELP[selected()])
    chooser.bind('<<ComboboxSelected>>',explain_scenario);explain_scenario()
    command_var=tk.StringVar(value='Todavía no envié una orden de operación.');local_error='';last_command=None
    def send(op,**args):
        nonlocal local_error,last_command
        try:
            if not controls(e.snapshot()).get(op):raise ValueError('Esta acción no está disponible con el estado actual. Consultá la ayuda o esperá la conexión.')
            last_command=e.command(op,**args);local_error=''
        except (ValueError,queue.Full) as exc:local_error=str(exc)
    def start():
        if e.latest and not e.finished and not e.paused:
            if not messagebox.askyesno('Otra ejecución','Hay un ensayo en curso. ¿Inicio otro desde el principio? Conservo el anterior por separado.',parent=root):return
        send('RUN',scenario=selected(),samples=a.samples)
    buttons={}
    for op,callback in [('RUN',start),('STOP',lambda:send('STOP')),
                        ('CAL_ZERO',lambda:send('CAL_ZERO')),
                        ('SET_TIME',lambda:send('SET_TIME',utc_seconds=int(datetime.now(timezone.utc).timestamp())%86400)),
                        ('POWER_STATUS',lambda:send('POWER_STATUS'))]:
        b=tk.Button(tools,text=OPS[op],command=callback);b.pack(side='left',padx=2);buttons[op]=b
    worker=None;switching=False;closing=False;first_start=True
    def runner(reset):
        try:
            if source=='usb':serial_loop(e,a.port,reset_once=reset)
            elif source=='pc':PCBench(e).run_loop()
            else:replay_loop(e,a.replay,a.speed)
        except Exception as exc:e.status='ERROR: '+str(exc);e.disconnected(str(exc));e.event('source_error',reason=str(exc))
    def launch():
        nonlocal worker,first_start
        e.stop.clear();worker=threading.Thread(target=runner,args=(a.reset_once and first_start,),daemon=True)
        first_start=False;worker.start()
    def toggle_connection():
        nonlocal switching
        if switching:return
        if worker and worker.is_alive():
            switching=True;e.stop.set()
            def finish():
                nonlocal switching
                if worker.is_alive():root.after(100,finish)
                else:e.disconnected('Cierre manual del puerto');switching=False
            finish()
        else:launch()
    # Ubico opciones auxiliares en otra fila para no amontonar botones.
    helpers=tk.Frame(root,bg='white');helpers.pack(fill='x',padx=10)
    connection_button=tk.Button(helpers,text='Cerrar conexión USB',command=toggle_connection);connection_button.pack(side='left')
    tk.Label(helpers,textvariable=scenario_help,bg='white',anchor='w',wraplength=900).pack(side='left',padx=8)
    tk.Label(root,textvariable=command_var,bg='white',fg='#174b70',anchor='w').pack(fill='x',padx=10)
    metrics=tk.Frame(root,bg='white');metrics.pack(fill='x',padx=8,pady=4)
    metric_vars={};gap_hint=tk.StringVar()
    for i,(key,label,hint) in enumerate([
        ('received','Muestras recibidas','Formato válido; incluye repeticiones'),
        ('unique','Muestras diferentes','Acumulado de esta sesión de PC'),
        ('saved','Guardadas en CSV','Destino principal · todas las ejecuciones'),
        ('pending','Esperando guardado','Ya recibidas; aún no confirmadas en disco'),
        ('gaps','Faltantes detectados','Sólo esta ejecución · no prueba causa RF'),
        ('rejected','Mensajes rechazados','No se guardan como mediciones')]):
        box=tk.LabelFrame(metrics,text=label,bg='white',fg='#172f49');box.grid(row=0,column=i,sticky='nsew',padx=3)
        v=tk.StringVar(value='0');metric_vars[key]=v
        tk.Label(box,textvariable=v,font=('Segoe UI',17,'bold'),bg='white',fg='#123a60').pack()
        if key=='gaps':
            tk.Label(box,textvariable=gap_hint,bg='white',fg='#41576f',font=('Segoe UI',9),wraplength=210).pack(padx=5)
        else:tk.Label(box,text=hint,bg='white',fg='#41576f',font=('Segoe UI',9),wraplength=210).pack(padx=5)
        metrics.columnconfigure(i,weight=1,uniform='metrics')
    note_label=tk.Label(root,textvariable=fresh,bg='#f3f5f7',anchor='w');note_label.pack(fill='x',padx=10)
    telemetry=tk.Frame(root,bg='white');telemetry.pack(fill='x',padx=8,pady=3)
    field_vars={};value_labels=[];gps_note=tk.StringVar();power_text=tk.StringVar()
    def text_window(name,text,compact=False):
        win=tk.Toplevel(root);win.title(name);win.transient(root);win.geometry('650x380' if compact else '880x650')
        tk.Button(win,text='Cerrar',command=win.destroy).pack(side='bottom',pady=6)
        box=tk.Text(win,wrap='word',font=('Segoe UI',12),padx=15,pady=15);scroll=ttk.Scrollbar(win,command=box.yview);box.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right',fill='y');box.pack(fill='both',expand=True);box.insert('end',text)
        if compact:box.tag_configure('heading',font=('Segoe UI',16,'bold'));box.tag_add('heading','1.0','1.end')
        box.configure(state='disabled')
    for i,(group,description,keys) in enumerate(GROUPS):
        box=ttk.LabelFrame(telemetry,text=group);box.grid(row=0,column=i,sticky='nsew',padx=3);telemetry.columnconfigure(i,weight=1,uniform='telemetry')
        tk.Label(box,text=description,bg='white',fg='#41576f',font=('Segoe UI',9),wraplength=320,justify='left',anchor='w').grid(row=0,column=0,columnspan=2,sticky='w',padx=5)
        for row,k in enumerate(keys,1):
            name,unit,meaning=FIELDS_INFO[k]
            label=tk.Label(box,text=name+' ⓘ',bg='white',anchor='w',cursor='hand2',font=('Segoe UI',10))
            label.grid(row=row,column=0,sticky='w',padx=5)
            label.bind('<Button-1>',lambda event,key=k:text_window(FIELDS_INFO[key][0],FIELDS_INFO[key][0]+'\n\n'+FIELDS_INFO[key][2]+'\n\n'+('Unidad: '+FIELDS_INFO[key][1] if FIELDS_INFO[key][1] else 'Se muestra como texto o cantidad, sin unidad física.'),compact=True))
            v=tk.StringVar(value='—');field_vars[k]=v
            lab=tk.Label(box,textvariable=v,bg='white',fg='#123a60',anchor='e',font=('Segoe UI',11));lab.grid(row=row,column=1,sticky='e',padx=5);value_labels.append(lab)
        box.columnconfigure(1,weight=1)
        if group=='Energía':
            tk.Label(box,textvariable=power_text,bg='white',justify='left',anchor='nw',wraplength=300,font=('Segoe UI',10)).grid(row=len(keys)+1,column=0,columnspan=2,sticky='w',padx=5,pady=6)
        if group=='Ubicación GPS':tk.Label(box,textvariable=gps_note,bg='white',justify='left',wraplength=300,font=('Segoe UI',9)).grid(row=len(keys)+1,column=0,columnspan=2,sticky='w',padx=5)
    graphs=tk.Frame(root,bg='white');graphs.pack(fill='both',expand=True,padx=10,pady=3)
    groups=[('Altura sobre el inicio · m',['ALTITUDE']),('Batería · V',['VOLTAGE']),('Consumo · A',['CURRENT']),
            ('Aceleración · m/s²',['ACCEL_R','ACCEL_P','ACCEL_Y']),('Velocidad de giro · rad/s',['GYRO_R','GYRO_P','GYRO_Y']),('Presión · kPa',['PRESSURE'])]
    canvases=[]
    for i,_ in enumerate(groups):
        canvas=tk.Canvas(graphs,bg='white',height=105,highlightthickness=1,highlightbackground='#b5c2ce');canvas.grid(row=i//3,column=i%3,sticky='nsew');canvases.append(canvas)
    for i in range(3):graphs.columnconfigure(i,weight=1)
    for i in range(2):graphs.rowconfigure(i,weight=1)
    alerts=tk.StringVar();storage_text=tk.StringVar()
    statusbar=tk.Frame(root,bg='white');statusbar.pack(side='bottom',fill='x',before=header)
    tk.Label(statusbar,textvariable=cut,bg='#eaf1f8',fg='#173b60',anchor='w',wraplength=1500).pack(fill='x',padx=10)
    tk.Label(statusbar,textvariable=alerts,bg='#fff0d5',anchor='w',wraplength=1500).pack(fill='x',padx=10)
    tk.Label(statusbar,textvariable=storage_text,bg='white',anchor='w',fg='#41576f',font=('Segoe UI',9)).pack(fill='x',padx=10)
    footer=tk.Frame(statusbar,bg='white');footer.pack(fill='x',padx=10,pady=3)
    help_text='''CÓMO LEER ESTA ESTACIÓN\n\n1. Origen: ESP32 USB significa que la placa envía datos por cable. PC significa simulación sin placa. Grabación reproduce datos anteriores y no envía órdenes. Todos los valores de este perfil son inventados.\n\n2. Estado: abrir el puerto no garantiza que lleguen datos recientes. La edad del último dato sigue aumentando durante un corte. Los valores históricos se marcan y no se presentan como actuales. El fin o la detención de un ensayo son distintos de una avería.\n\n3. Contadores: recibidas incluye muestras de formato válido repetidas; diferentes cuenta las muestras nuevas aceptadas. Guardadas y esperando guardado corresponden al CSV principal de esta sesión, que puede contener varias ejecuciones. Cada copia tiene sus propios contadores. Los diagnósticos y las órdenes no son muestras.\n\n4. Desconexión: esperando guardado NO cuenta mensajes que no llegaron. Durante un corte no sé cuántos emitió la placa. Si vuelve la misma identidad, un contador posterior permite detectar un hueco. Puede reducirse si luego llegan muestras tardías. Si se reinició o empezó otra ejecución no comparo esos contadores ni invento pérdidas. Quitar el USB puede cortar también la alimentación.\n\n5. Acciones: Iniciar crea un nuevo ensayo y conserva el anterior. Detener pide parar la emisión simulada. Poner altura en cero y sincronizar hora se permiten en la preparación en la base. Batería/solar devuelve valores sintéticos. Enviada, aceptada y ejecutada son pasos diferentes; sin respuesta no equivale a ejecutada.\n\n6. Conexión USB: cerrar el puerto no garantiza detener el emisor. Conectar reabre el puerto y verifica identidad; no vuelve a iniciar por sí solo la misión. Al reenchufar busco un único adaptador compatible; si hay varios, hace falta elegir explícitamente el puerto al abrir la app.\n\n7. Gráficos: el eje horizontal es el contador de muestra, no segundos. No uno líneas a través de contadores faltantes. Cada ejecución tiene sus propios gráficos y archivos. R/P/Y identifican los tres ejes; no confundir velocidad de giro con ángulo de orientación.\n\n8. Guardado: CSV contiene mediciones; el registro completo conserva también bytes, órdenes y diagnósticos. Confirmado significa escritura, flush y fsync; no prueba resistencia a un corte eléctrico. Ante error se informa qué destino falla y cuántos registros siguen pendientes o fueron descartados.\n\nHacé clic en el nombre de una medición marcado ⓘ para ver su significado, referencia y unidad. En Datos técnicos y archivos podés consultar identidades, originales, órdenes y cortes. Esta pantalla no acredita radio, sensores reales, autonomía o cumplimiento de vuelo.'''
    tk.Button(footer,text='Cómo leer esta pantalla',command=lambda:text_window('Ayuda de la estación',help_text)).pack(side='left')
    def details():
        s=e.snapshot();parts=['SESIÓN DE PC: '+store.session,'Estado interno: '+s['status'],'Perfil: '+a.profile,
             'Arranque / ejecución del emisor: '+str(s['epoch']),'Segmento de archivos: '+s['segment'],
             '\nCONTEOS TÉCNICOS','Tramas recibidas (incluye control/diagnóstico): '+str(s['frames_received']),
             'Mensajes de control: '+str(s['control_received']),'Diagnósticos: '+str(s['diagnostics']),
             'Tramas excesivas: '+str(s['overflows']),'Duplicados en ejecución: '+str(s['duplicates']),
             'Conflictos en ejecución: '+str(s['conflicts']),'Detalle de huecos incompleto: '+str(s['gaps_uncertain']),
             '\nDESTINOS — cada fila tiene su propio alcance']
        for w in s['storage']:parts.append(f"{w['root']}\n{w['kind']}: guardados {w['saved']}; pendientes {w['pending']}; descartados {w['dropped']}; error {w['error'] or 'ninguno'}")
        parts+=['\nCORTES — últimas 64 entradas en pantalla; diario completo en archivo']+[interruption_text(c) for c in s['interruptions']]
        parts+=['\nÚLTIMAS ÓRDENES']+[command_text(c,s['epoch'])+'\nID: '+c['id'] for c in s['commands']]
        parts+=['\nÚLTIMOS VALORES RECIBIDOS (unidades del emisor)\n'+json.dumps(s['latest'] or s.get('last_sample'),ensure_ascii=False,indent=2)]
        text_window('Datos técnicos y archivos — captura de este momento','\n'.join(parts))
    tk.Button(footer,text='Datos técnicos, archivos y cortes',command=details).pack(side='left',padx=5)
    if a.profile=='legacy-usb-0.1':tk.Button(footer,text='Separar nueva ejecución',command=e.new_legacy_segment).pack(side='left')
    tk.Label(footer,text='ⓘ Clic en una medición para entenderla · Ctrl+M minimiza sin detener el registro',bg='white',font=('Segoe UI',9)).pack(side='right')
    history=deque(maxlen=300);current=None;auto_started=False;last_health=0
    def redraw(old):
        for canvas,(name,keys) in zip(canvases,groups):
            canvas.delete('all');w,h=canvas.winfo_width(),canvas.winfo_height()
            if w<150 or h<95:
                canvas.create_text(8,12,text='Ampliá la ventana para ver este gráfico',anchor='w',font=('Segoe UI',9));continue
            canvas.create_text(8,12,text=name+(' · histórico' if old else ''),anchor='w',font=('Segoe UI',10,'bold'))
            if not history:
                canvas.create_text(w/2,h/2,text='Esperando muestras de esta ejecución',fill='#41576f');continue
            x=[int(p['PACKET_COUNT']) for p in history];series=[[float(p[k]) for p in history] for k in keys]
            lo=min(map(min,series));hi=max(map(max,series))
            if lo==hi:lo-=.5;hi+=.5
            pad=(hi-lo)*.08;lo-=pad;hi+=pad;left,right,top,bottom=55,w-15,32,h-30
            canvas.create_line(left,top,left,bottom,right,bottom,fill='#63788c')
            canvas.create_text(left-3,top,text=f'{hi:.2f}',anchor='e',font=('Segoe UI',9))
            canvas.create_text(left-3,bottom,text=f'{lo:.2f}',anchor='e',font=('Segoe UI',9))
            canvas.create_text(left,bottom+13,text=str(x[0]),font=('Segoe UI',9));canvas.create_text(right,bottom+13,text=str(x[-1]),font=('Segoe UI',9))
            canvas.create_text(w/2,bottom+13,text='Número de muestra',font=('Segoe UI',9))
            for j,(ys,color) in enumerate(zip(series,['#114da0','#a52e20','#24732c'])):
                if len(keys)>1:canvas.create_text(w-100+j*35,12,text=['R','P','Y'][j],fill=color,font=('Segoe UI',10,'bold'))
                group=[]
                for i,y in enumerate(ys):
                    if i and x[i]!=x[i-1]+1:
                        if len(group)>=4:canvas.create_line(*group,fill=color,width=2)
                        group=[]
                    group.extend([left+(x[i]-x[0])/max(1,x[-1]-x[0])*(right-left),bottom-(y-lo)/(hi-lo)*(bottom-top)])
                if len(group)>=4:canvas.create_line(*group,fill=color,width=2)
    def update():
        nonlocal current,auto_started,last_health
        if closing:return
        snap=e.snapshot();view=presentation(snap,a.data_stale_seconds);flags=quality_flags(snap,a.data_stale_seconds,a.gps_stale_seconds)
        elapsed=time.monotonic()-started
        if elapsed-last_health>=5:
            last_health=elapsed
            e.event('gui_health',ui_state=view['title'],interruption=view['interruption'],quality_flags=flags,elapsed=elapsed,
                    working_set_bytes=memory_reader(),memory_reader_initializations=memory_api.cache_info().misses,
                    totals={k:snap[k] for k in ['total_valid','total_unique','invalid','overflows','data_age','link_age','unique','observed_gaps']},
                    storage=snap['storage'],history_size=len(history),update_queue=e.updates.qsize())
        if current!=snap['segment']:current=snap['segment'];history.clear()
        while not e.updates.empty():
            try:segment,packet=e.updates.get_nowait()
            except queue.Empty:break
            if segment==current:history.append(display(packet.data))
        title.set(view['title']);explanation.set(view['explanation']);fresh.set(view['note']);cut.set(view['interruption']);gps_note.set(view['gps_note'])
        note_label.configure(fg='#825100' if view['old'] else '#41576f')
        for lab in value_labels:lab.configure(fg='#746653' if view['old'] else '#123a60')
        for k,v in field_vars.items():v.set(view['values'][k])
        primary=next((w for w in snap['storage'] if w['destination']==0 and w['kind']=='csv'),{})
        vals=dict(received=snap['total_valid'],unique=snap['total_unique'],saved=primary.get('saved',0),pending=primary.get('pending',0),gaps=snap['observed_gaps'],rejected=snap['invalid'])
        for k,v in metric_vars.items():v.set((view['gap_value'] if k=='gaps' else str(vals[k]))+(' · detalle incompleto' if k=='gaps' and snap['gaps_uncertain'] else ''))
        gap_hint.set(view['gap_note'])
        power=snap['power']
        power_text.set('Solar: sin consulta de estado.\nUsá Consultar batería y solar.' if power is None else f"Última consulta sintética:\nBatería {power['voltage']} V · Solar {power['solar_voltage']} V\nHace {age(time.monotonic()-power['at'])}; no son mediciones físicas.")
        allow=controls(snap)
        for op,b in buttons.items():b.configure(state='normal' if allow[op] else 'disabled')
        connection_button.configure(text='Cerrando conexión…' if switching else ('Cerrar conexión USB' if worker and worker.is_alive() else 'Conectar USB'),state='normal' if source=='usb' and not switching else 'disabled')
        chooser.configure(state='disabled' if source=='replay' else 'readonly')
        selected_command=next((c for c in reversed(snap['commands']) if c['id']==last_command),None)
        if selected_command is None:selected_command=next((c for c in reversed(snap['commands']) if not c.get('handshake_connection')),None)
        command_var.set(local_error or command_text(selected_command,snap['epoch']))
        issues=[]
        if flags['gps_no_fix']:issues.append('GPS sin solución: no hay posición actual válida.')
        if flags['gps_stale']:issues.append('GPS sin actualizar aunque siguen llegando otras mediciones.')
        if flags['mission_clock_frozen'] and not snap.get('paused') and not snap.get('done'):issues.append('El contador avanza, pero la hora del emisor no cambia.')
        if snap['overflows']:issues.append(f"Tramas demasiado largas: {snap['overflows']}. Conservé los bytes; ver datos técnicos.")
        if snap['conflicts']:issues.append(f"Mismo contador con valores distintos: {snap['conflicts']}. Requiere revisión.")
        for w in snap['storage']:
            if w['error'] or w['dropped']:issues.append(f"{'Principal' if w['destination']==0 else 'Respaldo'} {w['kind']}: {w['pending']} pendientes, {w['dropped']} descartados. "+('Error de guardado: '+w['error'] if w['error'] else ''))
        alerts.set(' | '.join(issues) or 'Sin avisos adicionales de recepción o guardado.')
        paths=[]
        for dest in sorted(set(w['destination'] for w in snap['storage'])):
            csv=next(w for w in snap['storage'] if w['destination']==dest and w['kind']=='csv')
            paths.append(f"{'Principal' if dest==0 else 'Copia '+str(dest)}: {csv['saved']} muestras CSV guardadas · {csv['pending']} esperando · {csv['dropped']} descartadas")
        storage_text.set(' | '.join(paths)+' · Ubicaciones y registro completo en Datos técnicos y archivos')
        if a.auto_run and not auto_started and e.peer and not e.ambiguous:
            auto_started=True
            for op,args in [('CAL_ZERO',{}),('SET_TIME',{'utc_seconds':int(datetime.now(timezone.utc).timestamp())%86400}),('POWER_STATUS',{}),('RUN',{'scenario':selected(),'samples':a.samples})]:
                try:last_id=e.command(op,**args)
                except (ValueError,queue.Full) as exc:e.event('auto_run_error',reason=str(exc))
        redraw(view['old'])
        if a.duration and elapsed>=a.duration:close()
        else:root.after(250,update)
    def close():
        nonlocal closing
        closing=True;e.stop.set()
        def finish():
            if worker and worker.is_alive():root.after(100,finish)
            else:store.close();root.destroy()
        finish()
    root.protocol('WM_DELETE_WINDOW',close);root.bind('<Control-m>',lambda event:root.iconify())
    if a.start_minimized:root.after(750,root.iconify)
    launch();update();root.mainloop()
