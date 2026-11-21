# ASTRA-18 — COMMS — Verificar SX1276 contra X1–X6 v2 y seleccionar modo RF

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-18)

Estado observado: En curso. Asignación: Cristian Ponsone. Creación: Eduardo Landoni.

## Descripción original consultada

## Objetivo

Evaluar SX1276 contra X1–X6 del anexo CONAE v2 y proponer el modo RF para revisión conjunta del ICD con Edu y Systems.

## Trabajo a realizar

* Revisar documentación oficial Semtech y comparar LoRa/FSK/GFSK: robustez, tasa, CRC, identificación, destino y verificación.
* Mapear banda X1, prohibición de broadcast X2, comienzo de misión X3 (TBR), tasa X4, contenido X5 y consulta batería/solar X6.
* Definir direccionamiento y aceptación de paquetes propios sin confundir filtrado de TEAM_ID con ausencia de broadcast o de interferencia.
* El NetID/PANID con número de equipo era X2 v1 y NO aparece en v2: conservarlo como antecedente; su implementación sólo será una decisión interna justificada si se adopta en el ICD.
* Preparar consulta sobre el comando automático de X3 y sobre cualquier documento separado de protocolo.
* No fijar frecuencia exacta, modo, potencia, Sync Word, destino o framing unilateralmente.

## Entregable

Matriz Requisito v2 | implementación candidata | evidencia | estado, con relación a los IDs v1 y recomendación de modo RF.

## Criterio de finalización

* X1–X6 evaluados con evidencia y pendientes identificados.
* Modo y destino sin broadcast justificados y acordados en ASTRA-19.
* X3 aclarado o registrado TBR con responsable.
* No se exige como obligación v2 el NetID/PANID retirado.
* Fuentes y configuración de ensayo permiten reproducir la evaluación.

## Referencia vigente y revisión

Anexo CONAE v2 publicado el 16/10/2026: https://www.argentina.gob.ar/sites/default/files/2026/08/anexo_requerimientos_tecnicos\_-\_cansat_universitario_2026-2027_v2.pdf

Informe de impacto v1 → v2: https://docs.google.com/document/d/1WwZ83me8W0qA7T8eum6xSrYxVtpbYoT9OYq1Z0WPMNI/edit?usp=drivesdk

Matriz completa y fuentes conservadas: https://drive.google.com/drive/folders/16P_8tdACes23uirmR-koQlB5iE0oVhEf

Esta actualización cambia la referencia de diseño; no acredita implementación ni ensayo físico. Se conservan responsable y estado. Presupuesto fuera de esta revisión.

## Comentarios conservados

### 2026-10-17T12:29:03.603-0300 — comentario 10014

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-18?focusedCommentId=10014). Última edición informada: 2026-10-17T12:41:59.524-0300.

## Bitácora 17/10/2026 — descripción anterior conservada y motivo de su actualización

Incorporo al historial la descripción que conservé antes de actualizar la referencia de v1 a v2. Dejo esta versión anterior para que podamos reconstruir la evolución de la tarea. Este registro no implica una aprobación ni una nueva implementación.

**Título anterior:** COMMS — Verificar SX1276 contra X1–X7 y seleccionar modo RF

### Descripción anterior íntegra

## Objetivo

Determinar si el SX1276 puede satisfacer de forma defendible los requisitos CONAE X1–X7 y seleccionar el modo de operación RF a utilizar en el prototipo/PDR.

## Trabajo a realizar

* Revisar datasheet oficial Semtech SX1276.
* Comparar LoRa vs FSK/GFSK para: identificación de red, direccionamiento unicast, CRC, tasa de datos, robustez y facilidad de verificación.
* Mapear X1–X7 a funciones/configuración concreta del SX1276 y del protocolo ASTRA.
* Definir cómo se implementarán NetID/PANID equivalente y prohibición de broadcast.
* Identificar cualquier requisito que siga siendo TBR y preparar consulta a CONAE si fuera necesaria.

## Entregable

Matriz `Requisito CONAE | Implementación SX1276 | Evidencia | Estado` + recomendación de modo RF.

## Criterio de finalización

* X1–X7 evaluados uno por uno.
* La selección LoRa/FSK/GFSK está justificada con documentación oficial.
* NetID/PANID y unicast quedan técnicamente definidos o marcados TBR.
* Fuentes oficiales enlazadas.
* Resultado listo para incorporar a la PDR y al ICD de comunicaciones.

### Qué cambió y por qué

La descripción actual distingue requisitos CONAE v2, convenciones heredadas v1 y decisiones internas pendientes. Cambios concretos: retiro de NetID/PANID como obligación normativa, renumeración de X, redacción ambigua del comienzo de misión y ausencia del formato detallado en el PDF v2. Se preservaron responsable y estado.

Registro los avances, las correcciones y sus fundamentos como entradas de bitácora. Si necesito actualizar una descripción, primero conservo la versión anterior y explico el cambio. Dejo el material necesario para preparar el PDR dentro de Jira. La migración y su matriz están en ASTRA-26; el contrato compartido, en ASTRA-19.

### 2026-10-17T12:31:25.774-0300 — comentario 10025

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-18?focusedCommentId=10025). Última edición informada: 2026-10-17T12:42:01.802-0300.

## Bitácora 17/10/2026 — identificación propia y comparación RF después de v2

### Propuesta que quiero evaluar con el equipo

Al desaparecer la obligación expresa NetID/PANID y mantenerse la prohibición de broadcast, proponemos construir identificación lógica y destinos propios en nuestro protocolo. La intención atribuida al organizador es una interpretación del equipo; no una aclaración oficial de CONAE. Podemos ensayar aislamiento lógico con emisores sintéticos antes de disponer de radio.

### Qué confirmó la revisión del fabricante

SX1276 admite LoRa y FSK; GFSK usa conformado gaussiano de FSK. En packet mode FSK puede aceptarse sólo NodeAddress (AddressFiltering=01); la opción que acepta también BroadcastAddress no corresponde al ensayo sin broadcast. En LoRa hay filtrado por software del payload; no trasladar registros de direccionamiento FSK a LoRa.

Fuente del fabricante: Semtech SX1276/77/78/79 Rev.4, secciones 4.1.5, 4.2.2.3 y 4.2.13, copia publicada por distribuidor: https://cdn-shop.adafruit.com/product-files/3179/sx1276_77_78_79.pdf

### Propuesta para revisar con Edu

Evaluar una envolvente lógica con versión, identificación de red/equipo, origen, destino, tipo, secuencia e integridad, manteniendo el modelo de telemetría desacoplado. No se eligieron aún tamaños, valores de direcciones, algoritmo de integridad, frecuencia, modulación ni Sync Word. Un NetID propio sería una decisión ASTRA; no una nueva obligación CONAE ni un requisito que haya que simular para cumplir.

Identificar el equipo y dirigir cada paquete a un destinatario permiten descartar tráfico ajeno. Una antena sigue recibiendo energía de otras emisiones y pueden existir interferencias. El identificador no demuestra autenticidad ni confidencialidad. El criterio defendible es aceptar/procesar sólo el tráfico destinado al extremo correcto y demostrarlo, sin prometer exclusividad física de la señal.

### Ensayos propuestos y resultados esperados

1. Mezclar dos emisores sintéticos: aceptar el equipo propio, registrar/rechazar el ajeno.
2. Mismo equipo con destino equivocado: no aceptar telemetría ni ejecutar comando.
3. Trama incompleta, versión incompatible o integridad fallida: rechazar sin bloquear recepción.
4. Repetición y atraso: conservar observación, evitar duplicar medida o actuación.
5. Comando destinado al extremo correcto: demostrar recepción, aceptación y resultado por separado.
6. Con RF integrado, repetir en ambos sentidos y medir pérdidas/latencia mientras otro emisor comparte canal. El filtrado no recupera una colisión física.

### Estado real y próximo paso

Estas pruebas de identificación extendida son un plan: todavía no se implementó esta envolvente ni se ensayó LoRa/FSK/GFSK. El parser de banco sí compara TEAM_ID, que cubre sólo una parte. Comparar robustez, tiempo de aire a 1 Hz, comandos, consumo, complejidad y disponibilidad del módulo; cerrar Radio Profile e ICD en ASTRA-19 y demostrar interoperabilidad ASTRA-24. La eliminación de NetID/PANID no descarta ninguno de esos modos por sí sola.

### 2026-10-17T12:43:26.355-0300 — comentario 10029

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-18?focusedCommentId=10029). Última edición informada: 2026-10-17T12:43:26.355-0300.

## Bitácora 17/10/2026 — estado de trabajo y alcance

Paso esta tarea de Backlog a **En curso**.

Ya empecé a revisar la v2, comparar LoRa/FSK/GFSK y proponer identificación y destinos propios. Me falta cerrar el Radio Profile y la verificación con Edu.

Uso Backlog para ideas que todavía no asumimos; Por hacer para trabajo previsto sin iniciar; y En curso cuando ya estoy trabajando. La tarea sigue abierta hasta cumplir sus criterios y conservar la evidencia. En adelante gestiono únicamente tareas que creé o que están asignadas a mí; las dependencias con Edu y Rebe las documento desde mis propias tareas.

### 2026-10-19T19:28:16.200-0300 — comentario 10038

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-18?focusedCommentId=10038). Última edición informada: 2026-10-19T19:28:16.200-0300.

## 19/10/2026 — COMENTARIO 4 — Comparación v1/v2 de groundstation en GitHub

Publiqué la selección del análisis que afecta a recepción, datos y comunicaciones de mi área, para reconstruir desde el PDR qué cambia y qué sigue pendiente. Conservo las conclusiones anteriores y sus fuentes; esta entrada enlaza su versión en GitHub.

La exigencia anterior de NetID/PANID no aparece en v2; la prohibición de broadcast sigue vigente como X2. Conservo la cadencia de X4 y los seis componentes de aceleración y giro de X5. Dejo TBR la redacción de X3 y no selecciono frecuencia, modulación, potencia, Sync Word ni direccionamiento. La ficha de interfaz explica los acuerdos que necesito con Edu; no constituye un ICD aprobado.

Análisis: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/docs/requisitos/v1-v2-groundstation-2026-10-19.md  
Ficha de pendientes: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/docs/interfaces/pendientes-groundstation-2026-10-19.md  
Cambio publicado: https://github.com/edulandoni/astra-cansat/commit/a1a7d383ed4498b540c0f7a12500a66f84bc3551

Verifiqué las fuentes importadas y enlaces locales; no hice ensayos RF ni cierro la selección de modo. La tarea continúa En curso. La metodología publicada se limita a groundstation y manejo de datos; no la impongo a otras áreas.

### 2026-10-19T21:03:37.146-0300 — comentario 10067

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-18?focusedCommentId=10067). Última edición informada: 2026-10-19T21:03:37.146-0300.

## 19/10/2026 — COMENTARIO 5 — ACTUALIZACIÓN de X2/X3 con respuestas del aula

Amplío el comentario 4 y los TBR anteriores con la respuesta oficial de Pablo González del 19/10: https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2963#p50093 y https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2960#p50090

Para X2 alcanza con paquetes con dirección de destino, definida por el equipo. El formato de telemetría lo definimos y justificamos nosotros. El inicio de misión lo comunica el CanSat al detectar separación real y se admite transmitir durante ascenso. La cuenta del aula no define por sí sola el TEAM_ID ni sus bits.

Esto reduce los TBR de interpretación, pero no selecciona LoRa/FSK, dirección, Sync Word, frecuencia, CRC ni estructura. Siguen pendientes el Radio Profile y contrato compartido. El filtrado no elimina interferencias ni acredita autenticación. También se aclara que no se permiten transmisores auxiliares ajenos al intercambio telemétrico del equipo; hay que considerar esa restricción al planear pruebas de campo.

No cambié firmware ni realicé RF. La tarea continúa En curso. Registro de fuentes, versión y pendientes: https://github.com/edulandoni/astra-cansat/blob/5f9d8c310ecbecc9e1b7d0cc8d29d5d43df7b406/ground-station/docs/aula/2026-10-19/revision-aula.md

## Historial de cambios de campos

### 2026-10-13T01:43:10.055-0300 — cambio 10075

Autoría original: Eduardo Landoni.

Campo: Rank.

Antes: (sin valor informado)

Después: Ranked higher

### 2026-10-13T01:56:03.266-0300 — cambio 10087

Autoría original: Eduardo Landoni.

Campo: assignee.

Antes: cristianponsone9

Después: Cristian Ponsone

### 2026-10-17T12:13:42.062-0300 — cambio 10114

Autoría original: Cristian Ponsone.

Campo: description.

Antes: h2. Objetivo

Determinar si el SX1276 puede satisfacer de forma defendible los requisitos CONAE X1–X7 y seleccionar el modo de operación RF a utilizar en el prototipo/PDR.

h2. Trabajo a realizar

* Revisar datasheet oficial Semtech SX1276.
* Comparar LoRa vs FSK/GFSK para: identificación de red, direccionamiento unicast, CRC, tasa de datos, robustez y facilidad de verificación.
* Mapear X1–X7 a funciones/configuración concreta del SX1276 y del protocolo ASTRA.
* Definir cómo se implementarán NetID/PANID equivalente y prohibición de broadcast.
* Identificar cualquier requisito que siga siendo TBR y preparar consulta a CONAE si fuera necesaria.

h2. Entregable

Matriz {{Requisito CONAE | Implementación SX1276 | Evidencia | Estado}} + recomendación de modo RF.

h2. Criterio de finalización

* X1–X7 evaluados uno por uno.
* La selección LoRa/FSK/GFSK está justificada con documentación oficial.
* NetID/PANID y unicast quedan técnicamente definidos o marcados TBR.
* Fuentes oficiales enlazadas.
* Resultado listo para incorporar a la PDR y al ICD de comunicaciones.

Después: h2. Objetivo

Evaluar SX1276 contra X1–X6 del anexo CONAE v2 y proponer el modo RF para revisión conjunta del ICD con Edu y Systems.

h2. Trabajo a realizar

* Revisar documentación oficial Semtech y comparar LoRa/FSK/GFSK: robustez, tasa, CRC, identificación, destino y verificación.
* Mapear banda X1, prohibición de broadcast X2, comienzo de misión X3 (TBR), tasa X4, contenido X5 y consulta batería/solar X6.
* Definir direccionamiento y aceptación de paquetes propios sin confundir filtrado de TEAM_ID con ausencia de broadcast o de interferencia.
* El NetID/PANID con número de equipo era X2 v1 y NO aparece en v2: conservarlo como antecedente; su implementación sólo será una decisión interna justificada si se adopta en el ICD.
* Preparar consulta sobre el comando automático de X3 y sobre cualquier documento separado de protocolo.
* No fijar frecuencia exacta, modo, potencia, Sync Word, destino o framing unilateralmente.

h2. Entregable

Matriz Requisito v2 | implementación candidata | evidencia | estado, con relación a los IDs v1 y recomendación de modo RF.

h2. Criterio de finalización

* X1–X6 evaluados con evidencia y pendientes identificados.
* Modo y destino sin broadcast justificados y acordados en ASTRA-19.
* X3 aclarado o registrado TBR con responsable.
* No se exige como obligación v2 el NetID/PANID retirado.
* Fuentes y configuración de ensayo permiten reproducir la evaluación.

h2. Referencia vigente y revisión

Anexo CONAE v2 publicado el 16/10/2026: [https://www.argentina.gob.ar/sites/default/files/2026/08/anexo_requerimientos_tecnicos_-_cansat_universitario_2026-2027_v2.pdf|https://www.argentina.gob.ar/sites/default/files/2026/08/anexo_requerimientos_tecnicos_-_cansat_universitario_2026-2027_v2.pdf|smart-link]

Informe de impacto v1 → v2: [https://docs.google.com/document/d/1WwZ83me8W0qA7T8eum6xSrYxVtpbYoT9OYq1Z0WPMNI/edit?usp=drivesdk|https://docs.google.com/document/d/1WwZ83me8W0qA7T8eum6xSrYxVtpbYoT9OYq1Z0WPMNI/edit?usp=drivesdk|smart-link]

Matriz completa y fuentes conservadas: [https://drive.google.com/drive/folders/16P_8tdACes23uirmR-koQlB5iE0oVhEf|https://drive.google.com/drive/folders/16P_8tdACes23uirmR-koQlB5iE0oVhEf|smart-link]

Esta actualización cambia la referencia de diseño; no acredita implementación ni ensayo físico. Se conservan responsable y estado. Presupuesto fuera de esta revisión.

Campo: summary.

Antes: COMMS — Verificar SX1276 contra X1–X7 y seleccionar modo RF

Después: COMMS — Verificar SX1276 contra X1–X6 v2 y seleccionar modo RF

### 2026-10-17T12:42:30.433-0300 — cambio 10119

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Backlog

Después: Por hacer

### 2026-10-17T12:43:16.883-0300 — cambio 10126

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Por hacer

Después: En curso

