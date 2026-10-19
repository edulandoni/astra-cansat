(function(root){
 'use strict';
 const finite=x=>typeof x==='number'&&Number.isFinite(x);
 const bad=(reason,extra={})=>({value:null,valid:false,reason,...extra});
 function altitude(p,p0){if(!finite(p)||!finite(p0)||p<=0||p0<=0)return bad('Presión o referencia inválida.');return {value:44330*(1-Math.pow(p/p0,0.1903)),valid:true,unit:'m',origin:'calculated',model:'ISA aproximado, referencia local'};}
 function descent(samples,maxGap=2){
  if(!Array.isArray(samples)||samples.length<3)return bad('Faltan muestras para ajustar una pendiente.');
  for(let i=0;i<samples.length;i++){if(!finite(samples[i].t)||!finite(samples[i].h))return bad('Muestra inválida.');if(i&&samples[i].t<=samples[i-1].t)return bad('Tiempos duplicados o fuera de orden.');if(i&&samples[i].t-samples[i-1].t>maxGap)return bad('Hay un hueco demasiado grande para esta ventana.');}
  const n=samples.length,mt=samples.reduce((a,s)=>a+s.t,0)/n,mh=samples.reduce((a,s)=>a+s.h,0)/n;
  const denom=samples.reduce((a,s)=>a+(s.t-mt)**2,0);if(denom<=0)return bad('Ventana sin duración.');
  return {value:-samples.reduce((a,s)=>a+(s.t-mt)*(s.h-mh),0)/denom,valid:true,unit:'m/s',origin:'calculated',span:samples.at(-1).t-samples[0].t,sampleCount:n};
 }
 function energy(samples,maxGap=2){
  if(!Array.isArray(samples)||samples.length<2)return bad('Faltan muestras de potencia.');
  if(samples.some(s=>!finite(s.t)||!finite(s.v)||!finite(s.i)))return bad('Datos eléctricos inválidos.');
  let joules=0,covered=0,missing=0;
  for(let j=1;j<samples.length;j++){
   const dt=samples[j].t-samples[j-1].t;if(dt<=0)return bad('Tiempos duplicados o fuera de orden.');
   if(dt>maxGap){missing+=dt;continue;}
   joules+=(samples[j].v*samples[j].i+samples[j-1].v*samples[j-1].i)/2*dt;covered+=dt;
  }
  if(!covered)return bad('No hay intervalos cubiertos.',{coveredSeconds:0,missingSeconds:missing});
  return {value:joules/3600,valid:true,unit:'Wh',origin:'calculated',partial:missing>0,coveredSeconds:covered,missingSeconds:missing,spanSeconds:covered+missing};
 }
 function power(v,i){return finite(v)&&finite(i)?{value:v*i,valid:true,unit:'W',origin:'calculated'}:bad('Tensión o corriente inválida.');}
 const api={altitude,descent,energy,power};
 if(typeof module==='object'&&module.exports)module.exports=api;else root.Measurements=api;
})(typeof window==='undefined'?globalThis:window);
