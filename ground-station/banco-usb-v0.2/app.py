"""ASTRA-22: pantalla experimental sin pestañas; origen y guardado explícitos."""
import argparse
import hashlib
import json
import queue
import threading
import time
import tkinter as tk
from tkinter import ttk
from collections import deque
from datetime import datetime,timezone
from pathlib import Path
from journal import Store
from engine import Engine,display
from sources import PCBench,serial_loop,replay_loop
from wire import FIELDS,PROFILE,SCENARIOS

UNITS=dict(ALTITUDE='m AGL',TEMPERATURE='°C',PRESSURE='kPa',VOLTAGE='V',CURRENT='A',
           GPS_ALTITUDE='m MSL',GPS_LATITUDE='°',GPS_LONGITUDE='°',
           **{k:'rad/s' for k in ['GYRO_R','GYRO_P','GYRO_Y']},
           **{k:'m/s²' for k in ['ACCEL_R','ACCEL_P','ACCEL_Y']})

def working_set_bytes():
    """Mido memoria del propio proceso en Windows; no estimo si no hay API."""
    import sys
    if sys.platform!='win32':return None
    import ctypes
    from ctypes import wintypes
    class Counters(ctypes.Structure):
        _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(k,ctypes.c_size_t) for k in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage']]
    obj=Counters();obj.cb=ctypes.sizeof(obj)
    current=ctypes.WinDLL('kernel32').GetCurrentProcess;current.restype=wintypes.HANDLE
    get=ctypes.WinDLL('psapi').GetProcessMemoryInfo
    get.argtypes=[wintypes.HANDLE,ctypes.POINTER(Counters),wintypes.DWORD];get.restype=wintypes.BOOL
    return obj.WorkingSetSize if get(current(),ctypes.byref(obj),obj.cb) else None

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--port');p.add_argument('--source',choices=['pc','usb','replay'])
    p.add_argument('--profile',choices=[PROFILE,'legacy-usb-0.1'],default=PROFILE)
    p.add_argument('--team',default='1000');p.add_argument('--output',type=Path,default=Path(__file__).parent/'runs')
    p.add_argument('--backup',type=Path);p.add_argument('--reset-once',action='store_true')
    p.add_argument('--replay',type=Path);p.add_argument('--speed',type=float,default=1)
    p.add_argument('--auto-run',action='store_true');p.add_argument('--samples',type=int,default=131)
    p.add_argument('--duration',type=float,help='Cierro el ensayo al alcanzar estos segundos reales; no acelera el emisor')
    a=p.parse_args();source=a.source or ('usb' if a.port else 'pc')
    if source=='usb' and not a.port:p.error('USB requiere --port')
    if source=='replay' and not a.replay:p.error('Reproducción requiere --replay')
    if not a.team.isascii() or not a.team.isdigit() or len(a.team)!=4:p.error('TEAM de banco: cuatro dígitos')
    if a.speed<=0:p.error('Velocidad positiva requerida')
    store=Store(a.output,a.backup);e=Engine(store,a.team,a.profile,{'pc':'PC_BENCH','usb':'USB_BENCH','replay':'REPLAY'}[source])
    store.emit('environment',source=e.source,profile=a.profile,source_sha256={str(f.relative_to(Path(__file__).parent)):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path(__file__).parent.rglob('*') if f.suffix in {'.py','.ino'}},duration=a.duration,samples=a.samples)
    started=time.monotonic();last_health=0
    root=tk.Tk();root.title('ASTRA — Banco USB v0.2 — '+e.source+' — datos sintéticos / RF pendiente')
    root.geometry(f'{min(1500,root.winfo_screenwidth()-20)}x{min(1000,root.winfo_screenheight()-60)}+0+0');root.configure(bg='white')
    if root.tk.call('tk','windowingsystem')=='win32':root.state('zoomed')
    root.option_add('*Font','{Segoe UI} 14')
    header=tk.StringVar();detail=tk.StringVar();command_state=tk.StringVar();alert=tk.StringVar()
    for var,bg in [(header,'#eaf1f8'),(detail,'#eaf1f8'),(alert,'#fff0d5')]:
        tk.Label(root,textvariable=var,bg=bg,anchor='w',justify='left',wraplength=1450).pack(fill='x')
    controls=tk.Frame(root,bg='white');controls.pack(fill='x');scenario=tk.StringVar(value='NOMINAL')
    ttk.Combobox(controls,textvariable=scenario,values=SCENARIOS,state='readonly',width=19).pack(side='left')
    def send(op,**args):
        try:e.command(op,**args)
        except (ValueError,queue.Full) as exc:command_state.set(str(exc))
    buttons=[('Iniciar',lambda:send('RUN',scenario=scenario.get(),samples=a.samples)),('Parar',lambda:send('STOP')),
             ('Cero simulado',lambda:send('CAL_ZERO')),('Hora PC',lambda:send('SET_TIME',utc_seconds=int(datetime.now(timezone.utc).timestamp())%86400)),
             ('Batería/solar',lambda:send('POWER_STATUS')),('Nuevo segmento',e.new_legacy_segment)]
    for title,callback in buttons:
        b=tk.Button(controls,text=title,command=callback);b.pack(side='left',padx=2)
        if title=='Nuevo segmento' and a.profile==PROFILE:b.configure(state='disabled')
        elif source=='replay' or a.profile!=PROFILE:
            if title!='Nuevo segmento':b.configure(state='disabled')
    tk.Label(root,textvariable=command_state,bg='white',anchor='w').pack(fill='x')
    grid=tk.Frame(root,bg='white');grid.pack(fill='x');labels={}
    for i,name in enumerate(FIELDS):
        row,col=i%8,(i//8)*2
        tk.Label(grid,text=name,bg='white',anchor='w').grid(row=row,column=col,sticky='w',padx=6)
        labels[name]=tk.StringVar(value='—');tk.Label(grid,textvariable=labels[name],bg='white',fg='#123a60',anchor='w').grid(row=row,column=col+1,sticky='w',padx=6)
    graphs=tk.Frame(root,bg='white');graphs.pack(fill='both',expand=True)
    groups=[('Altitud (m)',['ALTITUDE']),('Batería (V)',['VOLTAGE']),('Corriente (A)',['CURRENT']),
            ('Aceleración (m/s²)',['ACCEL_R','ACCEL_P','ACCEL_Y']),('Giro (rad/s)',['GYRO_R','GYRO_P','GYRO_Y']),('Presión (kPa)',['PRESSURE'])]
    canvases=[]
    for i,_ in enumerate(groups):
        c=tk.Canvas(graphs,bg='white',highlightthickness=1,highlightbackground='#777');c.grid(row=i//3,column=i%3,sticky='nsew');canvases.append(c)
    for i in range(3):graphs.columnconfigure(i,weight=1)
    for i in range(2):graphs.rowconfigure(i,weight=1)
    history=deque(maxlen=300);current=None;auto_started=False
    def redraw():
        for canvas,(title,keys) in zip(canvases,groups):
            canvas.delete('all');w,h=canvas.winfo_width(),canvas.winfo_height()
            if w<150 or h<100:continue
            canvas.create_text(8,14,text=title,anchor='w',font=('Segoe UI',14,'bold'))
            if not history:continue
            x=[int(p['PACKET_COUNT']) for p in history];series=[[float(p[k]) for p in history] for k in keys]
            lo=min(map(min,series));hi=max(map(max,series))
            if lo==hi:lo-=.5;hi+=.5
            pad=(hi-lo)*.08;lo-=pad;hi+=pad;left,right,top,bottom=70,w-15,40,h-35
            canvas.create_line(left,top,left,bottom,right,bottom,width=2)
            for y,text in [(top,f'{hi:.2f}'),(bottom,f'{lo:.2f}')]:canvas.create_text(left-4,y,text=text,anchor='e',font=('Segoe UI',14,'bold'))
            canvas.create_text(left,bottom+16,text=str(x[0]));canvas.create_text(right,bottom+16,text=str(x[-1]))
            for ys,color in zip(series,['#114da0','#a52e20','#24732c']):
                group=[]
                for i,y in enumerate(ys):
                    if i and x[i]!=x[i-1]+1:
                        if len(group)>=4:canvas.create_line(*group,fill=color,width=3)
                        group=[]
                    group.extend([left+(x[i]-x[0])/max(1,x[-1]-x[0])*(right-left),bottom-(y-lo)/(hi-lo)*(bottom-top)])
                if len(group)>=4:canvas.create_line(*group,fill=color,width=3)
    def update():
        nonlocal current,auto_started,last_health
        snap=e.snapshot()
        elapsed=time.monotonic()-started
        if elapsed-last_health>=5:
            last_health=elapsed
            e.event('gui_health',elapsed=elapsed,working_set_bytes=working_set_bytes(),totals={k:snap[k] for k in ['total_valid','total_unique','invalid','overflows','data_age','link_age','unique','observed_gaps']},storage=snap['storage'],history_size=len(history),update_queue=e.updates.qsize())
        if current!=snap['segment']:current=snap['segment'];history.clear()
        while not e.updates.empty():
            try:segment,packet=e.updates.get_nowait()
            except queue.Empty:break
            if segment==current:history.append(display(packet.data))
        data=display(snap['latest'])
        for k,var in labels.items():var.set((data[k]+' '+UNITS.get(k,'')) if k in data else '—')
        age=snap['data_age'];fresh='SIN DATOS ACTUALES' if age is None else f'Edad del dato {age:.1f} s'+(' — ANTIGUO' if age>3 else '')
        link_age=snap['link_age'];link_text='sin mensaje válido' if link_age is None else f'último mensaje válido hace {link_age:.1f} s'
        header.set(f"{snap['source']} | {snap['status']} | {link_text} | {fresh} | TEAM {a.team} FICTICIO | segmento {current}")
        power=snap['power'];solar='Sin consulta batería/solar' if power is None else f"Batería simulada {power['voltage']} V | Solar simulado {power['solar_voltage']} V | edad {time.monotonic()-power['at']:.1f} s"
        detail.set(f"Tramas RX {snap['frames_received']} | control {snap['control_received']} | válidos del segmento {snap['received']} | únicos {snap['unique']} | huecos {snap['observed_gaps']} | duplicados {snap['duplicates']} | conflictos {snap['conflicts']} | rechazos totales {snap['invalid']}\n{solar}")
        flags=[]
        if snap['ambiguous']:flags.append('Sesión ambigua; no muestro datos anteriores como actuales')
        if snap['clock_warning']:flags.append('Contador avanza pero hora de misión no avanza: revisar')
        if data and data['GPS_SATS']=='0':flags.append('GPS SIN FIX; posición retenida, edad '+str(round(snap['gps_age'],1) if snap['gps_age'] is not None else 'desconocida')+' s')
        if snap['done']:flags.append('Simulación terminada; no se esperan más muestras')
        for status in snap['storage']:
            flags.append(f"D{status['destination']} {status['kind']}: confirmados {status['saved']}, pendientes {status['pending']}, descartados {status['dropped']}"+(' ERROR '+status['error'] if status['error'] else ''))
        alert.set(' | '.join(flags))
        if snap['commands']:
            c=snap['commands'][-1]
            state_text={'queued':'En cola','sent':'Enviada','accepted':'Aceptada','rejected':'Rechazada','executed':'Ejecutada en simulación','timeout':'Sin respuesta a tiempo','unknown':'Resultado desconocido'}.get(c['state'],c['state'])
            result=c.get('result',{});previous_context=bool(result) and (result.get('boot'),result.get('run'))!=snap['epoch']
            command_state.set(('Histórico de otro contexto: ' if previous_context else '')+c['op']+': '+state_text+(' — respuesta tardía' if c['late'] else '')+' '+result.get('reason',''))
        if a.auto_run and not auto_started and e.peer:
            auto_started=True
            send('CAL_ZERO');send('SET_TIME',utc_seconds=int(datetime.now(timezone.utc).timestamp())%86400);send('POWER_STATUS');send('RUN',scenario=scenario.get(),samples=a.samples)
        redraw()
        if a.duration and elapsed>=a.duration:close()
        else:root.after(250,update)
    def runner():
        try:
            if source=='usb':serial_loop(e,a.port,reset_once=a.reset_once)
            elif source=='pc':PCBench(e).run_loop()
            else:replay_loop(e,a.replay,a.speed)
        except Exception as exc:e.status='ERROR: '+str(exc);e.event('source_error',reason=str(exc))
    thread=threading.Thread(target=runner,daemon=True);thread.start()
    def close():
        e.stop.set()
        def finish():
            if thread.is_alive():root.after(100,finish)
            else:store.close();root.destroy()
        finish()
    root.protocol('WM_DELETE_WINDOW',close);update();root.mainloop()

if __name__=='__main__':main()
