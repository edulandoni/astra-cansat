/* Estructura ASCII del anexo 2026/27 con datos de simulación y decisiones pendientes explícitas. */
(function (root, factory) {
  const api = factory(typeof module === 'object' && module.exports ? require('./core.js') : root.CanSat);
  if (typeof module === 'object' && module.exports) module.exports = api; else root.Ground = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function (C) {
  'use strict';
  const TRANSPORT = 'CONAE-ASCII-S/0.1';
  const FIELDS = ['TEAM_ID','MISSION_TIME','PACKET_COUNT','MODE','STATE','ALTITUDE','TEMPERATURE','PRESSURE','VOLTAGE','CURRENT',
    'GYRO_R','GYRO_P','GYRO_Y','ACCEL_R','ACCEL_P','ACCEL_Y','GPS_TIME','GPS_ALTITUDE','GPS_LATITUDE','GPS_LONGITUDE','GPS_SATS','CMD_ECHO'];
  const MEASURES = {ALTITUDE:'altitude',TEMPERATURE:'temperature',PRESSURE:'pressure',VOLTAGE:'voltage',CURRENT:'current',
    GYRO_R:'gx',GYRO_P:'gy',GYRO_Y:'gz',ACCEL_R:'ax',ACCEL_P:'ay',ACCEL_Y:'az',GPS_ALTITUDE:'gpsAltitude',
    GPS_LATITUDE:'lat',GPS_LONGITUDE:'lon',GPS_SATS:'satellites'};
  const STATES = ['LAUNCH_PAD','ASCENT','APOGEE','DESCENT','PROBE_RELEASE','PAYLOAD_RELEASE','LANDED'];
  const PHASE = {LAUNCH_PAD:'PREPARADO',ASCENT:'ASCENSO',APOGEE:'APOGEO',DESCENT:'DESCENSO',PROBE_RELEASE:'TRANSICION',PAYLOAD_RELEASE:'TRANSICION',LANDED:'ATERRIZADO'};
  const clock = seconds => {
    const n = ((Math.floor(seconds) % 86400) + 86400) % 86400;
    return [Math.floor(n/3600),Math.floor(n/60)%60,n%60].map(v=>String(v).padStart(2,'0')).join(':');
  };
  const validClock = str => /^([01]\d|2[0-3]):[0-5]\d:[0-5]\d$/.test(str);
  const seconds = str => str.split(':').reduce((sum,v)=>sum*60+Number(v),0);
  const optional = value => value === '' ? null : Number(value);
  function parseFrame(raw, team = '0000') {
    if (/[^\x20-\x7e]/.test(raw)) throw Error('Se esperaba texto ASCII sin caracteres de control.');
    const parts = raw.split(',');
    if (parts.length < 22 || parts.length === 23 || (parts.length > 22 && parts[22] !== '')) throw Error('Campos o separador opcional incorrectos.');
    const f = Object.fromEntries(FIELDS.map((name,i)=>[name,parts[i]]));
    if (!/^\d{4}$/.test(f.TEAM_ID) || f.TEAM_ID !== team) throw Error('TEAM_ID no coincide con el equipo de prueba.');
    if (f.MODE !== 'S') throw Error('Sólo se aceptan paquetes S en esta estación de simulación.');
    if (!validClock(f.MISSION_TIME) || (f.GPS_TIME !== '' && !validClock(f.GPS_TIME))) throw Error('Hora UTC inválida.');
    if (!/^[1-9]\d*$/.test(f.PACKET_COUNT) || !Number.isSafeInteger(Number(f.PACKET_COUNT))) throw Error('Contador inválido.');
    if (!STATES.includes(f.STATE)) throw Error('Estado de software desconocido.');
    if (f.CMD_ECHO.length > 80 || !/^[A-Za-z0-9_]*$/.test(f.CMD_ECHO)) throw Error('Eco de comando incompatible con el perfil de práctica.');
    for (const key of Object.keys(MEASURES)) {
      if (f[key] !== '' && !/^-?\d+(\.\d+)?$/.test(f[key])) throw Error('Campo numérico inválido: '+key);
      if (f[key] !== '' && !Number.isFinite(Number(f[key]))) throw Error('Número no finito: '+key);
    }
    if (f.GPS_SATS !== '' && !/^\d+$/.test(f.GPS_SATS)) throw Error('GPS_SATS debe ser entero.');
    f.OPTIONAL_DATA = parts.slice(23);
    return f;
  }
  function generateFrame(t, config = {}) {
    const generated = C.generated(t,config.seed || 42), m=generated.measurements;
    const missingGPS = config.gps && t>=65 && t<=85;
    const fixed = (key,n) => m[key] === null ? '' : m[key].toFixed(n);
    const state = generated.phase === 'PREPARADO' ? 'LAUNCH_PAD' : generated.phase === 'ASCENSO' ? 'ASCENT' :
      generated.phase === 'APOGEO' ? 'APOGEE' : generated.phase === 'ATERRIZADO' ? 'LANDED' : generated.phase === 'TRANSICION' ? 'PROBE_RELEASE' : 'DESCENT';
    const utc = clock((config.utcStartSeconds === undefined ? 43200 : config.utcStartSeconds)+t);
    const values = [config.team || '0000',utc,String(config.txSeq || t+1),'S',state,fixed('altitude',1),fixed('temperature',1),fixed('pressure',1),
      fixed('voltage',1),fixed('current',2),fixed('gx',2),fixed('gy',2),fixed('gz',2),fixed('ax',2),fixed('ay',2),fixed('az',2),
      missingGPS?'':utc,missingGPS?'':fixed('gpsAltitude',1),missingGPS?'':fixed('lat',4),missingGPS?'':fixed('lon',4),missingGPS?'':String(m.satellites),
      config.echo || '', '', 'SOLAR_SIGNAL='+(0.8+Math.sin(t/20)*0.04).toFixed(2), 'RESTART_COUNT='+(config.reset && t>=75 ? 1 : 0)];
    return values.join(',')+'\r';
  }
  function chunksFor(t, config = {}) {
    if (config.telemetryOn === false || config.gap && t>=30 && t<=38) return [];
    let wire = generateFrame(t,config);
    if (config.corrupt && t%17===10) wire='0000,PAQUETE_DANADO\r';
    else if (config.duplicate && t%13===7) wire+=wire;
    const encoded=C.bytes(wire); if(config.fragment===false) return [encoded];
    const sizes=[7,29,83,11,137],chunks=[];
    for(let i=0,j=0;i<encoded.length;j++) {const end=Math.min(encoded.length,i+sizes[(j+t)%sizes.length]);chunks.push(encoded.slice(i,end));i=end;}
    return chunks;
  }
  const COMMAND = {CAL:['CAL','CAL'],ST_GPS:['ST,GPS','STGPS'],CX_ON:['CX,ON','CXON'],CX_OFF:['CX,OFF','CXOFF'],
    INFO:['INFO,BATT_SOLAR','INFOBATT_SOLAR'],MEC_DEMO:['MEC,DEMO,ON','MECDEMOON'],PING:['PING','PING'],MARCA:['MARCA','MARCA']};
  class Receiver extends C.Receiver {
    constructor(meta={}) {
      super({...meta,transport:TRANSPORT}); this.team=meta.team || '0000';
      if(!/^\d{4}$/.test(this.team))throw Error('Equipo de simulación inválido.');
      this.lastRestart=0; this.counterEpoch=1; this.highestCount=0;
    }
    parse(raw,at) {
      let fields;
      try { fields=parseFrame(raw,this.team); } catch(error) {this.reject(raw,error.message,at);return;}
      const extra=Object.fromEntries(fields.OPTIONAL_DATA.map(s=>{const pos=s.indexOf('=');return pos<0?[s,'']:[s.slice(0,pos),s.slice(pos+1)];}));
      const restart=Number(extra.RESTART_COUNT||0),seq=Number(fields.PACKET_COUNT);
      if (Number.isInteger(restart) && restart>this.lastRestart) {
        if (seq < this.highestCount) {this.counterEpoch++;this.event('warning','Reinicio con contador retrocedido: continuidad incierta.',at);}
        else {this.counts.resets++;this.event('reset','Reinicio simulado: contador y hora conservados.',at);}
        this.lastRestart=restart;
      }
      this.highestCount=Math.max(this.highestCount,seq);
      const obj={v:C.VERSION,source:'simulation',team:this.team,boot:'counter-epoch-'+this.counterEpoch,
        seq,sent:at,phase:PHASE[fields.STATE],measurements:{},protocolFields:fields};
      for(const [field,key] of Object.entries(MEASURES)) obj.measurements[key]=optional(fields[field]);
      const before=this.raw.length, sample=super.parse(JSON.stringify(obj),at);
      if(this.raw.length>before) this.raw[this.raw.length-1].raw=raw;
      if(sample && !sample.duplicate && !sample.outOfOrder) for(const cmd of this.commands) {
        if(cmd.state==='sent' && cmd.expectedEcho===fields.CMD_ECHO) {cmd.state='echo_confirmed';cmd.echoAt=at;this.event('command','Eco recibido: '+fields.CMD_ECHO,at);}
      }
      return sample;
    }
    command(name,at,acknowledged=true,log=true) {
      const cmd=super.command(name,at,acknowledged,log);
      const [args,echo]=COMMAND[name];cmd.wire='CMD,'+this.team+','+args;cmd.expectedEcho=echo;
      cmd.state=acknowledged?'sent':'unconfirmed';cmd.functionalResult=null;
      this.events[this.events.length-1].message=cmd.wire+(acknowledged?' · enviado al emisor ficticio':' · sin respuesta esperada');
      return cmd;
    }
  }
  function createReceiver(meta={}) {return meta.transport === undefined || meta.transport===TRANSPORT ? new Receiver(meta) : new C.Receiver(meta);}
  function validateSession(data) {
    C.validateSession(data);
    if(data.meta.transport && data.meta.transport!==TRANSPORT) throw Error('Transporte de sesión desconocido.');
    return data;
  }
  function replay(data) {
    validateSession(data);
    const receiver=data.meta.transport===TRANSPORT?new Receiver(data.meta):new C.Receiver(data.meta);
    for(const op of data.operations) {
      if(op.type==='chunk')receiver.feed(Uint8Array.from(op.bytes),op.at);else receiver.command(op.name,op.at,op.acknowledged);
    }
    return receiver;
  }
  function csv(receiver) {
    if(receiver.meta.transport!==TRANSPORT) return C.csv(receiver);
    const data=receiver.raw.filter(entry=>entry.accepted).map(entry=>entry.raw.split(','));
    const width=Math.max(22,...data.map(row=>row.length));
    const headers=FIELDS.slice();if(width>22)headers.push('',...Array.from({length:width-23},(_,i)=>'OPTIONAL_DATA_'+(i+1)));
    const rows=[headers,...data.map(row=>Array.from({length:width},(_,i)=>row[i]||''))];
    const cell=v=>{let text=String(v);if(/^[=+@-]/.test(text)&&!/^[-+]?\d+(\.\d+)?$/.test(text))text="'"+text;return '"'+text.replace(/"/g,'""')+'"';};
    return rows.map(row=>row.map(cell).join(',')).join('\r\n');
  }
  return {TRANSPORT,FIELDS,MEASURES,STATES,clock,seconds,parseFrame,generateFrame,chunksFor,Receiver,createReceiver,validateSession,replay,csv,COMMAND};
});
