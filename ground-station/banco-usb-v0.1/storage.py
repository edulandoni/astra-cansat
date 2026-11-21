import csv
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from protocol import FIELDS

class Recorder:
    def __init__(self, root, team, backup=None):
        self.paths = []
        self.files = []
        self.writers = []
        self.error = ''
        session = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')+'_'+uuid.uuid4().hex[:12]
        self.directory = Path(root)/session
        self.directory.mkdir(parents=True, exist_ok=False)
        self.raw = (self.directory/'reception.jsonl').open('x',encoding='utf-8')
        roots = [self.directory]
        if backup:
            dest = Path(backup)/session
            dest.mkdir(parents=True,exist_ok=False)
            roots.append(dest)
        for dest in roots:
            path = dest/f'Flight_{team}.csv'
            handle = path.open('x',newline='',encoding='utf-8')
            writer = csv.writer(handle)
            writer.writerow(FIELDS)
            handle.flush()
            self.paths.append(path)
            self.files.append(handle)
            self.writers.append(writer)
    def event(self, **values):
        self.raw.write(json.dumps({'received_utc':datetime.now(timezone.utc).isoformat(), **values},ensure_ascii=False)+'\n')
        self.raw.flush()
    def save(self, packet):
        # Optional columns are not silently dropped. This v0.1 adapter explicitly
        # rejects them at ingestion until their header definition is agreed.
        for handle,writer in zip(self.files,self.writers):
            try:
                writer.writerow(packet.values)
                handle.flush()
                os.fsync(handle.fileno())
            except OSError as exc:
                self.error = str(exc)
    def close(self):
        for handle in self.files+[self.raw]:
            handle.close()
