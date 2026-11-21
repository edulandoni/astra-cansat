# ASTRA-23 — COMMS — Integrar SX1276 con ESP32 Ground Radio

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-23)

Estado observado: Por hacer. Asignación: Cristian Ponsone. Creación: Eduardo Landoni.

## Descripción original consultada

## Objetivo

Integrar el módulo SX1276 con el ESP32 de Ground Station y convertirlo en un gateway RF↔USB conforme al Radio Profile/ICD aprobado.

## Trabajo a realizar

* Cablear SPI, RESET e IRQ/DIO necesarios.
* Implementar inicialización y configuración del SX1276 desde parámetros centralizados.
* Aplicar frecuencia, modulación, sync/network ID, addressing, CRC, potencia y demás parámetros del ICD.
* Recibir telemetría RF y reenviarla a la notebook sin modificar el contenido del paquete.
* Recibir telecomandos desde la notebook y transmitirlos al CanSat.
* Reportar errores de radio y, cuando sea posible, métricas como RSSI/SNR.

## Entregable

Firmware `ASTRA_GroundRadio v0.1` + esquema de conexiones ESP32↔SX1276.

## Criterio de finalización

* RX y TX bidireccional demostrados en banco.
* Configuración coincide exactamente con el ICD vigente.
* No se utiliza broadcast.
* El gateway puede operar de forma continua sin resets durante al menos 2 h de ensayo de banco.
* La aplicación de PC no requiere cambios en parser/GUI al pasar de simulador USB a RF.



## Comentarios conservados

### 2026-10-17T12:15:03.037-0300 — comentario 10013

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-23?focusedCommentId=10013). Última edición informada: 2026-10-17T12:15:03.037-0300.

## Trazabilidad RF v2 — 17/10/2026

Actualizar referencias a X1–X6: broadcast es X2; tasa 1 Hz X4; contenido X5; batería/solar X6; X3 comienzo de misión requiere aclaración. NetID/PANID con número de equipo ya no aparece como obligación en v2.

Mantener dependencia del Radio Profile/ICD compartido ASTRA-18/19. No hay parámetros RF elegidos por esta auditoría. Destino sin broadcast, CRC, comandos/respuestas y payload versionado se prueban con ambos extremos en ASTRA-24; filtrado de TEAM_ID no prueba ausencia de broadcast ni inmunidad a interferencias. La estimación de tiempo de aire ASTRA-25 debe recalcularse con el paquete máximo y sobrecargas acordados.

Informe: https://docs.google.com/document/d/1WwZ83me8W0qA7T8eum6xSrYxVtpbYoT9OYq1Z0WPMNI/edit?usp=drivesdk  
Fuentes: https://drive.google.com/drive/folders/16P_8tdACes23uirmR-koQlB5iE0oVhEf

### 2026-10-17T12:43:35.005-0300 — comentario 10033

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-23?focusedCommentId=10033). Última edición informada: 2026-10-17T12:43:35.005-0300.

## Bitácora 17/10/2026 — estado de trabajo y alcance

Paso esta tarea de Backlog a **Por hacer**.

Voy a integrar SX1276 con el ESP32 cuando identifiquemos el módulo y cerremos el Radio Profile/ICD. Es trabajo previsto, todavía sin cableado ni integración RF realizados.

Uso Backlog para ideas que todavía no asumimos; Por hacer para trabajo previsto sin iniciar; y En curso cuando ya estoy trabajando. La tarea sigue abierta hasta cumplir sus criterios y conservar la evidencia. En adelante gestiono únicamente tareas que creé o que están asignadas a mí; las dependencias con Edu y Rebe las documento desde mis propias tareas.

### 2026-10-19T19:28:24.996-0300 — comentario 10042

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-23?focusedCommentId=10042). Última edición informada: 2026-10-19T19:28:24.996-0300.

## 19/10/2026 — COMENTARIO 3 — Referencias de tierra para la integración futura

Dejé publicada la arquitectura del banco USB y sus límites como referencia para la futura integración del gateway. La importación no implementa el SX1276 ni configura RF.

Guía del banco: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/banco-usb-v0.1/README.md  
Necesidades de interfaz de tierra: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/docs/interfaces/pendientes-groundstation-2026-10-19.md  
Cambio publicado: https://github.com/edulandoni/astra-cansat/commit/a1a7d383ed4498b540c0f7a12500a66f84bc3551

Conservo la separación de adquisición, parser, almacenamiento y GUI como objetivo de integración. Todavía debo acordar el Radio Profile, identificar la placa y verificar cableado, alimentación y comunicación física. No probé radio ni antena en esta carga. Mantengo la tarea Por hacer: documentar dependencias no significa haber iniciado la integración física.

## Historial de cambios de campos

### 2026-10-13T01:43:11.687-0300 — cambio 10080

Autoría original: Eduardo Landoni.

Campo: Rank.

Antes: (sin valor informado)

Después: Ranked higher

### 2026-10-13T01:55:56.632-0300 — cambio 10085

Autoría original: Cristian Ponsone.

Campo: assignee.

Antes: cristianponsone9

Después: Cristian Ponsone

### 2026-10-17T12:42:39.952-0300 — cambio 10123

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Backlog

Después: Por hacer

