# ASTRA-22 — GND — Implementar GUI PDR mínima de telemetría en tiempo real

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-22)

Estado observado: En curso. Asignación: Cristian Ponsone. Creación: Eduardo Landoni.

## Descripción original consultada

## Objetivo

Construir una primera GUI funcional de Ground Station que demuestre el flujo completo de telemetría y cubra los requisitos CONAE aplicables a visualización.

## Trabajo a realizar

* Mostrar simultáneamente los campos de telemetría requeridos, sin pestañas.
* Usar tema claro, tipografía ≥14 pt y gráficos/ejes legibles bajo luz intensa.
* Graficar en tiempo real altitud, voltaje, corriente, aceleración XYZ y giro XYZ.
* Mostrar tiempo de misión, temperatura, GPS, paquetes recibidos/perdidos, estado FSW y CMD_ECHO.
* Incorporar indicadores de estado de enlace y logging.
* No acoplar la GUI directamente al puerto serie: consumir datos desde el módulo de telemetría/parser.

## Entregable

`ASTRA Ground Station GUI v0.1` ejecutable en la notebook de Cristian + capturas para PDR.

## Criterio de finalización

* Todos los datos requeridos aparecen simultáneamente.
* Los gráficos actualizan a 1 Hz sin congelar la interfaz.
* La GUI permanece operativa durante una misión simulada completa.
* Diseño compatible con G5–G8 y G12–G14.
* Capturas y arquitectura listas para la PDR.



## Comentarios conservados

### 2026-10-17T12:14:56.866-0300 — comentario 10010

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10010). Última edición informada: 2026-10-17T12:14:56.866-0300.

## Revisión de GUI frente a v2 — 17/10/2026

G5–G8 y G12–G14 conservan contenido. El banco Python muestra 22 campos y seis gráficos simultáneos sin pestañas. Se comprobó geometría de ventana; falta inspección bajo sol y en portátil de operación.

G6: presentar giro en rad/s o junto a conversión SI; hoy el banco etiqueta grados/s. Conservar datos brutos con unidad de origen, sin cambiar sólo una etiqueta. Ejes/validez GPS y formato temporal deben cerrarse en el ICD. Falta señal solar y operación de comandos del esquema final; CMD_ECHO=NONE no demuestra ejecución. No transferir a operación el comportamiento de v04 que pausa la simulación al abrir una ayuda.

Informe: https://docs.google.com/document/d/1WwZ83me8W0qA7T8eum6xSrYxVtpbYoT9OYq1Z0WPMNI/edit?usp=drivesdk  
Banco y evidencias sintéticas: https://drive.google.com/drive/folders/16P_8tdACes23uirmR-koQlB5iE0oVhEf

### 2026-10-17T12:31:23.792-0300 — comentario 10024

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10024). Última edición informada: 2026-10-17T12:31:23.792-0300.

## Bitácora 17/10/2026 — pantalla del banco y límites de validación

### Por qué y qué se buscó

G5–G8/G12–G14 requieren lectura y gráficos simultáneos, legibilidad bajo luz intensa y conteos/estado visibles. La pantalla consume la adquisición separada para mantener el registro aunque el dibujo demore. Se eligió Tkinter para que la simulación PC funcione con el Python disponible sin instalar un framework gráfico adicional.

### Qué hicimos y verificamos

GUI con 22 campos del perfil heredado y seis gráficos simultáneos: altitud, voltaje, corriente, aceleración XYZ, giro XYZ y presión. Fondo claro, texto de 14 pt, ejes destacados, sin pestañas. Se muestra conexión, logging, respaldo configurado/ausente, conteos y advertencia de datos antiguos tras tres segundos. El gráfico deja abiertos los huecos entre contadores. Historial de presentación acotado a 300 muestras, independiente del archivo.

Comprobación geométrica: ventana de 1450×949, 45 etiquetas y seis gráficos; ninguna etiqueta fuera de la ventana en la comprobación realizada. No fue un ensayo bajo sol ni valida todo tamaño/escala de portátil. Las nueve pruebas corresponden al software de datos; no certifican legibilidad ni operación de campo.

### Límites y siguiente trabajo

Faltan telecomandos y señal solar del esquema definitivo. El giro se muestra en grados/s: para G6 acordar y presentar conversión a rad/s con unidad correcta, conservando los datos originales. MODE/STATE/CMD_ECHO/horas/GPS siguen el perfil de banco v1 y requieren ICD. En el HTML v04 abrir una ayuda pausa la simulación; ese comportamiento no se adopta como recepción operativa.

El PDR puede mostrar la interfaz y el flujo de datos sintéticos con etiqueta de simulación. Para cerrar: notebook real, sol, distancia de lectura, resolución/escala, dos horas y casos de enlace/registro fallidos.  
Código y evidencia: https://drive.google.com/file/d/1dOL2imloQJ7vsTKhMbexEt3YG8NyAUSK/view  
Informe: https://docs.google.com/document/d/1WwZ83me8W0qA7T8eum6xSrYxVtpbYoT9OYq1Z0WPMNI/edit

### 2026-10-17T12:43:32.356-0300 — comentario 10032

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10032). Última edición informada: 2026-10-17T12:43:32.356-0300.

## Bitácora 17/10/2026 — estado de trabajo y alcance

Paso esta tarea de Backlog a **En curso**.

Ya implementé la pantalla del banco con telemetría y gráficos simultáneos. Me faltan unidades/payload definitivos, solar/comandos y prueba de legibilidad con la notebook real.

Uso Backlog para ideas que todavía no asumimos; Por hacer para trabajo previsto sin iniciar; y En curso cuando ya estoy trabajando. La tarea sigue abierta hasta cumplir sus criterios y conservar la evidencia. En adelante gestiono únicamente tareas que creé o que están asignadas a mí; las dependencias con Edu y Rebe las documento desde mis propias tareas.

### 2026-10-19T19:28:22.883-0300 — comentario 10041

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10041). Última edición informada: 2026-10-19T19:28:22.883-0300.

## 19/10/2026 — COMENTARIO 4 — GUI y antecedente visual conservados

Publiqué la GUI del banco USB del 17/10 junto con una guía comprensible de su alcance. Conservo el antecedente v04 como DEPRECATED, sin editar su código ni sus explicaciones originales. Sus referencias reglamentarias son históricas v1 y algunas ayudas externas no están recuperadas en esta copia.

El banco permite mostrar el recorrido de datos sintéticos y mantiene separada la pantalla de adquisición, parser y registro. Las nueve pruebas del banco y las trece pruebas de lógica v04 aprobaron. No hice una verificación visual nueva ni un ensayo bajo sol, de pantalla de operación o de misión física; no cierro G12/G13 por esos tests.

Guía: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/README.md  
Banco: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/banco-usb-v0.1/README.md  
Histórico: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/archive/DEPRECATED/estacion-v04/README.md  
Verificación y límites: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/docs/pruebas-2026-10-19.md  
Cambio publicado: https://github.com/edulandoni/astra-cansat/commit/a1a7d383ed4498b540c0f7a12500a66f84bc3551

Quedan pendientes unidades SI, telecomandos y solar, pruebas de pantalla y operación real. La tarea continúa En curso.

### 2026-10-19T21:03:43.526-0300 — comentario 10070

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10070). Última edición informada: 2026-10-19T21:03:43.526-0300.

## 19/10/2026 — COMENTARIO 5 — ACTUALIZACIÓN de evidencia GUI y señal solar para PDR

La respuesta del 19/10 permite cumplir la señal solar mostrando la tensión medida del panel; no exige demostrar carga de batería: https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2963#p50093

El ítem 74 del PDR (diapositiva 77; Scoresheet fila 151) pide prototipo de pantalla, gráficos, comandos/calibración verificados y creación/presentación de CSV. La expectativa menciona calibración de ángulos sin un requisito equivalente claro en el anexo: queda TBR con vuelo, no agrego una orden obligatoria unilateral.

Nuestra GUI y evidencias sintéticas permiten mostrar el prototipo, pero faltan dato solar, operación de comandos, conversión/unidades SI y pruebas en notebook/sol. CMD_ECHO=NONE no demuestra ejecución y ninguna lectura del aula cambia eso. No edité la GUI ni hice nueva comprobación visual de la aplicación operativa.

Mantengo En curso. Esquema de datos y respuestas se acuerdan en ASTRA-24; la revisión de fuentes queda en ASTRA-37: https://github.com/edulandoni/astra-cansat/blob/5f9d8c310ecbecc9e1b7d0cc8d29d5d43df7b406/ground-station/docs/aula/2026-10-19/revision-aula.md

### 2026-10-23T22:01:58.953-0300 — comentario 10115

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10115). Última edición informada: 2026-10-23T22:01:58.953-0300.

23/10/2026 — COMENTARIO 6 — Primera pantalla con datos del ESP32 físico y corrección del arranque de banco

Abrí la GUI con COM5 a 115200 y comprobé visualmente tablas y gráficos recibiendo datos del ESP32, con TEAM1000 ficticio y modo S. La primera sesión comenzó en el contador 2, tuvo siete rechazos y conservó 76 muestras (2–77). La cerré voluntariamente para corregir el inicio; no fue fin de misión ni pérdida RF. Conservo esa sesión local.

El registro mostró seis tramas de diagnóstico de arranque y una muestra precedida por LF. Agregué --bench-reset-once, con verificación de que haya --port: reinicio EN/RTS una vez y guardo 0,5 s de arranque fuera del parser para este sketch conocido. No activo esta ventana en uso normal ni modifico el parser. No es un telecomando de vuelo ni opción para RF.

Abrí una sesión nueva y comprobé visualmente los gráficos y el resultado final: 131 paquetes válidos y únicos, contadores 1–131, cero rechazados, duplicados o huecos observados, estado LANDED. El CSV quedó guardado. Dejé la ventana abierta con la misión terminada; después indica datos antiguos porque el sketch finaliza sus 131 muestras, sin que eso pruebe una falla del enlace. Para repetir una sesión conservando contadores desde cero cierro y vuelvo a abrir con la opción de banco.

[Informe y procedimiento](https://github.com/edulandoni/astra-cansat/blob/f20d88ed7d0ec93e23a42f4f07f9a05e4c77c12f/ground-station/docs/2026-10-23-prueba-usb-fisica-actualizacion-02.md) · [CSV de la GUI](https://github.com/edulandoni/astra-cansat/blob/f20d88ed7d0ec93e23a42f4f07f9a05e4c77c12f/ground-station/evidence/2026-10-23-esp32-usb/gui-02/Flight_1000.csv) · [Resultado comparativo y versiones de código](https://github.com/edulandoni/astra-cansat/blob/f20d88ed7d0ec93e23a42f4f07f9a05e4c77c12f/ground-station/evidence/2026-10-23-esp32-usb/gui-02/resultado.json) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/f20d88ed7d0ec93e23a42f4f07f9a05e4c77c12f). Pasaron once pruebas de software; reconexión cubierta sólo con puerto simulado. No hay RF, sensores reales, autonomía ni G2 acreditados. Mantengo la tarea en curso y conservo las entradas anteriores.

### 2026-10-23T23:27:15.328-0300 — comentario 10118

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10118). Última edición informada: 2026-10-23T23:27:15.328-0300.

23/10/2026 — COMENTARIO 7 — ACTUALIZACIÓN COMENTARIO 6: interfaz de banco bidireccional

Preparé una GUI nueva que mantiene22campos y seis gráficos simultáneos. Separa origen PC_BENCH/USB_BENCH/REPLAY, datos actuales de histórico, tramas/control/telemetría, rechazos, huecos, duplicados y conflictos. Muestro guardados, pendientes y descartes por escritor/destino: recibir no equivale a guardar.

Los botones envían órdenes sólo al perfil de banco: iniciar/parar, cero ficticio, horaPC y alimentación sintética. La pantalla distingue en cola, enviada, aceptada, rechazada, ejecutada en simulación, timeout y resultado desconocido; el botón no certifica ejecución. No hay órdenes a radio ni actuadores.

Muestro edad de dato, GPS sin fix y posición retenida identificada; un cambio de segmento deja de mostrar valores anteriores como actuales. Convierto explícitamente °/s del perfil conocido a rad/s en pantalla, conservando el original enCSV. No declaro avería por lectura constante.

Observé la GUIUSB de esta etapa con otra misión nominal de131muestras. Las últimas mejoras de contadores, estados en español, ventana maximizada y gui_health se observaron después con origenPC: no las presento como toda la campaña física ni como dos horas. Instrumenté cada5s el progreso de Tk, colas, historial acotado y memoria del proceso para la prueba prolongada, que sigue pendiente.

[Aplicación y comandos](https://github.com/edulandoni/astra-cansat/tree/114616a4dc5d1f09706b623581b9fdd0714621da/ground-station/banco-usb-v0.2) · [Informe y matriz de pendientes](https://github.com/edulandoni/astra-cansat/blob/114616a4dc5d1f09706b623581b9fdd0714621da/ground-station/docs/2026-10-23-banco02-actualizacion-01.md) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/114616a4dc5d1f09706b623581b9fdd0714621da). Pasaron diez pruebas v0.2 y once de regresión v0.1. Faltan ensayo físico de RST/reconexión, ≥2h conGUI, legibilidad al sol y hardwareRF. Mantengo En curso.

### 2026-10-23T23:48:17.192-0300 — comentario 10130

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10130). Última edición informada: 2026-10-23T23:48:17.192-0300.

23/10/2026 — COMENTARIO 8 — ACTUALIZACIÓN COMENTARIO 7: Pantalla después del RST e identidad pendiente

Observé la pantallaUSB después del segundoEN/RST: campos y gráficos vacíos, segmento nuevo yCSV anterior aún con131muestras. OtroRUN recibió1..131/LANDED y se guardó aparte. El primer intento había quedado esperando descarga sin hello; laGUI anterior retenía datos viejos marcados antiguos. Conservé la incidencia.

Agregué invalidación inmediata de los valores ante el diagnósticoROM del banco, sin esperar ahello ni inventar identidad. Muestro por separado antigüedad del último mensaje válido y de la medición, y marco respuestas de órdenes de otro contexto como históricas. Guardados acumula sesiónPC; válidos/únicos/huecos corresponden al segmento.

La corrección pasó12pruebas de software y reproducción de los bytes reales capturados; cargué después el proceso nuevo y observé recepciónUSB. No atribuyo el arreglo al proceso que produjo la primera captura. La desconexión/reconexión se verifica aparte; continúan pendientes≥2h reales conGUI, respaldo externo y legibilidad de campo.

[Informe y límites](https://github.com/edulandoni/astra-cansat/blob/0603ad93182850e4ebad856d7a56b54970ddaa30/ground-station/docs/2026-10-23-rst-fisico-actualizacion-03.md) · [Evidencia](https://github.com/edulandoni/astra-cansat/blob/0603ad93182850e4ebad856d7a56b54970ddaa30/ground-station/evidence/2026-10-23-banco02/rst-fisico-05/resultado-rst-05.json) · [Drive verificado](https://drive.google.com/file/d/1A_4vETJ2wQrLxzcoFHSlFh6Tiv1cQs2x/view?usp=drivesdk) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/0603ad93182850e4ebad856d7a56b54970ddaa30). Conservo originales y comentarios anteriores.

### 2026-10-24T00:25:23.309-0300 — comentario 10134

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10134). Última edición informada: 2026-10-24T00:25:23.309-0300.

24/10/2026 — COMENTARIO 9 — ACTUALIZACIÓN COMENTARIO 8: Reconexión conGUI y reproducción visible en dos destinos

Observé el nuevo contexto después de reconectar: campos y gráficos vacíos, histórico guardado. Inicié otra misión1..131 yLANDED. La pantalla distinguió datos antiguos de dato actual y conservó contadores/estado por escritor.

La captura registró un desborde de trama al abrir el puerto, aunque ese proceso todavía no mostraba el aviso. Agregué el aviso visible de trama excesiva para que no quede oculto detrás de rechazos0 o descartes de archivo0. Pasaron13tests, incluido equipo ajeno/diagnóstico/trama larga y recuperación de muestra válida. No atribuyo el cambio a la pantalla anterior.

Después observéREPLAY con órdenes deshabilitadas,131tramas y cuatro escritores(raw/CSVdeC:yD:); lascopias cerraron sinerrores/pendientes/descartes y susarchivos coinciden. Son discos físicosdistintos. No es recepciónESP32simultánea niensayo dedoshoras. Mantengo En curso.

[Informe con evidencia y límites](https://github.com/edulandoni/astra-cansat/blob/2863fee267eeb3f48826e8876e279ca096ab091f/ground-station/docs/2026-10-24-reconexion-y-doble-soporte-actualizacion-04.md) · [Drive verificado](https://drive.google.com/file/d/11qcMyyB8SE5QESRkXl5xLetJK-FeWNE2/view?usp=drivesdk) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/2863fee267eeb3f48826e8876e279ca096ab091f). Conservo entradas y originales.

### 2026-10-24T00:45:48.666-0300 — comentario 10139

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10139). Última edición informada: 2026-10-24T00:45:48.666-0300.

24/10/2026 — COMENTARIO 10 — ACTUALIZACIÓN COMENTARIO 9: GUI sin tapar el chat y control del ensayo prolongado

Agregué inicio minimizado y Ctrl+M para minimizar el banco sin enviar comandos. Así puedo mantener visibles las preguntas del chat mientras adquisición, archivo y callbacks siguen activos. Cierro la sesión de control de pantalla después de cada operación concreta; no la mantengo en espera.

La corrida prolongada está en curso desde 00:36:19 ART, con 7261 muestras y ventana de 7280 s. Registro progreso de Tk, memoria residente, historial, cola de pantalla y escritores. El analizador no aprobará continuidad si hay más de 10 s entre controles de GUI. Una ventana minimizada por sí sola no demuestra operatividad.

Las fuentes se congelaron antes de iniciar. El lanzador mantiene una inhibición transitoria de suspensión por inactividad y la libera al salir, sin cambiar ajustes persistentes. No equivale a autonomía de batería. La corrección de identidad evita confundir el mismo número de orden entre sesiones de PC y conserva respuestas históricas.

Todavía no publico un resultado de dos horas ni cierro la tarea. Las pruebas de software suman 15; los ensayos físicos cortos y sus revisiones están separados del inicio prolongado.

[Informe y evidencia por revisión](https://github.com/edulandoni/astra-cansat/blob/38ae9999af98395e376030089cf5f2c7447f409f/ground-station/docs/2026-10-24-cadencia-identidad-e-inicio-prolongado-actualizacion-05.md) · [Drive verificado](https://drive.google.com/file/d/1j6m_KdBn266iJZAxvZD4yM1B4rH_MkQ-/view?usp=drivesdk) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/38ae9999af98395e376030089cf5f2c7447f409f). Conservo resultados, fuentes y comentarios anteriores.

### 2026-10-24T01:02:53.773-0300 — comentario 10145

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10145). Última edición informada: 2026-10-24T01:02:53.773-0300.

24/10/2026 — COMENTARIO 11 — Última posición válida cuando el mensaje no tiene fix

Durante la revisión encontré que la GUI mostraba los campos GPS de la trama aunque GPS_SATS fuera cero. Nuestro emisor repetía la posición previa y ocultaba ese caso: otro mensaje sin fix puede traer ceros u otras coordenadas numéricas. Corregí sólo la presentación: hora, altitud y coordenadas pasan a la última solución válida con etiqueta y edad; sin solución anterior aparecen vacías y con aviso explícito. Cuando vuelve el fix, muestro el dato nuevo. El CSV y los valores originales recibidos quedan intactos.

Pasaron 16 pruebas de software, incluido un caso sin fix inicial, otro con coordenadas diferentes de la última válida y recuperación posterior. Observé además una GUI REPLAY con dos mensajes sintéticos: contador 51, satélites 0, última posición válida etiquetada y seis gráficas visibles. No es una prueba GPS física. Cerré esa reproducción y el control del escritorio; la adquisición USB prolongada continúa independiente.

La corrida de dos horas conserva su snapshot anterior y no acreditará esta corrección posterior. No reinicié el ensayo ni le atribuyo código que no ejecutó. La regla de validez es del banco: debe acordarse para vuelo.

[Informe, prueba y huellas](https://github.com/edulandoni/astra-cansat/blob/36629a493f3c8dc2eefaebf0aeea4ae89c02dbed/ground-station/docs/2026-10-24-gps-presentacion-actualizacion-06.md) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/36629a493f3c8dc2eefaebf0aeea4ae89c02dbed) · [Drive](https://drive.google.com/file/d/1JU0LwK6cDEL9UNOkmGc4HA9bGGrDVUUS/view?usp=drivesdk). Mantengo las entradas previas y los pendientes de RF, interoperabilidad y operación prolongada.

### 2026-10-24T01:11:38.013-0300 — comentario 10148

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10148). Última edición informada: 2026-10-24T01:11:38.013-0300.

24/10/2026 — COMENTARIO 12 — ACTUALIZACIÓN del ensayo prolongado: medidor corregido y nuevo intento

Interrumpí deliberadamente la primera corrida tras 1906 muestras y 1905,063 s entre primera y última. El resultado queda false: no son dos horas. No hubo pérdidas declaradas por escritores, errores de encuadre ni conflictos en el segmento nominal, pero la memoria crecía. Aislé la causa: el medidor creaba tipos de ctypes en cada consulta y la caché global los retenía. Tener colas e historial acotados no demostraba memoria total acotada.

Corregí el medidor para definir tipo y API una sola vez. Pasaron 17 pruebas, incluida una de 500 consultas sin nuevos tipos después de inicializar. El nuevo gui_health registra las inicializaciones y el analizador exige una sola. Conservo resultado, salud, huellas, diario y CSV del intento anterior; no los reemplazo ni recalifico como aprobados.

Cerré esa GUI con vaciado de escritores, confirmé liberación de la inhibición transitoria de suspensión y envié STOP de banco antes de la nueva campaña. Inicié otro snapshot el 24/10 a las 01:09:00 ART, con las correcciones del medidor y GPS: 7261 muestras, ventana de 7280 s, cierre previsto cerca de 03:10:20 ART. No recargué firmware ni reinicié físicamente. Calibración, hora, alimentación y RUN quedaron confirmados. La campaña nueva todavía no tiene resultado final.

[Informe, intento interrumpido y configuración nueva](https://github.com/edulandoni/astra-cansat/blob/ce3220891ece63d2fcaa0c7990ec8d3eaa63181f/ground-station/docs/2026-10-24-medidor-y-reinicio-prolongado-actualizacion-07.md) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/ce3220891ece63d2fcaa0c7990ec8d3eaa63181f) · [Drive](https://drive.google.com/file/d/1kBmo1uFNJLebHIolXAUBUiQ9eailEgpe/view?usp=drivesdk). Mantengo los pendientes y las tareas abiertas. No acredita RF, autonomía ni respaldo externo simultáneo.

### 2026-10-24T03:18:14.352-0300 — comentario 10154

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10154). Última edición informada: 2026-10-24T03:18:14.352-0300.

24/10/2026 — COMENTARIO 13 — Aceptación del banco USB y límites para el PDR

La GUI acompañó el flujo USB prolongado: 1407 controles durante los datos, con mayor intervalo de 5,266 s, historial máximo de 300 muestras y cola de pantalla máxima de una, frente a límite 250. Después de dos horas observé el contador 7247, origen USB_BENCH, campos completos y seis gráficas legibles. Las imágenes se mostraron en el chat; la exportación no entregó el PNG esperado y no afirmo que exista un archivo de captura de GUI.

La memoria residente del proceso osciló entre 36,26 y 44,86 MiB, con una sola inicialización del medidor en cada control. Conservo toda la serie y su gráfica: no confundo working set con todo el heap ni convierto el rango observado en garantía de duración ilimitada. La corrección de GPS sin fix está incluida en el snapshot de esta segunda corrida; la prueba específica de coordenadas inválidas sigue en su entrada anterior, porque esta corrida fue nominal.

La aplicación cerró a las 03:10:21 ART y liberó su inhibición transitoria de suspensión. Volví al chat y cerré el control de pantalla; no quedó en espera durante la adquisición. No modifiqué ajustes persistentes de Windows. La suite actual tiene 18 pruebas pasadas; la corrección offline del recuperador es posterior al snapshot de GUI y queda identificada por separado.

Puedo respaldar operación USB sintética de dos horas con datos/archivo y progreso de interfaz medidos. Siguen pendientes legibilidad al sol, operación RF, integración con vuelo y alimentación autónoma.

[Informe final y matriz de la etapa](https://github.com/edulandoni/astra-cansat/blob/44bf6ea88a04acfa460dd77bdb8c62d4a6fb9a29/ground-station/docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md) · [Commit de resultados verificado](https://github.com/edulandoni/astra-cansat/commit/44bf6ea88a04acfa460dd77bdb8c62d4a6fb9a29) · [Drive: informe final](https://drive.google.com/file/d/1i-pRyjTcZRqRaD8nuIt3MrOW22W6Hu90/view?usp=drivesdk) · [Aclaración de reproducción](https://github.com/edulandoni/astra-cansat/blob/838e0a187472e0d7dcc2f6c4f8dee8abf5856c4d/ground-station/docs/2026-10-24-control-reproduccion-actualizacion-10.md) · [Drive: control de fuentes](https://drive.google.com/file/d/1fEv5ZasO5i-YNfuKfulLwAH6NjjiO8yn/view?usp=drivesdk).

### 2026-10-24T03:58:59.885-0300 — comentario 10161

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10161). Última edición informada: 2026-10-24T03:58:59.885-0300.

24/10/2026 — COMENTARIO 14 — ACTUALIZACIÓN: GPS actualizado y enlace activo: avisos separados en la GUI

Agregué “GPS SIN ACTUALIZAR” para distinguir GPS con satélites declarados pero reloj estancado de telemetría reciente. Si envejece toda la telemetría, muestro ese problema sin asignárselo además al GPS. Los umbrales de antigüedad son configurables; los 3 s del banco no fijan requisitos de vuelo. Un sensor constante no se declara averiado por ese único motivo.

Verifiqué una GUI real con reproducción a 0,5×: contador 6, telemetría de 0,7 s de antigüedad, GPS de 10,7 s y aviso visible. Conservé la captura JPEG original, el registro de salud y el procedimiento. Las órdenes permanecieron deshabilitadas durante reproducción. El ensayo utilizó datos sintéticos, sin GPS físico.

La comparación de seis trazas y los límites están en el informe de calidad; la investigación correspondiente quedó finalizada en ASTRA-34. Mantengo esta tarea de GUI abierta porque todavía faltan sus condiciones pendientes, incluida legibilidad al sol.

[Informe y evidencia de GUI](https://github.com/edulandoni/astra-cansat/blob/9735087c1074754895273c4109553f5b350c7faf/ground-station/docs/investigacion/2026-10-24-calidad-medida-y-cierre-investigacion.md)
[Copia verificada en Drive](https://drive.google.com/file/d/11kA0UM5kLgTEHoe7xPqLGoDgF6xS9x5n/view)

### 2026-10-25T22:39:14.091-0300 — comentario 10169

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10169). Última edición informada: 2026-10-25T22:39:14.091-0300.

25/10/2026 — COMENTARIO 15 — Demostración entendible para mostrar el trabajo con la placa

Preparé una explicación en primera persona y un visor sencillo para poder contar qué hicimos: la placa ensaya un vuelo con valores inventados, los manda por USB y la PC los recibe, muestra y guarda. Distingo esta comunicación física de sensores reales, RF y vuelo, que siguen pendientes.

Abrí una sesión USB nueva en COM5 con el firmware ya instalado y un reinicio por RTS, sin cargar ni pedir BOOT. Observé la GUI en ASCENT, contador 17 y altura sintética de 255 m. Conservé una trama excesiva del inicio en el registro bruto; su causa sigue sin determinar. El primer RUN conservó 124 muestras antes de iniciar otro y la sesión interactiva tiene cambios de contexto separados. No califico los segmentos interrumpidos como misiones completas ni como pérdidas de radio. Dejé el banco disponible para explorar y cerré el control de pantalla después de volver al chat.

Para repetir la presentación sin depender de la placa preparé HTML autónomo y GIF: ambos usan exactamente las 131 filas verificadas de la campaña USB del 24/10, no la sesión abierta de hoy. La reproducción permite pausa, recorrido, reinicio y velocidad; identifica fecha, fuente sintética y límites. No es una filmación de la placa ni una nueva prueba de aceptación.

Verifiqué igualdad de las 131 filas con el CSV original, 66 cuadros del GIF y funcionamiento del visor en navegador: avance hasta mensaje 71 / 233,3 m y pausa en 83 / 173,3 m. Corregí un error de avance antes de publicar. Conservo captura del visor y procedencia; no modifiqué las fuentes del banco ni cerré esta tarea.

[Demostración, explicación y procedencia en GitHub](https://github.com/edulandoni/astra-cansat/tree/76dfadb436ece902a9a585bf2e0fa582f341d9ed/ground-station/docs/demostraciones/2026-10-25)
[Commit verificado remoto](https://github.com/edulandoni/astra-cansat/commit/76dfadb436ece902a9a585bf2e0fa582f341d9ed)
[Guía verificada en Drive, material PDR/video](https://drive.google.com/file/d/14--5FWO4lhjk0ety2si84Nr1hmepVYE-/view)

La incidencia de configuración de Windows se diagnosticó por separado, con registro privado; no publiqué configuración, credenciales ni logs de la PC en Jira o GitHub.

### 2026-10-25T23:29:13.190-0300 — comentario 10171

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10171). Última edición informada: 2026-10-25T23:29:13.190-0300.

25/10/2026 — COMENTARIO 16 — ACTUALIZACIÓN: interfaz nativa organizada y ayudas de operación

Organicé la pantalla de escritorio en cuatro grupos: Vuelo, Energía, Ubicación GPS y Movimiento. Cada medición tiene una ayuda accesible con ⓘ que explica significado, referencia y unidad. Reescribí las ayudas para describir exclusivamente cómo se usa la aplicación actual: no remiten a archivos anteriores ni narran cambios de versión. La historia del desarrollo queda en este diario y en los documentos fechados. Conservé la estética sencilla y el funcionamiento nativo Tk; esta mejora no usa HTML.

Agregué un estado principal explicado, origen de datos y seis contadores con su alcance: recibidas, diferentes, guardadas CSV, esperando guardado, faltantes detectados y rechazadas. Identifico la última muestra histórica y su edad; no confundo puerto abierto con mediciones actuales. Los seis gráficos tienen unidades, eje de número de muestra, leyendas y cortes en los huecos. Al cambiar de ejecución comienzo otro contexto.

Los controles indican iniciar/detener ensayo, altura cero, hora UTC y consulta sintética batería/solar. Deshabilito acciones incompatibles con el estado y órdenes durante reproducción. Cerrar conexión USB no significa detener el emisor; Conectar USB comprueba identidad y no inicia otra misión por sí solo. La detención confirmada no se muestra como avería de telemetría.

Verifiqué visualmente la pantalla y la nueva explicación de altura en la aplicación real; conservé capturas finales e intermedias identificadas. Probé desconexión física con reinicio y cierre manual del puerto con continuidad. Este último mostró 18 faltantes, 113 muestras guardadas y cero pendientes de escritura. Las 30 pruebas de software aprobaron. Los detalles de conservación y cortes están registrados también en ASTRA-21.

Separo presentación de recepción y escritura. Los datos siguen siendo sintéticos enviados por USB físico; no prueban sensores, radio o vuelo. La trama excesiva de la reconexión física queda como incidencia pendiente. No atribuyo a esta revisión la campaña anterior de dos horas ni verifico aún legibilidad al sol; mantengo esta tarea en curso. Conservo el comentario 15 y su demostración como historia, sin presentarlos como la interfaz vigente.

[Informe, pruebas y límites](https://github.com/edulandoni/astra-cansat/blob/caeac641b2e9c319c9430d9ea77429761487f898/ground-station/docs/2026-10-25-interfaz-y-cortes-usb.md) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/caeac641b2e9c319c9430d9ea77429761487f898) · [Copia verificada en Drive](https://drive.google.com/file/d/1VWU1Pd1KdSjfwjtSn-LmJwobT6fQLu5E/view)

### 2026-10-26T13:06:46.363-0300 — comentario 10195

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10195). Última edición informada: 2026-10-26T13:06:46.363-0300.

26/10/2026 — COMENTARIO 17: interfaz Qt y separación de fuentes

Implementé la interfaz vigente del Laboratorio con Qt Widgets, conservando Engine/Store, reglas de identidad/reconexión y registros del banco. La entrada es laboratorio/app.py. La versión Tk se conserva en el histórico.

USB, simulación PC y reproducción se eligen explícitamente; al abrir no hay datos. Al perder USB se informa la interrupción, se marcan los valores históricos y crece la edad de la última muestra. No activo un generador PC como sustitución. El contador de pendientes corresponde al CSV recibido y aún no escrito; los faltantes durante un corte pueden quedar por determinar. Mantengo el gráfico separado ante huecos/segmentos y la inspección de datos originales.

La organización es por subsistema, con títulos descriptivos y estados concretos. No uso hooks ni discurso publicitario. Las explicaciones y límites se consultan bajo demanda. El recorrido para reuniones queda en ASTRA-41, comentario 6.

Pasaron diez pruebas del Laboratorio (incluida navegación/renderizado Qt fuera de pantalla, USB simulado sin sustitución por PC, arranque vacío, reproducción inmutable y cierre seguro) y 34 del banco de cámaras. No abrí ventanas de escritorio, puertos ni hice maniobras físicas. La revisión de renders no acredita una campaña real de USB; esa validación sigue pendiente.

Commit verificado: https://github.com/edulandoni/astra-cansat/commit/2ec5f14ac67013419b621dabe80db65f789ee91d  
Informe: https://drive.google.com/file/d/1xjyXdTRGrbRHotr_UmtU2hH3VxnEphuT/view  
Control: https://github.com/edulandoni/astra-cansat/blob/2ec5f14ac67013419b621dabe80db65f789ee91d/ground-station/evidence/2026-10-26-laboratorio-qt/control-02.json

La tarea permanece abierta por ensayos físicos y criterios pendientes de la misión.

### 2026-10-26T13:39:31.807-0300 — comentario 10197

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-22?focusedCommentId=10197). Última edición informada: 2026-10-26T13:39:31.807-0300.

26/10/2026 — COMENTARIO 18: telemetría completa dentro del Laboratorio Qt

Integré 22 variables y once gráficos para los quince canales numéricos: altura, presión, temperatura, batería, corriente, giro XYZ en rad/s, aceleración XYZ, altura GPS, satélites, latitud y longitud. Cada valor conserva unidad y condición; los gráficos no unen huecos ni completan posiciones GPS sin solución. La pantalla mantiene 180 muestras del segmento y 300 eventos; el registro completo continúa en disco.

Agregué áreas de comandos, escritores por destino, identidad/cortes/calidad y tramas ASCII originales. Los contadores distinguen recibidos, válidos, guardados, pendientes y descartados. Los faltantes durante un corte pueden seguir indeterminados; nunca se suman como pendientes de escritura. USB, PC y reproducción son fuentes explícitas. Reproducción no habilita órdenes.

Comprobé los 22 valores, once series, cuatro escritores con dos destinos, comandos confirmados, corte simulado, histórico y bloqueo de órdenes. La suite final pasó 14 pruebas del Laboratorio más 34 de cámaras, conservando cinco misiones completas y cierre seguro. Revisé renders fuera de pantalla; no hice una campaña física nueva ni ensayos de legibilidad bajo sol. Esto no cierra los requisitos de operación de campo o protocolo de vuelo.

Commit: https://github.com/edulandoni/astra-cansat/commit/7713a4f6dcb95ac1dd8c6c1e825f344321f80b59  
Informe de cobertura: https://github.com/edulandoni/astra-cansat/blob/7713a4f6dcb95ac1dd8c6c1e825f344321f80b59/ground-station/docs/historial/2026-10-26-laboratorio-completo-04.md  
Control: https://github.com/edulandoni/astra-cansat/blob/7713a4f6dcb95ac1dd8c6c1e825f344321f80b59/ground-station/evidence/2026-10-26-laboratorio-qt/control-04.json  
Drive: https://drive.google.com/file/d/1nx08o0w5nks4paOe-By2I7upJycqMB0b/view?usp=drivesdk

La integración general y sus ensayos están en ASTRA-41, comentario 7. Mantengo esta tarea En curso por validación física y dependencias pendientes.

## Historial de cambios de campos

### 2026-10-13T01:43:11.324-0300 — cambio 10079

Autoría original: Eduardo Landoni.

Campo: Rank.

Antes: (sin valor informado)

Después: Ranked higher

### 2026-10-13T01:56:02.014-0300 — cambio 10086

Autoría original: Cristian Ponsone.

Campo: assignee.

Antes: cristianponsone9

Después: Cristian Ponsone

### 2026-10-17T12:42:37.690-0300 — cambio 10122

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Backlog

Después: Por hacer

### 2026-10-17T12:43:24.059-0300 — cambio 10129

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Por hacer

Después: En curso

