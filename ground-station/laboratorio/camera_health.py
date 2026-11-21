"""ASTRA-39/24: interpretación propuesta de reportes. No es aún la interfaz de Edu."""


class RecordingHealth:
    def __init__(self, device, timeout=3.0):
        if not device or timeout <= 0:
            raise ValueError('Identidad y timeout positivo requeridos.')
        self.device, self.timeout = device, timeout
        self.report = None
        self.received_at = None
        self.progress_at = None

    def accept(self, report, now):
        fields = ['report_seq', 'frames_written', 'bytes_written', 'uptime_ms', 'last_write_ms']
        if report.get('device') != self.device or not report.get('boot') or not report.get('segment'):
            raise ValueError('Falta identidad del contexto de grabación.')
        if any(type(report.get(f)) is not int or report[f] < 0 for f in fields):
            raise ValueError('Contadores inválidos.')
        if report['last_write_ms'] > report['uptime_ms'] or type(report.get('recording')) is not bool:
            raise ValueError('Tiempo o estado contradictorio.')
        previous = self.report
        same = previous and (previous['boot'], previous['segment']) == (report['boot'], report['segment'])
        if same:
            if report['report_seq'] <= previous['report_seq']:
                raise ValueError('Reporte repetido o fuera de orden; no renuevo antigüedad.')
            if any(report[f] < previous[f] for f in fields):
                raise ValueError('Contadores retrocedieron sin cambio de contexto.')
        progressed = same and report['frames_written'] > previous['frames_written'] and report['bytes_written'] > previous['bytes_written']
        if not same:
            self.progress_at = None
        elif progressed:
            self.progress_at = now
        self.report, self.received_at = dict(report), now

    def view(self, now):
        if self.report is None or now - self.received_at > self.timeout:
            return 'UNKNOWN'
        r = self.report
        if r.get('error'):
            return 'ERROR'
        if not r['recording']:
            return 'NOT_RECORDING'
        if not r['frames_written'] or not r['bytes_written']:
            return 'START_UNCONFIRMED'
        write_age = (r['uptime_ms'] - r['last_write_ms']) / 1000 + now - self.received_at
        if write_age > self.timeout or (self.progress_at is not None and now - self.progress_at > self.timeout):
            return 'WRITE_STALLED'
        if self.progress_at is None:
            return 'PROGRESS_UNCONFIRMED'
        return 'WRITING_REPORTED'
