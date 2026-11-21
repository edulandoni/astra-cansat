"""ASTRA-24/25/39/41: entrega documental PDR; no abre puertos ni cambia software de vuelo."""
from pathlib import Path
import argparse, csv, hashlib, importlib.util, json, math, re, shutil
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Polygon
from reportlab.graphics import renderSVG

REPO=Path(__file__).resolve().parents[4]
BASE='https://github.com/edulandoni/astra-cansat/blob/193e58c2297c41b5c7d973ab515bc36df86f5060/ground-station/'
S={
'E01':('USB prolongado y CSV',BASE+'docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md'),
'E02':('Cortes y reconexión USB',BASE+'docs/2026-10-25-interfaz-y-cortes-usb.md'),
'E03':('Laboratorio Qt completo',BASE+'docs/historial/2026-10-26-laboratorio-completo-04.md'),
'E04':('Fotos de ambas unidades y lector',BASE+'docs/camaras/2026-10-26-ambas-camaras-sd-y-lector-07.md'),
'E05':('Grabación segmentada y supervisión',BASE+'docs/camaras/2026-10-27-grabacion-segmentada-y-supervision-usb.md'),
'E06':('Payload y perfil LoRa',BASE+'docs/interfaces/2026-10-26-payload-sf-confiabilidad-04.md'),
'E07':('Presupuesto de enlace y entradas pendientes',BASE+'docs/interfaces/2026-10-24-enlace-destinos-y-revision.md'),
'E08':('Comandos definidos desde vuelo',BASE+'docs/interfaces/2026-10-25-comandos-definidos-desde-vuelo.md'),
'E09':('Vista Wi-Fi confirmada',BASE+'docs/camaras/2026-10-27-vista-wifi-confirmada-y-red-compartida.md'),
'M01':('Taoglas OMB.915.B05F21, rev. A, pp.4 y 8','https://www.taoglas.com/datasheets/OMB.915.B05F21.pdf'),
'M02':('Taoglas TI.92.2113, rev. A, pp.4 y 8-9','https://www.taoglas.com/datasheets/TI.92.2113.pdf'),
'M03':('Digi A09-Y11NF','https://www.digi.com/products/models/antennas/a09-y11nf'),
'M04':('Semtech SX1276, rev.7, pp.31 y 84','https://cdn.sparkfun.com/assets/7/7/3/2/2/SX1276_Datasheet.pdf'),
'N01':('Corte oficial PARCIAL del 17/11',BASE+'docs/aula/2026-11-17/Informe_aula_2026-11-17_0047_ART.md')}

DECISIONS=[
('D01','Paquete de vuelo','Layout completo: campo, offset/longitud o delimitador, tipo, endian, escala, unidad, rango, validez, versión y tamaño máximo total. Confirmar si 55 B incluye cabecera de aplicación.','Edu define; tierra adapta','Sin layout no cierro parser, payload ni airtime final.'),
('D02','Perfil RF','Módulo/revisión/pinout; frecuencia/canal, LoRa o FSK, SF/BW/CR o bitrate, potencia y régimen, CRC, sincronización, origen/destino y tiempos de TX/RX.','Revisión conjunta con Edu','Sin perfil y sensibilidad del mismo modo no cierro margen ni interoperabilidad.'),
('D03','Telecomandos','Cero de altura, UTC, alimentación/solar y espera/activación: bytes, argumentos, estados permitidos, respuestas, rechazo, duplicados y timeout.','Edu define vuelo','Un eco no confirma ejecución; no reenvío automáticamente una actuación.'),
('D04','Estados y reinicios','Estados/evento de separación; referencia de altura; misión/arranque/contador/rollover; qué persiste y cómo se distingue dato viejo.','Edu define vuelo','Necesario para graficar y contar huecos sin inventar continuidad.'),
('D05','Cámaras: control y potencia','Evento de inicio, parada/límite, START discreta o bus, niveles/pines, control de alimentación y continuidad ante reset del OBC.','Revisión con Edu/EPS','Definir antes de cablear o declarar autonomía; no depende de botones en misión.'),
('D06','Cámaras: reportes','Qué puede devolver cada cámara al OBC y qué cabe en telemetría: unidad/arranque, cuadros/bytes guardados, última escritura, espacio y errores; cadencia de consulta.','Revisión conjunta','Si sólo hay START no puedo prometer supervisión en vuelo.'),
('D07','Hardware y geometría','Antenas reales de vuelo/tierra, conectores/coaxiales, alimentación y ubicación previstas, distancia oblicua de diseño o rango, versiones ya implementadas y evidencia disponible.','Revisión con Edu','Completa arquitectura, montaje y entradas del presupuesto; desconocidos quedan TBD.')]

MESSAGE='''Edu, estoy cerrando nuestra entrega para que Rebe pueda armar el PDR. Ya tenemos documentados el banco USB, los registros, el Laboratorio, las pruebas de cámaras y los cálculos de radio. Para que la parte compartida quede consistente necesito tu definición actual, aunque sea preliminar, de esto:

1. Paquete: formato completo, campos/tipos/unidades/escala, orden de bytes y tamaño máximo. ¿Los ~55 bytes incluyen versión, origen/destino, contador y validez? Pasame un ejemplo real de paquete y cómo se interpreta.

2. Radio: módulo y revisión exactos, pinout y antenas que tenemos; frecuencia, modo, SF/BW/CR o bitrate, potencia, CRC/direcciones y cómo repartimos el tiempo entre telemetría a 1 Hz y órdenes. Si ya lo tenés implementado, pasame esa configuración y versión.

3. Comandos: cómo pedimos cero de altura, ajuste UTC, batería/solar y espera/activación; argumentos, estados permitidos, respuesta de ejecución/error y qué pasa si repetimos una orden o no llega respuesta. Adapto tierra a lo que definas vos.

4. Estados y reset: qué estados/eventos vas a enviar, cómo identificamos misión/arranque y qué pasa con contador, hora y configuración después de reiniciar. Confirmame también las referencias/unidades de altura, GPS e IMU y cómo marcás un sensor inválido.

5. Cámaras: cuándo arrancan y terminan, si las manejás con START o por un bus, pines/niveles y alimentación; cómo evitamos que un reset del OBC corte la grabación. ¿Podemos devolver al OBC progreso real de guardado y errores de cada cámara? Con sólo START no podemos confirmar desde tierra que siguen escribiendo.

6. Integración: qué antenas/conectores/cables y esquema de alimentación vamos a presentar, y qué distancia/recorrido tomamos para calcular el enlace. Pasame también cualquier prueba nueva que hayas hecho para no describir como pendiente algo que ya esté verificado.

No hace falta tener todo construido para responder: separá qué ya está definido/probado, qué proponés para el PDR y qué queda pendiente. Con esa versión adapto lo nuestro y le dejamos a Rebe un diseño coherente con sus evidencias. Lo que falte lo registramos explícito, sin inventarlo.
'''

EVIDENCE=[
('E01','USB / datos sintéticos','7261 paquetes; 7260.328 s; CSV reconstruido con igual SHA-256','Adquisición y conservación de esa revisión','No RF, sensores reales ni batería','ASTRA-20/21'),
('E02','USB físico / datos sintéticos','Corte y reconexión; 312 muestras en una sesión. Cierre/reapertura: hueco observable de 18','Histórico/identidad y faltantes separados','No garantiza conservación durante corte eléctrico','ASTRA-21/22'),
('E03','Software / Qt offscreen','22 campos, 11 gráficos, 15 canales numéricos','Funciones de Laboratorio y separación de fuentes','No legibilidad al sol ni protocolo final','ASTRA-22/41'),
('E04','Fotos / lector externo','Dos JPEG nuevos por unidad, VGA RGB, comparados por bytes/CRC/huella','Foto y SD de ambas por turnos con una tarjeta','No grabación simultánea con dos SD','ASTRA-39'),
('E05','Cámara 1 / SD / copia USB','123 cuadros; 29.828024 s entre extremos; 4.090113 fps; hueco máximo 0.479809 s','Grabación de baja cadencia e integridad de copia','No misión completa, batería, reset OBC ni lector externo en esa grabación','ASTRA-39/24'),
('E09','Cámara 1 / Wi-Fi local','Vista previa confirmada por operador','Imagen local en Laboratorio','Sin fps/latencia medidos ni escritura simultánea verificada','ASTRA-39/41'),
('E06','Cálculo offline','108 hipótesis de payload/perfiles LoRa','Tiempo de aire bajo hipótesis explícitas','No pérdidas, alcance o energía medidos','ASTRA-40'),
('E07','Cálculo offline','FSPL 915 MHz / 1 km = 91.676205 dB; margen ASTRA desconocido','Fórmula y dependencias trazables','Ejemplo numérico no es margen real','ASTRA-25')]

TESTS=[
('V01','Trama y unidades','Vectores de Edu válidos, extremos, inválidos, versión y destinatario ajenos','Comparar bytes y valores; rechazar inválidos sin actuación','Pendiente ICD / ensayo conjunto','X2/X5/X6; ASTRA-24'),
('V02','Órdenes','Cero, UTC, alimentación; duplicados, expiración, corte y rechazo','Separar aceptación/ejecución; no repetir actuación por timeout','Banco probado; vuelo pendiente','G1/G15/F3/F4; ASTRA-24'),
('V03','RF a 1 Hz','Perfil y trama máxima, órdenes/guardas, TX/RX y versiones registrados','Medir recepción única, ráfagas, RTT y presupuesto temporal; umbrales a acordar','Pendiente hardware/perfil','X4; ASTRA-23/24/25'),
('V04','Enlace y antenas','Distancia oblicua, orientación, polarización, montaje/coaxial y entorno','Comparar modelos con mismas condiciones y margen objetivo acordado','Pendiente campaña RF','ASTRA-25'),
('V05','Registro y respaldo','Diario/CSV y soporte externo realmente independiente','Conteos/huellas, recuperación y errores de cada destino; no rellenar huecos','USB prolongado previo; respaldo físico simultáneo pendiente','G2; ASTRA-21'),
('V06','Dos cámaras','Cada unidad con su SD, alimentación y firmware identificados','Duración que cubra misión y margen acordados; cuadros/tiempos/errores; lectura externa','Cámara 1 breve probada; conjunto pendiente','C6/C7/SN6/SN7; ASTRA-39'),
('V07','Arranque y reset','Energía representativa, sin botones/USB; reset OBC y cámara por separado','Propuesta: 20 ciclos por unidad y registrar primer guardado, fallos y archivos; cantidad no certifica fiabilidad','Pendiente circuito y ensayo','F5 / cámaras; ASTRA-39/24'),
('V08','Energía y SD','Espera/arranque/grabación, SD ausente/llena/lenta y cierre incompleto','Medir tensión/corriente/picos y archivos recuperables; criterios EPS/tiempo a acordar','Pendiente banco físico','E4/E7 y cámaras; ASTRA-39')]

def make_diagram(kind):
 d=Drawing(500,225); navy=colors.HexColor('#17334C'); teal=colors.HexColor('#087E8B'); gray=colors.HexColor('#64748B')
 def box(x,y,w,h,lines,col=teal):
  d.add(Rect(x,y,w,h,rx=5,fillColor=colors.HexColor('#F1F6FA'),strokeColor=col,strokeWidth=1))
  for j,s in enumerate(lines):d.add(String(x+w/2,y+h-17-j*13,s,fontName='Segoe',fontSize=9,textAnchor='middle',fillColor=navy))
 def arrow(x1,y1,x2,y2,dash=False):
  ux,uy=(x2-x1)/math.hypot(x2-x1,y2-y1),(y2-y1)/math.hypot(x2-x1,y2-y1)
  d.add(Line(x1,y1,x2,y2,strokeColor=gray,strokeWidth=1.2,strokeDashArray=[4,3] if dash else None));d.add(Polygon([x2,y2,x2-6*ux+3*uy,y2-6*uy-3*ux,x2-6*ux-3*uy,y2-6*uy+3*ux],fillColor=gray,strokeColor=gray))
 if kind=='arquitectura':
  box(5,150,105,53,['STM32 + SX1276','Vuelo / propuesto'],gray);arrow(110,176,155,176,True)
  box(155,150,120,53,['SX1276 + ESP32','Gateway / pendiente'],gray);arrow(275,176,315,176,True)
  box(315,150,175,53,['PC / Laboratorio Qt','Adquisición + validación'])
  box(5,55,145,53,['ESP32 simulador USB','Datos sintéticos probados']);arrow(150,81,315,163)
  box(315,55,83,53,['Diario','original']);box(410,55,80,53,['CSV','por sesión'])
  arrow(355,150,355,108);arrow(450,150,450,108)
  d.add(String(6,20,'Línea discontinua: integración RF futura. USB de banco no prueba enlace de vuelo.',fontName='Segoe',fontSize=8,fillColor=gray))
 else:
  box(10,135,130,62,['Antena candidata','Mástil/trípode estable','Orientación registrada'],gray)
  box(190,135,130,62,['Gateway terrestre','Caja + alivio de tensión','Coaxial caracterizado'],gray)
  box(370,135,120,62,['Notebook','Batería / respaldo','USB + registro'],teal)
  arrow(140,166,190,166,True);arrow(320,166,370,166,True)
  box(75,30,350,63,['Propuesta de montaje, no construcción verificada','Separar antena de personas/PC; conservar polarización','Longitud/pérdida del cable y altura: definir y medir'],gray)
 return d

def main():
 p=argparse.ArgumentParser();p.add_argument('--salida',required=True,type=Path);args=p.parse_args();out=args.salida;out.mkdir(parents=True,exist_ok=True)
 public=Path(__file__).parent
 pdfmetrics.registerFont(TTFont('Segoe',r'C:\Windows\Fonts\segoeui.ttf'));pdfmetrics.registerFont(TTFont('SegoeB',r'C:\Windows\Fonts\segoeuib.ttf'))
 pdfmetrics.registerFontFamily('Segoe',normal='Segoe',bold='SegoeB',italic='Segoe',boldItalic='SegoeB')
 spec=importlib.util.spec_from_file_location('airtime',REPO/'ground-station/tools/airtime_lora.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
 rows=[]
 for n in [55,100,255]:
  for sf in [7,9,10]:rows.append(a.airtime(n,sf,125000,1,8,1,0))
 assert abs(rows[0]['airtime_seconds']-.107776)<1e-9 and abs(rows[5]['airtime_seconds']-1.026048)<1e-9
 fspl=20*math.log10(4*math.pi*1000*915e6/299792458);assert abs(fspl-91.676205)<.000001
 calc={'status':'CALCULO_NO_RF_NO_APROBADO','hypotheses':'BW125kHz, CR4/5, preámbulo8, encabezado explícito, CRC; payload total de aplicación hipotético','lora':rows,'fspl_915MHz_1000m_dB':fspl,'astra_link_margin_dB':None,'unknowns':'perfil, sensibilidad, antena vuelo, pérdidas, distancia y margen objetivo','source':S['M04'][1]}
 evidence=REPO/'ground-station/evidence/2026-10-24-banco02/usb-prolongado-13/resultado-original.json';src=json.loads(evidence.read_text(encoding='utf-8'));assert src['packets']==7261
 for kind in ['arquitectura','montaje']:
  svg=renderSVG.drawToString(make_diagram(kind));(public/(kind+'.svg')).write_text(svg,encoding='utf-8')
 def dump_csv(name,header,data):
  with (public/name).open('w',encoding='utf-8',newline='') as f:w=csv.writer(f);w.writerow(header);w.writerows(data)
 dump_csv('matriz_evidencias.csv',['id','tipo','resultado','afirmacion_sostenible','limite','jira','fuente'],[(*r,S[r[0]][1]) for r in EVIDENCE])
 dump_csv('decisiones_para_Edu.csv',['id','tema','respuesta_necesaria','coordinacion','consecuencia'],DECISIONS)
 dump_csv('plan_verificacion.csv',['id','objeto','configuracion','criterio','estado','trazabilidad'],TESTS)
 (public/'calculos.json').write_text(json.dumps(calc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (public/'Mensaje_para_Edu.txt').write_text(MESSAGE,encoding='utf-8')
 template={'status':'DRAFT_NOT_APPROVED','version':None,'approved_by':[],'telemetry':{'encoding':None,'application_max_bytes':None,'byte_order':None,'fields':[],'valid_example_hex_or_text':None,'decoded_example':None,'invalid_examples':[]},'radio':{k:None for k in ['module_revision','pinout_reference','carrier_hz','modulation','sf_or_bitrate','bandwidth_hz','coding_rate','tx_power_dbm','tx_duty_conditions','sync_word','phy_crc','application_integrity','source_address','destination_address','telemetry_period_ms','command_rx_window_ms','guard_ms','profile_sensitivity_dbm']},'commands':[],'mission':{'states':[],'separation_event':None,'counter_reset_and_rollover':None,'clock_persistence':None,'measurement_validity':None},'cameras':{'start_event':None,'stop_condition':None,'electrical_interface':None,'power_switching':None,'obc_reset_behavior':None,'status_return_interface':None,'status_fields':[]},'ground':{'antenna_model':None,'connector_and_cable':None,'mount':None,'losses_db':None,'slant_range_m':None,'target_margin_db':None}}
 (public/'Interfaz_para_completar_con_Edu.json').write_text(json.dumps(template,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 sections=[]
 def section(title,paras,tables=(),diagram=None):sections.append((title,paras,tables,diagram))
 section('1. Estado de la entrega',[
 'Preparé este aporte de groundstation y cámaras para que Rebe redacte el PDR. Reúne arquitectura, resultados, alternativas, fuentes y verificación. Es una consolidación documental del 17/11/2026: no ejecuté nuevos ensayos físicos ni aprobé el contrato de vuelo.',
 'El software de banco y la evidencia USB están disponibles para describir. La interfaz de vuelo, radio, energía y cámaras en misión conservan decisiones conjuntas y ensayos abiertos. Una propuesta documentada permite explicar el diseño preliminar; no equivale a demostrar cumplimiento.',
 'Antes de incorporar un resultado hay que conservar su versión y alcance. El ensayo prolongado antecede al Laboratorio Qt; no atribuyo sus dos horas a la versión actual. Los informes diarios y respaldos no son ensayos técnicos nuevos.'
 ],[(['Bloque','Material preparado','Condición de cierre'],[
 ['Tierra / software','Arquitectura, funciones y evidencia USB','Adaptar a la interfaz final; campo pendiente'],
 ['Comunicaciones','Airtime, alternativas y fórmula de enlace','D01/D02/D07 y ensayo RF'],
 ['Antenas','Dos patrones revisados y montaje propuesto','Unidad real, pérdidas y selección conjunta'],
 ['Cámaras','Progreso de guardado y prueba breve','D05/D06, potencia y ensayo dual'],
 ['Verificación','Matriz con evidencia y campaña pendiente','Revisar con requisitos / versión vigente']])])
 section('2. Arquitectura y conexiones de tierra',[
 'La arquitectura de vuelo propuesta es STM32 + SX1276, enlace RF, SX1276 + ESP32 terrestre, USB y PC. La flecha RF es una integración pendiente. El camino ya probado utiliza un ESP32 que genera datos sintéticos por USB, sin radio.',
 'En la PC separo recepción/encuadre, validación, modelo de datos, presentación y escritores por destino. Conservo originales y CSV por sesión. El segundo destino sólo cuenta como respaldo independiente si está en otro soporte y se verifica; dos carpetas del mismo disco comparten fallas.',
 'No fijo GPIO SPI, IRQ, alimentación o adaptadores sin identificar la placa de radio y su revisión. El módulo informado por Edu es NiceRF LoRa1276-915/SX1276; la correspondencia con el pinout conserva una discrepancia documentada. USB del gateway, sensor de cámara y bus de vuelo son interfaces distintas.'
 ],[(['Componente','Interfaz prevista','Estado'],[
 ['ESP32 terrestre / PC','USB serie, fuente explícita','Banco probado; receptor RF pendiente'],
 ['SX1276 / ESP32','SPI + control/IRQ, alimentación según módulo','Pines, variante y desacoplo por confirmar'],
 ['Antena / radio','50 ohm; coaxial/conector del equipo real','Ganancias/pérdidas no fijadas'],
 ['PC / soportes','Diario y CSV, errores por escritor','Ensayos previos E01/E02; simultáneo externo pendiente']])], 'arquitectura')
 section('3. Software y evidencia de banco',[
 'El Laboratorio Qt presenta 22 campos y once gráficos para quince canales numéricos. Permite fuentes explícitas USB, simulación PC y reproducción; abre sin mediciones. Una desconexión conserva histórico y edad, sin iniciar simulación como sustituto. Los gráficos no unen huecos ni dibujan un GPS sin solución [E03].',
 'En el ensayo prolongado recibí y guardé 7261 paquetes sintéticos en 7260.328 segundos monotónicos. El intervalo medio observado fue 1.000045 s, con extremos 0.937 y 1.063 s. El CSV reconstruido coincide por SHA-256 con el adquirido; el segmento nominal cerró sin descartes o errores de escritores [E01].',
 'La campaña incluyó una misión inicial y permanencia posterior en LANDED: demuestra duración del flujo de banco, no vuelo, autonomía o sensores. Los cortes USB, identidades y huecos tienen campañas y revisiones separadas [E02].',
 'Para una demostración se puede usar reproducción del CSV conservado, mostrando claramente su origen histórico. Las órdenes permanecen deshabilitadas en reproducción. Una demostración nueva debe registrar fuente, versión, resultado y límites; no la presento como ya grabada.'
 ],[(['Evidencia','Resultado útil para el PDR','Límite'],[
 ['E01','7261 filas; reconstrucción coincidente','USB / valores sintéticos / revisión anterior'],
 ['E02','Reconexión y hueco de 18 muestras observable','No conservación garantizada ante corte eléctrico'],
 ['E03','22 campos y 11 gráficos integrados','Validación Qt offscreen; sol pendiente'],
 ['Órdenes de banco','Cero, hora y alimentación ficticias','No ejecución física STM32 por RF']])])
 section('4. Paquete, tiempo de aire y enlace',[
 'Edu define bytes y comandos de vuelo; adapto tierra a esa versión [E08]. Los 22 campos ASCII son el perfil de banco; unos 55 bytes son una estimación, no un layout aprobado. El tamaño de aplicación debe incluir sus cabeceras, identidad, destino, versión, validez y controles acordados.',
 'Recalculé nueve hipótesis con la herramienta existente: LoRa, BW 125 kHz, CR 4/5, preámbulo 8, encabezado explícito y CRC físico. El CRC y encabezado de radio están incluidos por la fórmula; órdenes, respuestas, cambios TX/RX y guardas se presupuestan aparte [E06/M04].',
 'Propongo comparar SF7 como candidato temporal inicial y SF9/SF10 como alternativas según el margen del mismo perfil, sin configurarlos ni aprobarlos. SF10 con 100 bytes supera un segundo antes de órdenes. Mayor SF puede mejorar sensibilidad y aumentar ocupación; sólo una campaña permite evaluar confiabilidad.',
 'El margen real permanece desconocido: Prx = Ptx + Gtx + Grx - pérdidas - FSPL; margen = Prx - sensibilidad del perfil. A 915 MHz y 1 km oblicuo, FSPL = 91.676205 dB. No uso esta distancia como trayectoria confirmada ni sensibilidad extrema de otro SF para cerrar la cuenta [E07]. La potencia y régimen requieren revisión del módulo; no asumo +20 dBm continuo.'
 ],[(['Payload de aplicación','SF7','SF9','SF10'],[
 ['55 B (hipótesis)','107.776 ms','349.184 ms','657.408 ms'],
 ['100 B (hipótesis)','174.336 ms','553.984 ms','1026.048 ms'],
 ['255 B (hipótesis)','399.616 ms','1250.304 ms','2295.808 ms']])])
 section('5. Antenas y montaje propuesto',[
 'Actualizo la comparación del 23/10: ahora pude inspeccionar visualmente patrones oficiales de dos candidatas. Son alternativas de tierra, no componentes adquiridos o seleccionados. Mantengo Digi A09-Y11NF como alternativa direccional secundaria con patrón exacto pendiente; no reutilizo como oficial una curva de otro equipo.',
 'En OMB revisé la p.8: hay diferencias entre cortes y mínimos, no cobertura esférica. En TI.92 revisé pp.8-9, recta y articulada: la orientación modifica el patrón. No extraigo de las curvas una ganancia mínima garantizada sobre la trayectoria ni copio sus imágenes sin permiso.',
 'Como propuesta de portabilidad priorizaría evaluar el dipolo compacto TI.92; la OMB permite comparar otra distribución angular pero exige soporte mayor. La elección final necesita perfil, recorrido, pérdidas y disponibilidad. Propongo mástil/trípode estable, radio protegida y alivio de tensión; coaxial corto y caracterizado, sin fijar altura o longitud como requisitos [D07].'
 ],[(['Candidata','Dato de fabricante','Patrón / restricción'],[
 ['Taoglas TI.92.2113','902-928 MHz; SMA macho; 198 mm; 22.5 g','Ficha A: pico 1.21 dBi recta / 2.14 articulada. Web dice máximo 2.9: discrepancia, no adoptar sin aclarar [M02].'],
 ['Taoglas OMB.915.B05F21','902-928 MHz; N hembra; pico 5.9 dBi','1094 +/-30 mm; antena 500 g + soporte 70 g. Patrón oficial p.8 inspeccionado [M01].'],
 ['Digi A09-Y11NF','Yagi 900 MHz; 11.1 dBi; N hembra','Apuntado y patrón exacto del modelo por confirmar. No dar alcance por ganancia pico [M03].']])], 'montaje')
 section('6. Cámaras: arquitectura y operación',[
 'La propuesta mantiene dos ESP32-CAM/OV2640, cenit y nadir, cada una con SD, alimentadas por el sistema de potencia. El objetivo es que el computador de vuelo inicie y supervise la grabación sin depender de la notebook. El circuito y los pines de control no quedan aprobados por este documento.',
 'Propongo la secuencia: espera, alimentación/arranque, foto + escritura/lectura de chequeo, armado, inicio con margen antes del descenso requerido, grabación autónoma, cierre y recuperación. El evento y margen de inicio deben acordarse con vuelo; cero de altura no inicia automáticamente video. Apagar Wi-Fi no equivale a apagar sensor o cortar consumo.',
 'Para reportar progreso necesito por unidad identidad/arranque, ejecución/segmento, cuadros y bytes guardados, última escritura, espacio y error. Un inicio aceptado, una foto o un LED no confirman continuidad. Si vence el reporte, tierra muestra desconocido. Si sólo hay START discreta falta resolver un canal de retorno [D05/D06].',
 'Ambas unidades produjeron JPEG VGA RGB y guardaron/leyeron con lector externo en un ensayo por turnos, usando una sola SD [E04]. Después cámara 1 grabó 123 cuadros en 29.828024 s entre extremos: 4.090113 fps y hueco máximo 0.479809 s. La copia USB se verificó y el MP4 se creó en PC, sin inventar cuadros [E05].',
 'La cámara siguió mientras cerré seguimiento USB ocho segundos, conservando alimentación USB: no demuestra batería o supervivencia al reset del OBC. Falta grabación dual, energía, arranque sin botones, SD llena/lenta y recuperación ante corte. Wi-Fi es mantenimiento local; sonido queda fuera de esta etapa. No hay prueba nueva en este paquete.'
 ])
 section('7. Verificación y riesgos que quedan abiertos',[
 'Dejo una campaña ordenada para cerrar integración. Los criterios cuantitativos que dependen de misión, enlace o energía se acuerdan antes de probar. Los veinte ciclos de arranque son una propuesta de banco, no una certificación estadística. Una prueba pasada de una revisión no se hereda automáticamente a otra.',
 'Esta tabla alimenta la matriz de requisitos: no sustituye la matriz vigente de Rebe ni declara cumplimiento por tener un documento. El cierre de cada ensayo conserva versión, configuración, procedimiento, registros y evidencia de resultado.'
 ],[(['ID / objeto','Ensayo y aceptación propuestos','Estado'],[[r[0]+' / '+r[1],r[3],r[4]] for r in TESTS])])
 section('8. Texto técnico para incorporar al PDR',[
 'Ground segment architecture. We propose an STM32/SX1276 flight node, an SX1276/ESP32 ground gateway and a USB-connected PC. RF integration is pending. The implemented USB bench uses an ESP32-generated synthetic telemetry source. Acquisition, parsing, data quality, presentation and storage are separated; retained values are marked historical after a link interruption.',
 'Implemented software and evidence. The native Qt laboratory integrates 22 telemetry fields and 11 plots. A previous USB bench revision received and stored 7,261 synthetic packets over 7,260.328 seconds; offline reconstruction produced an identical CSV hash. This demonstrates that bench configuration, not flight sensors, RF performance, battery autonomy or a two-hour validation of the current Qt application.',
 'Communications design. The final payload and command encoding are defined by flight software and adapted on the ground side. A 55-byte payload is an estimate. Under BW125 kHz, CR4/5, eight preamble symbols, explicit header and PHY CRC, calculated airtimes are 107.776 ms at SF7, 349.184 ms at SF9 and 657.408 ms at SF10. Commands and guard times require additional allocation. The real link margin remains TBD until profile-specific sensitivity, antennas, losses and geometry are fixed.',
 'Camera payload. We propose two autonomous ESP32-CAM units with independent microSD storage. Both units produced independently readable VGA colour photographs in sequential bench tests. Camera 1 subsequently recorded 123 frames with a measured first-to-last interval of 29.828024 s and a mean rate of 4.090113 fps. Recording continued when USB monitoring was closed while USB power remained connected. Dual-camera operation, flight power, startup without manual intervention and OBC-reset tolerance remain to be verified.',
 'Verification status. Existing results are labelled as calculations, software tests, physical USB tests or camera bench tests. Flight ICD approval, RF interoperability, antenna/mount selection, power measurements and complete-mission dual recording remain open. Each proposed test has explicit configuration and acceptance evidence; no missing measurement is replaced by an assumed zero.'
 ])
 section('9. Definiciones necesarias y acceso a evidencia',[
 'Estas decisiones no están escondidas en el texto para Rebe. La tabla editable decisiones_para_Edu.csv conserva las preguntas, coordinación y efecto sobre el cierre. Edu puede contestar con una versión preliminar y ejemplos, distinguiendo implementado, propuesto y pendiente. El mensaje separado está preparado para copiar; no fue enviado.',
 'D01 paquete; D02 radio; D03 telecomandos; D04 estados/reinicios; D05 control y potencia de cámaras; D06 reportes de guardado; D07 hardware y geometría. Con esos datos completo el contrato terrestre y las cuentas. Hasta entonces los campos compartidos siguen TBD/TBR.',
 'Referencias E01-E09: evidencia propia conservada. M01-M04: fabricantes. N01: cobertura oficial parcial. Las fuentes enlazadas mantienen su fecha; no afirmo haber revalidado todo el aula o todos los PDF hoy. El formato final de entrega y vencimiento concreto requieren comprobación en la actividad oficial.'
 ])
 navy=colors.HexColor('#17334C');teal=colors.HexColor('#087E8B');grey=colors.HexColor('#596A7D')
 normal=ParagraphStyle('Body',fontName='Segoe',fontSize=9.5,leading=14,textColor=navy,spaceAfter=10)
 title=ParagraphStyle('Title',parent=normal,fontName='SegoeB',fontSize=21,leading=26,spaceAfter=16)
 small=ParagraphStyle('Small',parent=normal,fontSize=8,leading=11,spaceAfter=5)
 cell=ParagraphStyle('Cell',parent=normal,fontSize=8.4,leading=11,spaceAfter=0)
 def para(t,style=normal):return Paragraph(escape(t),style)
 story=[];md=['# Entrega técnica de groundstation y cámaras para PDR','', '17/11/2026 - v1. Rebe integra el PDR; esta entrega aporta diseño, evidencia y pendientes.','']
 for n,(t,paras,tables,diag) in enumerate(sections):
  if n:story.append(PageBreak())
  story.append(para(t,title));md.extend(['## '+t,''])
  if diag:story.extend([make_diagram(diag),Spacer(1,9)]);md.extend(['!['+t+']('+diag+'.svg)',''])
  for txt in paras:story.append(para(txt));md.extend([txt,''])
  for head,data in tables:
   widths=([95,215,185] if len(head)==3 else [150,115,115,115])
   if len(head)==2:widths=[48,447]
   table=Table([[para(x,cell) for x in head]]+[[para(str(x),cell) for x in row] for row in data],colWidths=widths,repeatRows=1,hAlign='LEFT')
   table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DCECF0')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.8,teal),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#D8E0E8'))]));story.extend([table,Spacer(1,9)])
   md.extend(['| '+' | '.join(head)+' |','|'+'|'.join(['---']*len(head))+'|']+['| '+' | '.join(str(x).replace('|','/') for x in row)+' |' for row in data]+[''])
  if n==8:
   for key,(label,url) in S.items():story.append(Paragraph('<font color="#087E8B">'+key+'</font> - <link href="'+url+'">'+escape(label)+'</link>',small))
 md.extend(['## Fuentes enlazadas','']+['- ['+k+' - '+v[0]+']('+v[1]+')' for k,v in S.items()])
 (public/'Entrega_para_Rebe.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
 en='\n\n'.join(sections[7][1])+'\n';(public/'Texto_tecnico_EN.md').write_text(en,encoding='utf-8')
 (public/'README.md').write_text('# Aporte PDR del 17/11/2026\n\n[Documento principal](Entrega_para_Rebe.md) · [Texto en inglés](Texto_tecnico_EN.md) · [Mensaje para Edu](Mensaje_para_Edu.txt) · [Evidencias](matriz_evidencias.csv) · [Decisiones](decisiones_para_Edu.csv) · [Plan de pruebas](plan_verificacion.csv) · [Cálculos](calculos.json).\n\nConsolidación y cálculos offline. Sin nuevos ensayos físicos, aprobación de ICD o perfil RF. El PDF de consulta se publica en Drive propio; fuentes de fabricantes y medios privados no se republican.\n',encoding='utf-8')
 def page(c,doc):
  c.saveState();c.setFillColor(grey);c.setFont('Segoe',8);c.drawString(45,817,'ASTRA / GROUNDSTATION Y CÁMARAS');c.drawRightString(550,817,'PDR - 17/11/2026 - v1');c.setStrokeColor(colors.HexColor('#D8E0E8'));c.line(45,805,550,805);c.drawString(45,25,'Diseño preliminar y evidencia de banco - pendientes explícitos');c.drawRightString(550,25,str(doc.page));c.restoreState()
 pdf=out/'Aporte_PDR_para_Rebe_2026-11-17_v1.pdf';SimpleDocTemplate(str(pdf),pagesize=A4,rightMargin=50,leftMargin=45,topMargin=55,bottomMargin=45,title='ASTRA - Aporte PDR de groundstation y cámaras',author='ASTRA - Groundstation').build(story,onFirstPage=page,onLaterPages=page)
 for f in public.iterdir():
  if f.is_file() and f.suffix in ['.md','.txt','.csv','.svg','.json']:
   text=f.read_text(encoding='utf-8')
   with f.open('w',encoding='utf-8',newline='\n') as stream:stream.write(text)
   shutil.copy2(f,out/f.name)
 manifest={'prepared_date':'2026-11-17','jira':['ASTRA-24','ASTRA-25','ASTRA-39','ASTRA-41'],'physical_tests_today':False,'radio_configured':False,'hardware_ports_opened':False,'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in out.iterdir() if f.is_file() and f.name!='manifest_entrega.json'},'source_commit':'193e58c2297c41b5c7d973ab515bc36df86f5060'}
 (out/'manifest_entrega.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(pdf)

if __name__=='__main__':main()
