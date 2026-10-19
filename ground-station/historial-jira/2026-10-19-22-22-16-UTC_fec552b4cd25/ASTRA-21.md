# ASTRA-21 — GND — Implementar receptor serial, parser y logging CSV v0.1

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-21)

Estado observado: En curso. Asignación: Cristian Ponsone. Creación: Eduardo Landoni.

## Descripción original consultada

## Objetivo

Crear la capa de adquisición de la Ground Station independiente de la GUI y del medio RF.

## Trabajo a realizar

* Abrir/reconectar puerto serie de forma robusta.
* Recibir líneas ASCII completas y validar framing.
* Parsear todos los campos CONAE.
* Rechazar/registrar paquetes malformados sin bloquear la aplicación.
* Calcular paquetes recibidos y perdidos usando PACKET_COUNT.
* Registrar telemetría en `Flight_<TEAM_ID>.csv` con encabezados correctos.
* Diseñar la capa para que posteriormente la fuente USB pueda reemplazarse por el gateway SX1276 sin modificar parser/GUI.

## Entregable

Módulo de ingestión/parsing/logging v0.1 + CSV generado desde el simulador ESP32.

## Criterio de finalización

* Procesa una misión simulada completa sin pérdida por software.
* Detecta saltos de PACKET_COUNT.
* Tolera líneas corruptas y reconexión del puerto.
* Genera CSV válido y legible por Excel.
* La lógica de parsing está desacoplada de la presentación gráfica.



## Comentarios conservados

### 2026-10-17T12:14:54.870-0300 — comentario 10009

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10009). Última edición informada: 2026-10-17T12:14:54.870-0300.

## Revisión de adquisición y CSV frente a v2 — 17/10/2026

El banco Python separa framer/parser, adquisición, CSV/registro bruto y GUI. Tiene reconexión serie programada y copia de CSV configurable. G2 sigue vigente. Flight\_<TEAM_ID>.csv, CR y las 22 columnas se conservan como perfil heredado v1, no formato oficial v2 confirmado.

Falta comprobar puerto/reconexión físicos, dos horas, segundo disco independiente, disco lleno y desconexión del respaldo. Los fallos de CSV se anuncian sin recuperación automática; un fallo del registro bruto puede detener adquisición. Definir política de degradación y recuperación. Acordar identificación de sesión, RX exitosos/únicos/duplicados, límites de pérdidas observables y tratamiento de GPS ausente/antiguo. Los opcionales todavía se rechazan en este adaptador hasta acordar encabezados/esquema.

No eliminar el filtrado de equipo por retirarse NetID/PANID: son capas diferentes.  
Informe: https://docs.google.com/document/d/1WwZ83me8W0qA7T8eum6xSrYxVtpbYoT9OYq1Z0WPMNI/edit?usp=drivesdk  
Fuentes y banco: https://drive.google.com/drive/folders/16P_8tdACes23uirmR-koQlB5iE0oVhEf

### 2026-10-17T12:31:21.802-0300 — comentario 10023

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10023). Última edición informada: 2026-10-17T12:31:21.802-0300.

## Bitácora 17/10/2026 — decisiones de recepción y registro del banco

### Motivo y resultado esperado

Necesitamos conservar datos aunque la interfaz se demore y distinguir errores de enlace, de formato y de almacenamiento. El prototipo v04 exportaba manualmente y guardaba en memoria; el banco Python agrega adquisición y escritura continua separadas de la presentación. La intención es cubrir G2/G14 y preparar el cambio de USB simulado a USB de gateway sin rehacer parser/GUI.

### Decisiones implementadas

* Framer CR acotado a 2048 bytes; una trama excesiva se descarta hasta el próximo CR para recuperar sincronización. El contrato ASCII/CR es heredado de v1 y pendiente del ICD.
* Validación de número/campos/modo/estado/horas/coordenadas y rechazo de datos no finitos. No equivale a CRC ni detecta toda alteración numérica plausible.
* Sesión nueva por ejecución y Flight_1000.csv con columnas del perfil heredado; se preservan versiones y no se sobrescribe una misión anterior.
* reception.jsonl registra recepciones aceptadas, rechazos y desconexiones; los bytes inválidos se guardan en hexadecimal.
* CSV de registros válidos únicos. Las recepciones duplicadas siguen en el registro bruto. Un paquete atrasado puede completar un hueco sin reemplazar el dato actual en pantalla.
* Contadores separados de recepciones válidas, registros únicos, duplicados y huecos entre contadores observados. No se inventan pérdidas antes del primer paquete ni después del último. Retrocesos se avisan como ambiguos ante reset/atraso/duplicado.
* Worker separado de GUI y cola de presentación acotada. Si ésta se llena, se descarta una actualización antigua de pantalla; el CSV no se descarta por esa causa.
* Reconexión serial programada cada dos segundos y framer nuevo al reconectar para no unir fragmentos de conexiones distintas.
* CSV con flush/fsync y segunda copia configurable mediante --backup; dos directorios del mismo disco no prueban respaldo independiente.

### Resultados y límites

Los nueve tests de software incluyen fragmentación, tramas inválidas, límites de buffer, duplicados/atrasados y comparación de ambos CSV en escenarios sintéticos. Falta reconexión con cable/puerto real, disco lleno, desconexión de respaldo, dos horas y corte de energía.

Un fallo del log bruto puede detener la adquisición; los errores CSV se anuncian sin reintento/reconstrucción automática. Falta diseñar operación degradada y recuperación. El gateway ESP32 todavía no tiene archivo independiente ni cola durable. GPS ausente/frescura y opcionales necesitan contrato; la adquisición actual rechaza extensiones sin esquema de encabezados acordado.

### Qué sigue y qué sirve para PDR

Definir política de fallos por destino, identidad de sesión y conteos, y ensayar PC/USB/discos antes de reclamar robustez operativa. El PDR puede mostrar separación de módulos, formato de evidencia y casos sintéticos; la redundancia física sigue como plan.  
Código y logs: https://drive.google.com/file/d/1dOL2imloQJ7vsTKhMbexEt3YG8NyAUSK/view  
Informe y matriz de migración: https://docs.google.com/document/d/1WwZ83me8W0qA7T8eum6xSrYxVtpbYoT9OYq1Z0WPMNI/edit

### 2026-10-17T12:43:30.339-0300 — comentario 10031

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10031). Última edición informada: 2026-10-17T12:43:30.339-0300.

## Bitácora 17/10/2026 — estado de trabajo y alcance

Paso esta tarea de Backlog a **En curso**.

Ya implementé recepción, parser, contadores y registro CSV en el banco. Me faltan reconexión física, fallos de disco, respaldo independiente y pruebas prolongadas.

Uso Backlog para ideas que todavía no asumimos; Por hacer para trabajo previsto sin iniciar; y En curso cuando ya estoy trabajando. La tarea sigue abierta hasta cumplir sus criterios y conservar la evidencia. En adelante gestiono únicamente tareas que creé o que están asignadas a mí; las dependencias con Edu y Rebe las documento desde mis propias tareas.

## Historial de cambios de campos

### 2026-10-13T01:43:11.015-0300 — cambio 10078

Autoría original: Eduardo Landoni.

Campo: Rank.

Antes: (sin valor informado)

Después: Ranked higher

### 2026-10-13T01:56:07.402-0300 — cambio 10088

Autoría original: Cristian Ponsone.

Campo: assignee.

Antes: cristianponsone9

Después: Cristian Ponsone

### 2026-10-17T12:42:35.357-0300 — cambio 10121

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Backlog

Después: Por hacer

### 2026-10-17T12:43:21.528-0300 — cambio 10128

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Por hacer

Después: En curso

