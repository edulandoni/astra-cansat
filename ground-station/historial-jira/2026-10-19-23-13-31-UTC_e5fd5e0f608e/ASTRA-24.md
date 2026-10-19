# ASTRA-24 — COMMS — Ejecutar prueba de interoperabilidad STM32 ↔ ESP32/SX1276

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-24)

Estado observado: Por hacer. Asignación: Cristian Ponsone. Creación: Eduardo Landoni.

## Descripción original consultada

## Objetivo

Demostrar que los dos extremos desarrollados por separado interoperan usando exclusivamente la baseline del ICD de comunicaciones.

## Trabajo a realizar

* Configurar Black Pill + SX1276 con el mismo Radio Profile que Ground Station.
* Ejecutar telemetría STM32→ESP32 y telecomandos ESP32→STM32.
* Verificar formato, TEAM_ID, packet count, CRC, addressing/unicast y CMD_ECHO.
* Probar reinicio de uno de los extremos y recuperación del enlace.
* Registrar incompatibilidades como issue y corregir el ICD antes que aplicar parches locales divergentes.

## Responsabilidades

Cristian lidera el ensayo de interfaz/Ground Segment. Edu implementa y corrige el extremo STM32/Flight Software. Cambios compartidos requieren actualización del ICD.

## Entregable

Acta de prueba de interoperabilidad v0.1 con configuración utilizada, resultados, fallos y evidencias.

## Criterio de finalización

* Telemetría válida recibida durante una misión simulada completa.
* Telecomandos obligatorios de prueba cruzan el enlace y generan respuesta/CMD_ECHO.
* Se demuestra recuperación tras al menos un reset controlado.
* No existen parámetros RF hardcodeados de forma contradictoria entre ambos firmwares.



## Comentarios conservados

### 2026-10-17T12:43:37.008-0300 — comentario 10034

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-24?focusedCommentId=10034). Última edición informada: 2026-10-17T12:43:37.008-0300.

## Bitácora 17/10/2026 — estado de trabajo y alcance

Paso esta tarea de Backlog a **Por hacer**.

Voy a realizar con Edu la prueba de interoperabilidad entre ambos extremos. Depende del ICD y de los firmwares y módulos integrados; todavía no iniciamos ese ensayo.

Uso Backlog para ideas que todavía no asumimos; Por hacer para trabajo previsto sin iniciar; y En curso cuando ya estoy trabajando. La tarea sigue abierta hasta cumplir sus criterios y conservar la evidencia. En adelante gestiono únicamente tareas que creé o que están asignadas a mí; las dependencias con Edu y Rebe las documento desde mis propias tareas.

### 2026-10-19T19:28:27.116-0300 — comentario 10043

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-24?focusedCommentId=10043). Última edición informada: 2026-10-19T19:28:27.116-0300.

## 19/10/2026 — COMENTARIO 2 — Explicación de la interfaz pendiente con vuelo

Dejé una ficha de groundstation para entender qué necesitamos acordar entre ambos extremos: campos y unidades, identificación, validez de datos, CRC, comandos, reinicios y parámetros de radio. Explico el ICD como una ficha de acuerdo que permite interpretar igual cada mensaje.

Ficha: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/docs/interfaces/pendientes-groundstation-2026-10-19.md  
Cambio publicado: https://github.com/edulandoni/astra-cansat/commit/a1a7d383ed4498b540c0f7a12500a66f84bc3551

No es un contrato aprobado ni fija decisiones de Edu. No modifiqué protocol/ ni firmware de vuelo. No ejecuté interoperabilidad STM32↔ESP32/SX1276; sigo dependiendo del acuerdo compartido y de disponer de ambos extremos para el ensayo. La tarea continúa Por hacer.

## Historial de cambios de campos

### 2026-10-13T01:54:43.792-0300 — cambio 10082

Autoría original: Eduardo Landoni.

Campo: Rank.

Antes: (sin valor informado)

Después: Ranked higher

### 2026-10-13T01:55:51.090-0300 — cambio 10084

Autoría original: Cristian Ponsone.

Campo: assignee.

Antes: cristianponsone9

Después: Cristian Ponsone

### 2026-10-17T12:42:42.448-0300 — cambio 10124

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Backlog

Después: Por hacer

