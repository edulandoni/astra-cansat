# ASTRA-20 — GND — Implementar simulador de vuelo CONAE en ESP32 por USB

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-20)

Estado observado: En curso. Asignación: Cristian Ponsone. Creación: Eduardo Landoni.

## Descripción original consultada

## Objetivo

Usar el ESP32 de la Ground Station como generador de telemetría de vuelo ficticia para desarrollar la aplicación de PC antes de integrar el enlace RF.

## Trabajo a realizar

* Generar a 1 Hz paquetes ASCII con el formato oficial CONAE.
* Simular una misión coherente: LAUNCH_PAD → ASCENT → APOGEE → DESCENT → eventos de recovery → LANDED.
* Generar perfiles plausibles de altitud, presión, temperatura, batería, corriente, IMU y GPS.
* Incrementar PACKET_COUNT correctamente.
* Incluir escenarios de prueba seleccionables: nominal, pérdida de paquetes, paquete corrupto, pérdida GPS y reset simulado.
* Transmitir inicialmente por USB Serial a la notebook.

## Entregable

Firmware `GCS_FlightSimulator v0.1` + ejemplo de log de una misión completa.

## Criterio de finalización

* Emite 1 paquete/s durante una misión completa.
* El formato es parseable y compatible con CONAE.
* El perfil de vuelo tiene estados y variables coherentes.
* Al menos un escenario de fallo puede activarse.
* Funciona conectado por USB sin depender todavía del SX1276.



## Comentarios conservados

### 2026-10-17T12:14:52.795-0300 — comentario 10008

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10008). Última edición informada: 2026-10-17T12:14:52.795-0300.

## Evaluación del banco frente a v2 — 17/10/2026

Quedó conservado en Drive un banco Python y sketch ESP32 USB con perfil heredado v1, 131 muestras y escenarios NOMINAL/PACKET_LOSS/CORRUPTED_PACKET/GPS_LOSS/RESET. Nueve pruebas de software vuelven a aprobar: nominal 131 válidos; pérdidas 13 huecos; corruptos 10 rechazos y 10 huecos; RESET lógico tres huecos.

Pendientes: identificar placa y compilar/cargar; medir tasa USB; corregir escenario de verificación C3 (h=500−(t−30)² no sostiene 15±3 m/s); distinguir señales IMU ilustrativas de dinámica coherente. RESET es omisión de entrega con contador/hora en RAM, no corte/reinicio físico F1/F2/F5. El ASCII22 y nombres de estados ya no figuran como formato obligatorio en el PDF v2 y quedan por confirmar en ICD.

Informe y alcance: https://docs.google.com/document/d/1WwZ83me8W0qA7T8eum6xSrYxVtpbYoT9OYq1Z0WPMNI/edit?usp=drivesdk  
Código, tests y logs sintéticos: https://drive.google.com/drive/folders/16P_8tdACes23uirmR-koQlB5iE0oVhEf

Este comentario documenta el prototipo; la tarea conserva su estado y no se afirma ensayo de hardware.

### 2026-10-17T12:31:19.882-0300 — comentario 10022

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10022). Última edición informada: 2026-10-17T12:41:52.867-0300.

## Bitácora 17/10/2026 — desarrollo del simulador de misión y alcance alcanzado

### Por qué lo hicimos

Tengo el microcontrolador destinado a tierra, aunque todavía no identifiqué el modelo exacto y no tengo la antena. Se preparó un banco que permita desarrollar recepción, parser, registro y pantalla antes de integrar SX1276 o depender del firmware STM32 de Edu. No requiere comprar hardware para iniciar en PC y evita fijar unilateralmente el Radio Profile.

### Qué esperamos demostrar

Una misión sintética transmitida/entregada a razón nominal de una muestra por segundo, con variables y estado visibles, registro íntegro de paquetes aceptados y anomalías detectables. Queremos mantener el mismo payload y parser cuando el transporte USB provenga después del gateway RF, sujeto al ICD acordado.

### Qué hicimos

Banco Python separado en simulator.py, protocol.py, acquisition.py, storage.py y app.py. Sketch GCS_FlightSimulator.ino preparado para Arduino ESP32, todavía sin compilación/carga. Se genera una misión de 131 instantes de muestreo: plataforma, ascenso, apogeo, descenso, eventos de recuperación y aterrizaje. Altitud, presión, temperatura, alimentación, IMU y GPS son ficticios. Se conserva perfil ASCII22 heredado de v1, marcado como banco pendiente de aprobación; 1000 es TEAM_ID ficticio. No hay radio ni actuadores.

### Escenarios y resultados de software

* NOMINAL: 131 paquetes válidos, cero huecos observados.
* PACKET_LOSS: 118 válidos y 13 huecos observados.
* CORRUPTED_PACKET: 121 válidos, 10 rechazados y 10 huecos.
* GPS_LOSS: 131 válidos; retención del último fix y señal de ausencia mediante GPS_SATS=0, convención provisional del banco.
* RESET: 128 válidos y tres huecos; omisión lógica de entrega con contador y hora conservados en RAM.

Nueve tests aprobados: misión/estados; reconstrucción en todos los tamaños de fragmento ensayados; recuperación de trama excesiva; validación; atrasados/duplicados/huecos; salto grande sin reservar memoria proporcional; cinco escenarios con comparación de dos CSV; GPS retenido; sesiones sin sobrescritura. Durante la verificación se detectó una colisión de nombres al crear sesiones casi simultáneas: se corrigió agregando identificador único a la carpeta y se repitieron los tests con éxito.

### Hasta dónde llegamos y por qué

Se verificó software en la notebook. Faltan modelo exacto de placa, toolchain/configuración, compilación, carga y puerto físico. RESET no ejecuta reinicio real ni corte: no acredita F1/F2/F5. PACKET_LOSS no es una medición RF. La primera fase de descenso usa h=500−(t−30)² y no representa régimen sostenido 15±3 m/s: corregir antes de usarla como evidencia C3. Las lecturas IMU son ilustrativas y no validan dinámica. La tasa real de hardware y dos horas de continuidad no se ensayaron.

### Evidencia y repetición

Código, sketch, nueve tests, informe de verificación y logs/CSV de los cinco escenarios: https://drive.google.com/file/d/1dOL2imloQJ7vsTKhMbexEt3YG8NyAUSK/view  
Carpeta de respaldo documental: https://drive.google.com/drive/folders/16P_8tdACes23uirmR-koQlB5iE0oVhEf  
Dentro del paquete ejecutar python app.py para NOMINAL, o --scenario PACKET_LOSS/CORRUPTED_PACKET/GPS_LOSS/RESET. Repetir software con python -m unittest -v test_ground. Serial exige pyserial y puerto real identificado. El código y la evidencia quedan accesibles por enlace; el intento de adjuntar el ZIP directamente a Jira no llegó a completarse porque el host de carga no resolvió en esta sesión.

### Material para PDR y siguiente paso

Se puede afirmar que existe un prototipo reproducible con escenarios y validación de software. Corregir perfil físico, cerrar esquema con Edu, identificar placa y ensayar USB antes de integrar RF. No afirmar misión real, cumplimiento integral v2 ni persistencia física.

### 2026-10-17T12:43:28.289-0300 — comentario 10030

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10030). Última edición informada: 2026-10-17T12:43:28.289-0300.

## Bitácora 17/10/2026 — estado de trabajo y alcance

Paso esta tarea de Backlog a **En curso**.

Ya preparé el simulador PC y el sketch ESP32, ejecuté nueve pruebas de software y conservé los registros. Me falta identificar la placa, corregir el perfil de verificación y probar USB físico.

Uso Backlog para ideas que todavía no asumimos; Por hacer para trabajo previsto sin iniciar; y En curso cuando ya estoy trabajando. La tarea sigue abierta hasta cumplir sus criterios y conservar la evidencia. En adelante gestiono únicamente tareas que creé o que están asignadas a mí; las dependencias con Edu y Rebe las documento desde mis propias tareas.

### 2026-10-17T12:45:26.936-0300 — comentario 10036

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10036). Última edición informada: 2026-10-17T12:45:26.936-0300.

## Bitácora 17/10/2026 — redacción y estados de mis tareas

Corregí doce comentarios propios y las referencias equivalentes del informe para que expresen mi trabajo en primera persona y el trabajo compartido como equipo. Conservé el contenido técnico y las capturas de las descripciones anteriores; la corrección es de redacción y autoría, sin atribuir nuevos ensayos o aprobaciones.

Organizo mis tareas con este criterio:

* **En curso:** ASTRA-18 (evaluación RF), ASTRA-20 (simulador), ASTRA-21 (recepción/CSV) y ASTRA-22 (pantalla). Ya tengo análisis, implementación o evidencia de trabajo iniciado; todavía quedan sus criterios de cierre.
* **Por hacer:** ASTRA-23 (integración SX1276), ASTRA-24 (interoperabilidad) y ASTRA-25 (link budget). Son compromisos de desarrollo y ensayo, pendientes de comenzar en su alcance específico y de resolver sus dependencias.
* **Backlog:** lo reservo para ideas que todavía no asumimos como trabajo previsto. No cierro una tarea sólo por documentarla o por tener pruebas parciales.

De ahora en adelante sólo modifico tareas que creé o que están asignadas a mí. Documento las dependencias con Edu y Rebe desde mis tareas, sin intervenir en las suyas. Para esta corrección puntual de autoría revisé únicamente comentarios que yo había publicado; no cambié estados, responsables ni descripciones de sus tareas. Los próximos avances quedan registrados en la tarea correspondiente con motivo, alcance, resultados, limitaciones y evidencia.

### 2026-10-17T12:51:27.592-0300 — comentario 10037

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10037). Última edición informada: 2026-10-17T12:51:27.592-0300.

## 17/10/2026 — COMENTARIO 5 — Metodología fija del diario

Acordamos registrar la evolución del proyecto como un diario que conserva íntegramente cada entrada. Aplico este criterio desde ahora como metodología fija de trabajo y trazabilidad para el PDR.

### Entradas originales

Registro cada avance con fecha real, número correlativo dentro de la tarea y tema:

**DD/MM/AAAA — COMENTARIO N — tema**

Dejo qué hice o hicimos, por qué, qué esperábamos, hasta dónde llegamos, pruebas/resultados, evidencia, limitaciones y pendientes.

### Cambios posteriores

Si una decisión cambia, deja de servir o necesita una corrección, no borro, edito ni sustituyo la entrada anterior. Publico un comentario nuevo:

**DD/MM/AAAA — ACTUALIZACIÓN COMENTARIO N (del DD/MM/AAAA) — tema**

Identifico el original con su número, fecha y enlace. Explico qué punto actualizo, qué cambió, por qué, con qué evidencia, desde cuándo aplica y qué consecuencias tiene para el diseño, las pruebas y otras tareas. Indico si la conclusión anterior queda corregida, ampliada, sustituida o descartada, pero siempre conservo su contenido.

Si hay varias actualizaciones de la misma decisión, vinculo también la actualización anterior para reconstruir toda la cadena. Para los comentarios antiguos sin numeración uso su fecha y enlace de Jira; no los edito para renumerarlos ni cambio retroactivamente su fecha.

### Ejemplo de aplicación

Si inicialmente seleccionamos un microcontrolador para prototipo y posteriormente validamos que sirve para vuelo, conservo la entrada inicial. Agrego una actualización a esa entrada con los requisitos revisados, pruebas y fundamentos que respaldan su nuevo uso. Una posibilidad o una simulación no se registra como validación física ya realizada.

### Descripciones, estados y archivos

Mantengo la descripción original de la tarea. Los cambios de alcance o criterio técnico se registran en nuevas actualizaciones. Los archivos se conservan por versión, sin reemplazar el original vinculado a una entrada anterior. Los estados operativos pueden avanzar mediante las transiciones de Jira y dejo el motivo en el diario; su evolución no borra el trabajo anterior.

Esta metodología sustituye el criterio anterior que permitía actualizar una descripción después de conservar una copia. Desde ahora la actualización va en una entrada nueva. Para la organización vigente: ideas en Backlog, trabajo previsto en Por hacer y trabajo iniciado en En curso. Sólo gestiono tareas que creé o que están asignadas a mí, y escribo por mi trabajo en primera persona y por el equipo cuando corresponda.

### 2026-10-19T19:28:18.460-0300 — comentario 10039

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10039). Última edición informada: 2026-10-19T19:28:18.460-0300.

## 19/10/2026 — COMENTARIO 6 — Banco, antecedentes y diario de mi área publicados en GitHub

Publiqué mi línea de trabajo en la rama groundstation para conservar código, decisiones y pruebas vinculadas a Jira. Todo el cambio está dentro de ground-station/; main y las carpetas de otras áreas conservan su estado previo. Jira sigue siendo la bitácora principal para el PDR.

Conservo sin alterar las fuentes del banco Python y el sketch ESP32 del 17/10. Recuperé desde Drive la estación v04 y el laboratorio v05; los identifiqué como DEPRECATED — históricos. Sus originales se conservan, con advertencias actuales separadas y huellas de importación. La numeración de esos prototipos no se mezcla con banco-usb-v0.1.

Repetí las nueve pruebas automatizadas del banco: aprobadas. La lógica histórica v04 aprobó trece pruebas. El guardado de capturas aprobó cuatro pruebas; conservo también la primera salida fallida por una comprobación demasiado amplia del propio test y su corrección. No compilé ni cargué el sketch, no probé USB físico ni RF y no doy por demostrado C3, autonomía, persistencia eléctrica o respaldo en dos dispositivos.

Guía: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/README.md  
Banco: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/banco-usb-v0.1/README.md  
Históricos: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/archive/DEPRECATED/README.md  
Pruebas y límites: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/docs/pruebas-2026-10-19.md  
Método de mi área: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/docs/metodologia-2026-10-19.md  
Cambio publicado: https://github.com/edulandoni/astra-cansat/commit/a1a7d383ed4498b540c0f7a12500a66f84bc3551

Dejé activa una tarea diaria a las 21:00 de Argentina que consulta mis tareas de Jira y agrega capturas nuevas a GitHub cuando hay cambios. Su ejecución depende de la aplicación, la máquina y las conexiones. La programación activa no acredita todavía una ejecución futura. También respaldo al cerrar cada tanda. El mecanismo no modifica descripciones ni estados y evita ciclos por sus propios avisos.

Próximo trabajo: identificar la placa, compilar y cargar el simulador, probar recepción y reconexión físicas, corregir el perfil de descenso y completar las funciones pendientes. Mantengo esta tarea En curso.

### 2026-10-19T19:30:01.870-0300 — comentario 10045

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10045). Última edición informada: 2026-10-19T19:30:01.870-0300.

## 19/10/2026 — COMENTARIO 7 — Cierre del respaldo Jira → GitHub

\[JIRA-GITHUB-SYNC\]

Publiqué una segunda captura que conserva la consulta inicial y agrega las siete entradas de publicación de esta tanda: siete tareas, veintiséis comentarios y el historial de cambios de campos consultado. Verifiqué que los diecinueve comentarios previos, las descripciones, responsables y estados se conservaron.

Captura de cierre: https://github.com/edulandoni/astra-cansat/tree/groundstation/ground-station/historial-jira/2026-10-19-22-28-52-UTC_b451bf12d17f  
Cierre y enlaces a cada tarea: https://github.com/edulandoni/astra-cansat/blob/groundstation/ground-station/docs/historial/2026-10-19-cierre-publicacion.md  
Cambio de respaldo: https://github.com/edulandoni/astra-cansat/commit/b0a383b9b12b0348ed9cf75f02328cf3d3d3eb9e

La rama groundstation quedó publicada y main conservó su referencia. El respaldo diario quedó activo a las 21:00 de Argentina. Este aviso del propio respaldo no dispara otra captura por sí solo; queda en Jira y se incluirá con la siguiente captura que tenga cambios reales. Las copias públicas excluyen correos, identificadores de cuenta y comentarios restringidos o internos; no incluyen adjuntos binarios ni reacciones.

### 2026-10-19T19:32:28.996-0300 — comentario 10046

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10046). Última edición informada: 2026-10-19T19:32:28.996-0300.

## 19/10/2026 — ACTUALIZACIÓN COMENTARIOS 6 y 7 (del 19/10/2026) — COMENTARIO 8 — Control del respaldo

Originales: https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10039 y https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10045

La comprobación real del cierre mostró que Jira devuelve la etiqueta del respaldo con escapes. El control inicial creó una captura adicional del propio aviso. Conservo esa captura y la de la corrección; no borro registros para ocultar el problema.

Corregí la detección para reconocer la etiqueta normal y escapada, y para comparar capturas antiguas con la regla actual sin modificar sus manifest. El control posterior con la lectura real devolvió «Sin cambios» y no creó otra carpeta.

La batería actual del historial aprueba cinco pruebas, incluidas la etiqueta escapada y la compatibilidad con huellas anteriores. Se mantienen aprobadas las nueve pruebas del banco y las trece de lógica v04. No se realizaron nuevos ensayos de hardware.

Actualización documentada: https://github.com/edulandoni/astra-cansat/blob/groundstation/ground-station/docs/historial/2026-10-19-actualizacion-etiqueta-jira.md  
Corrección publicada: https://github.com/edulandoni/astra-cansat/commit/4fe04e377c9a786dc15dec4e406010c534b3a1bc  
Capturas conservadas: https://github.com/edulandoni/astra-cansat/tree/groundstation/ground-station/historial-jira

Mantengo la programación diaria y el estado En curso. Esta corrección actualiza el resultado anterior; no sustituye las entradas originales.

### 2026-10-19T19:33:02.310-0300 — comentario 10048

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10048). Última edición informada: 2026-10-19T19:33:02.310-0300.

## 19/10/2026 — COMENTARIO 9 — Respaldo final de las actualizaciones

\[JIRA-GITHUB-SYNC\]

Publiqué la captura que incluye la corrección del control de etiquetas y sus entradas de Jira. Conserva siete tareas y veintinueve comentarios consultados, además del historial de cambios de campos. Mantengo las capturas anteriores sin cambios.

Captura final: https://github.com/edulandoni/astra-cansat/tree/groundstation/ground-station/historial-jira/2026-10-19-22-32-37-UTC_5e8c1ca39b67  
Cambio de respaldo: https://github.com/edulandoni/astra-cansat/commit/b03f95cf9bfad95c683c40cf92b8e891684b9771

Este aviso del propio respaldo no dispara una captura adicional por sí solo. Se conserva en Jira y se incorpora a la siguiente captura que tenga cambios reales. Continúan pendientes los ensayos físicos y los acuerdos de interfaz ya documentados.

### 2026-10-19T20:41:48.519-0300 — comentario 10059

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10059). Última edición informada: 2026-10-19T20:41:48.519-0300.

## 19/10/2026 — COMENTARIO 10 — ACTUALIZACIÓN de ubicación de los comentarios 4 a 9

Revisé la bitácora y separé lo transversal del desarrollo del simulador. Conservo íntegros los comentarios y descripciones anteriores; esta corrección cambia dónde continúa cada tema, no sus resultados ni fechas.

* Comentario del 17/10 sobre redacción y estados (id 10036): la metodología y administración de mi área continúan en ASTRA-33; el estado del simulador sigue en esta tarea.
* Comentario 5, metodología fija (10037): la referencia vigente es ASTRA-33, comentario 1: https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10054
* Comentario 6, publicación (10039): la parte del banco/simulador permanece aquí; la GUI histórica corresponde a ASTRA-22 y la metodología/exportador/respaldo a ASTRA-33.
* Comentarios 7, 8 y 9 (10045, 10046 y 10048): el respaldo de Jira y la corrección de su etiqueta continúan en ASTRA-33, comentario 2: https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10055

Esta tarea conserva generación de misión y escenarios, sketch ESP32, compilación/carga y prueba USB. No cierro sus pendientes por ordenar documentación. Mantengo En curso. Los avisos generales de respaldo ya tienen destino propio y no deben seguir agregándose aquí. La captura histórica conservará la ubicación original para reconstruir la corrección.

### 2026-10-19T21:03:39.317-0300 — comentario 10068

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10068). Última edición informada: 2026-10-19T21:03:39.317-0300.

## 19/10/2026 — COMENTARIO 11 — ACTUALIZACIÓN del contexto de simulación según el aula

Amplío las hipótesis del banco con las aclaraciones del 19/10: https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2960#p50090 y https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2963#p50093

La espera previa es con el CanSat activado y consumo mínimo; no se exige transmitir durante las dos horas hipotéticas en rampa. Se permite telemetría en ascenso. El comienzo de misión se comunica al detectar separación real. Contenedor y carga útil descienden juntos y se admite otro sistema activo/pasivo para la segunda etapa. La altura esperada supera 500 m y es inferior a 1000 m; no es un apogeo nominal exacto.

El formato propio está permitido, pero nuestro ASCII22 y los estados siguen siendo una convención del banco pendiente de acuerdo, no una aprobación automática. No modifiqué el simulador: la trayectoria C3, IMU ilustrativa, RESET lógico y hardware pendiente conservan sus límites. Próximo ajuste: separar espera, ascenso y evento de separación en el modelo con semántica acordada; no inventar el perfil del vector mientras falta su documento.

El PDR pide plan de simulación (ítem 79, diapositiva 82). Los resultados existentes sirven como evidencia sintética identificada. Mantengo En curso. Revisión completa: https://github.com/edulandoni/astra-cansat/blob/5f9d8c310ecbecc9e1b7d0cc8d29d5d43df7b406/ground-station/docs/aula/2026-10-19/revision-aula.md

## Historial de cambios de campos

### 2026-10-13T01:43:10.718-0300 — cambio 10077

Autoría original: Eduardo Landoni.

Campo: Rank.

Antes: (sin valor informado)

Después: Ranked higher

### 2026-10-13T01:56:09.606-0300 — cambio 10089

Autoría original: Eduardo Landoni.

Campo: assignee.

Antes: cristianponsone9

Después: Cristian Ponsone

### 2026-10-17T12:42:32.873-0300 — cambio 10120

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Backlog

Después: Por hacer

### 2026-10-17T12:43:19.226-0300 — cambio 10127

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Por hacer

Después: En curso

