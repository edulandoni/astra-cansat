/**
 * Modelo de dimensionamiento y fallas, sin hardware ni datos de vuelo.
 * Ejecutar con: node verification/ground-station-redundancy-analysis.js
 * Los identificadores del modelo son locales; no definen el protocolo de radio.
 */
function requireCondition(value, message) {
  if (!value) throw new Error(message);
}
function airtimeMs(bytes, sf, bw=125000, cr=1) {
  const lowRate = Number(2 ** sf / bw >= 0.016);
  const payloadSymbols = 8 + Math.max(Math.ceil((8*bytes - 4*sf + 28 + 16) / (4*(sf-2*lowRate))) * (cr+4), 0);
  return (8 + 4.25 + payloadSymbols) * 2 ** sf / bw * 1000;
}
function recoveryPlan(liveBytes, sf) {
  const liveMs = airtimeMs(liveBytes,sf);
  const replayMs = airtimeMs(208,sf);
  const commandMs = airtimeMs(23,sf);
  const guardMs = 50;
  const spareMs = 1000-liveMs-commandMs-guardMs;
  const replayPerSlot = Math.max(0,Math.floor(spareMs/replayMs));
  return {sf,liveBytes,liveMs:Math.round(liveMs*1000)/1000,
    replayMs:Math.round(replayMs*1000)/1000,commandMs:Math.round(commandMs*1000)/1000,guardMs,
    liveAndControlFits:spareMs >= 0,replayPerSlot,secondsFor60Missing:replayPerSlot ? Math.ceil(60/replayPerSlot):null,
    exclusiveReplay60Seconds:60*replayMs/1000};
}
function deliveryExperiment(policy, cutStage, gatewayPowerLoss=false) {
  // Archivo persistente del receptor se conserva toda la sesion, aun tras ACK.
  const gatewayArchive = new Map(policy === 'durable_archive' ? [[102,'original']] : []);
  const gatewayQueue = new Map([[102,'original']]);
  let pcRam = new Map(), pcDisk = new Map(), acknowledged = false;
  pcRam.set(102,'original');
  if (policy === 'ack_ram') {acknowledged=true;gatewayQueue.delete(102);}
  if (cutStage >= 2) pcDisk.set(102,'original'); // commit durable idealizado
  if (policy === 'durable_archive' && cutStage >= 3) {acknowledged=true;gatewayQueue.delete(102);}
  pcRam.clear(); // corte de PC; la escritura persistente del modelo sobrevive
  if (gatewayPowerLoss) gatewayQueue.clear();
  const replaySource = new Map([...gatewayArchive,...gatewayQueue]);
  const beforeReplay = pcDisk.size;
  for (const [id,payload] of replaySource) pcDisk.set(id,payload);
  for (const [id,payload] of replaySource) pcDisk.set(id,payload); // duplicado de recuperacion
  return {policy,cutStage,gatewayPowerLoss,acknowledged,
    originallyDurable:beforeReplay,finalUniqueRecords:pcDisk.size,
    lost:!pcDisk.has(102),archiveRetained:gatewayArchive.has(102)};
}
function causalExample() {
  const original = {id:102,measuredAt:'13:14:02',value:'original'};
  const observations = [
    {...original,receivedAt:'13:14:08',receiver:'A',source:'recovered'},
    {...original,receivedAt:'13:14:09',receiver:'B',source:'recovered'}
  ];
  const unique = new Map();
  for (const observation of observations) unique.set(observation.id, observation.value);
  requireCondition(unique.size===1 && observations.length===2,'Duplicate merge failed');
  requireCondition(observations.every(x=>x.measuredAt===original.measuredAt),'Original time lost');
  return {uniqueMeasurements:unique.size,receiptObservations:observations.length,
    measurementTimePreserved:true,wireCounterSemantics:'not modeled; requires agreed extension'};
}
function analyze() {
  const experiments=[];
  for(const policy of ['ack_ram','durable_archive'])
    for(const cutStage of [1,2,3])
      for(const gatewayPowerLoss of [false,true])
        experiments.push(deliveryExperiment(policy,cutStage,gatewayPowerLoss));
  const positive=experiments.filter(x=>x.policy==='durable_archive');
  requireCondition(positive.every(x=>!x.lost && x.finalUniqueRecords===1),'Durable model lost record');
  requireCondition(experiments.some(x=>x.policy==='ack_ram' && x.lost),'Negative control missing');
  const buffers=[60,120].map(seconds=>({seconds,rateHz:1,payloadBytes:200,
    localMetadataBytes:24,bytes:seconds*224,KiB:seconds*224/1024}));
  const radio=[7,8,9].flatMap(sf=>[128,200].map(bytes=>recoveryPlan(bytes,sf)));
  requireCondition(radio.find(x=>x.sf===7&&x.liveBytes===200).replayPerSlot===1,'Radio expectation');
  requireCondition(radio.find(x=>x.sf===8&&x.liveBytes===200).replayPerSlot===0,'Radio expectation');
  requireCondition(!radio.find(x=>x.sf===9&&x.liveBytes===200).liveAndControlFits,'Live deadline expectation');
  return {kind:'synthetic_design_analysis_not_hardware_validation',
    buffers,twoHourLogBytes:7200*224,
    max255BytePacket120SecondBufferBytes:120*(255+24),
    radioAssumptions:{bandwidthHz:125000,codingRate:'4/5',preambleSymbols:8,crc:true,
      header:'explicit',slotMs:1000,replayBytes:208,commandBytes:23,totalGuardMs:50,
      exclusions:'extra acknowledgements, address overhead beyond assumed sizes, retries, errors, RF regulations',
      scheduling:'fixed one-second slots; whole packets cannot cross next live slot; conservative example'},
    radio,holdUpConstantCurrentExample:{currentA:0.1,allowedVoltageDropV:0.5,
      capacitanceFFor100ms:0.1*0.1/0.5,capacitanceFFor1second:0.1*1/0.5,
      exclusions:'ESR, regulator efficiency and dynamics, temperature, tolerance, SD write worst case'},
    experiments,causalExample:causalExample(),
    assumptions:['durable commits are ideal and do not corrupt unrelated data',
      'receiver archival media survives the modeled power interruption',
      'no physical radio, flash controller, filesystem or battery behavior is simulated',
      'no claim of zero real-world loss or acceptance of retransmitted data by judges']};
}
const result=analyze();
if(typeof process!=='undefined') process.stdout.write(JSON.stringify(result,null,2)+'\n');
