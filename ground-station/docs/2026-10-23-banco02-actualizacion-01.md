# 23/10/2026 — ACTUALIZACIÓN 01: banco resistente a fallos y USB bidireccional

Amplío la [prueba física v0.1](2026-10-23-prueba-usb-fisica-actualizacion-02.md), sin sustituir su sketch ni sus registros. Mi nueva línea experimental está en [banco-usb-v0.2](../banco-usb-v0.2/README.md). Esta entrada cierra el primer bloque de implementación y ensayos; no declara terminada toda la etapa.

Diarios: [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20), [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21), [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22), [ASTRA-34](https://astrateam2026.atlassian.net/browse/ASTRA-34). La propuesta de interfaz se documenta en ASTRA-24 y la investigación/antenas en ASTRA-35/25.

## Problema y decisión

Una pantalla nominal no demuestra que pueda conservar y explicar los datos ante fallos. Separé adquisición, control, estado, escritores y GUI. Cada destino y formato tiene cola acotada y estado propio. Recibido, validado, único, confirmado en archivo, pendiente y descartado tienen significados diferentes. Conservé bytes, diagnósticos y órdenes; un diagnóstico de arranque no consume la primera muestra ni se cuenta como telemetría.

Distingo sesión PC, arranque del emisor y ejecución de misión. Los valores anteriores dejan de ser actuales al cambiar contexto. En el banco identifico boot/run; ante un contador antiguo sin identidad suficiente dejo ambigüedad explícita. El emisor y la PC comparan resultados de escenarios mediante declaraciones oracle. No pretendo que dos algoritmos propios sean prueba independiente de física.

## Qué implementé

- Firmware nuevo con los cinco escenarios seleccionables por USB, RUN/STOP, cero de altitud ficticio, hora relativa a PC y consulta sintética de batería/solar. Ninguna orden acciona hardware externo. No habilité radio.
- Perfil `bench-usb-0.2`: control ASCII JSON con prefijo @BENCH y CR, separado de los 22 campos compatibles. No es el contrato de vuelo aprobado. Las órdenes tienen ID, estados y timeout sin reenvío automático; repetir una orden conocida no vuelve a ejecutarla.
- Escritores independientes raw/CSV, por destino, con reintentos y archivos nuevos después de una escritura incierta. Límite explícito: 600 eventos pendientes por escritor y detalle acotado de pérdidas. Una cola llena no significa conservación garantizada.
- Pantalla con origen, edades, contadores, confirmación por destino y seis gráficos. Giro mostrado en rad/s por conversión del perfil conocido, conservando °/s originales. Sin fix no invento posición. Un valor constante no declara un sensor averiado.
- Reproducción a velocidad original/acelerada, con salidas nuevas; recuperación offline desde JSONL o CSV con contexto, procedencia y bloqueo ante conflicto. No relleno datos ausentes.

## Ensayo físico inicial

Cargué el nuevo sketch en mi ESP32-D0WD-V3 por COM5 a 115200, conservando el respaldo privado de flash original. Compilación: Arduino CLI1.5.1, core3.3.12, DIO40MHz/4MB; 310956 bytes de programa y 25324 de variables. La escritura verificó sus cuatro bloques. La secuencia manual BOOT → EN/RST → soltar BOOT volvió a ser necesaria; no deduzco el modo de la luz.

Corrida real: 24/10/2026 02:02:26–02:13:36 UTC, equivalente a 23/10 23:02:26–23:13:36 ART. Son cinco misiones sintéticas por USB físico, no radio. Ejecuté calibración ficticia, hora PC, consulta de alimentación y cinco RUN. Repetí cada RUN ya conocido y las secuencias conservaron los contadores previstos, sin reiniciar por esa repetición.

| Escenario | Válidos únicos | Rechazados del segmento | Omisiones declaradas | Resultado |
|---|---:|---:|---:|---|
| NOMINAL | 131 | 0 | 0 | Coincide |
| PACKET_LOSS | 118 | 0 | 13 | Coincide |
| CORRUPTED_PACKET | 121 | 10 | 0 | Coincide |
| GPS_LOSS | 131 | 0 | 0 | 15 muestras sin fix, posición/hora retenidas |
| RESET lógico | 128 | 0 | 3 | Coincide; no reinicio físico |

En total confirmé 629 filas de telemetría y 2884 eventos en el diario, cero pendientes y cero descartes de escritor al cerrar. Cada CSV coincide con los paquetes de su segmento. NOMINAL: mediana de intervalo de llegada 1,0113 s; mínimo0,9792 y máximo1,0828 s. El ciclo del sketch agrega tiempo de emisión: la primera y última muestra abarcan132,573 s para130 intervalos. No presento esto como frecuencia exacta de1Hz ni medición de latencia RF; ajustar una agenda sin deriva sigue siendo una mejora por comprobar en otra carga.

Conservo [resultado original](../evidence/2026-10-23-banco02/usb-campaign-original-01.json): su campo rejected era acumulado entre casos. La [verificación posterior por segmento](../evidence/2026-10-23-banco02/usb-cinco-escenarios-01.json), reproducible con analyze.py, aclara que GPS_LOSS y RESET no agregaron rechazos. No edité el original para ocultarlo. El diario bruto original queda local, con huella publicada; los [cinco CSV sintéticos](../evidence/2026-10-23-banco02/usb-cinco-escenarios-01/segments/) se conservan sin cambios.

La campaña física empezó antes de las mejoras posteriores del handshake de reconexión, recuperación CSV e informe. No conservó snapshot exacto de todos los módulos Python de aquel proceso: no le atribuyo retrospectivamente la revisión final. La [campaña PC posterior](../evidence/2026-10-23-banco02/pc-campaign-original-01.json) guarda huellas, es acelerada y también compara los cinco escenarios; no la cuento como nueva prueba USB. La GUI USB posterior recibió otra misión nominal de131 muestras, observada en pantalla; sus pruebas físicas de reinicio siguen abiertas.

## Pruebas de software

Pasaron diez pruebas v0.2: fragmentación byte a byte y escenarios, aislamiento/reintento de escritor, desborde informado, contextos/GPS/conflictos, duplicados y respuestas tardías, ambigüedad antigua/SI, reloj congelado, reproducción y recuperación, control malformado y handshake tras pérdida del anuncio. La recuperación CSV/JSONL y la comparación entre ambas fuentes también quedaron verificadas. Pasaron las once pruebas de regresión v0.1, sin modificar sus fuentes.

El fallo de escritura es inyectado por software: no demuestra que una microSD sobreviva a extracción en caliente o que fsync garantice persistencia eléctrica. El ensayo de fragmentación extrema puede agotar deliberadamente el escritor bruto acotado; compara parser y pérdidas declaradas, no conservación ilimitada a cualquier tasa.

## Aceptación y pendientes al corte

| Criterio | Estado real |
|---|---|
| Cinco escenarios y contraste con emisor | Ejecutado por USB físico; ver tabla |
| Fragmentación/diagnósticos/colas/fallos de escritura | Ejecutado en software; arranque real observado |
| Duplicar RUN sin volver a ejecutar | Ejecutado en los cinco escenarios USB |
| Timeout, respuesta tardía y reinicio con orden pendiente | Software ejecutado; reinicio físico pendiente |
| Pulsar RST y desconectar/reconectar USB | Preparado; requiere ensayo físico dedicado |
| Reconstrucción limpia y conflicto bloqueado | Software ejecutado, originales conservados |
| C: + microSD en discos distintos | Pendiente de conectar e identificar soporte; no acreditado con dos carpetas |
| ≥2 horas reales USB con GUI y memoria medida | Instrumentado con gui_health; todavía no acreditado |
| Autonomía, RF, STM32, legibilidad al sol | Pendientes externos; no quedan cubiertos por USB |

Puedo afirmar que tengo un banco USB bidireccional con cinco fallos controlados y adquisición/archivo comparables, más mecanismos verificados en software para explicar pérdidas y conflictos. No puedo afirmar todavía cierre integral de esta etapa, persistencia frente a corte eléctrico, cumplimiento de RF o interoperabilidad con Edu. Mantengo tareas abiertas y continuaré cada resultado físico en una actualización nueva.
