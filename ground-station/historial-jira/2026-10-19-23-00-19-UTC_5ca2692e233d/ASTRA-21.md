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

### 2026-10-19T19:28:20.617-0300 — comentario 10040

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10040). Última edición informada: 2026-10-19T19:28:20.617-0300.

## 19/10/2026 — COMENTARIO 4 — Parser, CSV y respaldo trazable en GitHub

Publiqué acquisition.py, protocol.py y storage.py como parte del banco USB conservado del 17/10. La separación permite revisar adquisición, validación, contadores y almacenamiento antes de integrar radio. No alteré esas fuentes durante la importación.

Las nueve pruebas automatizadas del banco aprobaron, incluidas las variantes sintéticas, huecos, duplicados, rechazo y recuperación, retención GPS y sesiones sin sobrescritura. La evidencia anterior conserva CSV y recepciones ficticias del 17/10. No la presento como vuelo real ni como verificación de USB físico o de dos soportes independientes.

Código y ejecución: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/banco-usb-v0.1/README.md  
Evidencia: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/docs/pruebas-2026-10-19.md  
Historial de Jira: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/historial-jira/README.md  
Respaldo: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/docs/respaldo-jira-2026-10-19.md  
Cambio publicado: https://github.com/edulandoni/astra-cansat/commit/a1a7d383ed4498b540c0f7a12500a66f84bc3551

Agregué un guardado de capturas que conserva las anteriores y rechaza lecturas incompletas o ajenas. Su prueba final aprobó cuatro casos; no guarda credenciales en el repositorio. El respaldo diario de este chat quedó activo a las 21:00 de Argentina, sujeto a la disponibilidad de la aplicación y sus conexiones.

Pendientes: reconexión física, fallos reales de almacenamiento y continuidad, doble soporte físico y esquema de datos acordado con vuelo. La tarea continúa En curso.

### 2026-10-19T19:32:31.128-0300 — comentario 10047

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10047). Última edición informada: 2026-10-19T19:32:31.128-0300.

## 19/10/2026 — ACTUALIZACIÓN COMENTARIO 4 (del 19/10/2026) — COMENTARIO 5 — Control del respaldo

Original: https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10040

La comprobación real del cierre mostró que Jira devuelve la etiqueta del respaldo con escapes. El control inicial creó una captura adicional del propio aviso. Conservo esa captura y la de la corrección; no borro registros para ocultar el problema.

Corregí la detección para reconocer la etiqueta normal y escapada, y para comparar capturas antiguas con la regla actual sin modificar sus manifest. El control posterior con la lectura real devolvió «Sin cambios» y no creó otra carpeta.

La batería actual del historial aprueba cinco pruebas, incluidas la etiqueta escapada y la compatibilidad con huellas anteriores. Se mantienen aprobadas las nueve pruebas del banco y las trece de lógica v04. No se realizaron nuevos ensayos de hardware.

Actualización documentada: https://github.com/edulandoni/astra-cansat/blob/groundstation/ground-station/docs/historial/2026-10-19-actualizacion-etiqueta-jira.md  
Corrección publicada: https://github.com/edulandoni/astra-cansat/commit/4fe04e377c9a786dc15dec4e406010c534b3a1bc  
Capturas conservadas: https://github.com/edulandoni/astra-cansat/tree/groundstation/ground-station/historial-jira

Mantengo la programación diaria y el estado En curso. Esta corrección actualiza el resultado anterior; no sustituye las entradas originales.

### 2026-10-19T19:59:51.410-0300 — comentario 10049

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10049). Última edición informada: 2026-10-19T19:59:51.410-0300.

## 19/10/2026 — COMENTARIO 6 — Investigación de innovación y prevención sin hardware

### Motivo y objetivo

Investigué qué puedo mejorar en groundstation y manejo de datos antes de conectar el microcontrolador. Busco anticipar fallas y elegir una contribución comprobable para el PDR, distinguiendo formato correcto de dato confiable. Mantengo separadas las ideas de lo ya implementado.

### Qué hice y con qué configuración

Revisé el banco publicado y fuentes técnicas de NASA Ames y pySerial. Agregué un experimento de Python independiente del banco, con diez sondeos de datos y fallas controladas. No modifiqué las fuentes del banco, el protocolo compartido ni otras áreas. Usé TEAM_ID 1000 ficticio, datos sintéticos y directorios temporales. El fallo de registro se inyecta como excepción controlada: no llené el disco ni desconecté dispositivos.

### Resultados observados

El control nominal aceptó 131 muestras y el identificador ajeno se rechazó. El parser aceptó una altura alterada a 3000 m, temperatura 999 °C y giro 9999 °/s: son números finitos con estructura válida, no umbrales operativos. También aceptó 20 alturas congeladas mientras cambiaba la presión y 10 paquetes con hora de misión congelada y contador creciente.

Un mismo contador con contenido distinto se contó como duplicado sin aviso específico de conflicto; ambos mensajes quedaron en raw. Al modelar un reinicio de contador hubo aviso de ambigüedad, pero latest conservó el contador alto anterior aunque siguieron entrando datos. Una excepción sintética al guardar raw terminó el worker con ERROR.

### Propuesta y cómo comprobarla

Propongo evaluar un indicador explicable de datos recientes, retenidos, sospechosos o ausentes, junto con una campaña reproducible de fallas. Mediría tiempo de aviso, anomalías omitidas, falsas alarmas y antigüedad del dato mostrado. Primero priorizaría la continuidad del registro y la identificación de datos actuales. También documenté simulador de misión coherente, pruebas de comandos entre programas de PC, entrenamiento del operador y análisis futuro de despliegues.

### Límites y pendientes

No implementé el monitor ni una corrección de almacenamiento en la aplicación de operación. Diez sondeos no estiman probabilidad real de fallas ni certifican requisitos. No probé hardware, USB físico o RF. No fijé umbrales, formato nuevo ni parámetros compartidos. Presión y altura barométrica pueden venir del mismo sensor y no son redundancia independiente. No afirmo novedad mundial ni reconocimiento de innovación por CONAE.

La investigación tiene antecedentes técnicos: el aporte por demostrar sería nuestra implementación y evaluación adaptada a la misión. Mantengo la tarea En curso. Las implementaciones propuestas siguen pendientes de selección; no creé tareas nuevas por mencionar ideas.

### Evidencia y fuentes

Informe: https://github.com/edulandoni/astra-cansat/blob/groundstation/ground-station/docs/investigacion/2026-10-19-innovacion-y-prevencion.md  
Experimento reproducible: https://github.com/edulandoni/astra-cansat/tree/groundstation/ground-station/experiments/2026-10-19-prevencion  
Resultados: https://github.com/edulandoni/astra-cansat/tree/groundstation/ground-station/evidence/2026-10-19-investigacion-prevencion  
Cambio publicado: https://github.com/edulandoni/astra-cansat/commit/82a80614e186a5f8b50559eea8a293503154f02d  
NASA Ames: https://ntrs.nasa.gov/citations/20090037065  
pySerial: https://pyserial.readthedocs.io/en/latest/url_handlers.html

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

