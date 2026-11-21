'use strict';
const help={
 blocks:['Compartir instrumentos','No hace falta un sensor por cada número. La IMU reúne seis ejes; el barómetro aporta presión para calcular altura; una placa INA mide tensión y corriente. Las fórmulas agregan información, pero también heredan errores y límites. Seis bloques no incluyen cámaras, reloj, memoria ni contactos.'],
 baro:['Barómetro','Mide presión absoluta. La altura depende de la presión del suelo y un modelo atmosférico; la velocidad depende además de tiempos y filtro. No reemplazar la altura barométrica requerida por GPS. La temperatura del chip está influida por su placa y calor interno.'],
 temp:['Temperatura interna','Un termómetro separado, colocado lejos de fuentes de calor según el objetivo, ayuda a representar la temperatura interna definida. Hay que medir su respuesta térmica. Temperatura interna no es automáticamente temperatura del aire exterior.'],
 imu:['Aceleración y giro','Una IMU de seis ejes ofrece aceleración en tres ejes y velocidad angular en tres. Giro en grados por segundo no es ángulo. En reposo el acelerómetro normalmente detecta gravedad. La unidad ACCEL del anexo es ambigua y debe aclararse; no inventar una conversión a aceleración angular.'],
 gps:['Solución GPS','El receptor estima posición y altura sobre el nivel medio del mar, aporta UTC y satélites. Son distintas de la altura relativa del barómetro. No garantiza rumbo de la carcasa; satélites no prueban una solución válida. Guardar antigüedad y validez.'],
 electric:['Una placa para tensión y corriente','El INA mide tensión de bus y caída sobre una resistencia conocida. De allí se obtiene corriente. Si está antes de todas las ramas del pack principal, cubre cámaras, radio y actuadores. La baliza tiene batería independiente. Medir después de un regulador no equivale a medir la batería.'],
 solar:['Panel requerido','Un panel produce señal eléctrica al recibir radiación. Con una carga y circuito ADC definidos podemos detectar iluminación y comparar valores calibrados. Orientación, sombra y temperatura influyen; no presentar voltios como irradiancia en W/m². Una LDR no sustituye el panel exigido.'],
 pressure:['Presión actual','Entrada ficticia del barómetro. hPa se usa aquí por comodidad; el protocolo exige presión en kPa, por lo que 1013,25 hPa son 101,325 kPa. Ambas presiones de la fórmula deben usar la misma unidad.'],
 reference:['Referencia P0','Es presión en el lugar de partida, fijada con CAL y registrada. Usar 1013,25 hPa sin medirla puede desplazar la altura. Calibrar a cero no elimina deriva meteorológica, calentamiento o errores de montaje.'],
 voltage:['Tensión de batería','Diferencia eléctrica en los bornes del pack. Si el instrumento mide del lado de carga de un shunt, documentar cómo se obtiene tensión real del pack. Un valor regulado de 5 V no describe la descarga de una batería de 8 V.'],
 current:['Corriente total','Flujo de carga del pack principal hacia todas sus ramas. Su signo y rango se calibran con carga conocida. Los picos entre dos transmisiones pueden perderse a 1 Hz; el muestreo local debe ser más rápido y conservar datos relevantes.'],
 altitude:['Altura a partir de presión','Se calcula 44330 × [1 − (P/P0)^0,1903] en metros. Es un modelo atmosférico aproximado con referencia local; el sensor mide presión. No medir altura con regla virtual ni atribuir exactitud de centímetros porque el resultado tiene decimales.'],
 power:['Potencia','P = V × I, expresada en W. Requiere tensión y corriente del mismo sistema y tiempos cercanos. Dos lecturas instrumentales permiten este cálculo sin comprar vatímetro extra.'],
 descent:['Velocidad de descenso','La pendiente de altura respecto al tiempo produce velocidad vertical. La calculadora ajusta una recta a las muestras válidas; signo positivo representa descenso. Usa al menos tres muestras y rechaza huecos mayores a 1,5 s en este ejemplo de 1 Hz. Ese umbral es didáctico, no oficial.'],
 energy:['Energía integrada','Se integra potencia con los intervalos reales usando trapecios y se divide por 3600 para Wh. Los intervalos con huecos grandes no se rellenan. El total entonces es parcial y muestra segundos cubiertos y omitidos; no es una cifra completa de consumo.'],
 gaps:['Tiempos y huecos','Perder muestras no significa que el vehículo dejó de moverse. Un hueco impide afirmar una pendiente continua; energía se puede sumar sólo en intervalos suficientemente cubiertos. Un timestamp repetido hace inválido este ejemplo. No asumir Δt=1 s para todos los paquetes reales.'],
 budget:['Presupuesto preliminar','La referencia completa es ARS 660.784,32 de vehículo y ARS 393.000 de apoyo/desarrollo/envíos, sin reserva. Se agrega 20% de planificación, no gasto realizado. Valores publicados y asignaciones estimadas están separados en el Excel. No están cerrados masa, radio, panel, estructura ni mecanismos.'],
 radio:['Precio objetivo y compatibilidad','El punto inicial reserva ARS 180.000 por extremo. Un objetivo de 45.000 muestra el ahorro posible, pero no prueba que exista una oferta apta. Radios de 433 MHz no cumplen. Dirección de destino y TEAM_ID no son necesariamente NetID/PanID. La alternativa LoRa requiere revisar modelo y firmware con organizador/docente.'],
 cap:['Límite C9','El vehículo debe costar menos de ARS 1.000.000; exactamente ese importe no cumple. Análisis y soporte terrestre quedan excluidos. La comparación numérica del laboratorio no certifica el proyecto: todavía hay precios estimados y ensayos físicos pendientes.'],
 full:['Lo que desembolsa el equipo','El costo de hardware y ensayos incluye estación terrestre, herramientas de banco, prototipos, repuestos y envíos además del vehículo. Puede superar el límite C9 porque C9 tiene otro alcance. Notebook propia/UTN y laboratorio prestado son hipótesis pendientes; viajes se presupuestan cuando haya sede y plan.'],
 innovation:['Verificar lo ocurrido con evidencia','La propuesta relaciona contacto de mecanismo, video sincronizado, velocidad de descenso y giro. Puede medir tiempo hasta el nuevo régimen y estabilidad antes/después. Los métodos ya existen; no prometemos novedad mundial. El experimento, métricas y datos propios deben justificar la aportación.']
};
const $=id=>document.getElementById(id),fmt=(v,d=2)=>new Intl.NumberFormat('es-AR',{maximumFractionDigits:d,minimumFractionDigits:d}).format(v);
function number(id){const e=$(id);return e.value.trim()!==''&&e.validity.valid?Number(e.value):NaN;}
function result(id,r,d=2){$(id).textContent=r.valid?`${fmt(r.value,d)} ${r.unit}`:'Sin dato válido';}
function update(){
 const ids=['baro','temp','imu','gps','electric','solar'],count=ids.filter(id=>$(id).checked).length;
 $('coverage').textContent=`${count} de 6 entradas disponibles. ${count===6?'Cobertura de los bloques previstos; video y eventos físicos van aparte.':'Faltan mediciones obligatorias. Los cálculos dependientes no reemplazan el sensor que falló.'}`;
 const baro=$('baro').checked,electric=$('electric').checked,v=number('voltage'),i=number('current'),rate=number('rate');
 result('altitude',Measurements.altitude(baro?number('pressure'):NaN,number('reference')));
 result('power',Measurements.power(electric?v:NaN,i));
 let samples=Array.from({length:10},(_,j)=>({t:j,h:600-rate*j,v,i}));
 if($('fault').value==='gap')samples=samples.filter(s=>s.t<4||s.t>6);
 if($('fault').value==='time')samples[5].t=samples[4].t;
 const dr=Measurements.descent(baro?samples:[],1.5),en=Measurements.energy(electric?samples:[],1.5);
 result('descent',dr);$('descent-note').textContent=dr.valid?`Ajuste con ${dr.sampleCount} muestras en ${dr.span} s.`:dr.reason;
 result('energy',en,5);$('energy-note').textContent=en.valid?`${en.partial?'TOTAL PARCIAL. ':''}${en.coveredSeconds} s cubiertos; ${en.missingSeconds} s omitidos.`:en.reason;
 const r=number('radio-price');
 if(Number.isFinite(r)){
  const flight=(660784.32+r-180000)*1.2,project=(1053784.32+2*(r-180000))*1.2;
  $('flight-cost').textContent=`$ ${fmt(flight)}`;$('project-cost').textContent=`$ ${fmt(project)}`;
  $('cap-note').textContent=flight<1000000?'Asignación bajo C9; cumplimiento técnico y cotizaciones pendientes.':'Revisar: esta asignación alcanza o supera el límite estricto.';
 }else{$('flight-cost').textContent=$('project-cost').textContent='Falta precio válido';$('cap-note').textContent='No se calcula un costo sin precio objetivo.';}
}
document.querySelectorAll('input,select').forEach(e=>e.addEventListener('input',update));
document.querySelectorAll('[data-info]').forEach(b=>b.addEventListener('click',()=>{const [title,body]=help[b.dataset.info];$('help-title').textContent=title;$('help-text').replaceChildren();const p=document.createElement('p');p.textContent=body;$('help-text').append(p);$('help').showModal();}));
$('close').addEventListener('click',()=>$('help').close());update();
