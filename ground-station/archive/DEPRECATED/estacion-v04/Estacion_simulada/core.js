/* Núcleo independiente del navegador. Protocolo de práctica CS-SIM/1, no CONAE. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.CanSat = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const VERSION = 'CS-SIM/1';
  const LIMITS = { frames: 10000, bytes: 4000000, frameChars: 4096, ticks: 3600 };
  const SPECS = {
    altitude: ['m AGL', -50, 2000], temperature: ['°C', -80, 100], pressure: ['kPa', 10, 120],
    voltage: ['V', 0, 20], current: ['A', 0, 10],
    ax: ['m/s²', -200, 200], ay: ['m/s²', -200, 200], az: ['m/s²', -200, 200],
    gx: ['°/s', -2000, 2000], gy: ['°/s', -2000, 2000], gz: ['°/s', -2000, 2000],
    lat: ['°', -90, 90], lon: ['°', -180, 180], gpsAltitude: ['m MSL', -500, 10000], satellites: ['', 0, 60]
  };
  const PHASES = ['PREPARADO', 'ASCENSO', 'APOGEO', 'DESCENSO', 'DESCENSO_RAPIDO', 'TRANSICION', 'DESCENSO_LENTO', 'ATERRIZADO'];
  const COMMANDS = ['PING', 'MARCA', 'CAL', 'ST_GPS', 'CX_ON', 'CX_OFF', 'INFO', 'MEC_DEMO'];
  const bytes = s => new TextEncoder().encode(s);
  const round = (x, n = 2) => Math.round(x * 10 ** n) / 10 ** n;
  function generated(t, seed = 42) {
    const noise = (key, a = 1) => Math.sin((t + seed * 0.17 + key * 4.13) * (key * 0.07 + 1.31)) * a;
    let h = 0, phase = 'PREPARADO';
    if (t >= 5 && t < 45) { h = (t - 5) * 15; phase = 'ASCENSO'; }
    else if (t >= 45 && t < 48) { h = 600; phase = 'APOGEO'; }
    else if (t >= 48 && t < 56) { h = 600 - (t - 48) * 15; phase = 'DESCENSO_RAPIDO'; }
    else if (t >= 56 && t < 152) { h = 480 - (t - 56) * 5; phase = t < 59 ? 'TRANSICION' : 'DESCENSO_LENTO'; }
    else if (t >= 152) phase = 'ATERRIZADO';
    const flight = h > 0;
    const lat = -34.17 + (flight ? (t - 5) * 0.000003 : t >= 152 ? 147 * 0.000003 : 0);
    const lon = -58.95 + (flight ? Math.sin(t / 40) * 0.0003 : t >= 152 ? Math.sin(152 / 40) * 0.0003 : 0);
    return { v: VERSION, source: 'simulation', team: 'UTN-FRD-DEMO', boot: 'boot-1', seq: t + 1,
      sent: t, phase, measurements: {
        altitude: round(h + (flight ? noise(1, 0.35) : 0), 1),
        temperature: round(23 - h * 0.0065 + noise(2, 0.12), 1),
        pressure: round(101.325 * (1 - h / 44330) ** 5.255, 2),
        voltage: round(6.6 - t * 0.0008 + noise(3, 0.015), 2), current: round(0.18 + (flight ? 0.04 : 0) + noise(4, 0.01), 3),
        ax: round(noise(5, flight ? 1.2 : 0.03)), ay: round(noise(6, flight ? 0.8 : 0.03)),
        az: round(9.81 + noise(7, flight ? 0.6 : 0.04)), gx: round(noise(8, flight ? 14 : 0.2)),
        gy: round(noise(9, flight ? 9 : 0.2)), gz: round(noise(10, flight ? 6 : 0.2)),
        lat: round(lat, 6), lon: round(lon, 6), gpsAltitude: round(h + 20, 1), satellites: 9
      } };
  }
  function chunksFor(t, config = {}) {
    const msg = generated(t, config.seed || 42);
    if (config.reset && t >= 75) { msg.boot = 'boot-2'; msg.seq = t - 74; }
    if (config.gps && t >= 65 && t <= 85) {
      for (const k of ['lat', 'lon', 'gpsAltitude', 'satellites']) msg.measurements[k] = null;
    }
    if (config.gap && t >= 30 && t <= 38) return [];
    let wire = JSON.stringify(msg) + '\n';
    if (config.corrupt && t % 17 === 10) wire = '{"v":"CS-SIM/1","broken":\n';
    if (config.duplicate && t % 13 === 7) wire += JSON.stringify(msg) + '\n';
    const encoded = bytes(wire);
    if (config.fragment === false) return [encoded];
    const sizes = [7, 29, 83, 11, 137];
    const chunks = [];
    for (let i = 0, j = 0; i < encoded.length; j++) {
      const end = Math.min(encoded.length, i + sizes[(j + t) % sizes.length]);
      chunks.push(encoded.slice(i, end)); i = end;
    }
    return chunks;
  }
  class Receiver {
    constructor(meta = {}) {
      this.meta = { id: meta.id || 'sim-' + Date.now() + '-' + Math.random().toString(16).slice(2, 8), origin: 'simulation', protocol: VERSION,
        startedUTC: meta.startedUTC || new Date().toISOString(), clock: 'simulation-monotonic-seconds', ...meta };
      if (this.meta.origin !== 'simulation' || this.meta.protocol !== VERSION ||
        typeof this.meta.id !== 'string' || !/^[a-zA-Z0-9_-]{1,80}$/.test(this.meta.id)) throw Error('Identidad de sesión de simulación inválida.');
      this.decoder = new TextDecoder('utf-8', { fatal: true });
      this.delimiter = this.meta.transport === 'CONAE-ASCII-S/0.1' ? '\r' : '\n';
      this.buffer = ''; this.discarding = false; this.currentTime = 0;
      this.raw = []; this.samples = []; this.events = []; this.operations = [];
      this.epochs = new Map(); this.activeBoot = null; this.latest = null; this.lastAcceptedAt = null;
      this.counts = { chunks: 0, bytes: 0, frames: 0, valid: 0, rejected: 0, unique: 0, duplicates: 0, outOfOrder: 0, resets: 0 };
      this.commands = []; this.stopped = false;
    }
    event(kind, message, at = this.currentTime) { this.events.push({ at, kind, message }); }
    feed(chunk, at, log = true) {
      if (this.stopped) return;
      if (!(chunk instanceof Uint8Array) || !Number.isFinite(at) || at < this.currentTime) throw Error('Fragmento o tiempo inválido.');
      if (this.counts.bytes + chunk.length > LIMITS.bytes || this.raw.length >= LIMITS.frames) {
        this.stopped = true; this.event('limit', 'Registro lleno. Exportá la sesión y comenzá otra.', at); return;
      }
      this.currentTime = at; this.counts.chunks++; this.counts.bytes += chunk.length;
      if (log) this.operations.push({ type: 'chunk', at, bytes: Array.from(chunk) });
      let decoded;
      try { decoded = this.decoder.decode(chunk, { stream: true }); }
      catch (_) {
        this.reject(this.buffer, 'Codificación UTF-8 inválida', at); this.buffer = '';
        this.decoder = new TextDecoder('utf-8', { fatal: true }); this.discarding = true; return;
      }
      for (const character of decoded) {
        if (character === this.delimiter) {
          if (!this.discarding && this.buffer.length) this.parse(this.buffer.replace(/\r$/, ''), at);
          this.buffer = ''; this.discarding = false;
        } else if (!this.discarding) {
          this.buffer += character;
          if (this.buffer.length > LIMITS.frameChars) {
            this.reject(this.buffer, 'Mensaje excede el límite de 4096 caracteres', at);
            this.buffer = ''; this.discarding = true;
          }
        }
      }
    }
    reject(raw, reason, at) {
      if (this.raw.length >= LIMITS.frames) { this.stopped = true; return; }
      this.counts.frames++; this.counts.rejected++;
      this.raw.push({ id: this.counts.frames, at, channel: 'simulated-byte-stream', raw, accepted: false, reason });
      this.event('rejected', reason, at);
    }
    parse(raw, at) {
      if (this.raw.length >= LIMITS.frames) { this.stopped = true; return; }
      let obj;
      try { obj = JSON.parse(raw); } catch (_) { this.reject(raw, 'JSON incompleto o dañado', at); return; }
      if (!obj || obj.v !== VERSION || obj.source !== 'simulation' || !Number.isSafeInteger(obj.seq) || obj.seq < 1 ||
        typeof obj.boot !== 'string' || !obj.boot.length || obj.boot.length > 64 || !Number.isFinite(obj.sent) || obj.sent < 0 ||
        !PHASES.includes(obj.phase) || !obj.measurements || typeof obj.measurements !== 'object' || Array.isArray(obj.measurements)) {
        this.reject(raw, 'Cabecera o estructura incompatible con CS-SIM/1', at); return;
      }
      const measures = {};
      for (const [k, [unit, min, max]] of Object.entries(SPECS)) {
        const v = obj.measurements[k];
        const quality = v === null || v === undefined ? 'missing' : typeof v !== 'number' || !Number.isFinite(v) ? 'rejected' : v < min || v > max ? 'out_of_range' : 'valid';
        measures[k] = { value: quality === 'valid' ? v : null, original: v === undefined ? null : v, unit, quality };
      }
      let epoch = this.epochs.get(obj.boot);
      if (!epoch) {
        epoch = { first: obj.seq, max: obj.seq, seen: new Set() }; this.epochs.set(obj.boot, epoch);
        if (this.activeBoot !== null) { this.counts.resets++; this.event('reset', 'Nueva época del emisor: ' + obj.boot, at); }
        this.activeBoot = obj.boot;
      }
      const duplicate = epoch.seen.has(obj.seq);
      const outOfOrder = !duplicate && (obj.boot !== this.activeBoot || obj.seq < epoch.max);
      this.counts.frames++; this.counts.valid++;
      if (duplicate) { this.counts.duplicates++; this.event('duplicate', 'Secuencia duplicada ' + obj.seq, at); }
      else {
        epoch.seen.add(obj.seq); epoch.first = Math.min(epoch.first, obj.seq); epoch.max = Math.max(epoch.max, obj.seq);
        this.counts.unique++; if (outOfOrder) this.counts.outOfOrder++;
      }
      const sample = { at, seq: obj.seq, boot: obj.boot, sent: obj.sent, phase: obj.phase, measures,
        protocolFields: this.meta.transport === 'CONAE-ASCII-S/0.1' ? obj.protocolFields || null : null, duplicate, outOfOrder };
      this.raw.push({ id: this.counts.frames, at, channel: 'simulated-byte-stream', raw, accepted: true,
        reason: duplicate ? 'Duplicado' : outOfOrder ? 'Llegada tardía' : 'Válido' });
      if (!duplicate && !outOfOrder) {
        if (this.latest && this.latest.phase !== sample.phase) this.event('phase', sample.phase, at);
        this.latest = sample; this.lastAcceptedAt = at; this.samples.push(sample);
      }
      return sample;
    }
    get missing() {
      let n = 0; for (const e of this.epochs.values()) n += e.max - e.first + 1 - e.seen.size; return n;
    }
    get observedSpan() {
      let n = 0; for (const e of this.epochs.values()) n += e.max - e.first + 1; return n;
    }
    command(name, at, acknowledged = true, log = true) {
      if (!COMMANDS.includes(name) || !Number.isFinite(at) || at < this.currentTime) throw Error('Comando de práctica inválido.');
      this.currentTime = at;
      if (log) this.operations.push({ type: 'command', name, at, acknowledged: Boolean(acknowledged) });
      const command = { id: this.commands.length + 1, name, at, origin: 'simulation',
        state: acknowledged ? 'echo_confirmed' : 'unconfirmed', functionalResult: null };
      this.commands.push(command); this.event('command', name + (acknowledged ? ': eco simulado recibido' : ': sin confirmación'), at);
      return command;
    }
    export(nextTick = 0, config = {}) {
      return { format: 'CS-SIM-SESSION/1', meta: this.meta, nextTick, config,
        operations: this.operations, raw: this.raw, counts: this.counts, commands: this.commands };
    }
  }
  function validateSession(data) {
    if (!data || data.format !== 'CS-SIM-SESSION/1' || !data.meta || data.meta.origin !== 'simulation' ||
      data.meta.protocol !== VERSION || typeof data.meta.id !== 'string' || !/^[a-zA-Z0-9_-]{1,80}$/.test(data.meta.id) ||
      typeof data.meta.startedUTC !== 'string' || !Number.isFinite(Date.parse(data.meta.startedUTC)) ||
      !Number.isInteger(data.nextTick) || data.nextTick < 0 || data.nextTick > LIMITS.ticks ||
      !Array.isArray(data.operations) || data.operations.length > 150000) throw Error('Archivo de sesión de práctica incompatible.');
    let time = 0, size = 0;
    for (const op of data.operations) {
      if (!Number.isFinite(op.at) || op.at < time || op.at > LIMITS.ticks) throw Error('Tiempo de recepción inválido.');
      time = op.at;
      if (op.type === 'chunk') {
        if (!Array.isArray(op.bytes) || !op.bytes.length || op.bytes.length > LIMITS.frameChars ||
          op.bytes.some(b => !Number.isInteger(b) || b < 0 || b > 255)) throw Error('Fragmento inválido.');
        size += op.bytes.length; if (size > LIMITS.bytes) throw Error('Sesión demasiado grande.');
      } else if (op.type !== 'command' || !COMMANDS.includes(op.name) || typeof op.acknowledged !== 'boolean') throw Error('Operación desconocida.');
    }
    if (time > data.nextTick) throw Error('Duración inconsistente.');
    return data;
  }
  function replay(data) {
    validateSession(data); const receiver = new Receiver(data.meta);
    for (const op of data.operations) {
      if (op.type === 'chunk') receiver.feed(Uint8Array.from(op.bytes), op.at);
      else receiver.command(op.name, op.at, op.acknowledged);
    }
    return receiver;
  }
  function csv(receiver) {
    const keys = Object.keys(SPECS);
    const rows = [['origin', 'session', 'receive_s', 'send_s', 'epoch', 'sequence', 'phase', ...keys.flatMap(k => [k, k + '_unit', k + '_quality'])]];
    for (const s of receiver.samples) rows.push(['simulation', receiver.meta.id, s.at, s.sent, s.boot, s.seq, s.phase,
      ...keys.flatMap(k => [s.measures[k].value, s.measures[k].unit, s.measures[k].quality])]);
    const cell = v => { const str = v === null || v === undefined ? '' : String(v); return '"' + str.replace(/"/g, '""') + '"'; };
    return rows.map(row => row.map(cell).join(',')).join('\r\n');
  }
  return { VERSION, SPECS, PHASES, COMMANDS, LIMITS, Receiver, generated, chunksFor, replay, validateSession, csv, bytes };
});
