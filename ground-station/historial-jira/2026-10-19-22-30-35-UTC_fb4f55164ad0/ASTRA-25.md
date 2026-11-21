# ASTRA-25 — COMMS — Realizar link budget preliminar y plan de ensayo RF 915 MHz

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-25)

Estado observado: Por hacer. Asignación: Cristian Ponsone. Creación: Eduardo Landoni.

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

