(function(){
  'use strict';
  const C=window.CanSat,G=window.Ground,L=window.Learning,$=id=>document.getElementById(id);
  const fieldSpecs={TEAM_ID:['Equipo',''],MISSION_TIME:['UTC misión',''],PACKET_COUNT:['Transmitidos',''],MODE:['Modo',''],STATE:['Estado software',''],CMD_ECHO:['Eco CMD',''],GPS_TIME:['UTC GPS',''],GPS_SATS:['Satélites GPS',''],solar:['Señal solar','norm.'],
    ALTITUDE:['Altitud AGL','m'],TEMPERATURE:['Temp. interna','°C'],PRESSURE:['Presión','kPa'],VOLTAGE:['Tensión','V'],CURRENT:['Corriente','A'],GPS_ALTITUDE:['Altitud GPS MSL','m'],GPS_LATITUDE:['Latitud','°'],GPS_LONGITUDE:['Longitud','°'],
    GYRO_R:['Giro R / X','°/s'],GYRO_P:['Giro P / Y','°/s'],GYRO_Y:['Giro Yaw / Z','°/s'],ACCEL_R:['Acel. R / X','m/s² †'],ACCEL_P:['Acel. P / Y','m/s² †'],ACCEL_Y:['Acel. Yaw / Z','m/s² †'],received:['Recibidos válidos',''],lost:['Huecos observados*',''],freshness:['Antigüedad','s']};
  const groups={'mission-readings':['TEAM_ID','MISSION_TIME','PACKET_COUNT','MODE','STATE','CMD_ECHO','GPS_TIME','GPS_SATS','solar'],
    'sensor-readings':['ALTITUDE','TEMPERATURE','PRESSURE','VOLTAGE','CURRENT','GPS_ALTITUDE','GPS_LATITUDE','GPS_LONGITUDE'],
    'motion-readings':['ACCEL_R','ACCEL_P','ACCEL_Y','GYRO_R','GYRO_P','GYRO_Y','received','lost','freshness']};
  const faults=[['fragment','Recepción por fragmentos','Un paquete se entrega en varias partes.'],['gap','Corte de enlace','Sin paquetes recibidos entre 30 y 38 s.'],['duplicate','Paquetes duplicados','Llegadas repetidas cada 13 ticks.'],['corrupt','Paquetes dañados','Estructura inválida cada 17 ticks.'],['gps','GPS sin solución','Campos GPS ausentes entre 65 y 85 s.'],['reset','Reinicio del emisor','A los 75 s, conservando contador y hora.']];
  const commandLabels={CAL:'CAL',ST_GPS:'Hora GPS',CX_ON:'CX ON',CX_OFF:'CX OFF',INFO:'INFO',MEC_DEMO:'MEC demo'};
  let r,tick=0,running=false,timer=null,config,replayData=null,replayIndex=0,resumeAfterHelp=false;
  let txSeq=0,telemetryOn=true,echo='',pendingFaults={fragment:true,gap:false,duplicate:false,corrupt:false,gps:false,reset:false};
  const time=n=>Math.floor(Math.max(0,n)/60).toString().padStart(2,'0')+':'+Math.floor(Math.max(0,n)%60).toString().padStart(2,'0');
  const now=()=>Math.max(0,tick-1);
  const age=()=>r.lastAcceptedAt===null?null:now()-r.lastAcceptedAt;
  function info(key,label){const b=document.createElement('button');b.className='info';b.dataset.help=key;b.textContent='ⓘ';b.setAttribute('aria-label',label||'Explicar '+L.topics[key][0]);return b;}
  for(const [id,keys]of Object.entries(groups))for(const key of keys){
    const row=document.createElement('div');row.className='data-row';row.id='row-'+key;
    const name=document.createElement('span');name.className='field-name';name.append(document.createTextNode(fieldSpecs[key][0]),info(key));
    const value=document.createElement('span');value.className='field-value';value.id='value-'+key;value.textContent='—';row.append(name,value);$(id).querySelector('.data-rows').append(row);
  }
  for(const [key,label]of Object.entries(commandLabels)){
    const wrap=document.createElement('span');wrap.className='with-help';const b=document.createElement('button');b.textContent=label;b.dataset.command=key;b.id='cmd-'+key;wrap.append(b,info(key));$('command-controls').append(wrap);
  }
  for(const [id,label,desc]of faults){
    L.topics['fault-'+id]=[label,desc,'Una estación debe seguir registrando y distinguir un problema de enlace de un dato físico. Este ensayo permite comprobarlo antes de disponer del vehículo.',
      L.topics.scenarios[3],L.topics.scenarios[4],'Escenario propio de práctica; ver descripción general de fallas.'];
    const row=document.createElement('div');row.className='scenario-choice';const input=document.createElement('input');input.type='checkbox';input.id='fault-'+id;input.checked=pendingFaults[id];
    input.addEventListener('change',()=>pendingFaults[id]=input.checked);
    const text=document.createElement('label');text.htmlFor=input.id;const strong=document.createElement('strong');strong.textContent=label;text.append(strong,document.createTextNode(desc));row.append(input,text,info('fault-'+id));$('scenario-options').append(row);
  }
  function pause(){running=false;clearInterval(timer);timer=null;$('play').textContent=tick?'▶ Continuar':'▶ Iniciar';}
  function schedule(){clearInterval(timer);timer=setInterval(advance,1000/Number($('speed').value));}
  function start(){if(isEnd())return;running=true;$('play').textContent='Ⅱ Pausar';schedule();render();}
  function isEnd(){return r.stopped || tick>=(replayData?replayData.nextTick:C.LIMITS.ticks);}
  function reset(){
    pause();tick=0;txSeq=0;telemetryOn=true;echo='';replayData=null;replayIndex=0;
    const utc=new Date(),utcStartSeconds=utc.getUTCHours()*3600+utc.getUTCMinutes()*60+utc.getUTCSeconds();
    config={...pendingFaults,seed:42,team:'0000',utcStartSeconds};
    r=new G.Receiver({team:'0000'});$('notice').textContent='Sólo datos ficticios. † Unidad ACCEL pendiente. * Huecos dentro del tramo observado. 0000 no asignado.';render();
  }
  function advance(){
    if(isEnd()){pause();render();return;}
    if(replayData){
      while(replayIndex<replayData.operations.length&&replayData.operations[replayIndex].at<=tick){const op=replayData.operations[replayIndex++];
        if(op.type==='chunk')r.feed(Uint8Array.from(op.bytes),op.at);else r.command(op.name,op.at,op.acknowledged);}
    }else{
      if(telemetryOn)txSeq++;
      for(const chunk of G.chunksFor(tick,{...config,txSeq,telemetryOn,echo}))r.feed(chunk,tick);
    }
    tick++;if(isEnd())pause();render();
  }
  function fieldValue(key){
    if(key==='received')return String(r.counts.valid);
    if(key==='lost')return r.observedSpan?String(r.missing):'—';
    if(key==='freshness')return age()===null?'—':String(age());
    const sample=r.latest;if(!sample)return '—';const fields=sample.protocolFields;
    if(key==='solar'){
      const solar=fields&&Array.isArray(fields.OPTIONAL_DATA)?((fields.OPTIONAL_DATA.find(s=>s.startsWith('SOLAR_SIGNAL='))||'').split('=')[1]||''):'';
      return /^\d+(\.\d+)?$/.test(solar)&&Number(solar)>=0&&Number(solar)<=1?solar:'—';
    }
    const measure=G.MEASURES[key]&&sample.measures[G.MEASURES[key]];
    if(measure&&measure.quality!=='valid')return '—';
    if(fields)return fields[key]||'—';
    if(measure&&measure.value!==null)return String(measure.value);
    if(key==='PACKET_COUNT')return String(sample.seq);
    return '—';
  }
  function draw(id,keys,range){
    const canvas=$(id),w=canvas.clientWidth,h=parseFloat(getComputedStyle(canvas).height),dpr=devicePixelRatio||1;
    if(!w||!h)return;canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);const ctx=canvas.getContext('2d');ctx.scale(dpr,dpr);
    const left=62,right=12,top=12,bottom=27,pw=w-left-right,ph=h-top-bottom;
    const t0=Math.max(0,now()-180),t1=Math.max(now(),t0+20),visible=r.samples.filter(s=>s.at>=t0);
    const values=visible.flatMap(s=>keys.map(k=>s.measures[k].value)).filter(v=>v!==null);
    if(values.length){const min=Math.min(...values),max=Math.max(...values),pad=(range[1]-range[0])*.05;range=[min<range[0]?min-pad:range[0],max>range[1]?max+pad:range[1]];}
    const x=t=>left+(t-t0)/(t1-t0)*pw,y=v=>top+(range[1]-v)/(range[1]-range[0])*ph;
    ctx.font='bold 19px Segoe UI,Arial';ctx.fillStyle='#000';const digits=range[1]<10?2:0;
    for(let i=0;i<=2;i++){const v=range[0]+(range[1]-range[0])*i/2,yy=y(v);ctx.strokeStyle='#aaa';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(left,yy);ctx.lineTo(w-right,yy);ctx.stroke();ctx.textAlign='right';ctx.fillText(v.toFixed(digits),left-7,yy+6);}
    ctx.lineWidth=2.5;ctx.strokeStyle='#000';ctx.beginPath();ctx.moveTo(left,top);ctx.lineTo(left,h-bottom);ctx.lineTo(w-right,h-bottom);ctx.stroke();
    const steps=w<420?2:4;
    for(let i=0;i<=steps;i++){const t=t0+(t1-t0)*i/steps;ctx.textAlign=i===0?'left':i===steps?'right':'center';ctx.fillText(Math.floor(t)+' s',x(t),h-3);}
    ctx.save();ctx.beginPath();ctx.rect(left,top,pw,ph);ctx.clip();
    keys.forEach((key,i)=>{ctx.strokeStyle='#000';ctx.lineWidth=3;ctx.setLineDash(i===0?[]:i===1?[10,5]:[2,5]);ctx.beginPath();let previous=null;
      for(const s of visible){const v=s.measures[key].value;if(v===null){previous=null;continue;}if(!previous||s.at-previous.at>1.5)ctx.moveTo(x(s.at),y(v));else ctx.lineTo(x(s.at),y(v));previous=s;}ctx.stroke();
    });ctx.restore();
  }
  function checkFit(){const warning=$('fit-warning');warning.hidden=true;const fits=$('station').getBoundingClientRect().bottom<=innerHeight&&document.documentElement.scrollWidth<=innerWidth;warning.hidden=fits;$('station').dataset.fits=String(fits);}
  function render(){
    $('session-clock').textContent=time(tick);const stale=age()!==null&&age()>=3;
    $('link').textContent=r.stopped?'Registro lleno':replayData?'REPRODUCCIÓN':age()===null?'Esperando datos':stale?'DESACTUALIZADO '+age()+' s':running?'Recibiendo · 1 Hz':'Ensayo pausado';
    for(const key of Object.keys(fieldSpecs)){
      const el=$('value-'+key),value=fieldValue(key);el.replaceChildren(document.createTextNode(value));
      if(value!=='—'&&fieldSpecs[key][1]){const unit=document.createElement('span');unit.className='unit';unit.textContent=fieldSpecs[key][1];el.append(unit);}
      const isMeasure=Boolean(G.MEASURES[key]);$('row-'+key).classList.toggle('stale',isMeasure&&stale);$('row-'+key).classList.toggle('invalid',isMeasure&&r.latest&&value==='—');
    }
    draw('chart-altitude',['altitude'],[0,650]);draw('chart-voltage',['voltage'],[6,7]);draw('chart-current',['current'],[0,.4]);draw('chart-accel',['ax','ay','az'],[-3,12]);draw('chart-gyro',['gx','gy','gz'],[-20,20]);
    for(const key of Object.keys(commandLabels))$('cmd-'+key).disabled=Boolean(replayData)||r.stopped;
    $('play').disabled=isEnd();$('step').disabled=isEnd();checkFit();
  }
  function showHelp(key){
    const topic=L.topics[key];if(!topic)return;resumeAfterHelp=running;pause();$('help-title').textContent=topic[0];$('help-body').replaceChildren();$('live-diagnostic').replaceChildren();
    const titles=['Qué es','Por qué sirve','Qué hace esta simulación','Cómo interpretarlo','Regla o alcance'];
    topic.slice(1).forEach((text,i)=>{const section=document.createElement('section');section.className='help-section';const h=document.createElement('h3'),p=document.createElement('p');h.textContent=titles[i];p.textContent=text;section.append(h,p);$('help-body').append(section);});
    if(key==='diagnostics')diagnosticDetails();
    if(key==='references')referenceDetails();
    $('help-dialog').showModal();
  }
  function diagnosticDetails(){
    const dl=document.createElement('dl');for(const [key,value]of Object.entries({...r.counts,huecos:r.missing,bufferCaracteres:r.buffer.length})){const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=key;dd.textContent=String(value);dl.append(dt,dd);}$('live-diagnostic').append(dl);
    const original=document.createElement('pre');original.textContent=r.raw.length?r.raw[r.raw.length-1].raw+'␍':'Sin mensaje completo.';$('live-diagnostic').append(original);
    const list=document.createElement('ol');for(const event of r.events.slice(-12).reverse()){const li=document.createElement('li');li.textContent=time(event.at)+' · '+event.message;list.append(li);}$('live-diagnostic').append(list);
    const commands=document.createElement('pre');commands.textContent=r.commands.map(c=>time(c.at)+' '+(c.wire||c.name)+' → '+c.state).join('\n')||'Sin comandos.';$('live-diagnostic').append(commands);
  }
  function referenceDetails(){
    const comparisons=[['PWr Aerospace · prototipo de 2023','PWr-pantalla-123.png','En su PDR, p. 123, muestran una interfaz oscura con pestañas. Es un antecedente de diseño; en nuestra edición G12/G13 exigen otra presentación.'],
      ['Descendere · diseño de 2022','Descendere-pantalla-175.png','En su PDR, p. 175, muestran datos, gráficas, mapa, original recibido y controles juntos. Usamos esa idea de información operativa agrupada, con el tema claro y la tipografía que exige nuestro anexo.']];
    for(const [title,file,caption]of comparisons){const section=document.createElement('section');section.className='help-section';const h=document.createElement('h3');h.textContent=title;
      const image=document.createElement('img');image.src='../Referencias/'+file;image.alt='Página original con la pantalla de '+title;image.style.width='100%';image.style.height='auto';
      const p=document.createElement('p');p.textContent=caption;section.append(h,image,p);$('live-diagnostic').append(section);}
  }
  $('annex-link').href=L.source;
  document.addEventListener('click',event=>{const help=event.target.closest('[data-help]');if(help)showHelp(help.dataset.help);const cmd=event.target.closest('[data-command]');if(cmd)sendCommand(cmd.dataset.command);});
  $('close-help').onclick=$('done-help').onclick=()=>$('help-dialog').close();
  $('help-dialog').addEventListener('close',()=>{if(resumeAfterHelp&&!$('scenario-dialog').open)start();else render();resumeAfterHelp=false;});
  $('play').onclick=()=>{if(running){pause();render();}else start();};$('step').onclick=()=>{pause();advance();};$('speed').onchange=()=>{if(running)schedule();};$('restart').onclick=reset;
  $('references').onclick=()=>showHelp('references');$('diagnostics').onclick=()=>showHelp('diagnostics');
  $('scenarios').onclick=()=>{pause();$('scenario-dialog').showModal();};$('close-scenario').onclick=()=>$('scenario-dialog').close();
  $('all-faults').onclick=()=>{for(const [id]of faults){pendingFaults[id]=true;$('fault-'+id).checked=true;}};
  $('apply-scenario').onclick=()=>{$('scenario-dialog').close();reset();start();};
  function sendCommand(name){
    if(replayData)return;
    if(name==='CAL'&&tick>=5){$('notice').textContent='CAL sólo se ensaya en plataforma: iniciá una sesión nueva y enviá antes de los 5 s.';return;}
    if(name==='ST_GPS'&&(!r.latest||fieldValue('GPS_TIME')==='—'||(age()||0)>=3)){$('notice').textContent='No se ensaya ST GPS sin una hora GPS reciente. Avanzá hasta recibir un dato válido.';return;}
    const cmd=r.command(name,now(),true);
    echo=cmd.expectedEcho;if(name==='CX_OFF')telemetryOn=false;if(name==='CX_ON')telemetryOn=true;
    $('notice').textContent=cmd.wire+' · emisor ficticio. Se espera eco en un paquete posterior; no prueba una acción física.';render();
  }
  function download(text,type,suffix){const url=URL.createObjectURL(new Blob([text],{type})),a=document.createElement('a');a.href=url;a.download='SIMULACION_'+r.meta.id.replace(/[^a-zA-Z0-9_-]/g,'_')+suffix;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);$('notice').textContent='Archivo de práctica generado. La segunda copia física debe guardarse y verificarse en otro soporte.';}
  $('save').onclick=()=>download(JSON.stringify(r.export(tick,config)),'application/json','.json');$('csv').onclick=()=>download('\uFEFF'+G.csv(r),'text/csv;charset=utf-8','_telemetria.csv');$('open').onclick=()=>$('import').click();
  $('import').onchange=async event=>{const file=event.target.files[0];if(!file)return;try{if(file.size>20000000)throw Error('Máximo 20 MB.');const data=G.validateSession(JSON.parse(await file.text()));
    pause();replayData=data;replayIndex=0;tick=0;config=data.config||{};r=data.meta.transport===G.TRANSPORT?new G.Receiver(data.meta):new C.Receiver(data.meta);
    $('notice').textContent='Reproducción preparada: '+file.name+'. Los campos que no existían en v03 quedan ausentes. Pulsá Iniciar.';render();
    }catch(error){$('notice').textContent='No se abrió la sesión: '+error.message;}event.target.value='';};
  let resizeTimer;window.addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(render,80);});
  window.stationDiagnostics=()=>({tick,running,replay:Boolean(replayData),fits:$('station').dataset.fits==='true',counts:{...r.counts},missing:r.missing,latest:r.latest,samples:r.samples,session:r.export(tick,config)});
  reset();
})();
