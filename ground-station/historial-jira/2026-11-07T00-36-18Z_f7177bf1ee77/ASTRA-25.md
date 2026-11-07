# ASTRA-25 — COMMS — Realizar link budget preliminar y plan de ensayo RF 915 MHz

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-25)

Estado observado: En curso. Asignación: Cristian Ponsone. Creación: Eduardo Landoni.

## Descripción original consultada

## Objetivo

Cuantificar el margen esperado del enlace CanSat↔Ground Station y definir cómo se verificará experimentalmente antes de CDR/FRR.

## Trabajo a realizar

* Relevar potencia TX, sensibilidad RX, pérdidas de cable/conectores y ganancias de antena con fuentes oficiales.
* Calcular FSPL para distancias representativas del perfil de misión y un caso conservador.
* Definir margen de enlace preliminar.
* Considerar orientación/polarización, shadowing por estructura y pérdida por desalineación.
* Proponer escalera de ensayos LOS a distancias crecientes con registro de RSSI/SNR/packet loss.
* Identificar qué datos de antenas/módulos siguen TBD.

## Entregable

Link budget v0.1 + plan de ensayo RF.

## Criterio de finalización

* Todas las entradas del cálculo tienen fuente o están marcadas TBD.
* Se reporta margen de enlace y sensibilidad a pérdidas adicionales.
* Existe un plan de ensayo reproducible.
* Resultados listos para alimentar selección de antena definitiva y PDR/CDR.



## Comentarios conservados

### 2026-10-17T12:31:32.033-0300 — comentario 10028

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-25?focusedCommentId=10028). Última edición informada: 2026-10-17T12:31:32.033-0300.

## Bitácora 17/10/2026 — capacidad de enlace y redundancia como antecedentes de diseño

### Por qué se analizó

Necesitamos sostener telemetría a 1 Hz y permitir comandos sin que duplicados o recuperación de históricos ocupen todo el enlace. Antes de elegir modo/perfil calculamos tiempo de aire y memoria; no damos por probado un alcance por usar SX1276.

### Trabajo y resultados anteriores conservados

El cálculo de capacidad se contrastó en 2304 comparaciones de fórmulas con el driver de referencia usado en el análisis. Ejemplo hipotético LoRa, BW125 kHz, CR4/5, preámbulo 8, cabecera explícita, CRC: un payload de 200 bytes requiere 317,696 ms en SF7, 563,712 ms en SF8 y 1004,544 ms en SF9. Son resultados de ese conjunto de supuestos, no el Radio Profile elegido. En SF9 ese paquete ya supera un segundo antes de comandos/márgenes.

Con 200 B de datos y 24 B locales, dos minutos a 1 Hz ocupan 26 880 B y dos horas 1 612 800 B, antes de otros costos. Un ejemplo de recuperación con histórico de 208 B, comando de 23 B y margen total50 ms permite un histórico adicional por ventana de segundo en SF7; con paquete actual200 B no cabe bajo ese esquema SF8. Recuperación masiva compite con datos actuales: prioridad inferior y control de backlog por acordar.

### Qué cambia con v2 y qué falta

Al no incluir el anexo consultado un formato detallado, hay que cerrar en ICD payload máximo, envolvente/destino, integridad, respuestas y reintentos y recalcular. El programa de fórmulas no prueba propagación, antenas, potencia, sensibilidad del módulo instalado, interferencias ni pérdidas reales. Falta link budget trazable y escalera de ensayos LOS con RSSI/SNR/pérdidas según modo.

No se eligen SF, modulación, potencia ni frecuencia por estos ejemplos. La comparación LoRa/FSK/GFSK y aislamiento lógico se registra en ASTRA-18. Dos receptores o memorias sólo se justifican por la falla que cubren y sus dependencias comunes; no hay segunda estación física validada.

### Evidencia para el PDR

Código reproducible: https://github.com/edulandoni/astra-cansat/blob/docs/ground-station-continuidad/verification/ground-station-capacity-analysis.py  
Resultados: https://github.com/edulandoni/astra-cansat/blob/docs/ground-station-continuidad/verification/ground-station-capacity-analysis.json  
Modelo de redundancia: https://github.com/edulandoni/astra-cansat/blob/docs/ground-station-continuidad/verification/ground-station-redundancy-analysis.js  
Informe de fuentes/antecedentes e impacto actual: https://docs.google.com/document/d/1WwZ83me8W0qA7T8eum6xSrYxVtpbYoT9OYq1Z0WPMNI/edit  
Para usarlo en PDR presentar hipótesis, resultados teóricos y validación RF todavía pendiente.

### 2026-10-17T12:43:38.943-0300 — comentario 10035

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-25?focusedCommentId=10035). Última edición informada: 2026-10-17T12:43:38.943-0300.

## Bitácora 17/10/2026 — estado de trabajo y alcance

Paso esta tarea de Backlog a **Por hacer**.

Voy a preparar el link budget y el plan RF. Los cálculos previos de tiempo de aire y memoria son antecedentes útiles, pero todavía no constituyen el presupuesto de enlace con parámetros y antenas concretos.

Uso Backlog para ideas que todavía no asumimos; Por hacer para trabajo previsto sin iniciar; y En curso cuando ya estoy trabajando. La tarea sigue abierta hasta cumplir sus criterios y conservar la evidencia. En adelante gestiono únicamente tareas que creé o que están asignadas a mí; las dependencias con Edu y Rebe las documento desde mis propias tareas.

### 2026-10-19T19:28:29.251-0300 — comentario 10044

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-25?focusedCommentId=10044). Última edición informada: 2026-10-19T19:28:29.251-0300.

## 19/10/2026 — COMENTARIO 3 — Ubicación de antecedentes y límites del enlace

Dejé el mapa de trazabilidad de mi área y la referencia al trabajo anterior para que el análisis de enlace pueda reconstruirse desde Jira y GitHub. Conservo el PR histórico sin modificarlo; esta carga no recalcula ni aprueba un presupuesto de enlace.

Mapa: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/docs/trazabilidad-2026-10-19.md  
Estado: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/docs/estado-2026-10-19.md  
Antecedente: https://github.com/edulandoni/astra-cansat/pull/1  
Cambio publicado: https://github.com/edulandoni/astra-cansat/commit/a1a7d383ed4498b540c0f7a12500a66f84bc3551

Siguen pendientes parámetros RF acordados, modelos y datos de antenas, entradas respaldadas, margen calculado y ensayo reproducible con evidencia. Los resultados de software de esta carga no verifican alcance, sensibilidad ni potencia. Mantengo Por hacer para el entregable de esta tarea.

### 2026-10-19T21:03:47.923-0300 — comentario 10072

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-25?focusedCommentId=10072). Última edición informada: 2026-10-19T21:03:47.923-0300.

## 19/10/2026 — COMENTARIO 4 — ACTUALIZACIÓN del entregable de antena para PDR

La plantilla oficial fija para tierra comparación de al menos dos antenas con patrones (ítem 71, diapositiva 74), montaje portátil/de mesa (72/75) y selección justificada (73/76). El mapa conserva también las filas 148–150 del Scoresheet.

Los cálculos anteriores de tiempo de aire y memoria no cubren esos entregables ni prueban alcance. Siguen faltando modelos y patrones respaldados, montaje, Radio Profile acordado, entradas del presupuesto de enlace, márgenes y ensayos físicos. No seleccioné antena ni inventé ganancias.

La respuesta oficial anuncia cotas superiores a 500 m e inferiores a 1000 m y un documento del vector pendiente: es contexto preliminar, no una distancia operativa final garantizada. La limitación de transmisores auxiliares debe considerarse en el plan de campo.

Conservo Por hacer para el presupuesto de enlace y la campaña RF. La lectura del requisito no equivale a ejecutar su diseño. Informe y fuentes: https://github.com/edulandoni/astra-cansat/blob/5f9d8c310ecbecc9e1b7d0cc8d29d5d43df7b406/ground-station/docs/aula/2026-10-19/revision-aula.md

### 2026-10-23T23:28:37.778-0300 — comentario 10121

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-25?focusedCommentId=10121). Última edición informada: 2026-10-23T23:28:37.778-0300.

23/10/2026 — COMENTARIO 5 — ACTUALIZACIÓN COMENTARIO 4: comparación preliminar y link budget con entradas pendientes

Comparé Taoglas OMB.915.B05F21 y Digi A09-Y11NF con fuentes del fabricante, montaje, patrón disponible, ganancia y riesgos de uso. No seleccioné una antena final. Taoglas declara902–928MHz y5,9dBi pico; Digi identifica Yagi900MHz11,1dBi y N-hembra. El PDRITBA difiere en conector: lo dejoTBR. Observé el patrón de Yagi reproducido en su PDR, pero falta confirmar la curva del modelo suministrado. El PDFTaoglas se leyó en texto por buscador; su descarga directa dio403 y no afirmo inspección de sus curvas. Los intentosL-com entregaronHTML, noPDF válidos.

Calculé espacio libre con ITU-R P.525-5 para un barrido ilustrativo915/928MHz y500/1000m oblicuos:85,656–91,799dB. No son frecuencia elegida, trayectoria nominal ni alcance acreditado. Dejé fórmula completa de potencia recibida y margen, con potencia, antena de vuelo/orientación, cables, sensibilidad del modo, polarización, distancia máxima y margen objetivo comoTBD. La diferencia de ganancias de pico no asegura ventaja durante toda la misión.

Preparé plan de comparación RF con mismas condiciones, orientación/movimiento, datosTX/RX/guardados, comandos y tiempos. No configuréRF ni trasladé autorizaciones de otros países. Falta perfil compartido y hardware real para cerrar el presupuesto y probarlo.

Como ya inicié cálculo y entregable, paso de Por hacer a En curso; quedan criterios de cierre pendientes.

[Comparación, cuentas, fuentes y plan](https://github.com/edulandoni/astra-cansat/blob/fc6e6d22b46104127b1a83c973ac86c4a22b59a9/ground-station/docs/interfaces/2026-10-23-antenas-y-link-budget-preliminar.md) · [Propuesta de interfaz](https://github.com/edulandoni/astra-cansat/blob/fc6e6d22b46104127b1a83c973ac86c4a22b59a9/ground-station/docs/interfaces/2026-10-23-propuesta-banco-y-vuelo.md) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/fc6e6d22b46104127b1a83c973ac86c4a22b59a9). Conservo el comentario4 y su referencia a la plantilla.

### 2026-10-23T23:37:16.918-0300 — comentario 10127

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-25?focusedCommentId=10127). Última edición informada: 2026-10-23T23:37:16.918-0300.

23/10/2026 — COMENTARIO 6 — ACTUALIZACIÓN COMENTARIO 5: airtime reproducible del payload actual

Agregué un calculador offline de tiempo de aireLoRa con fórmulaSemtechSX1276rev4p31 y entradas explícitas. Medí121–134bytes en629tramasUSB conservadas, incluyendoCR. No son todavía el payloadRF acordado ni sus sobrecargas.

Para134bytes, preámbulo8, encabezado explícito, CRC yCR4/5: SF7/BW125kHz da0,220416s; SF9 da0,697344s; SF12 da5,087232s. Son hipótesis de comparación, no perfil seleccionado. SF12 no entra a1Hz; los otros casos aún necesitan espacio para órdenes, respuestas y guardas. FSK/GFSK requieren otro modelo. No fijo parámetros por este barrido.

Pasaron dos pruebas numéricas/restricciones, incluyendoDE requerido para símbolo>16ms, límite255bytes y encabezado implícito enSF6. El cálculo no mide radio. La referencia−139dBm del módulo depende justamente deSF12/BW125kHz: no puedo combinarla con un airtime rápido como si fueran el mismo perfil. También registré la limitación+20dBm de la copiaSemtechrev4 comoTBR contra documento vigente/placa real, distinta de normativa local.

El presupuesto sigue con entradasTBD; la identificación NiceRF/variante es informada porEdu y su pinout aún no coincide con la foto. Mantengo En curso y no declaro margen/alcance probado.

[Informe, fuentes y pendientes](https://github.com/edulandoni/astra-cansat/blob/bbfb056dd58998201dfe7927007a7542e7f6f030/ground-station/docs/interfaces/2026-10-23-modulo-radio-y-comandos-actualizacion-02.md) · [CopiaDrive verificada](https://drive.google.com/file/d/1EmtZu0pjrRJaI8IdB4p65ZEOzPC0QTGv/view?usp=drivesdk) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/bbfb056dd58998201dfe7927007a7542e7f6f030). Conservo todas las entradas anteriores.

### 2026-10-24T00:57:11.485-0300 — comentario 10144

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-25?focusedCommentId=10144). Última edición informada: 2026-10-24T00:57:11.485-0300.

24/10/2026 — COMENTARIO 7 — Capacidad temporal y máxima potencia

Actualizo la observación de la revisión 4 del comentario anterior: pude leer portada y página 84 de la hoja Semtech revisión 7, mayo de 2020, alojada por SparkFun. Sigue figurando el límite de 1 % de tiempo de transmisión a +20 dBm bajo las condiciones especificadas. Registré procedencia y SHA256; el enlace directo del fabricante no dio un PDF legible y no comprobé igualdad binaria con ese servidor. No afirmo haber auditado las 132 páginas o todas las erratas.

Repetí el cálculo offline con 134 bytes ilustrativos del banco y distintas hipótesis explícitas. Por ejemplo, SF6/BW500kHz/encabezado implícito da 31,392 ms: uno por segundo ocupa 3,1392 % antes de ACK, órdenes o guardas. SF12/BW125kHz no cabe siquiera en un segundo. Son ejemplos para discutir el perfil conjunto, no una selección de parámetros ni una demostración de imposibilidad de todo perfil.

Necesito acordar con Edu encuadre máximo, modulación/tasa, potencia y confirmaciones y verificar por separado restricciones aplicables y variante física. No supongo que la leyenda 100 mW permita transmitir continuamente ni uso sensibilidad extrema genérica para cerrar el enlace. No configuré RF ni cambié el protocolo compartido; integración y ensayos de radio siguen pendientes.

[Informe y cálculos reproducibles](https://github.com/edulandoni/astra-cansat/blob/cc4075ffbf28b259b30c99014396d9709bca429f/ground-station/docs/interfaces/2026-10-24-radio-potencia-y-airtime-actualizacion-03.md) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/cc4075ffbf28b259b30c99014396d9709bca429f) · [Copia Drive](https://drive.google.com/file/d/1CF6to_i1Z9hk2XQjHXkvRJWkqUhLIsOb/view?usp=drivesdk). Mantengo la entrada previa y los pendientes externos; esta revisión no acredita enlace físico.

### 2026-10-24T03:59:14.550-0300 — comentario 10163

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-25?focusedCommentId=10163). Última edición informada: 2026-10-24T03:59:14.550-0300.

24/10/2026 — COMENTARIO 8 — ACTUALIZACIÓN: Presupuesto de enlace calculable sin rellenar incógnitas

Agregué una herramienta que exige valores y fuentes explícitos. Los once datos del caso ASTRA siguen como TBD y el resultado real de margen permanece desconocido: no sustituyo incógnitas por cero.

Validé por separado un ejemplo puramente ilustrativo de 915 MHz a 1 km: pérdida de espacio libre 91,676 dB, potencia recibida −83,676 dBm y margen 26,324 dB con los supuestos detallados en el informe. Estos números no son una predicción para nuestro equipo. El cálculo referencia ITU-R P.525-5 y permite explorar pérdidas adicionales. Pasaron tres pruebas nuevas de presupuesto y las dos existentes de tiempo en aire.

Preparé un recorrido propuesto de ensayos de mesa y línea de vista, con registros de emisión, recepción, guardado y condiciones. RSSI/SNR dependen del modo disponible; una demora unidireccional exige relojes sincronizados, por lo que no la infiero de un intercambio sin esa condición.

Mantengo abierta la tarea: faltan confirmar perfil, sensibilidad aplicable, antenas, pérdidas, distancia y margen requerido. No seleccioné parámetros de transmisión.

[Propuesta, cálculo y pruebas en GitHub](https://github.com/edulandoni/astra-cansat/blob/9735087c1074754895273c4109553f5b350c7faf/ground-station/docs/interfaces/2026-10-24-enlace-destinos-y-revision.md)
[Copia verificada en Drive](https://drive.google.com/file/d/1X9307Zgf2K0nldBgBXXh91KqPXExgTjZ/view)

## Historial de cambios de campos

### 2026-10-13T01:53:22.576-0300 — cambio 10081

Autoría original: Eduardo Landoni.

Campo: assignee.

Antes: cristianponsone9

Después: Cristian Ponsone

### 2026-10-13T01:54:44.171-0300 — cambio 10083

Autoría original: Eduardo Landoni.

Campo: Rank.

Antes: (sin valor informado)

Después: Ranked higher

### 2026-10-17T12:42:44.849-0300 — cambio 10125

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Backlog

Después: Por hacer

### 2026-10-23T23:28:39.847-0300 — cambio 10149

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Por hacer

Después: En curso

