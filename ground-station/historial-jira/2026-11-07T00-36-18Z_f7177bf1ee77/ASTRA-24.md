# ASTRA-24 — COMMS — Ejecutar prueba de interoperabilidad STM32 ↔ ESP32/SX1276

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-24)

Estado observado: En curso. Asignación: Cristian Ponsone. Creación: Eduardo Landoni.

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

### 2026-10-23T23:28:31.611-0300 — comentario 10120

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-24?focusedCommentId=10120). Última edición informada: 2026-10-23T23:28:31.611-0300.

23/10/2026 — COMENTARIO 5 — Preparación iniciada: propuesta de interfaz y extremo USB de banco

Preparé una propuesta para revisar con Edu: campos/unidades, validez y edad, identidad de sesión/arranque/misión, comandos, confirmaciones, deduplicación y prueba conjunta. El ICD es el acuerdo para que ambos extremos interpreten los mismos bytes y resultados; esta propuesta no lo aprueba ni asigna trabajo a otra área.

Implementé mi extremo experimental bench-usb-0.2 con control JSON@BENCH/CR separado de22campos heredados. RUN/STOP, cero ficticio, horaPC y alimentación sintética ya se ejercitaron en banco. Las confirmaciones separan aceptado/ejecutado/rechazado y resultado desconocido tras interrupción. Timeout3s sin reenvío automático es sólo configuración de banco, no decisión para radio.

En el documento dejo tabla de cada campo y unidad, conversionesSI y asuntosTBD/TBR. TEAM1000 es ficticio. Un identificador de equipo permite filtrar la aplicación, pero no impide recepción física de otros transmisores; eliminar NetID heredado no autoriza broadcast. Frecuencia, modulación, potencia, SyncWord, CRC, direccionamiento, comandos y semántica final necesitan acuerdo con Edu y fuentes oficiales.

Inicio la preparación de esta tarea y la paso de Por hacer a En curso. No ejecuté aún interoperabilidad con STM32/SX1276, que sigue siendo el criterio central pendiente; no cierro la tarea por tener una propuesta.

[Propuesta para revisar](https://github.com/edulandoni/astra-cansat/blob/fc6e6d22b46104127b1a83c973ac86c4a22b59a9/ground-station/docs/interfaces/2026-10-23-propuesta-banco-y-vuelo.md) · [Contrato exclusivo del banco](https://github.com/edulandoni/astra-cansat/blob/fc6e6d22b46104127b1a83c973ac86c4a22b59a9/ground-station/banco-usb-v0.2/perfil-bench-usb-0.2.md) · [Resultados y límites](https://github.com/edulandoni/astra-cansat/blob/fc6e6d22b46104127b1a83c973ac86c4a22b59a9/ground-station/docs/2026-10-23-banco02-actualizacion-01.md) · [Commit documental verificado](https://github.com/edulandoni/astra-cansat/commit/fc6e6d22b46104127b1a83c973ac86c4a22b59a9). La implementación conserva su commit114616a, enlazado desde el informe.

### 2026-10-23T23:37:13.285-0300 — comentario 10126

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-24?focusedCommentId=10126). Última edición informada: 2026-10-23T23:37:13.285-0300.

23/10/2026 — COMENTARIO 6 — ACTUALIZACIÓN COMENTARIO 5: preparo los comandos de mi lado

Con el módulo informado porEdu abrí el pendiente de preparar catálogo y contrato de telecomandos: identidad/destino, nombre y argumentos, calibración, tiempoUTC, consulta batería/solar, inicio real separado de simulación, confirmaciones, duplicados y reinicios. Puedo encargarme de la propuesta, interfazPC y pruebas de referencia; el extremo de vuelo y la adopción del contrato necesitan revisión conEdu. No doy por delegada su implementación ni toco su código.

SPI controla registros de radio; los comandos de misión los definimos entre ambos extremos. El módulo no resuelve por sí solo qué significa una orden o cuándo se ejecutó. En la tabla nueva dejé qué falta acordar y qué prueba lo cerraría. ElJSON@BENCH, timeout3s y memoria de64órdenes actuales son experimentalesUSB: no pasan directamente aRF o vuelo.

El calculador de airtime mostró que debemos reservar tiempo para telemetría+orden+confirmación+guardas, con tamaño final aúnTBD. Separé recibido/aceptado/ejecutado/rechazado/desconocido; unACK de software no acredita un mecanismo físico. TEAM_ID real, destinatario, IDs persistentes y política de reintentos siguen pendientes. No habilito broadcast.

La tarea sigue En curso por preparación e interfaz de banco. No hice interoperabilidadSTM32/SX1276 ni aprobéICD. La discrepancia de pinout del módulo está registrada enASTRA-23.

[Informe, fuentes y pendientes](https://github.com/edulandoni/astra-cansat/blob/bbfb056dd58998201dfe7927007a7542e7f6f030/ground-station/docs/interfaces/2026-10-23-modulo-radio-y-comandos-actualizacion-02.md) · [CopiaDrive verificada](https://drive.google.com/file/d/1EmtZu0pjrRJaI8IdB4p65ZEOzPC0QTGv/view?usp=drivesdk) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/bbfb056dd58998201dfe7927007a7542e7f6f030). Conservo todas las entradas anteriores.

### 2026-10-24T03:59:10.911-0300 — comentario 10162

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-24?focusedCommentId=10162). Última edición informada: 2026-10-24T03:59:10.911-0300.

24/10/2026 — COMENTARIO 7 — ACTUALIZACIÓN: Paquete para revisar la interfaz con vuelo

Preparé un borrador de perfil con 18 entradas todavía TBD y once vectores de política de destinatario, sin elegir una codificación RF. Incluye qué debemos acordar sobre campos, identidades, confirmaciones, integridad y condiciones de ensayo. No convierte los mensajes JSON, los tiempos de espera ni las reglas del banco en decisiones de vuelo.

Como evidencia propia, repetí dos veces los catorce controles negativos/positivos del ESP32 USB: argumentos inválidos, órdenes fuera de estado, repetición sin ejecutar dos veces y equipo ajeno sin respuesta. Cada pasada conservó una misión de 131 muestras. Estas pruebas sirven para formular casos de interoperabilidad; no demuestran compatibilidad con STM32/SX1276.

La revisión con Edu y los ensayos entre extremos reales siguen pendientes. No modifiqué su trabajo ni configuré RF.

[Propuesta, cálculo y pruebas en GitHub](https://github.com/edulandoni/astra-cansat/blob/9735087c1074754895273c4109553f5b350c7faf/ground-station/docs/interfaces/2026-10-24-enlace-destinos-y-revision.md)
[Copia verificada en Drive](https://drive.google.com/file/d/1X9307Zgf2K0nldBgBXXh91KqPXExgTjZ/view)

[Ensayo USB y evidencia en GitHub](https://github.com/edulandoni/astra-cansat/blob/9735087c1074754895273c4109553f5b350c7faf/ground-station/docs/2026-10-24-ordenes-negativas-usb.md)
[Copia verificada en Drive](https://drive.google.com/file/d/1QplaMWPe9rHV-rlbhus5V2BN5VqaE4lY/view)

### 2026-10-25T23:45:41.275-0300 — comentario 10173

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-24?focusedCommentId=10173). Última edición informada: 2026-10-25T23:45:41.275-0300.

25/10/2026 — COMENTARIO 8 — ACTUALIZACIÓN: adapto groundstation a los comandos definidos desde vuelo

Acordamos que Edu define los comandos del extremo STM32 y yo adapto groundstation a esa definición. Así evitamos que tenga que acomodar su firmware a los comandos que usé para practicar en el banco USB. Se mantienen las funciones necesarias de referencia de altura, espera/activación y consultas de alimentación; falta recibir su semántica y codificación concretas. No equiparo automáticamente detener simulación con standby de vuelo.

RUN/STOP/CAL_ZERO/SET_TIME/POWER_STATUS y @BENCH siguen exclusivamente como perfil experimental; no quedan aprobados para RF ni los reenvío como protocolo de vuelo. Para implementar mi adaptador necesito especificación versionada y ejemplos de solicitudes/respuestas, destinatario, unidades, estados permitidos, confirmaciones, repetición y comportamiento tras reset. Las propuestas previas son casos para revisar, no una obligación impuesta a Edu.

Registré el estudio de cámaras en mi tarea nueva ASTRA-39. Comprobar ambas, armar/iniciar y finalizar grabación son funciones propuestas, sin nombres ni bytes aprobados. Separaré el inicio de cámaras de poner altura en cero para evitar que una calibración interrumpa o reinicie video. El evento real, sus condiciones y las respuestas quedan por acordar.

No cambié tareas ajenas, protocol/, firmware de vuelo ni RF. Esta actualización registra la coordinación; todavía no demuestra adaptación implementada ni interoperabilidad física.

[Decisión y pendientes](https://github.com/edulandoni/astra-cansat/blob/5a82e7a43b7efbc853dce1eabcbaaba637937ae0/ground-station/docs/interfaces/2026-10-25-comandos-definidos-desde-vuelo.md)
[Copia verificada en Drive](https://drive.google.com/file/d/1waOYI8gaSVj_ZbRJt4lpUy11T09jUUwp/view)
[Commit verificado](https://github.com/edulandoni/astra-cansat/commit/5a82e7a43b7efbc853dce1eabcbaaba637937ae0)

### 2026-10-27T12:37:40.990-0300 — comentario 10207

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-24?focusedCommentId=10207). Última edición informada: 2026-10-27T12:37:40.990-0300.

27/10/2026 — COMENTARIO 9 — ACTUALIZACIÓN COMENTARIO 8: necesidades de interfaz para cámaras y banco recibido

Conservo el acuerdo: Edu define empaquetado y comandos de vuelo; adapto tierra. Revisé su video de 119 s mediante 24 referencias visuales y transcripción local del audio completo. Se muestran diagnósticos de presión/temperatura, referencia de altura, IMU y GPS; Edu describe puesta a cero con Z. Esto no define todavía el paquete ni autoriza enviar literalmente Z desde groundstation. No medí precisión, latencia ni cadencia a partir del video.

Para integrar necesito versión y captura serial original, unidades/escalas, ejes/signos, referencias de reloj, altura relativa frente a altitud GPS, validez/antigüedad y comandos/respuestas versionados. Giro se expresa en rad/s cuando tengamos la conversión conocida, sin tratar datos crudos como unidades físicas.

Agregué la propuesta funcional de cámaras de ASTRA-39: chequeo individual, armado/inicio y cierre; consultas idempotentes y confirmaciones que distingan aceptado, primer cuadro guardado y progreso reciente. Propongo acordar identidad/arranque/segmento, contadores de captura/escritura, última escritura, espacio y errores, seleccionando el mínimo que entre en telemetría. Una imagen de chequeo es puntual; no reemplaza supervisión de la grabación autónoma.

Quedan por acordar evento y margen de inicio, continuidad ante reset del OBC, parada/cierre, repetición y estado desconocido. No definí bytes o nombres compartidos, no modifiqué vuelo/protocol ni habilité RF o Wi-Fi. Las coordenadas y el material recibido permanecen privados.

[Análisis del banco y estructura](https://drive.google.com/file/d/1g73wSBguzGUVMGfjwbWpa98AGUxuH7pn/view) · [Mecanismo propuesto de grabación](https://drive.google.com/file/d/1nqmUyeyEskOmAVhCWf9xwgv_X85RC2JB/view) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/070f622e920d5b1552f75afd7cecb22d8712cc32).

Es preparación de interoperabilidad; la prueba cruzada y los circuitos siguen pendientes.

### 2026-10-27T13:17:37.530-0300 — comentario 10210

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-24?focusedCommentId=10210). Última edición informada: 2026-10-27T13:17:37.530-0300.

27/10/2026 — COMENTARIO 10 — ACTUALIZACIÓN COMENTARIO 9: modelo verificable de progreso de cámaras

Preparé camera_health.py como intérprete de reportes propuestos: unidad, arranque, segmento, secuencia, cuadros/bytes escritos, tiempo de funcionamiento, última escritura, estado y error. No es un paquete ni un comando de vuelo aprobado. Edu conserva la definición de bytes/comandos; falta su contrato y adaptar este modelo a reportes reales.

El modelo distingue sin información, inicio sin confirmar, progreso sin confirmar, escritura reportada, escritura detenida, error y sin grabación. Un primer reporte no basta para confirmar progreso; deben avanzar cuadros y bytes dentro del mismo contexto y mantenerse reciente la escritura. Duplicados no renuevan vencimiento; un cambio de arranque/segmento requiere confirmar otra vez. Rechazo retrocesos y tiempos contradictorios. Un corte de enlace queda desconocido y no equivale a parada de la cámara.

Probé esos casos con reportes sintéticos. No conecté todavía este modelo a una cámara ni lo mostré como lectura independiente de SD. El nuevo camino Wi-Fi del Laboratorio se limita a mantenimiento local; WIFI_ON/WIFI_OFF son comandos de banco, no órdenes para enviar por SX1276. La grabación debe poder continuar sin notebook y sin radio, con circuito y política de reset pendientes de verificación.

Confirmamos una SD por cámara; sonido queda fuera de esta etapa. El arranque sin BOOT/RST durante operación y la continuidad ante reset del OBC son criterios pendientes, no supuestos cerrados por cargar firmware.

[Informe con estados y campaña](https://drive.google.com/file/d/10t6KUrzmzY8NIXgwcyGECH44kkWWwFVI/view) · [Código y evidencia verificados](https://github.com/edulandoni/astra-cansat/commit/af3ca3a519267624faae947deb2c62302517ee46). No cambié vuelo, protocol, perfil RF ni tareas ajenas.

### 2026-10-27T15:29:05.518-0300 — comentario 10216

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-24?focusedCommentId=10216). Última edición informada: 2026-10-27T15:29:05.518-0300.

27/10/2026 — COMENTARIO 11 — ACTUALIZACIÓN COMENTARIO 10: supervisión conectada a grabación real de banco

Conecté el modelo de salud al candidato local de cámara. Los reportes físicos separan capturados, escritos y leídos después de guardar, bytes, arranque/ejecución/segmento, última escritura, espacio y errores. La app exige progreso entre reportes y conserva desconocido cuando falta confirmación reciente. El conteo avanza después de comprobar JPEG e índice, no al aceptar inicio.

Probé en hardware inicio duplicado sin crear otra ejecución, rechazo del mismo ID con duración distinta, rechazo de parada dirigida a otra ejecución, cierre por límite y parada repetida. Cerré el seguimiento USB ocho segundos: la cámara siguió en el mismo contexto y pasó de 10 a 48 cuadros. No confundo cerrar el puerto con quitar alimentación. La lectura por USB permite recuperar y validar grabaciones de un arranque de captura anterior, manteniendo separado el arranque actual que atiende la copia.

REC_START/REC_STOP/REC_STATUS/REC_READ y sus argumentos pertenecen exclusivamente al banco experimental. No fijé nombres, bytes o tamaño del paquete de vuelo, no modifiqué protocol/ o STM32 ni habilité RF. Edu conserva la definición del contrato; queda adaptar estos conceptos y medir interoperabilidad real. El límite de duración es atendido por el bucle y no garantiza interrumpir una operación SD bloqueada mediante un temporizador externo.

La confirmación de escritura/lectura desde la cámara y la decodificación en PC son evidencia más fuerte que un LED, pero no certifican tolerancia a corte de energía o continuidad ante reset del OBC. Esos ensayos, el evento de inicio y el circuito de potencia siguen abiertos. No cierro esta tarea con el banco USB.

[Informe y estados](https://drive.google.com/file/d/1nEgEyNvVnetQ7JIwuVFRFMuSEvXUcduU/view?usp=drivesdk) · [Commit y evidencia verificados](https://github.com/edulandoni/astra-cansat/commit/ac9529e59acd114d49371cfe1141747c6bc5b37a).

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

### 2026-10-23T23:28:33.677-0300 — cambio 10148

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Por hacer

Después: En curso

