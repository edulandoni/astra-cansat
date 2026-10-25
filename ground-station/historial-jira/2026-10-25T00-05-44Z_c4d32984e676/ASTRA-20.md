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

### 2026-10-23T21:43:36.138-0300 — comentario 10111

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10111). Última edición informada: 2026-10-23T21:43:36.138-0300.

23/10/2026 — COMENTARIO 12 — Primer banco con mi ESP32 físico: identificación y compilación

Conecté la placa ZY-ESP32 por USB. Windows detectó CP2102, pero faltaba su controlador (código 28). Instalé Silicon Labs 11.5.0.417 del catálogo oficial Microsoft, verifiqué firma válida y coincidencia del ID USB; apareció COM5, estado OK. La descarga directa de Silicon Labs había fallado con HTTP403.

La conexión automática falló con Wrong boot mode (0x13). Mantuve BOOT, toqué y solté EN/RST y solté BOOT. Con --before no-reset consulté el chip: ESP32-D0WD-V3, revisión3.1, cristal40MHz y flash4MB. Dejo la secuencia documentada para poder repetirla. El firmware original declara2MB, distinto de la capacidad física detectada.

Compilé el sketch original sin cambiarlo con Arduino CLI1.5.1 y Arduino-ESP32 3.3.12, DIO40MHz/4MB/USB115200. Resultado:281044bytes de programa y22124 de variables. Resolví la búsqueda fallida de bits/c++config.h mediante una ruta corta del compilador, conservando los diagnósticos. Agregué un comando de compilación que crea salidas nuevas y guarda huellas.

Antes de escribir intenté copiar toda la flash original. La lectura a460800 se interrumpió porque el chip dejó de responder; el siguiente intento sin repetir BOOT no sincronizó. No tengo respaldo completo acreditado y todavía no cargué el simulador. Queda repetir entrada manual y lectura a menor velocidad, luego carga y misión completa. Las nueve pruebas del banco PC pasaron; no equivalen a recepción física.

[Guía, motivos, secuencia BOOT, límites y fuentes](https://github.com/edulandoni/astra-cansat/blob/f1585c3c647e34740b46b494b73b85c52a9d8e55/ground-station/docs/2026-10-23-banco-esp32-usb.md) · [Evidencia de preparación](https://github.com/edulandoni/astra-cansat/blob/f1585c3c647e34740b46b494b73b85c52a9d8e55/ground-station/evidence/2026-10-23-esp32-usb/preparacion-01.json) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/f1585c3c647e34740b46b494b73b85c52a9d8e55). ASTRA-21 conserva el capturador. TEAM1000 ficticio y formato heredado provisional; no configuré RF ni usé borneras/periféricos. Conservo todas las entradas anteriores.

### 2026-10-23T22:01:55.180-0300 — comentario 10113

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10113). Última edición informada: 2026-10-23T22:01:55.180-0300.

23/10/2026 — COMENTARIO 13 — ACTUALIZACIÓN COMENTARIO 12: carga y primera misión USB completa

Después de repetir BOOT apretado → pulsar y soltar EN/RST → soltar BOOT, pude leer toda la flash a 115200 baudios: 4.194.304 bytes en 383,1 segundos, SHA-256 a312ead25e36d3ab004b4fea46efae0fa43274c45631514b6cac47b30e809472. Conservo flash_original_intento03.bin en la carpeta temática de Descargas; no la publico ni la presento como respaldo independiente o restauración probada. Conservo los intentos fallidos anteriores. Esta corrida funcionó a menor velocidad, sin que eso identifique la causa física del fallo previo.

Cargué el sketch compilado sin modificar su fuente, con Arduino CLI 1.5.1 / Arduino-ESP32 3.3.12 y esptool 5.3.0. Las cuatro escrituras terminaron con hash verificado; no solicité borrado completo de flash. La placa ESP32-D0WD-V3 emitió por COM5 una misión sintética completa: 131 paquetes únicos, contadores 1–131, todos los estados hasta LANDED, cero rechazos, duplicados, huecos observados o desbordes. Intervalo mediano de llegada a PC 1,000 s; mínimo 0,891 s y máximo 1,109 s.

También registré mis observaciones de la luz: azul fija al conectar; apagado, encendido breve y apagado tras BOOT/EN; luego fija durante la lectura y titilando durante la recepción. No comprobé el circuito ni la correspondencia entre destellos y paquetes. Las observaciones quedan separadas de los controles seriales.

[Informe completo y secuencia](https://github.com/edulandoni/astra-cansat/blob/f20d88ed7d0ec93e23a42f4f07f9a05e4c77c12f/ground-station/docs/2026-10-23-prueba-usb-fisica-actualizacion-02.md) · [Evidencia de respaldo y carga](https://github.com/edulandoni/astra-cansat/blob/f20d88ed7d0ec93e23a42f4f07f9a05e4c77c12f/ground-station/evidence/2026-10-23-esp32-usb/respaldo-carga-02.json) · [Resultado de misión](https://github.com/edulandoni/astra-cansat/blob/f20d88ed7d0ec93e23a42f4f07f9a05e4c77c12f/ground-station/evidence/2026-10-23-esp32-usb/nominal-01/resultado.json) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/f20d88ed7d0ec93e23a42f4f07f9a05e4c77c12f).

ASTRA-21 conserva captura/CSV y ASTRA-22 la pantalla. Los datos son ficticios, TEAM1000 y formato heredado provisional; no hay prueba RF, sensores reales, autonomía, corte eléctrico o disco independiente. Quedan escenarios de fallo físicos e interfaz acordada con vuelo. Mantengo la tarea en curso.

### 2026-10-23T23:27:07.636-0300 — comentario 10116

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10116). Última edición informada: 2026-10-23T23:27:07.636-0300.

23/10/2026 — COMENTARIO 14 — ACTUALIZACIÓN COMENTARIO 13: firmware configurable y cinco escenarios USB

Conservé el sketch v0.1 y agregué AstraBench02, perfil experimental bench-usb-0.2. Lo compilé y cargué en mi ESP32-D0WD-V3, sin radio, sensores externos ni actuadores. Usa Arduino-ESP32 3.3.12, CLI1.5.1, flash4MB DIO40MHz y USB115200; 310956bytes de programa y25324 de variables. Conservé el respaldo original de flash. Para programar repetí BOOT apretado → pulsar/soltar EN/RST → soltar BOOT; la luz no demuestra el modo por sí sola.

Ahora selecciono por USB NOMINAL/PACKET_LOSS/CORRUPTED_PACKET/GPS_LOSS/RESET, sin recompilar. RUN/STOP, cero de altitud, hora PC y consulta batería/solar son efectos sintéticos. El modelo baja a15m/s hasta80% del máximo ilustrativo de500m y luego5m/s; no representa el vector ni prueba despliegues.

Campaña física del23/10 23:02–23:13ART: nominal131válidos; pérdidas118+13omisiones; corruptos121válidos+10rechazos; GPS131con15muestras sin fix; RESET128+3omisiones. Los629paquetes coinciden con el oráculo y losCSV. Repetí cadaRUN conocido: no reinició sus contadores. El RESET del escenario sigue siendo omisión lógica, distinto de RST físico. Intervalo nominal mediano1,0113s y130intervalos en132,573s: no afirmo1Hz exacto; queda corregir/ensayar la deriva de agenda en otra carga.

La campaña inicial precede a mejoras posteriores del receptor/handshake; no le atribuyo la revisión final. La campaña PC posterior con huellas también pasó los cinco casos, pero es acelerada. Conservo el informe original con rechazos acumulados y la verificación nueva por segmento, sin pisarlo. Faltan RST/desconexión físicos dedicados, soportes distintos y ≥2hUSB con GUI. No cierro la tarea ni afirmo RF/autonomía/protocolo de vuelo.

[Implementación](https://github.com/edulandoni/astra-cansat/tree/114616a4dc5d1f09706b623581b9fdd0714621da/ground-station/banco-usb-v0.2) · [Informe y límites](https://github.com/edulandoni/astra-cansat/blob/114616a4dc5d1f09706b623581b9fdd0714621da/ground-station/docs/2026-10-23-banco02-actualizacion-01.md) · [Contraste por segmento](https://github.com/edulandoni/astra-cansat/blob/114616a4dc5d1f09706b623581b9fdd0714621da/ground-station/evidence/2026-10-23-banco02/usb-cinco-escenarios-01.json) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/114616a4dc5d1f09706b623581b9fdd0714621da). ASTRA-21 conserva recepción/archivo; ASTRA-22 pantalla y ASTRA-24 propuesta de interfaz.

### 2026-10-23T23:48:09.041-0300 — comentario 10128

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10128). Última edición informada: 2026-10-23T23:48:09.041-0300.

23/10/2026 — COMENTARIO 15 — ACTUALIZACIÓN COMENTARIO 14: Ensayo RST físico y misión posterior

PulséEN/RST con laGUIUSB abierta. La primera pulsación reportada terminó a23:39:19ART enDOWNLOAD_BOOT/waiting for download; no arrancó el simulador. No comprobé la causa del estadoGPIO0. DejéBOOT suelto y repetí sóloEN/RST: a23:40:16 apareció hello con boot distinto, sin recargar firmware.

Inicié explícitamente otroRUN y recibí1..131/LANDED, separado de la misión anterior. Conservo131filas antes y131después. TrasRST reaparecieron offset12m y hora13:00:00 sintéticos; no había recalibrado eseRUN y no lo presento como persistenciaF1/F2.

El ensayo descubrió una limitación del receptor cuando hay diagnósticoROM sin hello: su corrección continúa enASTRA-21/22. La campaña física usó el proceso previo al arreglo; la reproducción posterior con código corregido no cuenta como otra pulsación. Faltan desconexiónUSB, soportes distintos y≥2h continuas; no cierro la tarea.

[Informe y límites](https://github.com/edulandoni/astra-cansat/blob/0603ad93182850e4ebad856d7a56b54970ddaa30/ground-station/docs/2026-10-23-rst-fisico-actualizacion-03.md) · [Evidencia](https://github.com/edulandoni/astra-cansat/blob/0603ad93182850e4ebad856d7a56b54970ddaa30/ground-station/evidence/2026-10-23-banco02/rst-fisico-05/resultado-rst-05.json) · [Drive verificado](https://drive.google.com/file/d/1A_4vETJ2wQrLxzcoFHSlFh6Tiv1cQs2x/view?usp=drivesdk) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/0603ad93182850e4ebad856d7a56b54970ddaa30). Conservo originales y comentarios anteriores.

### 2026-10-24T00:25:11.590-0300 — comentario 10132

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10132). Última edición informada: 2026-10-24T00:25:11.590-0300.

24/10/2026 — COMENTARIO 16 — ACTUALIZACIÓN COMENTARIO 15: Reconexión física y preparación de agenda fija

Desenchufé/reconecté elESP32 con la aplicación abierta. Recuperó el puerto y confirmó unboot nuevo mediante unsondeo, sin recargar firmware para esa prueba. Después hice cero ficticio, ajuste de hora yRUN: recibí otra misión1..131/LANDED, separada de las131muestras anteriores.

Conservé una anomalía al abrir: ráfaga malformada de12899bytes hastaCR, un desborde de encuadre y recuperación del siguiente mensaje válido. No atribuyo una causa ni lo confundo con pérdida de archivo. ASTRA-21 conserva detalle.

Preparé después agenda de vencimientos absolutos de1000ms para evitar sumar el tiempo de emisión a cada período. CompilaciónCLI1.5.1/core3.3.12 correcta:311008bytes de programa,25324de variables. El informe enlazado conserva el corte previo a cargar; la carga/medición nueva se documenta en otra actualización. No uso compilación como prueba de1Hz o de dos horas.

La reproducción posteriorC:+discoUSB es prueba de almacenamiento, noRF niESP32simultáneo. Mantengo la tarea abierta.

[Informe con evidencia y límites](https://github.com/edulandoni/astra-cansat/blob/2863fee267eeb3f48826e8876e279ca096ab091f/ground-station/docs/2026-10-24-reconexion-y-doble-soporte-actualizacion-04.md) · [Drive verificado](https://drive.google.com/file/d/11qcMyyB8SE5QESRkXl5xLetJK-FeWNE2/view?usp=drivesdk) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/2863fee267eeb3f48826e8876e279ca096ab091f). Conservo entradas y originales.

### 2026-10-24T00:45:37.590-0300 — comentario 10137

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10137). Última edición informada: 2026-10-24T00:45:37.590-0300.

24/10/2026 — COMENTARIO 17 — ACTUALIZACIÓN COMENTARIO 16: Cadencia física, identidad entre clientes e inicio prolongado

Cargué la agenda de vencimientos absolutos y recibí una misión de 131 muestras: 129,985347 s para 130 intervalos, media 0,999887 s, mínimo 0,947197 y máximo 1,041331 s. La mediana de llegada fue 1,017362 s; no la confundo con deriva acumulada. La revisión previa ocupaba 132,573 s en ese tramo. No afirmo reloj metrológico ni ausencia de jitter.

Detecté además que run basado sólo en seq podía repetirse entre sesiones PC. Cambié el banco a client_secuencia, conservando boot separado, y actualicé el emulador. El intento automático de programación falló antes de escribir con modo 0x13; después de BOOT/EN manual cargué la aplicación, hash verificado, sin reescribir bootloader/particiones ni repetir respaldo de flash. Compilación: 311336 bytes de programa y 25332 de variables.

Dos sesiones físicas de PC, sin reiniciar ESP32 entre ellas, conservaron el mismo boot y distintos run. Cada prueba de 12 muestras coincidió con el oráculo y repetir RUN no la reinició. Son pruebas cortas, no misiones completas.

Inicié el ensayo prolongado a 00:36:19 ART desde fuentes congeladas: 7261 muestras, ventana de 7280 s. Está EN CURSO; todavía no acredita dos horas. La memoria de deduplicación pertenece al cliente activo y no garantiza ejecución única entre clientes alternados o después de reset. RF y acuerdos de vuelo siguen pendientes.

[Informe y evidencia por revisión](https://github.com/edulandoni/astra-cansat/blob/38ae9999af98395e376030089cf5f2c7447f409f/ground-station/docs/2026-10-24-cadencia-identidad-e-inicio-prolongado-actualizacion-05.md) · [Drive verificado](https://drive.google.com/file/d/1j6m_KdBn266iJZAxvZD4yM1B4rH_MkQ-/view?usp=drivesdk) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/38ae9999af98395e376030089cf5f2c7447f409f). Conservo resultados, fuentes y comentarios anteriores.

### 2026-10-24T03:18:06.852-0300 — comentario 10152

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10152). Última edición informada: 2026-10-24T03:18:06.852-0300.

24/10/2026 — COMENTARIO 18 — Aceptación del banco USB y límites para el PDR

Cerré el segundo ensayo nominal con el ESP32 por USB: 7261 muestras únicas, contadores 1..7261, desde 01:09:02,751 hasta 03:10:03,084 ART del 24/10. El tiempo monotónico entre primera y última fue 7260,328 s, más de dos horas reales sin aceleración. Verifiqué también las 7261 declaraciones del emisor como emitted, la secuencia de su oráculo y done con 7261 muestras; coinciden con lo recibido.

La cadencia media de llegada fue 1,000045 s, con extremos 0,937/1,063 s; no uso la mediana como medida de deriva. La ejecución tiene identidad nueva, conserva las anteriores y usa el firmware cuya fuente tiene huella a0df3d3d47896444b252da68a17c0956168910fbf4cc7504b4bffba86de69fbe. No hice otra carga ni reinicio físico para esta corrida.

Conservo el primer intento interrumpido de 1906 muestras como no aprobado y la causa del medidor en sus entradas previas. Esta corrida acredita flujo sintético: después de la misión inicial continúa LANDED durante 7144 muestras. No representa un vuelo de dos horas, autonomía, movimiento GPS real o radio. Los cinco escenarios iniciales y sus versiones siguen documentados por separado; no atribuyo todas esas pruebas a una única revisión.

La matriz de cierre reúne escenario, comandos, identidades, pruebas y pendientes. Mantengo abiertos los criterios que todavía dependen del ICD, vuelo o RF.

[Informe final y matriz de la etapa](https://github.com/edulandoni/astra-cansat/blob/44bf6ea88a04acfa460dd77bdb8c62d4a6fb9a29/ground-station/docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md) · [Commit de resultados verificado](https://github.com/edulandoni/astra-cansat/commit/44bf6ea88a04acfa460dd77bdb8c62d4a6fb9a29) · [Drive: informe final](https://drive.google.com/file/d/1i-pRyjTcZRqRaD8nuIt3MrOW22W6Hu90/view?usp=drivesdk) · [Aclaración de reproducción](https://github.com/edulandoni/astra-cansat/blob/838e0a187472e0d7dcc2f6c4f8dee8abf5856c4d/ground-station/docs/2026-10-24-control-reproduccion-actualizacion-10.md) · [Drive: control de fuentes](https://drive.google.com/file/d/1fEv5ZasO5i-YNfuKfulLwAH6NjjiO8yn/view?usp=drivesdk).

### 2026-10-24T03:58:52.584-0300 — comentario 10159

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10159). Última edición informada: 2026-10-24T03:58:52.584-0300.

24/10/2026 — COMENTARIO 19 — ACTUALIZACIÓN: Guardas del simulador comprobadas en el ESP32

Ejecuté dos pasadas físicas de los mismos catorce controles por USB, con una misión nominal de 131 muestras en cada pasada. No son 28 tipos de prueba diferentes. Conservé ambas capturas y el resultado declarado por el emisor.

Comprobé argumentos inválidos, hora fuera de rango, órdenes incompatibles con el estado y repetición de RUN. Repetir RUN no reinició la misión ni duplicó su ejecución. Una orden de equipo ficticio ajeno quedó sin respuesta, no inició emisión y conservó el contexto; una consulta válida posterior respondió correctamente. STOP, calibración y configuración de hora aceptadas se ejecutaron en simulación. No pedí reinicios ni cargué firmware en esta campaña.

Las dos misiones conservaron exactamente los contadores 1–131, sin huecos ni muestras inválidas. El segundo ensayo confirmó también el cierre limpio de los destinos de almacenamiento. Esto verifica el banco actual, no el formato final CONAE ni comandos por radio. Mantengo pendiente la compatibilidad acordada con vuelo.

[Ensayo USB y evidencia en GitHub](https://github.com/edulandoni/astra-cansat/blob/9735087c1074754895273c4109553f5b350c7faf/ground-station/docs/2026-10-24-ordenes-negativas-usb.md)
[Copia verificada en Drive](https://drive.google.com/file/d/1QplaMWPe9rHV-rlbhus5V2BN5VqaE4lY/view)

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

