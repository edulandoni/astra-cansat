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

### 2026-10-19T21:03:45.852-0300 — comentario 10071

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-24?focusedCommentId=10071). Última edición informada: 2026-10-19T21:03:45.852-0300.

## 19/10/2026 — COMENTARIO 3 — ACTUALIZACIÓN del acuerdo de formato y comandos

Las respuestas del 19/10 confirman que el formato lo define y justifica el equipo: https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2961#p50091 y https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2963#p50093

Los ítems 55 y 56 del PDR (diapositivas 58 y 59) requieren un ejemplo completo de telemetría y lista/formatos de comandos. La cita heredada a una Mission Guide no obliga a copiar ASCII22. Debemos acordar con vuelo versión, campos/unidades, origen/destino, integridad, sesión, tiempo, estados y respuestas verificables.

Registrar en ese acuerdo: calibración barométrica a cero, ajuste UTC de F3, consulta batería/solar de X6 y mensaje de inicio enviado por el CanSat al detectar separación. La respuesta permite telemetría en ascenso. No equiparo recepción de un comando con aceptación o ejecución. La mención de calibración de ángulos en la plantilla queda por aclarar.

No aprobé un ICD, no modifiqué protocol/ y no ejecuté interoperabilidad física. Conservo Por hacer para el ensayo de esta tarea; este comentario aporta requisitos de preparación. Fuentes y lagunas: https://github.com/edulandoni/astra-cansat/blob/5f9d8c310ecbecc9e1b7d0cc8d29d5d43df7b406/ground-station/docs/aula/2026-10-19/revision-aula.md

### 2026-10-20T12:08:08.922-0300 — comentario 10091

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-24?focusedCommentId=10091). Última edición informada: 2026-10-20T12:08:08.922-0300.

## 20/10/2026 — COMENTARIO 4 — Aclaración CONAE para el acuerdo de comandos con vuelo

La [respuesta oficial p50098](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2965#p50098), del 20/10 a las 08:28, permite enviar comandos para acciones específicas, justificando su uso y cumpliendo la misión primaria. Actualiza la consulta que estaba abierta en el corte anterior. Fuente y control en ASTRA-37; panorama priorizado en ASTRA-38.

Para nuestra interfaz necesito acordar con Edu qué acciones admite tierra y en qué fases, cuáles siguen siendo autónomas, cómo se identifica el destinatario y cómo distinguimos envío, recepción, rechazo y ejecución. También necesitamos comportamiento frente a repetición, reinicio y ausencia de respuesta. Un eco no demuestra actuación física. Esta es una lista de pendientes a coordinar, no decisiones de vuelo que haya tomado unilateralmente.

La aclaración previa sobre X3 sigue siendo distinta: el CanSat detecta separación real y transmite comienzo de misión; puede telemetrar durante ascenso. El permiso para acciones específicas desde tierra no convierte el comienzo de misión en una orden manual general.

[Informe al corte](https://drive.google.com/file/d/13hQj8Ckp6KJv3cu1L5xeCX3Rwx4_NbLe/view?usp=drivesdk) y [documentación publicada](https://github.com/edulandoni/astra-cansat/commit/9208b923e87ddc301a89951e6b362ccd861e0d93). No implementé comandos, modifiqué protocol/ o firmware ni ejecuté interoperabilidad en esta tarea. Mantengo su estado Por hacer: registrar una aclaración de entrada no equivale a haber iniciado el ensayo de ambos extremos.

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

