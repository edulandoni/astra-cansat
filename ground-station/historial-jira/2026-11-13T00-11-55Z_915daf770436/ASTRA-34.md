# ASTRA-34 — GND — Investigar calidad de datos y prevención de fallas

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-34)

Estado observado: Finalizado. Asignación: Cristian Ponsone. Creación: Cristian Ponsone.

## Descripción original consultada

## Objetivo

Evaluar mejoras de groundstation con datos sintéticos, distinguiendo mensaje válido de dato reciente, coherente y conservado. Seleccionar mejoras por evidencia antes de comprometer implementación.

## Trabajo y entregable

Investigar indicadores explicables, antigüedad, sesiones, contradicciones y campañas reproducibles de fallas. Conservar hipótesis, sondeos, resultados y alternativas. Separar del trabajo de receptor/parser/CSV y de la GUI; vincular esos entregables cuando corresponda.

## Estado real y límites

Ya ejecuté diez sondeos de software y publiqué sus resultados. El monitor propuesto no está implementado ni validado; no hay hardware ni prueba RF. Los ensayos concretos de almacenamiento y reconexión conservan su bitácora técnica en ASTRA-21. Las ideas enumeradas no se convierten automáticamente en compromisos de desarrollo.

## Criterio para completar esta investigación

Comparar comportamiento actual y mejoras candidatas, métricas de detección/demora/falsas alarmas, dependencias del ICD y recomendación justificada. Crear o actualizar una tarea de implementación sólo cuando el alcance esté asumido. Conservar los originales y registrar cambios mediante actualizaciones fechadas.

## Comentarios conservados

### 2026-10-19T20:41:08.837-0300 — comentario 10056

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10056). Última edición informada: 2026-10-19T20:41:08.837-0300.

## 19/10/2026 — COMENTARIO 1 — Incorporación de la investigación de calidad y prevención

### Procedencia y objetivo

Incorporo aquí la investigación que registré en ASTRA-21, comentario 6:  
https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10049  
Conservo ese original y su fecha; esta entrada ordena el tema y no representa una segunda ejecución. Busco elegir mejoras verificables antes de conectarnos al hardware.

### Trabajo y resultados ya obtenidos

Ejecuté diez sondeos con datos sintéticos, TEAM_ID 1000 ficticio y fallas inyectadas. El nominal aceptó 131 muestras y rechazó equipo ajeno. El parser aceptó números finitos pero deliberadamente anómalos (altura 3000 m, temperatura 999 °C, giro 9999 °/s), alturas y hora congeladas. Un mismo contador con contenido diferente no tuvo aviso específico de conflicto; ambos quedaron raw. Ante retroceso del contador, latest conservó un valor alto anterior. La excepción controlada de escritura raw terminó el worker con ERROR.

Estos resultados distinguen validación de estructura y evaluación de calidad; no fijan umbrales operativos ni demuestran qué sensor falló. Presión/altura del mismo sensor no son redundancia independiente.

### Propuesta y límites

Propongo evaluar avisos explicables de dato reciente, retenido, sospechoso o ausente, con métricas de demora, detecciones omitidas y falsas alarmas. También registré ideas de simulación coherente, pruebas de comandos y entrenamiento de operador como posibilidades, no compromisos ya implementados. No implementé el monitor, no probé hardware ni RF y no cambio ICD ni parámetros compartidos.

Las comprobaciones concretas de volumen, reconexión y recuperación de CSV siguen como avance técnico de ASTRA-21, comentario 8:  
https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10051  
Las utilizo como evidencia relacionada, sin duplicar su bitácora ni afirmar integración operativa del recuperador.

### Evidencia y próximos pasos

Informe: https://github.com/edulandoni/astra-cansat/blob/82a80614e186a5f8b50559eea8a293503154f02d/ground-station/docs/investigacion/2026-10-19-innovacion-y-prevencion.md  
Experimento: https://github.com/edulandoni/astra-cansat/tree/82a80614e186a5f8b50559eea8a293503154f02d/ground-station/experiments/2026-10-19-prevencion  
Resultados: https://github.com/edulandoni/astra-cansat/tree/82a80614e186a5f8b50559eea8a293503154f02d/ground-station/evidence/2026-10-19-investigacion-prevencion

Comparar alternativas y acordar sesiones, unidades y métricas antes de implementar. Dejé la investigación En curso porque ya tiene análisis y sondeos ejecutados; no cierro funciones pendientes.

### 2026-10-19T20:44:01.243-0300 — comentario 10062

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10062). Última edición informada: 2026-10-19T20:44:01.243-0300.

## 19/10/2026 — COMENTARIO 2 — Ubicación en GitHub corregida

La investigación y sus sondeos continúan aquí. Los ensayos de reconexión y recuperación CSV permanecen en ASTRA-21; los informes originales conservan sus referencias históricas.

Agregué un índice por tema, sin cambiar resultados, código ni originales. La reorganización no constituye otro ensayo.

Guía de esta tarea: https://github.com/edulandoni/astra-cansat/blob/a4c26b05bc66ef77efa702f03256e4bb3ba2d3c8/ground-station/docs/temas/calidad-de-datos/README.md  
Mapa vigente: https://github.com/edulandoni/astra-cansat/blob/a4c26b05bc66ef77efa702f03256e4bb3ba2d3c8/ground-station/docs/trazabilidad-vigente-2026-10-19.md  
Cambio: https://github.com/edulandoni/astra-cansat/commit/a4c26b05bc66ef77efa702f03256e4bb3ba2d3c8

El comentario 1 de esta tarea conserva el motivo, trabajo previo, resultados y límites. Las próximas actualizaciones temáticas se agregan aquí.

### 2026-10-21T21:32:11.259-0300 — comentario 10101

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10101). Última edición informada: 2026-10-21T21:32:11.259-0300.

21/10/2026 — COMENTARIO 3 — ACTUALIZACIÓN de evidencia para prevenir falsos diagnósticos

El antecedente COSMOS de ASTRA-35 aporta un caso concreto: 525 filas, 89 identificadores ausentes en el intervalo de contador y campos GPS/giro a cero. No demuestra la causa de los huecos ni que cero sea una medición válida. La captura de GUI tampoco acredita el mismo conjunto completo que el CSV.

Para nuestras verificaciones propongo separar recibido, válido, guardado y faltante de contador; conservar origen y antigüedad; y evitar presentar GPS ausente como posición real o un hueco como pérdida RF confirmada. Las pruebas deberán indicar qué falla se inyectó y con qué registro contrastamos. Es una ampliación de criterios de investigación: hoy no cambié código ni ejecuté otro ensayo de ASTRA.

[Evidencia, método y límites](https://github.com/edulandoni/astra-cansat/blob/48b750db6e4ddadd9c2a5da429be37d7c82580b6/ground-station/docs/investigacion/2026-10-21-cosmos-csv-y-estacion.md) · [Métricas](https://github.com/edulandoni/astra-cansat/blob/48b750db6e4ddadd9c2a5da429be37d7c82580b6/ground-station/docs/investigacion/2026-10-21-cosmos-metricas.json) · [Informe Drive](https://drive.google.com/file/d/1-Wscr0q91TqCbbWjQxsjWEvwY-0xtl9g/view). No copio datos o parámetros extranjeros como requisito propio.

### 2026-10-23T21:04:05.980-0300 — comentario 10109

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10109). Última edición informada: 2026-10-23T21:04:05.980-0300.

23/10/2026 — COMENTARIO 4 — Criterios de calidad derivados del contraste RSX

El análisis de ASTRA-35 mostró un caso concreto: una misma planilla mezcla diagnósticos y telemetría; contar todas las filas como paquetes produciría una métrica equivocada. También hay un máximo de altitud anterior al estado APOGEE y un valor de giro plano que no permite confirmar actualización o movimiento físico por sí solo.

Propongo para nuestras pruebas separar contadores de telemetría, diagnóstico y rechazo de formato; conservar hora de recepción, tiempo de misión y antigüedad del último dato válido; distinguir estado enviado de evento confirmado. Una captura sin LANDED debe figurar incompleta, sin atribuir automáticamente su causa a pérdida RF. PACKET_RECV igual a PACKET_COUNT no es evidencia independiente sin verificar cómo se genera.

Son propuestas de diseño y criterios para ensayos futuros, no funciones implementadas o verificadas hoy. No modifiqué parser, GUI, ICD o perfil RF. El próximo paso técnico será convertir estos casos en entradas de prueba con resultado esperado y evidencia propia.

[Análisis, procedencia, celdas y métricas en GitHub](https://github.com/edulandoni/astra-cansat/blob/48debe0bf52d52cabf90e3d88413b39995a79011/ground-station/docs/investigacion/2026-10-23-rsx-datos-y-calidad.md) · [Copia en Drive, antecedentes RSX](https://drive.google.com/file/d/1EIHYAkLTOQDdIaa7gN4naSeGZsrNpmD4/view) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/48debe0bf52d52cabf90e3d88413b39995a79011). Conservo las entradas anteriores.

### 2026-10-23T23:27:19.141-0300 — comentario 10119

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10119). Última edición informada: 2026-10-23T23:27:19.141-0300.

23/10/2026 — COMENTARIO 5 — ACTUALIZACIÓN COMENTARIO 4: criterios convertidos en implementación y pruebas

Implementé en el banco nuevo separación de origen, edad de enlace y de medición, retención identificada de última soluciónGPS, conflictos de igual contador y aviso de reloj congelado mientras avanza contador. Un valor de sensor constante por sí solo no dispara avería. No convierto estado de vuelo declarado en evento físico confirmado.

En GPS_LOSS por USB llegaron131paquetes:15sin fix conservaron exactamente posición y hora de la última solución previa. El análisis posterior de la captura contrastó esos valores y losCSV. En software probé reloj congelado sin falsa alarma nominal, duplicados/conflictos, datos anteriores que dejan de ser actuales al cambiar arranque y respuesta tardía que no retrocede contexto.

Los escritores independientes permiten explicar diferencia entre recibido, validado y confirmado en cada archivo. Probé aislamiento/reintento y pérdida conocida al agotar una cola. La recuperación genera archivos nuevos con procedencia y bloquea discrepancias, sin inventar valores. Todo esto usa datos sintéticos: no acredita sensores reales, persistencia eléctrica, latencia RF ni autonomía.

[Implementación](https://github.com/edulandoni/astra-cansat/tree/114616a4dc5d1f09706b623581b9fdd0714621da/ground-station/banco-usb-v0.2) · [Evidencia USB](https://github.com/edulandoni/astra-cansat/blob/114616a4dc5d1f09706b623581b9fdd0714621da/ground-station/evidence/2026-10-23-banco02/usb-cinco-escenarios-01.json) · [Informe y límites](https://github.com/edulandoni/astra-cansat/blob/114616a4dc5d1f09706b623581b9fdd0714621da/ground-station/docs/2026-10-23-banco02-actualizacion-01.md) · [Commit](https://github.com/edulandoni/astra-cansat/commit/114616a4dc5d1f09706b623581b9fdd0714621da). La pantalla final fue observada también en origenPC; quedan RST/desconexión físicos y ≥2hUSB conGUI. El seguimiento de datos/archivo continúa en ASTRA-21 y pantalla en ASTRA-22. Mantengo En curso.

### 2026-10-23T23:48:21.296-0300 — comentario 10131

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10131). Última edición informada: 2026-10-23T23:48:21.296-0300.

23/10/2026 — COMENTARIO 6 — ACTUALIZACIÓN COMENTARIO 5: Incidencia real convertida en prueba de calidad

El primerEN/RST terminó en modo descarga y no produjohello. Encontré que esperar sólo una identidad nueva dejaba valores anteriores visibles como viejos, sin explicar inmediatamente la pérdida de contexto. Corregí el banco para invalidarlos ante el diagnósticoROM, conservando el histórico y dejando identidad desconocida; no infiero una causa física delGPIO0.

El segundoRST sí produjo boot diferente, pantalla vacía y otra misión1..131 separada. La corrección se verificó con12tests y reproduciendo el diagnóstico capturado:latest/epoch vacíos yambigüedad explícita hasta nueva identidad. No cuento reproducción como otroRST. Un sondeo único recuperahello perdido, sin repetir comandos anteriores.

Conservo ambosCSV y diario con procedencia. El offset/hora ficticios volvieron a sus iniciales trasRST: no es cumplimiento de persistencia de vuelo. Quedan desconexión física dedicada, soporte independiente y≥2hUSB conGUI/memoria medida; laGUI abierta con períodos largos sin flujo no acredita ese ensayo.

[Informe y límites](https://github.com/edulandoni/astra-cansat/blob/0603ad93182850e4ebad856d7a56b54970ddaa30/ground-station/docs/2026-10-23-rst-fisico-actualizacion-03.md) · [Evidencia](https://github.com/edulandoni/astra-cansat/blob/0603ad93182850e4ebad856d7a56b54970ddaa30/ground-station/evidence/2026-10-23-banco02/rst-fisico-05/resultado-rst-05.json) · [Drive verificado](https://drive.google.com/file/d/1A_4vETJ2wQrLxzcoFHSlFh6Tiv1cQs2x/view?usp=drivesdk) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/0603ad93182850e4ebad856d7a56b54970ddaa30). Conservo originales y comentarios anteriores.

### 2026-10-24T00:25:29.068-0300 — comentario 10135

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10135). Última edición informada: 2026-10-24T00:25:29.068-0300.

24/10/2026 — COMENTARIO 7 — ACTUALIZACIÓN COMENTARIO 6: Anomalía real, visibilidad y reconstrucción equivalente

La reconexión recuperó puerto yboot distinto, sin presentar mediciones anteriores como actuales. La misión posterior conservó1..131. Registré además la ráfaga malformada de12899bytes y el desborde deencuadre: causa pendiente, no pérdida dearchivo ni prueba de pérdidaRF. Añadí avisoGUI y prueba de trama excesiva+equipoajeno+diagnóstico+muestra válida;13tests pasaron.

Reproduje131tramas físicas aceptadas con origenREPLAY, conservando bytes reensamblados/tiempos y procedencia. Las salidasC:yD: se comprobaron en discosdistintos y dieron archivos idénticos. La reconstrucción desde lasdosfuentes reunió131candidatos y reprodujo elCSVsin cambiaroriginales. No relleno elperíodo sin generación ni lo llamo vuelo completo.

Quedan causa dela ráfaga, doshorascontinuas, persistenciaeléctrica y respaldofísicosimultáneo conESP32. Los datos siguen sintéticos; no atribuyo sensoresreales o autonomía al resultado. Mantengo En curso.

[Informe con evidencia y límites](https://github.com/edulandoni/astra-cansat/blob/2863fee267eeb3f48826e8876e279ca096ab091f/ground-station/docs/2026-10-24-reconexion-y-doble-soporte-actualizacion-04.md) · [Drive verificado](https://drive.google.com/file/d/11qcMyyB8SE5QESRkXl5xLetJK-FeWNE2/view?usp=drivesdk) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/2863fee267eeb3f48826e8876e279ca096ab091f). Conservo entradas y originales.

### 2026-10-24T00:45:54.455-0300 — comentario 10140

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10140). Última edición informada: 2026-10-24T00:45:54.455-0300.

24/10/2026 — COMENTARIO 8 — ACTUALIZACIÓN COMENTARIO 7: Pruebas contra falsa continuidad y falsa duración

Encontré y corregí la posible repetición de run al cambiar de sesión PC con el mismo arranque del emisor. La prueba física de dos clientes consecutivos conservó boot y cambió run, con 12 muestras correctas por corrida. El historial anterior no se reescribe.

Incorporé tiempo monotónico además de UTC. Una prueba de reproducción conserva ritmo aunque UTC retroceda; el analizador rechaza una captura USB corta como evidencia de dos horas. Pasaron 15 tests. La cadencia física corta dio media 0,999887 s, con jitter de llegada explícito; no uso esa medición como autonomía, exactitud absoluta o cumplimiento RF.

El ensayo prolongado se ejecuta desde snapshot y está pendiente de resultado. Compararé duración efectivamente observada, secuencia, CSV, almacenamiento, callbacks y memoria; no extrapolaré ausencia de fugas a tiempo ilimitado. El control de pantalla queda cerrado entre inspecciones y los contenedores siguen acotados. Mantengo la tarea abierta.

[Informe y evidencia por revisión](https://github.com/edulandoni/astra-cansat/blob/38ae9999af98395e376030089cf5f2c7447f409f/ground-station/docs/2026-10-24-cadencia-identidad-e-inicio-prolongado-actualizacion-05.md) · [Drive verificado](https://drive.google.com/file/d/1j6m_KdBn266iJZAxvZD4yM1B4rH_MkQ-/view?usp=drivesdk) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/38ae9999af98395e376030089cf5f2c7447f409f). Conservo resultados, fuentes y comentarios anteriores.

### 2026-10-24T01:02:57.613-0300 — comentario 10146

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10146). Última edición informada: 2026-10-24T01:02:57.613-0300.

24/10/2026 — COMENTARIO 9 — Última posición válida cuando el mensaje no tiene fix

Durante la revisión encontré que la GUI mostraba los campos GPS de la trama aunque GPS_SATS fuera cero. Nuestro emisor repetía la posición previa y ocultaba ese caso: otro mensaje sin fix puede traer ceros u otras coordenadas numéricas. Corregí sólo la presentación: hora, altitud y coordenadas pasan a la última solución válida con etiqueta y edad; sin solución anterior aparecen vacías y con aviso explícito. Cuando vuelve el fix, muestro el dato nuevo. El CSV y los valores originales recibidos quedan intactos.

Pasaron 16 pruebas de software, incluido un caso sin fix inicial, otro con coordenadas diferentes de la última válida y recuperación posterior. Observé además una GUI REPLAY con dos mensajes sintéticos: contador 51, satélites 0, última posición válida etiquetada y seis gráficas visibles. No es una prueba GPS física. Cerré esa reproducción y el control del escritorio; la adquisición USB prolongada continúa independiente.

La corrida de dos horas conserva su snapshot anterior y no acreditará esta corrección posterior. No reinicié el ensayo ni le atribuyo código que no ejecutó. La regla de validez es del banco: debe acordarse para vuelo.

[Informe, prueba y huellas](https://github.com/edulandoni/astra-cansat/blob/36629a493f3c8dc2eefaebf0aeea4ae89c02dbed/ground-station/docs/2026-10-24-gps-presentacion-actualizacion-06.md) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/36629a493f3c8dc2eefaebf0aeea4ae89c02dbed) · [Drive](https://drive.google.com/file/d/1JU0LwK6cDEL9UNOkmGc4HA9bGGrDVUUS/view?usp=drivesdk). Mantengo las entradas previas y los pendientes de RF, interoperabilidad y operación prolongada.

### 2026-10-24T01:11:42.020-0300 — comentario 10149

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10149). Última edición informada: 2026-10-24T01:11:42.020-0300.

24/10/2026 — COMENTARIO 10 — ACTUALIZACIÓN del ensayo prolongado: medidor corregido y nuevo intento

Interrumpí deliberadamente la primera corrida tras 1906 muestras y 1905,063 s entre primera y última. El resultado queda false: no son dos horas. No hubo pérdidas declaradas por escritores, errores de encuadre ni conflictos en el segmento nominal, pero la memoria crecía. Aislé la causa: el medidor creaba tipos de ctypes en cada consulta y la caché global los retenía. Tener colas e historial acotados no demostraba memoria total acotada.

Corregí el medidor para definir tipo y API una sola vez. Pasaron 17 pruebas, incluida una de 500 consultas sin nuevos tipos después de inicializar. El nuevo gui_health registra las inicializaciones y el analizador exige una sola. Conservo resultado, salud, huellas, diario y CSV del intento anterior; no los reemplazo ni recalifico como aprobados.

Cerré esa GUI con vaciado de escritores, confirmé liberación de la inhibición transitoria de suspensión y envié STOP de banco antes de la nueva campaña. Inicié otro snapshot el 24/10 a las 01:09:00 ART, con las correcciones del medidor y GPS: 7261 muestras, ventana de 7280 s, cierre previsto cerca de 03:10:20 ART. No recargué firmware ni reinicié físicamente. Calibración, hora, alimentación y RUN quedaron confirmados. La campaña nueva todavía no tiene resultado final.

[Informe, intento interrumpido y configuración nueva](https://github.com/edulandoni/astra-cansat/blob/ce3220891ece63d2fcaa0c7990ec8d3eaa63181f/ground-station/docs/2026-10-24-medidor-y-reinicio-prolongado-actualizacion-07.md) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/ce3220891ece63d2fcaa0c7990ec8d3eaa63181f) · [Drive](https://drive.google.com/file/d/1kBmo1uFNJLebHIolXAUBUiQ9eailEgpe/view?usp=drivesdk). Mantengo los pendientes y las tareas abiertas. No acredita RF, autonomía ni respaldo externo simultáneo.

### 2026-10-24T02:12:08.544-0300 — comentario 10151

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10151). Última edición informada: 2026-10-24T02:12:08.544-0300.

24/10/2026 — COMENTARIO 11 — Conflicto dentro del propio diario: reconstrucción bloqueada

Amplié la revisión del recuperador. Ya comparaba filas contradictorias entre copias, pero ignoraba la marca que deja el receptor cuando dos mensajes válidos tienen igual contador y distinto contenido. El receptor conserva el primero en CSV y registra el conflicto en el diario; el recuperador anterior podía declarar salida limpia desde ese diario aunque conociera la contradicción.

Ahora bloqueo la reconstrucción ante esa marca y explico archivo, línea, contexto y contador. En un caso sintético con contador 1 y altitudes 0,0/999,0 m, comprobé ambas versiones sobre el mismo original: antes escribía una fila; ahora no escribe CSV y registra un conflicto. El original conserva su huella. Pasaron 18 pruebas, incluida esta regresión y los casos previos de copias, CSV/JSONL y recuperación limpia.

No elijo cuál medición es verdadera ni infiero contradicciones ausentes: si sólo selecciono un CSV y falta el diario donde estaba la marca, esa información no está disponible. La herramienta es offline; no cambié firmware ni la GUI que está ejecutando el segundo intento prolongado.

[Informe y comparación antes/después](https://github.com/edulandoni/astra-cansat/blob/dfda37cca6aa97aabcd794932eae2cc42a911e15/ground-station/docs/2026-10-24-recuperacion-conflicto-interno-actualizacion-08.md) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/dfda37cca6aa97aabcd794932eae2cc42a911e15) · [Drive](https://drive.google.com/file/d/1WJHAB2SS6XynnDfCsKNPQJ-2bfINWXZS/view?usp=drivesdk). Conservo las entradas anteriores y sigo esperando el cierre real de la corrida USB.

### 2026-10-24T03:18:17.971-0300 — comentario 10155

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10155). Última edición informada: 2026-10-24T03:18:17.971-0300.

24/10/2026 — COMENTARIO 12 — Aceptación del banco USB y límites para el PDR

Cerré la campaña nominal prolongada con 7261 datos únicos, sin huecos, duplicados, conflictos, rechazos o descartes conocidos y con CSV igual al diario. Comprobé la declaración completa del emisor y reconstrucción idéntica conservando originales. La evidencia incluye la serie de salud completa, no sólo una captura o el contador final.

El intento anterior interrumpido queda preservado como no aprobado. La acumulación del medidor se aisló y corrigió; la segunda corrida registró una única inicialización y memoria residente entre 36,26 y 44,86 MiB. No atribuyo causa a sus variaciones sin medirla ni uso el working set como prueba universal de ausencia de fugas. El historial/colas observados respetaron sus límites.

La suite actual pasó 18 pruebas. Los casos de ausencia GPS, reloj congelado, mensajes contradictorios, timeout/respuesta tardía y escritores fallidos tienen evidencias específicas; no afirmo haber inyectado todos esos fallos en la corrida nominal de dos horas. La reconstrucción ahora bloquea tanto discrepancias entre copias como conflictos ya registrados dentro de un diario. Un CSV sin ese diario no permite inferir marcas ausentes.

La matriz distingue software, USB físico, reproducción y pendientes. Puedo presentar manejo de datos trazable ante los fallos ensayados como mejora propia demostrada. No acredita integridad frente a toda alteración numérica silenciosa, CRC de vuelo, autonomía, RF, ni valoración oficial de innovación.

[Informe final y matriz de la etapa](https://github.com/edulandoni/astra-cansat/blob/44bf6ea88a04acfa460dd77bdb8c62d4a6fb9a29/ground-station/docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md) · [Commit de resultados verificado](https://github.com/edulandoni/astra-cansat/commit/44bf6ea88a04acfa460dd77bdb8c62d4a6fb9a29) · [Drive: informe final](https://drive.google.com/file/d/1i-pRyjTcZRqRaD8nuIt3MrOW22W6Hu90/view?usp=drivesdk) · [Aclaración de reproducción](https://github.com/edulandoni/astra-cansat/blob/838e0a187472e0d7dcc2f6c4f8dee8abf5856c4d/ground-station/docs/2026-10-24-control-reproduccion-actualizacion-10.md) · [Drive: control de fuentes](https://drive.google.com/file/d/1fEv5ZasO5i-YNfuKfulLwAH6NjjiO8yn/view?usp=drivesdk).

### 2026-10-24T03:57:20.764-0300 — comentario 10157

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10157). Última edición informada: 2026-10-24T03:57:20.764-0300.

24/10/2026 — COMENTARIO 13 — ACTUALIZACIÓN de la investigación de calidad de datos

Completé la comparación y la recomendación previstas para esta investigación. Conservé los sondeos y conclusiones anteriores: la descripción original refleja aquel momento y esta entrada registra el estado nuevo.

Comparé las reglas anteriores documentadas con las candidatas en seis trazas reproducibles, con reloj controlado: nominal, altitud constante, GPS sin solución, reloj GPS congelado, reloj de misión congelado y pausa de telemetría con control activo. No ejecuté una versión histórica de la GUI. Las 3.144 observaciones no dieron avisos positivos fuera de las ventanas de fallo definidas; esto no es una estimación estadística de falsas alarmas ni una medición de latencia de vuelo. Detecté GPS sin solución en la primera muestra afectada; GPS congelado y pausa de telemetría a los 2,25 s desde la primera muestra defectuosa/esperada ausente; reloj de misión congelado a los 2 s. Registré también la recuperación.

La mejora distingue enlace activo, telemetría reciente y GPS actualizado. Si toda la telemetría envejece, no atribuyo el problema al GPS. Un valor constante por sí solo no demuestra un sensor averiado. Los umbrales de 3 s son configurables y exclusivos del banco; dependen de cadencia y validez que debemos acordar en el ICD antes de trasladarlos a vuelo.

Comprobé la presentación en una GUI real de reproducción: contador 6, telemetría de 0,7 s de antigüedad y GPS de 10,7 s, con aviso “GPS SIN ACTUALIZAR”. Conservé captura original, registros y procedimiento. Pasaron las 22 pruebas unitarias del banco, incluidas las nuevas de calidad y conservación del evento.

Recomiendo mantener estos avisos explicables en el banco. La implementación y sus ensayos continúan trazados en ASTRA-21/22 y la interfaz compartida en ASTRA-24. Doy por cumplidos los criterios de esta investigación; reviso su cierre mediante el flujo de Jira. Esto no acredita GPS físico, vuelo, RF ni aprobación del ICD.

[Informe, métricas y evidencia en GitHub](https://github.com/edulandoni/astra-cansat/blob/9735087c1074754895273c4109553f5b350c7faf/ground-station/docs/investigacion/2026-10-24-calidad-medida-y-cierre-investigacion.md)
[Copia verificada en Drive](https://drive.google.com/file/d/11kA0UM5kLgTEHoe7xPqLGoDgF6xS9x5n/view)

## Historial de cambios de campos

### 2026-10-19T20:39:34.384-0300 — cambio 10135

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Backlog

Después: Por hacer

### 2026-10-19T20:39:55.604-0300 — cambio 10139

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Por hacer

Después: En curso

### 2026-10-24T03:57:32.563-0300 — cambio 10150

Autoría original: Cristian Ponsone.

Campo: status.

Antes: En curso

Después: En revisión

### 2026-10-24T03:57:46.317-0300 — cambio 10151

Autoría original: Cristian Ponsone.

Campo: resolution.

Antes: (sin valor informado)

Después: Done

Campo: status.

Antes: En revisión

Después: Finalizado

