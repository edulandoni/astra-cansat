"""ASTRA-39: ventana nativa de chequeo de cámaras, exclusiva del banco USB."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from serial.tools import list_ports
from camera_session import Round, capture, read_evidence, read_registry


class CameraPanel:
    def __init__(self, root, registry, output):
        self.root, self.registry, self.output = root, registry, Path(output)
        self.round = Round()
        self.events = queue.Queue(maxsize=2)
        self.rows = {}
        self.buttons = []
        root.title('ASTRA — Comprobar cámaras — banco USB')
        root.geometry('1140x800')
        root.minsize(1000, 760)
        root.configure(bg='white')
        root.option_add('*Font', '{Segoe UI} 11')
        header = tk.Frame(root, bg='#eaf1f8')
        header.pack(fill='x')
        tk.Label(header, text='Comprobar cámaras', font=('Segoe UI', 19, 'bold'),
                 bg='#eaf1f8', fg='#123a60', anchor='w').pack(fill='x', padx=16, pady=(10, 4))
        tk.Label(header, text='Conectá una cámara, elegí su puerto y pedí una foto. Repetí con la otra.',
                 bg='#eaf1f8', anchor='w').pack(fill='x', padx=16)
        tk.Label(header, text='Foto + SD crea un archivo nuevo y comprueba su lectura desde la cámara. No borra ni formatea.',
                 bg='#eaf1f8', fg='#41576f', anchor='w').pack(fill='x', padx=16, pady=(2, 10))
        toolbar = tk.Frame(root, bg='white')
        toolbar.pack(fill='x', padx=14, pady=8)
        self.summary = tk.StringVar()
        tk.Label(toolbar, textvariable=self.summary, bg='white', fg='#123a60', anchor='w').pack(side='left', expand=True, fill='x')
        for label, action in [('Actualizar puertos', self.refresh_ports), ('Nueva ronda', self.new_round)]:
            button = tk.Button(toolbar, text=label, command=action)
            button.pack(side='right', padx=4)
            self.buttons.append(button)
        tk.Label(root, text='Una foto correcta no demuestra grabación continua, consumo ni apagado.\nEste chequeo es local por USB; no envía órdenes de vuelo ni usa radio.',
                 bg='#eaf1f8', fg='#41576f', justify='left', anchor='w').pack(side='bottom', fill='x', pady=(8, 0), ipady=8, ipadx=16)
        body = tk.Frame(root, bg='white')
        body.pack(fill='both', expand=True, padx=12)
        for column, key in enumerate(('camera1', 'camera2')):
            body.columnconfigure(column, weight=1, uniform='camera')
            box = tk.LabelFrame(body, text=f'Cámara {column+1}', bg='white', fg='#123a60', padx=10, pady=8)
            box.grid(row=0, column=column, sticky='nsew', padx=4)
            controls = tk.Frame(box, bg='white'); controls.pack(fill='x')
            tk.Label(controls, text='Puerto USB:', bg='white').pack(side='left')
            port = ttk.Combobox(controls, state='readonly', width=12); port.pack(side='left', padx=6)
            buttons = tk.Frame(box, bg='white'); buttons.pack(fill='x', pady=5)
            for label, save in [('Sólo foto', False), ('Foto + comprobar SD', True)]:
                button = tk.Button(buttons, text=label, command=lambda k=key, s=save: self.start(k, s))
                button.pack(side='left', padx=(0, 5)); self.buttons.append(button)
            open_button = tk.Button(box, text='Ver un chequeo guardado…', command=lambda k=key: self.open_saved(k))
            open_button.pack(anchor='w'); self.buttons.append(open_button)
            state = tk.StringVar(value='Sin comprobar en esta ronda.')
            tk.Label(box, textvariable=state, bg='white', anchor='w', justify='left', wraplength=480).pack(fill='x', pady=6)
            photo = tk.Label(box, text='La foto del chequeo aparece acá.\nNo es video en vivo.', bg='#edf2f6', fg='#41576f', width=40, height=12)
            photo.pack(fill='both', expand=True)
            stamp = tk.StringVar(value='Todavía no hay una foto conservada.')
            tk.Label(box, textvariable=stamp, bg='white', fg='#41576f', wraplength=480, justify='left', anchor='w').pack(fill='x', pady=7)
            self.rows[key] = dict(port=port, state=state, photo=photo, stamp=stamp, image=None)
        body.rowconfigure(0, weight=1)
        root.protocol('WM_DELETE_WINDOW', self.close)
        self.refresh_ports()
        self.render()
        root.after(100, self.poll)

    def refresh_ports(self):
        ports = sorted(p.device for p in list_ports.comports())
        for row in self.rows.values():
            row['port']['values'] = ports
            if row['port'].get() not in ports:
                row['port'].set('')

    def start(self, key, save):
        row = self.rows[key]
        if not row['port'].get():
            messagebox.showinfo('Elegir puerto', 'Elegí el puerto USB de la cámara conectada. No abro puertos por mi cuenta.', parent=self.root)
            return
        if self.round.busy:
            return
        self.round.start(key)
        port = row['port'].get()
        self.render()
        def worker():
            try:
                result = capture(key, self.registry[key], port, self.output, save)
            except Exception as exc:
                result = {'operation_ok': False, 'error': str(exc)}
            self.events.put((key, result))
        threading.Thread(target=worker, daemon=False).start()

    def open_saved(self, key):
        path = filedialog.askopenfilename(parent=self.root, title='Abrir resultado de un chequeo', filetypes=[('Resultado del chequeo', 'resultado.json')])
        if not path:
            return
        try:
            evidence = read_evidence(Path(path).parent, self.registry[key])
            self.round.photos[key] = evidence
            self.render()
        except Exception as exc:
            messagebox.showerror('No pude comprobar ese archivo', str(exc), parent=self.root)

    def new_round(self):
        self.round.new()
        self.render()

    def render(self):
        self.summary.set(self.round.summary())
        for button in self.buttons:
            button.configure(state='disabled' if self.round.busy else 'normal')
        for key, row in self.rows.items():
            result = self.round.results.get(key)
            if self.round.busy == key:
                status = 'Esperando una foto nueva y el resultado de la solicitud…'
            elif result and result.get('operation_ok'):
                status = 'Foto recibida y guardado/lectura en SD comprobados.' if result['sd_ok'] else 'Foto recibida. No solicité comprobar la SD.'
            elif result:
                status = ('Foto recibida, pero la comprobación no terminó bien.\n' if result.get('photo') else 'No pude completar la comprobación.\n') + result.get('error', '')
            else:
                status = 'Sin comprobar en esta ronda.'
            row['state'].set(status)
            evidence = self.round.photos.get(key)
            if evidence:
                with Image.open(evidence['photo']) as im:
                    im.thumbnail((420, 240))
                    row['image'] = ImageTk.PhotoImage(im.copy())
                row['photo'].configure(image=row['image'], text='', width=0, height=0)
        self.update_stamps()

    def update_stamps(self):
        for key, row in self.rows.items():
            evidence = self.round.photos.get(key)
            if evidence:
                captured = datetime.fromisoformat(evidence['finished_utc'])
                stamp = captured.astimezone().strftime('%d/%m/%Y %H:%M:%S %Z')
                seconds = int((datetime.now(timezone.utc) - captured).total_seconds())
                age = f'hace {seconds} s' if seconds >= 0 else 'revisar hora de la PC'
                context = 'Foto de esta solicitud' if self.round.results.get(key) is evidence else 'Foto conservada; no confirma esta ronda'
                row['stamp'].set(f'{context}\n{stamp} · {age}\n640 × 480 · color · archivo completo verificado')

    def poll(self):
        try:
            key, result = self.events.get_nowait()
        except queue.Empty:
            pass
        else:
            self.round.finish(key, result)
            self.render()
        self.update_stamps()
        self.root.after(100, self.poll)

    def close(self):
        if self.round.busy:
            messagebox.showinfo('Comprobación en curso', 'Espero el resultado y el cierre del puerto antes de salir. No desconectes la cámara ni retires la tarjeta.', parent=self.root)
            return
        self.root.destroy()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--registry', type=Path, required=True, help='Registro privado con dos identidades ya comprobadas')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--start-minimized', action='store_true')
    args = parser.parse_args()
    try:
        registry = read_registry(args.registry)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    root = tk.Tk()
    CameraPanel(root, registry, args.output)
    if args.start_minimized:
        root.iconify()
    root.mainloop()


if __name__ == '__main__':
    main()
