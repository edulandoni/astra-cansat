import argparse
import time
from collections import deque
from pathlib import Path
import tkinter as tk
from protocol import FIELDS
from simulator import SCENARIOS
from storage import Recorder
from acquisition import Acquisition

UNITS = {'ALTITUDE':'m AGL','TEMPERATURE':'°C','PRESSURE':'kPa','VOLTAGE':'V','CURRENT':'A',
         'GPS_ALTITUDE':'m MSL','GPS_LATITUDE':'° (TBR)','GPS_LONGITUDE':'° (TBR)',
         **{k:'°/s' for k in FIELDS[10:13]}, **{k:'m/s² — TBR' for k in FIELDS[13:16]}}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--team',default='1000')
    parser.add_argument('--scenario',choices=SCENARIOS,default='NOMINAL')
    parser.add_argument('--port',help='Ejemplo: COM5; omitir para simulación PC')
    parser.add_argument('--baud',type=int,default=115200)
    parser.add_argument('--bench-reset-once',action='store_true',help='Sólo simulador USB conocido: reiniciar por EN/RTS una vez y conservar 0,5 s de arranque fuera del parser; no usar con vuelo/RF')
    parser.add_argument('--output',default=str(Path(__file__).parent/'runs'))
    parser.add_argument('--backup',help='Directorio en un segundo disco; sin esto G2 queda pendiente')
    args = parser.parse_args()
    if len(args.team)!=4 or not args.team.isascii() or not args.team.isdigit():
        parser.error('TEAM_ID debe tener cuatro dígitos')
    if args.bench_reset_once and not args.port:
        parser.error('--bench-reset-once requiere --port')
    root = tk.Tk()
    root.title('ASTRA — Ground Station v0.1 — BANCO / RF pendiente')
    root.geometry(f'{min(1450,root.winfo_screenwidth()-60)}x{min(950,root.winfo_screenheight()-80)}')
    root.configure(bg='white')
    root.option_add('*Font','{Segoe UI} 14')
    recorder = Recorder(args.output,args.team,args.backup)
    acquisition = Acquisition(recorder,args.team,args.scenario,args.port,args.baud,bench_reset=args.bench_reset_once)
    status = tk.StringVar()
    status_label=tk.Label(root,textvariable=status,bg='#eaf1f8',anchor='w',justify='left',wraplength=1300)
    status_label.pack(fill='x')
    root.bind('<Configure>',lambda e: status_label.configure(wraplength=max(400,root.winfo_width()-30)) if e.widget is root else None)
    grid = tk.Frame(root,bg='white')
    grid.pack(fill='x')
    labels = {}
    for i,name in enumerate(FIELDS):
        row,col = i%8,(i//8)*2
        tk.Label(grid,text=name,bg='white',anchor='w').grid(row=row,column=col,sticky='w',padx=6)
        var=tk.StringVar(value='—')
        labels[name]=var
        tk.Label(grid,textvariable=var,bg='white',fg='#123a60',anchor='w').grid(row=row,column=col+1,sticky='w',padx=6)
    # Six simultaneous graphs; each IMU graph has all three axes.
    graph_frame=tk.Frame(root,bg='white')
    graph_frame.pack(fill='both',expand=True)
    groups=[('Altitud (m AGL)',['ALTITUDE']),('Batería (V)',['VOLTAGE']),('Corriente (A)',['CURRENT']),
            ('Aceleración (m/s², TBR)',['ACCEL_R','ACCEL_P','ACCEL_Y']),
            ('Giro (°/s)',['GYRO_R','GYRO_P','GYRO_Y']),('Presión (kPa)',['PRESSURE'])]
    canvases=[]
    for i,(title,keys) in enumerate(groups):
        c=tk.Canvas(graph_frame,bg='white',highlightthickness=1,highlightbackground='#777')
        c.grid(row=i//3,column=i%3,sticky='nsew',padx=3,pady=3)
        canvases.append(c)
    for i in range(3): graph_frame.columnconfigure(i,weight=1)
    for i in range(2): graph_frame.rowconfigure(i,weight=1)
    history=deque(maxlen=300)
    last_count=-1
    def redraw():
        for canvas,(title,keys) in zip(canvases,groups):
            canvas.delete('all')
            w,h=canvas.winfo_width(),canvas.winfo_height()
            if w<150 or h<130: continue
            canvas.create_text(12,16,text=title,anchor='w',font=('Segoe UI',14,'bold'))
            if not history: continue
            series=[[float(p.data[k]) for p in history] for k in keys]
            lo,hi=min(map(min,series)),max(map(max,series))
            if lo==hi: lo,hi=lo-.5,hi+.5
            pad=(hi-lo)*.1
            lo,hi=lo-pad,hi+pad
            left,right,top,bottom=68,w-15,48,h-48
            canvas.create_line(left,top,left,bottom,right,bottom,width=2)
            canvas.create_text(left-4,top,text=f'{hi:.2f}',anchor='e',font=('Segoe UI',14,'bold'))
            canvas.create_text(left-4,bottom,text=f'{lo:.2f}',anchor='e',font=('Segoe UI',14,'bold'))
            counts=[p.count for p in history]
            xmin,xmax=counts[0],max(counts[-1],counts[0]+1)
            canvas.create_text(left,bottom+20,text=str(xmin),font=('Segoe UI',14,'bold'))
            canvas.create_text(right,bottom+20,text=str(xmax),font=('Segoe UI',14,'bold'))
            canvas.create_text((left+right)/2,bottom+20,text='PACKET_COUNT',font=('Segoe UI',14,'bold'))
            for key,ys,color in zip(keys,series,['#114da0','#a52e20','#24732c']):
                # Gaps are left open rather than drawing invented continuity.
                for j in range(1,len(ys)):
                    if counts[j]!=counts[j-1]+1: continue
                    coords=[]
                    for index in [j-1,j]:
                        coords.extend([left+(counts[index]-xmin)/(xmax-xmin)*(right-left),bottom-(ys[index]-lo)/(hi-lo)*(bottom-top)])
                    canvas.create_line(*coords,fill=color,width=3)
                canvas.create_text(left+keys.index(key)*110,34,text=key,anchor='w',fill=color,font=('Segoe UI',14))
    def update():
        nonlocal last_count
        while not acquisition.updates.empty():
            p=acquisition.updates.get_nowait()
            if p.count>last_count:
                history.append(p)
                last_count=p.count
        with acquisition.lock: latest=acquisition.latest
        if latest:
            for k,v in latest.data.items(): labels[k].set(v+' '+UNITS.get(k,''))
        counter=acquisition.counter
        gps='SIN FIX — datos GPS retenidos' if latest and latest.data['GPS_SATS']=='0' else 'GPS simulado / reportado'
        age = time.monotonic()-acquisition.last_rx if acquisition.last_rx is not None else None
        freshness = 'SIN DATOS' if age is None else (f'DATOS ANTIGUOS ({age:.0f} s)' if age>3 else 'Datos recientes')
        status.set(f'{acquisition.status} | {freshness} | TEAM {args.team}'+(' FICTICIO' if args.team=='1000' else '')+
                   f' | RX válidos {counter.received} | únicos {counter.unique} | huecos observados {counter.lost} | duplicados {counter.duplicates} | rechazados {acquisition.invalid}\n'+
                   f'{gps} | {counter.warning} | '+('ERROR DE ARCHIVO: '+recorder.error if recorder.error else 'CSV: '+str(recorder.paths[0]))+
                   ('\nRespaldo configurado: '+str(recorder.paths[1]) if len(recorder.paths)>1 else '\nSin segundo disco configurado: G2 pendiente'))
        redraw()
        root.after(250,update)
    def close():
        acquisition.stop.set()
        def finish():
            if acquisition.thread.is_alive(): root.after(100,finish)
            else: root.destroy()
        finish()
    root.protocol('WM_DELETE_WINDOW',close)
    acquisition.thread.start()
    update()
    root.mainloop()

if __name__=='__main__': main()
