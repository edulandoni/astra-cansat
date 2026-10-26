"""ASTRA-22: pantalla experimental sin pestañas; origen y guardado explícitos."""
import argparse
import hashlib
import time
from functools import lru_cache
from pathlib import Path
from journal import Store
from engine import Engine
from quality import quality_flags
from wire import PROFILE

@lru_cache(maxsize=1)
def windows_memory_api():
    """Creo tipos y firmas una sola vez: ctypes retiene los tipos de puntero."""
    import ctypes
    from ctypes import wintypes
    class Counters(ctypes.Structure):
        _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(k,ctypes.c_size_t) for k in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage']]
    current=ctypes.WinDLL('kernel32').GetCurrentProcess;current.restype=wintypes.HANDLE
    get=ctypes.WinDLL('psapi').GetProcessMemoryInfo
    get.argtypes=[wintypes.HANDLE,ctypes.POINTER(Counters),wintypes.DWORD];get.restype=wintypes.BOOL
    return current,get,Counters

def working_set_bytes():
    """Mido memoria del propio proceso; no estimo si la API no está disponible."""
    import sys
    if sys.platform!='win32':return None
    import ctypes
    current,get,Counters=windows_memory_api()
    obj=Counters();obj.cb=ctypes.sizeof(obj)
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
    p.add_argument('--data-stale-seconds',type=float,default=3.)
    p.add_argument('--gps-stale-seconds',type=float,default=3.)
    p.add_argument('--start-minimized',action='store_true',help='Mantengo el ensayo activo sin tapar el chat')
    a=p.parse_args();source=a.source or ('usb' if a.port else 'pc')
    if source=='usb' and not a.port:p.error('USB requiere --port')
    if source=='replay' and not a.replay:p.error('Reproducción requiere --replay')
    if not a.team.isascii() or not a.team.isdigit() or len(a.team)!=4:p.error('TEAM de banco: cuatro dígitos')
    if a.speed<=0:p.error('Velocidad positiva requerida')
    try:quality_flags({},a.data_stale_seconds,a.gps_stale_seconds)
    except ValueError as exc:p.error(str(exc))
    store=Store(a.output,a.backup);e=Engine(store,a.team,a.profile,{'pc':'PC_BENCH','usb':'USB_BENCH','replay':'REPLAY'}[source])
    store.emit('environment',source=e.source,profile=a.profile,source_sha256={str(f.relative_to(Path(__file__).parent)):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path(__file__).parent.rglob('*') if f.suffix in {'.py','.ino'}},duration=a.duration,samples=a.samples)
    started=time.monotonic()
    from desktop import run_window
    run_window(e,store,a,source,started,working_set_bytes,windows_memory_api)

if __name__=='__main__':main()
