const {test}=require('node:test'),assert=require('node:assert/strict');
const C=require('../core.js');
const G=require('../protocol.js');
const meta={id:'test-v04',team:'0000',startedUTC:'2026-10-08T00:00:00Z'};
function run(config={},n=160){const r=new G.Receiver(meta);for(let t=0;t<n;t++)for(const chunk of G.chunksFor(t,config))r.feed(chunk,t);return r;}
test('all 22 base fields, optional delimiter, ASCII and CR termination are generated',()=>{
 const wire=G.generateFrame(0);assert.equal(wire.at(-1),'\r');assert(!wire.includes('\n'));assert(/^[\x20-\x7e]*\r$/.test(wire));
 const f=G.parseFrame(wire.slice(0,-1));assert.equal(Object.keys(f).length,23);assert.equal(f.MODE,'S');assert.equal(f.MISSION_TIME,'12:00:00');assert.equal(f.OPTIONAL_DATA.length,2);
 assert.equal(f.CURRENT.split('.')[1].length,2);assert.equal(f.PRESSURE.split('.')[1].length,1);
});
test('one-byte fragments, concatenated messages and whole frames yield identical data',()=>{
 const a=run({fragment:false},5),b=new G.Receiver(meta);const wire=Array.from({length:5},(_,t)=>G.generateFrame(t)).join('');
 for(const byte of C.bytes(wire))b.feed(Uint8Array.of(byte),4);
 assert.deepEqual(a.samples.map(s=>s.protocolFields),b.samples.map(s=>s.protocolFields));assert.equal(b.counts.valid,5);
 const c=run({fragment:true},5);assert.deepEqual(a.samples,c.samples);assert.deepEqual(a.raw,c.raw);
});
test('LF does not act as a packet terminator',()=>{
 const r=new G.Receiver(meta);r.feed(C.bytes(G.generateFrame(0).replace('\r','\n')),0);assert.equal(r.counts.frames,0);assert(r.buffer.length>0);
 r.feed(C.bytes('\r'),1);assert.equal(r.counts.rejected,1);
});
test('wrong team, F origin, invalid clocks, malformed numbers and bad optional separators are rejected',()=>{
 const wire=G.generateFrame(0).slice(0,-1);
 for(const mutate of [p=>p[0]='1234',p=>p[3]='F',p=>p[1]='25:00:00',p=>p[8]='abc',p=>p[22]='bad',p=>p[20]='1.5']){
  const parts=wire.split(',');mutate(parts);assert.throws(()=>G.parseFrame(parts.join(',')));
 }
});
test('GPS absence is distinct from numeric zero and leaves other sensors valid',()=>{
 const r=run({gps:true},70);assert.equal(r.latest.measures.lat.value,null);assert.equal(r.latest.measures.lat.quality,'missing');
 assert.equal(r.latest.protocolFields.GPS_TIME,'');assert.equal(r.latest.measures.voltage.quality,'valid');
 const initial=run({},1);assert.equal(initial.latest.measures.altitude.value,0);
});
test('duplicate packets do not refresh latest-data time or add graph points',()=>{
 const r=new G.Receiver(meta),wire=C.bytes(G.generateFrame(0));r.feed(wire,0);r.feed(wire,9);
 assert.equal(r.counts.valid,2);assert.equal(r.counts.duplicates,1);assert.equal(r.samples.length,1);assert.equal(r.lastAcceptedAt,0);
 assert.equal(G.csv(r).split('\r\n').length,3);
});
test('late valid packet repairs a gap without rewinding the latest display',()=>{
 const r=new G.Receiver(meta);for(const [seq,at]of [[10,0],[13,1],[11,2]])r.feed(C.bytes(G.generateFrame(at,{txSeq:seq})),at);
 assert.equal(r.missing,1);assert.equal(r.latest.seq,13);assert.equal(r.counts.outOfOrder,1);assert.equal(G.csv(r).split('\r\n').length,4);
});
test('fault session and restart preserve transmit counter and mission UTC',()=>{
 const r=run({gap:true,duplicate:true,corrupt:true,gps:true,reset:true});
 assert.equal(r.counts.unique,142);assert.equal(r.counts.valid,153);assert.equal(r.counts.frames,162);assert.equal(r.counts.rejected,9);assert.equal(r.counts.duplicates,11);assert.equal(r.counts.resets,1);assert.equal(r.missing,18);
 const s=r.samples.find(s=>s.at===75);assert.equal(s.seq,76);assert.equal(s.protocolFields.MISSION_TIME,'12:01:15');assert.equal(r.latest.protocolFields.STATE,'LANDED');
});
test('command is sent first; only a received telemetry echo confirms it',()=>{
 const r=new G.Receiver(meta),cmd=r.command('CAL',0,true);assert.equal(cmd.state,'sent');assert.equal(cmd.wire,'CMD,0000,CAL');
 r.feed(C.bytes(G.generateFrame(0,{echo:'CAL'})),0);assert.equal(cmd.state,'echo_confirmed');assert.equal(cmd.functionalResult,null);
 const off=r.command('CX_OFF',1,true);assert.equal(off.state,'sent');assert.equal(G.chunksFor(1,{telemetryOn:false}).length,0);assert.equal(off.state,'sent');
});
test('JSON replay preserves ASCII bytes, raw messages, samples, counts and command lifecycle',()=>{
 const r=new G.Receiver(meta);r.command('ST_GPS',0,true);
 for(let t=0;t<160;t++)for(const chunk of G.chunksFor(t,{echo:'STGPS',gap:true,corrupt:true,reset:true}))r.feed(chunk,t);
 const data=JSON.parse(JSON.stringify(r.export(160,{}))),other=G.replay(data);
 for(const key of ['raw','samples','counts','commands','operations','events'])assert.deepEqual(other[key],r[key]);
 assert.equal(other.raw[0].raw[0],'0');assert.equal(other.meta.transport,G.TRANSPORT);
});
test('legacy v03 JSON can still replay without inventing its missing official fields',()=>{
 const r=new C.Receiver(meta);for(let t=0;t<3;t++)for(const chunk of C.chunksFor(t))r.feed(chunk,t);
 const other=G.replay(r.export(3,{}));assert.equal(other.counts.valid,3);assert.equal(other.latest.protocolFields,null);
});
test('CSV includes all accepted receptions and pads optional columns',()=>{
 const r=new G.Receiver(meta);r.feed(C.bytes(G.generateFrame(0)),0);const minimal=G.generateFrame(1).split(',').slice(0,22).join(',')+'\r';r.feed(C.bytes(minimal),1);
 const lines=G.csv(r).split('\r\n');assert.equal(lines.length,3);assert.equal(lines[0].split(',').length,25);assert.equal(lines[2].split(',').length,25);assert(lines[0].startsWith('"TEAM_ID","MISSION_TIME"'));
});
test('bounded corrupt frame is recorded, recovery continues, unsafe metadata is refused',()=>{
 const r=new G.Receiver(meta);r.feed(C.bytes('x'.repeat(10000)+'\r'),0);r.feed(C.bytes(G.generateFrame(1)),1);assert.equal(r.counts.rejected,1);assert.equal(r.counts.valid,1);
 assert.throws(()=>G.replay({...r.export(2,{}),meta:{...r.meta,origin:'flight'}}));
});
