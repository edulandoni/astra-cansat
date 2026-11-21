from pathlib import Path
from datetime import datetime,timezone
import ctypes,json,runpy,sys
base=Path(__file__).resolve().parent
app=base/'source/ground-station/banco-usb-v0.2/app.py'
root=base/'output'
sys.path.insert(0,str(app.parent))
sys.argv=[str(app),'--port','COM5','--auto-run','--samples','7261','--duration','7280','--start-minimized','--output',str(root)]
kernel=ctypes.WinDLL('kernel32');hold=kernel.SetThreadExecutionState
hold.argtypes=[ctypes.c_uint32];hold.restype=ctypes.c_uint32
log=base/'power-lease.jsonl'
def record(**data):
 with log.open('a',encoding='utf-8') as h:h.write(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),**data))+'\n')
try:
 previous=hold(0x80000001)
 record(event='started',idle_sleep_hold_acquired=bool(previous),persistent_settings_changed=False)
 runpy.run_path(str(app),run_name='__main__')
 record(event='application_returned')
finally:
 restored=hold(0x80000000)
 record(event='released',idle_sleep_hold_release_call_succeeded=bool(restored))
