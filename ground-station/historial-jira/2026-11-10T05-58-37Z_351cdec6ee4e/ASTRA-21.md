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

### 2026-10-19T20:01:06.804-0300 — comentario 10050

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10050). Última edición informada: 2026-10-19T20:01:06.804-0300.

## 19/10/2026 — COMENTARIO 7 — Cierre del respaldo de la investigación

\[JIRA-GITHUB-SYNC\]

Conservo en GitHub una captura nueva que incluye el comentario 6 de investigación, con las siete tareas de mi alcance y su historial consultado. Las capturas anteriores permanecen intactas.

Captura: https://github.com/edulandoni/astra-cansat/tree/groundstation/ground-station/historial-jira/2026-10-19-23-00-19-UTC_5ca2692e233d  
Cambio de cierre: https://github.com/edulandoni/astra-cansat/commit/b00159f3e937ed94799fd119ff19d15ab00984ca  
Investigación y propuestas: https://github.com/edulandoni/astra-cansat/blob/groundstation/ground-station/docs/investigacion/2026-10-19-innovacion-y-prevencion.md

Este aviso de respaldo queda en Jira y se incluirá con la siguiente captura por cambios reales. No inicia otra captura por sí solo. La investigación no equivale a implementar las mejoras propuestas ni a probar hardware.

### 2026-10-19T20:13:23.209-0300 — comentario 10051

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10051). Última edición informada: 2026-10-19T20:13:23.209-0300.

## 19/10/2026 — ACTUALIZACIÓN COMENTARIO 6 (del 19/10/2026) — COMENTARIO 8 — Resiliencia y recuperación sin hardware

Original de investigación: https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10049

### Motivo y alcance

Amplié la investigación para comprobar cómo conserva datos el banco cuando falla la escritura, la presentación no consume actualizaciones y se corta una conexión ficticia. Agregué herramientas de experimento y un demostrador offline; no modifiqué los módulos del banco ni otras áreas.

### Configuración y resultados

1. Entregué 7200 mensajes sintéticos sin consumir la cola de presentación. Quedaron 7200 registros únicos en CSV y raw, y 250 actualizaciones en la cola. La ejecución duró segundos: prueba volumen y esa ruta de software, no dos horas reales de autonomía ni una GUI efectivamente bloqueada.
2. Inyecté diez excepciones de escritura del CSV principal y luego permití escribir de nuevo. De 31 mensajes, el principal conservó 21; respaldo y raw conservaron 31. Hubo aviso de error, pero los diez huecos no se rellenaron automáticamente.
3. Ejecuté el bucle serie real con un sustituto de software: apertura fallida, corte con fragmento incompleto y reconexión. Registró tres intentos y dos desconexiones, descartó el fragmento de la conexión anterior y conservó los contadores 2 y 3 de los paquetes completos. Las esperas de reconexión se registraron sin esperar físicamente.
4. Creé un recuperador de demostración para las copias de esa misma sesión de laboratorio. Generó un archivo nuevo con 31 registros, recuperando del respaldo los contadores 11–20 y dejando un archivo de procedencia. Comprobé por huellas que los originales no cambiaron. Un control negativo con altitud contradictoria fue detectado y la ejecución del programa no escribió un candidato recuperado.

### Aporte que propongo

Una estación que explique por paquete si lo recibió, dónde lo guardó, si puede recuperarse y si las copias se contradicen. Esto complementa el monitor de calidad de datos propuesto antes. Primero priorizaría continuidad del registro raw, conteos de guardado por destino y trazabilidad de cualquier reconstrucción.

### Límites y pendientes

Los dos destinos del ensayo son carpetas de un mismo disco. El fallo se produce antes de completar la fila: no demuestra tolerancia a escritura parcial o corte eléctrico. El puerto es un sustituto, no USB físico, COM real ni radio. La carga de 7200 paquetes no representa una trayectoria coherente durante dos horas.

El recuperador exige una sesión de laboratorio identificada y no separa vuelos o reinicios automáticamente. Si faltan mensajes en todas las copias no los inventa. La identidad real de sesión y cualquier cambio compartido siguen pendientes con Edu. No afirmo novedad mundial ni reconocimiento por el jurado.

Para el PDR puedo mostrar estas rutas y recuperaciones sintéticas, no cumplimiento físico. La tarea continúa En curso. El recuperador aún no está integrado en la aplicación operativa.

### Evidencia

Informe: https://github.com/edulandoni/astra-cansat/blob/groundstation/ground-station/docs/investigacion/2026-10-19-resiliencia-y-recuperacion.md  
Reproducción: https://github.com/edulandoni/astra-cansat/tree/groundstation/ground-station/experiments/2026-10-19-resiliencia  
Resultados: https://github.com/edulandoni/astra-cansat/tree/groundstation/ground-station/evidence/2026-10-19-resiliencia  
Recuperación y procedencia: https://github.com/edulandoni/astra-cansat/tree/groundstation/ground-station/evidence/2026-10-19-resiliencia-reconciliacion  
Cambio publicado: https://github.com/edulandoni/astra-cansat/commit/26e5e9bde25a19ff938584ae19d21a5f7ec1370f  
Fuentes técnicas oficiales: https://docs.python.org/3.12/library/unittest.mock-examples.html y https://docs.python.org/3.12/library/os.html#os.fsync

### 2026-10-19T20:22:14.256-0300 — comentario 10052

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10052). Última edición informada: 2026-10-19T20:22:14.256-0300.

## 19/10/2026 — ACTUALIZACIÓN COMENTARIO 6 — COMENTARIO 9: antecedentes CanSat y rotor generador

### Motivo y objetivo

Continúo la investigación sin hardware para elegir mejoras con evidencia y evitar repetir fallas. Busco distinguir qué se propuso, qué se ensayó y qué resultado quedó documentado. En paralelo estudié el descenso con hélices y generación eléctrica. Registro la exploración en mi área; no modifica decisiones de recuperación ni tareas de otros integrantes.

### Qué hice y qué encontré

Preparé un catálogo inicial de 35 registros equipo–edición: 10 finalistas escolares argentinos 2022/2023, los 20 primeros cinco puestos AAS 2023–2026, un premio Ground Station, tres antecedentes europeos y un informe de generación eólica. No son todos los CanSat del mundo ni 35 auditorías técnicas completas. Dejé identificadas fuentes, alcance y revisiones pendientes.

SEDS ITBA ganó AAS 2025, cuya misión oficial exigía autogiro. ICARE documentó en 2013 una propuesta CanSat con generador eólico: su informe es previo al vuelo y no demuestra energía real obtenida. No puedo afirmar novedad mundial de nuestra idea. En Cóndor Salvaje, sus autores reportan buena recepción de telemetría y despliegue parcial del parapente; por eso debemos medir comunicaciones y recuperación por separado.

Revisé la copia v2 conservada el 17/10: C3 exige paracaídas; C4 dice otro sistema de descenso al 80% de la altura máxima, con media 5 ± 3 m/s. Un rotor es candidato de investigación para C4, pendiente de admisibilidad y pruebas. No reemplaza los paneles solares de E3 ni la alimentación durante las dos horas dentro del cohete de E7. No envié consultas a CONAE ni definí parámetros RF.

### Cálculo ejecutado y evidencia

Publiqué un cálculo reproducible de escala gravitatoria, no una simulación aerodinámica. Supuse masa constante 0,5 kg, apogeo ficticio 500 m, rotor desde 400 m y descenso constante 5 m/s: 80 s y 0,5448 Wh gravitatorios. Con conversión global hipotética del 10%, resultarían 0,05448 Wh y 2,452 W medios durante esa fase; equivale a 3,27 minutos ideales a 1 W. Esa conversión no está medida ni demostrada. La potencia gravitatoria no es salida del generador.

El programa comprueba coherencia entre energía, potencia y duración, y conserva resultados JSON/CSV. Revisé enlaces locales, integridad de fuentes históricas, manifiestos y alcance de los archivos publicados. La energía eléctrica carga y frena el eje: hace falta modelar y probar su efecto en rpm, estabilidad y descenso.

### Hasta dónde llegué y pendientes

No hubo microcontrolador, prueba física, CFD, ensayo de despliegue ni validación de seguridad. Faltan más ediciones y participantes, lectura completa de PDR grandes y datos crudos posteriores al vuelo. En el PDR podemos afirmar que investigamos antecedentes y ejecutamos esta sensibilidad aritmética; no que el rotor funciona o que aportará determinada autonomía.

Próximo criterio de comparación: rotor libre frente a rotor cargado, energía neta, masa, estabilidad, arranque, carga abierta/cortocircuitada y cumplimiento de descenso. Mantengo ASTRA-21 En curso. Conservo los comentarios anteriores.

### Ubicación y versión

Cambio: https://github.com/edulandoni/astra-cansat/commit/f5fda9162f8b67d3ad70b086f3d3613f9f814434  
Antecedentes y fuentes: https://github.com/edulandoni/astra-cansat/blob/f5fda9162f8b67d3ad70b086f3d3613f9f814434/ground-station/docs/investigacion/2026-10-19-antecedentes-cansat.md  
Rotor, reglamento, hipótesis y límites: https://github.com/edulandoni/astra-cansat/blob/f5fda9162f8b67d3ad70b086f3d3613f9f814434/ground-station/docs/investigacion/2026-10-19-rotor-y-generacion.md  
Cálculo y reproducción: https://github.com/edulandoni/astra-cansat/tree/f5fda9162f8b67d3ad70b086f3d3613f9f814434/ground-station/experiments/2026-10-19-rotor  
Resultados: https://github.com/edulandoni/astra-cansat/tree/f5fda9162f8b67d3ad70b086f3d3613f9f814434/ground-station/evidence/2026-10-19-rotor-escala

Copias fechadas en mi carpeta Drive, verificadas después de subir:  
Antecedentes: https://drive.google.com/file/d/1BX75keo-wQGLqeGxd_uILAh4JPx_Acfk/view?usp=drivesdk  
Rotor: https://drive.google.com/file/d/1gn-23kr-wZz9REoaCJ5ZivTevtMtpFoc/view?usp=drivesdk  
Catálogo: https://drive.google.com/file/d/1FfjXDy4PqOR_YrYXC6q-z9sKzD_UhWG8/view?usp=drivesdk  
Las copias Markdown conservan las rutas relativas del repositorio; para navegar entre archivos uso los enlaces GitHub anteriores.

### 2026-10-19T20:23:07.030-0300 — comentario 10053

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10053). Última edición informada: 2026-10-19T20:23:07.030-0300.

## 19/10/2026 — COMENTARIO 10 — Respaldo del comentario 9

\[JIRA-GITHUB-SYNC\]

Conservé una captura nueva de mis siete tareas, incluyendo la investigación de antecedentes CanSat y rotor generador del comentario 9. No sustituí capturas ni comentarios anteriores. Verifiqué los manifiestos, los enlaces locales y que los cambios publicados pertenecen únicamente a ground-station; main conserva su versión anterior.

Captura y registro de publicación: https://github.com/edulandoni/astra-cansat/commit/074f5a64570c1bcdc1dca8f53700e4a16b3714ef

Índice de la captura: https://github.com/edulandoni/astra-cansat/tree/074f5a64570c1bcdc1dca8f53700e4a16b3714ef/ground-station/historial-jira/2026-10-19-23-22-39-UTC_17298caaaa4f

Este aviso identifica el respaldo ya publicado; no dispara otra captura por sí solo.

### 2026-10-19T20:41:50.606-0300 — comentario 10060

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10060). Última edición informada: 2026-10-19T20:41:50.606-0300.

## 19/10/2026 — COMENTARIO 11 — ACTUALIZACIÓN de ubicación de los comentarios 4 a 10

Corregí la mezcla de temas en esta tarea. Mantengo intactos los originales y sus archivos; no traslado ni borro comentarios. Desde esta entrada los avances continúan según su objetivo:

* Comentario 4 (10040): adquisición/parser/CSV permanecen en ASTRA-21; el exportador y respaldo documental de Jira corresponden a ASTRA-33.
* Comentarios 5, 7 y 10 (10047, 10050 y 10053): respaldo Jira → GitHub y su control continúan en ASTRA-33, comentario 2: https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10055
* Comentario 6 (10049): la investigación de calidad y prevención continúa en ASTRA-34, comentario 1: https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10056
* Comentario 8 (10051): sus ensayos concretos de registro, errores de escritura, reconexión virtual y reconciliación CSV sí corresponden a esta tarea; conservo aquí su bitácora técnica y la relaciono con ASTRA-34.
* Comentario 9 (10052): la revisión de otros CanSat continúa en ASTRA-35, comentario 1: https://astrateam2026.atlassian.net/browse/ASTRA-35?focusedCommentId=10057 ; el análisis del rotor generador continúa en ASTRA-36, comentario 1: https://astrateam2026.atlassian.net/browse/ASTRA-36?focusedCommentId=10058

El respaldo de CSV de vuelo pertenece a esta tarea; el respaldo de documentación de Jira pertenece a ASTRA-33. Son dos trabajos distintos.

ASTRA-21 conserva su descripción y estado En curso: todavía faltan pruebas físicas, operación degradada y acuerdos de sesión/esquema. Esta reorganización no prueba funciones nuevas ni cambia requisitos. Las referencias antiguas en documentos y commits se conservan como historial y tendrán un mapa de ubicación vigente en GitHub.

### 2026-10-19T21:03:41.482-0300 — comentario 10069

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10069). Última edición informada: 2026-10-19T21:03:41.482-0300.

## 19/10/2026 — COMENTARIO 12 — ACTUALIZACIÓN de registros y semántica con fuentes del aula

La respuesta oficial permite formato propio justificado y considera las dos altitudes, con barométrico ajustado a cero al lanzamiento: https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2961#p50091 y https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2959#p50085

La consecuencia para el receptor/CSV es conservar versión del esquema y unidades, distinguir altitud barométrica relativa de altitud GPS y registrar calibración/eventos sin renombrar columnas como si fueran equivalentes. El datum de GPS y la semántica final necesitan acuerdo de interfaz; no los deduzco de la aclaración. La tensión solar debe incorporarse al esquema acordado.

No cambié parser ni archivos originales: el adaptador actual aún usa el perfil heredado y rechaza extensiones sin esquema. Los ensayos sintéticos y los pendientes físicos conservan su alcance. Esta lectura no acredita captura solar, comandos o robustez nuevos.

Esta tarea conserva sólo efectos sobre recepción y almacenamiento de datos de vuelo. El inventario y las contradicciones generales quedan en ASTRA-37 y el respaldo documental en ASTRA-33. Fuente/versión: https://github.com/edulandoni/astra-cansat/blob/5f9d8c310ecbecc9e1b7d0cc8d29d5d43df7b406/ground-station/docs/aula/2026-10-19/revision-aula.md

### 2026-10-23T21:43:38.125-0300 — comentario 10112

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10112). Última edición informada: 2026-10-23T21:43:38.125-0300.

23/10/2026 — COMENTARIO 13 — Capturador reproducible para la primera prueba USB física

Agregué probar_banco_usb.py para conservar los bytes USB originales, usar nuestro parser y registrador CSV existentes y guardar un resultado por sesión: recibidos, únicos, huecos observados, duplicados, rechazos, estados, tiempos de llegada, errores y huellas. No cambié las fuentes originales del banco. --scenario sólo etiqueta el firmware ya cargado; no transmite comandos ni selecciona escenarios. --reset solicita un reinicio por RTS, no un corte eléctrico.

La ventana inicial de0,5segundos queda explícitamente fuera del parser y conservada en crudo porque el sketch conocido empieza al segundo; no debe reutilizarse sin revisión con otro firmware. Cada ejecución crea una carpeta nueva. El resultado nominal exige contadores1–131, llegada aLANDED y ausencia de rechazos, desbordes o errores. Los tiempos son observaciones de PC/USB, no latencia RF.

Comprobé sintaxis y ayuda del capturador, la compilación a través del nuevo comando PowerShell y las nueve pruebas existentes de parser/registro. La recepción de misión física sigue pendiente de cargar la placa: ASTRA-20 registra identificación correcta por COM5, procedimiento BOOT y lectura de respaldo interrumpida. No declaro el capturador validado contra una misión física todavía.

[Capturador](https://github.com/edulandoni/astra-cansat/blob/f1585c3c647e34740b46b494b73b85c52a9d8e55/ground-station/tools/probar_banco_usb.py) · [Guía y comandos](https://github.com/edulandoni/astra-cansat/blob/f1585c3c647e34740b46b494b73b85c52a9d8e55/ground-station/docs/2026-10-23-banco-esp32-usb.md) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/f1585c3c647e34740b46b494b73b85c52a9d8e55).

La próxima evidencia debe conservar CSV, recepción cruda, configuración/versión cargada y resultado. No hay sensores reales, RF o respaldo en disco independiente acreditados. Conservo el diario anterior.

### 2026-10-23T22:01:57.059-0300 — comentario 10114

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10114). Última edición informada: 2026-10-23T22:01:57.059-0300.

23/10/2026 — COMENTARIO 14 — ACTUALIZACIÓN COMENTARIO 13: capturador validado con una misión USB física

Ejecuté probar_banco_usb.py con COM5 a 115200, TEAM1000 ficticio, NOMINAL, --reset y --seconds 137. La sesión fue del 23/10 a las 21:53:09–21:55:27 ART, incluida preparación. Recibí y registré los contadores 1–131, 131 únicos, cero duplicados, huecos observados, rechazos o framing_overflows, sin errores de captura o archivo. Llegué a LANDED y guardé Flight_1000.csv. Verifiqué las huellas de los archivos. Los tiempos son de llegada a PC/USB; no son latencia RF ni reloj calibrado de vuelo.

Conservo completos los bytes USB y eventos de arranque localmente. La copia pública incluye el CSV, resultado y 131 eventos accepted, con exclusiones declaradas para el binario original y startup_window; no reescribe los originales. Es un circuito físico ESP32 → CP210x → USB → parser → CSV, con valores de misión generados artificialmente.

Al probar la GUI encontré seis tramas de diagnóstico y una primera muestra precedida por LF, contadas como siete rechazos. Agregué una opción explícita de banco a Acquisition: reiniciar EN/RTS una vez y conservar 0,5 s iniciales fuera del parser, sólo para el sketch conocido que comienza al segundo. La adquisición normal y el parser estricto no activan esa separación. La reconexión no repite deliberadamente ese reinicio; los efectos físicos del controlador/DTR/RTS aún requieren ensayo.

Pasaron once pruebas de software, incluidas dos sobre arranque y reconexión con puerto simulado. La segunda sesión de la GUI también guardó 131 muestras desde el contador 1, sin rechazos; su validación visual queda en ASTRA-22. No afirmo reconexión USB física ni corte de alimentación probado.

[Informe, configuración y límites](https://github.com/edulandoni/astra-cansat/blob/f20d88ed7d0ec93e23a42f4f07f9a05e4c77c12f/ground-station/docs/2026-10-23-prueba-usb-fisica-actualizacion-02.md) · [CSV del ensayo](https://github.com/edulandoni/astra-cansat/blob/f20d88ed7d0ec93e23a42f4f07f9a05e4c77c12f/ground-station/evidence/2026-10-23-esp32-usb/nominal-01/Flight_1000.csv) · [Resultado/huellas](https://github.com/edulandoni/astra-cansat/blob/f20d88ed7d0ec93e23a42f4f07f9a05e4c77c12f/ground-station/evidence/2026-10-23-esp32-usb/nominal-01/resultado.json) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/f20d88ed7d0ec93e23a42f4f07f9a05e4c77c12f). Quedan pruebas físicas de fallos, reinicio/sesión y respaldo en otro disco. Conservo el comentario anterior y mantengo la tarea en curso.

### 2026-10-23T23:27:11.421-0300 — comentario 10117

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10117). Última edición informada: 2026-10-23T23:27:11.421-0300.

23/10/2026 — COMENTARIO 15 — ACTUALIZACIÓN COMENTARIO 14: adquisición y guardado independientes

Implementé en una versión nueva recepción separada de escritores raw/CSV por destino. Cada escritor tiene600eventos pendientes como límite, estado propio, reintentos y archivos nuevos después de escritura incierta. Un fallo raw inyectado dejó funcionando CSV y el otro destino; al recuperar el destino drenó su cola. El desborde informa descartes y rangos de secuencia, con límite declarado del detalle. Es una prueba de software: dos carpetas locales no acreditan soportes independientes.

Separo sesiónPC, boot y run; al cambiar contexto limpio valores actuales y conservo el segmento anterior. Un contador antiguo sin identidad suficiente queda ambiguo. Redetecto sólo si existe un único CP210x; con varios exijo selección explícita. El sondeo nuevo de reconexión recupera contexto si perdí hello; una respuesta tardía antigua no hace retroceder el arranque vigente. Esto quedó ensayado en software; RST y desconexión físicos dedicados siguen pendientes.

En cinco escenarios USB físicos confirmé629filas y2884eventos, sin pendientes ni descartes al cerrar. Contrasté CSV con paquetes y oráculo por segmento. El informe inicial acumulaba rechazos entre casos; conservo ese original y agregué analyze.py y el resultado por segmento, que acredita10rechazos sólo en CORRUPTED_PACKET.

Agregué reproducción con salida nueva y recuperación offline desdeJSONL o CSV dentro del árbol original de sesión/segmento. Genero CSV reconstruido y procedencia; dos copias discrepantes o errores de lectura bloquean escritura automática. Se probaron recuperación desde cada fuente, deduplicación, conflicto y huellas sin cambios. No relleno datos ausentes. Flush+fsync completados no certifican supervivencia eléctrica.

[Fuentes y procedimiento](https://github.com/edulandoni/astra-cansat/tree/114616a4dc5d1f09706b623581b9fdd0714621da/ground-station/banco-usb-v0.2) · [Resultado físico](https://github.com/edulandoni/astra-cansat/blob/114616a4dc5d1f09706b623581b9fdd0714621da/ground-station/evidence/2026-10-23-banco02/usb-cinco-escenarios-01.json) · [Informe de aceptación parcial](https://github.com/edulandoni/astra-cansat/blob/114616a4dc5d1f09706b623581b9fdd0714621da/ground-station/docs/2026-10-23-banco02-actualizacion-01.md) · [Commit](https://github.com/edulandoni/astra-cansat/commit/114616a4dc5d1f09706b623581b9fdd0714621da). Pendientes: microSD identificada como disco distinto, recepción externa simultánea por conectividad, corte físico y ≥2hUSB con GUI. Mantengo En curso.

### 2026-10-23T23:48:13.159-0300 — comentario 10129

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10129). Última edición informada: 2026-10-23T23:48:13.159-0300.

23/10/2026 — COMENTARIO 16 — ACTUALIZACIÓN COMENTARIO 15: RST físico, conservación de segmentos e invalidación sin hello

ElRST cambió boot y la captura conservó dosCSV de131filas, contadores1..131 en cada segmento,262confirmados al cerrar, sin huecos/rechazos/duplicados. Antes hubo un intento que quedó en bootloader sin hello, con diagnóstico bruto conservado.

Corregí una limitación: al reconocer el diagnósticoROM de miESP32 en el perfil de banco invalido identidad y valores actuales, GPS/alimentación y órdenes pendientes, sin inventar boot. Un sondeoPOWER_STATUS nuevo y único después de0,5s puede recuperar una identidad cuyo hello se perdió; no repito órdenes anteriores ni reintento indefinidamente. Un bootloader sin firmware puede no responder y el resultado queda explícito.

Pasaron12tests, incluidos arranque sin hello y sondeo único. Reproduje la captura real con el receptor corregido: traswaiting for download quedaepoch vacío/latest vacío/contexto ambiguo; la reproducción completa conserva262únicos. Distingo esta verificación posterior de la captura física que todavía usó el proceso anterior.

Publiqué diario normalizado retirando sólo rutasroot de almacenamiento, con huella del original local yCSV sin cambios. El receptor corregido está abierto para la siguiente prueba de desconexión física. No acredita todavía soporte independiente, corte eléctrico ni≥2h continuas.

[Informe y límites](https://github.com/edulandoni/astra-cansat/blob/0603ad93182850e4ebad856d7a56b54970ddaa30/ground-station/docs/2026-10-23-rst-fisico-actualizacion-03.md) · [Evidencia](https://github.com/edulandoni/astra-cansat/blob/0603ad93182850e4ebad856d7a56b54970ddaa30/ground-station/evidence/2026-10-23-banco02/rst-fisico-05/resultado-rst-05.json) · [Drive verificado](https://drive.google.com/file/d/1A_4vETJ2wQrLxzcoFHSlFh6Tiv1cQs2x/view?usp=drivesdk) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/0603ad93182850e4ebad856d7a56b54970ddaa30). Conservo originales y comentarios anteriores.

### 2026-10-24T00:25:17.549-0300 — comentario 10133

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10133). Última edición informada: 2026-10-24T00:25:17.549-0300.

24/10/2026 — COMENTARIO 17 — ACTUALIZACIÓN COMENTARIO 16: Reconexión y doble soporte comprobados

El primer error del puerto retirado quedó a00:09:15,934ART y la reapertura a00:09:36,329ART. El intervalo20,395s incluye el tiempo desenchufado, no es latencia aislada de redetección. Los controlesGUI durante el corte mostraron ausencia de dato actual; un sondeo nuevo confirmó boot distinto. Después otroRUN guardó1..131 y conservé las131anteriores, enCSVseparados.

Hubo una ráfaga de12899bytes hastaCR: un desborde del encuadre de2048bytes, recuperación del siguiente mensaje válido y bytes observados conservados en bruto. No demostré causa ni llamo a esto reconexión sin anomalías. No fue desborde de almacenamiento: cierre sin descartes/pendientes.

Con el únicoUSB, cerréESP32 y reproduje131tramas aceptadas derivadas de esa captura a velocidad1 conGUI, escribiendoC: yD:. VerifiquéC:disco0/NVMe yD:disco1/USB, independientes. Sólo creé D:/ASTRA_Groundstation_2026-10-24_replay_01/. AmbosCSV1..131; diario,CSVyresumen tienen huellas idénticas entre destinos. Subtipo microSD/pendrive no verificable sólo porUSB, queda sin confirmar.

ReconstruíCSVnuevo desde ambosdiarios:131candidatos únicos, originales sin cambios y resultado idéntico alCSVguardado. No probé extracción en caliente ni corte eléctrico; tampoco recepciónESP32conrespaldoexternosimultáneo. Quedan≥2hcontinuas y pruebasRF/autonomía. Mantengo En curso.

[Informe con evidencia y límites](https://github.com/edulandoni/astra-cansat/blob/2863fee267eeb3f48826e8876e279ca096ab091f/ground-station/docs/2026-10-24-reconexion-y-doble-soporte-actualizacion-04.md) · [Drive verificado](https://drive.google.com/file/d/11qcMyyB8SE5QESRkXl5xLetJK-FeWNE2/view?usp=drivesdk) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/2863fee267eeb3f48826e8876e279ca096ab091f). Conservo entradas y originales.

### 2026-10-24T00:45:43.220-0300 — comentario 10138

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10138). Última edición informada: 2026-10-24T00:45:43.220-0300.

24/10/2026 — COMENTARIO 18 — ACTUALIZACIÓN COMENTARIO 17: Identidad de ejecución, reloj monotónico y verificación prolongada

Corregí la identidad de ejecución del banco para incluir cliente y secuencia. Dos sesiones físicas consecutivas mantuvieron el mismo boot y produjeron run distintos; cada una guardó sus 12 muestras sin huecos, duplicados o rechazos. Conservo las corridas anteriores con sus identificadores históricos.

Agregué UTC y tiempo monotónico transcurrido a los eventos. Uso el segundo para duración y reproducción cuando existe: un ajuste de hora de Windows no debe inventar tiempo de ensayo. Los archivos anteriores siguen usando su información disponible, sin marcas retrospectivas.

Pasaron 15 pruebas de software. El analizador rechazó correctamente una captura USB real de 12 muestras y 10,969 s como prueba de dos horas. Exige cierre de almacenamiento, duración real monotónica, secuencia, equivalencia CSV, escritores drenados y progreso observado de GUI.

El ensayo largo comenzó a 00:36:19 ART con 7261 muestras y ventana de 7280 s, desde snapshot conservado. Su resultado está pendiente. Uso sólo C: con el ESP32 ocupando el único USB; el respaldo en otro disco quedó probado separadamente en la actualización anterior. No afirmo respaldo externo simultáneo, persistencia eléctrica, RF o autonomía.

[Informe y evidencia por revisión](https://github.com/edulandoni/astra-cansat/blob/38ae9999af98395e376030089cf5f2c7447f409f/ground-station/docs/2026-10-24-cadencia-identidad-e-inicio-prolongado-actualizacion-05.md) · [Drive verificado](https://drive.google.com/file/d/1j6m_KdBn266iJZAxvZD4yM1B4rH_MkQ-/view?usp=drivesdk) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/38ae9999af98395e376030089cf5f2c7447f409f). Conservo resultados, fuentes y comentarios anteriores.

### 2026-10-24T01:11:34.326-0300 — comentario 10147

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10147). Última edición informada: 2026-10-24T01:11:34.326-0300.

24/10/2026 — COMENTARIO 19 — ACTUALIZACIÓN del ensayo prolongado: medidor corregido y nuevo intento

Interrumpí deliberadamente la primera corrida tras 1906 muestras y 1905,063 s entre primera y última. El resultado queda false: no son dos horas. No hubo pérdidas declaradas por escritores, errores de encuadre ni conflictos en el segmento nominal, pero la memoria crecía. Aislé la causa: el medidor creaba tipos de ctypes en cada consulta y la caché global los retenía. Tener colas e historial acotados no demostraba memoria total acotada.

Corregí el medidor para definir tipo y API una sola vez. Pasaron 17 pruebas, incluida una de 500 consultas sin nuevos tipos después de inicializar. El nuevo gui_health registra las inicializaciones y el analizador exige una sola. Conservo resultado, salud, huellas, diario y CSV del intento anterior; no los reemplazo ni recalifico como aprobados.

Cerré esa GUI con vaciado de escritores, confirmé liberación de la inhibición transitoria de suspensión y envié STOP de banco antes de la nueva campaña. Inicié otro snapshot el 24/10 a las 01:09:00 ART, con las correcciones del medidor y GPS: 7261 muestras, ventana de 7280 s, cierre previsto cerca de 03:10:20 ART. No recargué firmware ni reinicié físicamente. Calibración, hora, alimentación y RUN quedaron confirmados. La campaña nueva todavía no tiene resultado final.

[Informe, intento interrumpido y configuración nueva](https://github.com/edulandoni/astra-cansat/blob/ce3220891ece63d2fcaa0c7990ec8d3eaa63181f/ground-station/docs/2026-10-24-medidor-y-reinicio-prolongado-actualizacion-07.md) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/ce3220891ece63d2fcaa0c7990ec8d3eaa63181f) · [Drive](https://drive.google.com/file/d/1kBmo1uFNJLebHIolXAUBUiQ9eailEgpe/view?usp=drivesdk). Mantengo los pendientes y las tareas abiertas. No acredita RF, autonomía ni respaldo externo simultáneo.

### 2026-10-24T02:12:04.787-0300 — comentario 10150

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10150). Última edición informada: 2026-10-24T02:12:04.787-0300.

24/10/2026 — COMENTARIO 20 — Conflicto dentro del propio diario: reconstrucción bloqueada

Amplié la revisión del recuperador. Ya comparaba filas contradictorias entre copias, pero ignoraba la marca que deja el receptor cuando dos mensajes válidos tienen igual contador y distinto contenido. El receptor conserva el primero en CSV y registra el conflicto en el diario; el recuperador anterior podía declarar salida limpia desde ese diario aunque conociera la contradicción.

Ahora bloqueo la reconstrucción ante esa marca y explico archivo, línea, contexto y contador. En un caso sintético con contador 1 y altitudes 0,0/999,0 m, comprobé ambas versiones sobre el mismo original: antes escribía una fila; ahora no escribe CSV y registra un conflicto. El original conserva su huella. Pasaron 18 pruebas, incluida esta regresión y los casos previos de copias, CSV/JSONL y recuperación limpia.

No elijo cuál medición es verdadera ni infiero contradicciones ausentes: si sólo selecciono un CSV y falta el diario donde estaba la marca, esa información no está disponible. La herramienta es offline; no cambié firmware ni la GUI que está ejecutando el segundo intento prolongado.

[Informe y comparación antes/después](https://github.com/edulandoni/astra-cansat/blob/dfda37cca6aa97aabcd794932eae2cc42a911e15/ground-station/docs/2026-10-24-recuperacion-conflicto-interno-actualizacion-08.md) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/dfda37cca6aa97aabcd794932eae2cc42a911e15) · [Drive](https://drive.google.com/file/d/1WJHAB2SS6XynnDfCsKNPQJ-2bfINWXZS/view?usp=drivesdk). Conservo las entradas anteriores y sigo esperando el cierre real de la corrida USB.

### 2026-10-24T03:18:10.666-0300 — comentario 10153

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10153). Última edición informada: 2026-10-24T03:18:10.666-0300.

24/10/2026 — COMENTARIO 21 — Aceptación del banco USB y límites para el PDR

Completé adquisición y archivo de 7261 paquetes sintéticos por USB físico durante 7260,328 s reales entre primera y última muestra. El CSV tiene las mismas 7261 filas que los paquetes del diario, contadores 1..7261 y encabezado de 22 campos. Conservé 33234 eventos brutos. No hubo rechazos, desbordes, desconexiones, duplicados o conflictos durante el segmento nominal.

Los escritores raw y CSV cerraron con cero pendientes, errores y descartes. El máximo conjunto observado en controles periódicos fue de cinco pendientes, frente a 600 por escritor; no lo presento como máximo continuo de cada instante. Reconstruí después desde diario y CSV con el recuperador corregido: 7261 candidatos, cero conflictos/errores y originales intactos. La reconstrucción y el CSV adquirido tienen exactamente la misma SHA256: f62404025543b6391957352b5de0c081f91557d6c41f6d1e6fd83643f243e1c2. Comprobé además que el blob publicado en Git conserva esos bytes.

Verifiqué que los módulos activos y el firmware coinciden con el snapshot. El recuperador posterior es una herramienta offline separada. Aclaré que el manifiesto del directorio también contiene 22 productos de compilación ignorados; no se usan en adquisición ni son el artefacto autorizado para recargar. Los 29 archivos versionados sí coinciden byte a byte con el commit de fuente; la aclaración conserva el manifiesto original.

Conservo resultados previos de RST, reconexión y dos soportes. La causa de aquella ráfaga malformada sigue pendiente. La copia simultánea ESP32+soporte externo, persistencia eléctrica y RF no quedan acreditadas. El soporte externo ensayado era otro disco USB; no confirmé si era tarjeta o pendrive. El detalle de pérdidas tiene límites explícitos; no prometo conservación infinita.

[Informe final y matriz de la etapa](https://github.com/edulandoni/astra-cansat/blob/44bf6ea88a04acfa460dd77bdb8c62d4a6fb9a29/ground-station/docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md) · [Commit de resultados verificado](https://github.com/edulandoni/astra-cansat/commit/44bf6ea88a04acfa460dd77bdb8c62d4a6fb9a29) · [Drive: informe final](https://drive.google.com/file/d/1i-pRyjTcZRqRaD8nuIt3MrOW22W6Hu90/view?usp=drivesdk) · [Aclaración de reproducción](https://github.com/edulandoni/astra-cansat/blob/838e0a187472e0d7dcc2f6c4f8dee8abf5856c4d/ground-station/docs/2026-10-24-control-reproduccion-actualizacion-10.md) · [Drive: control de fuentes](https://drive.google.com/file/d/1fEv5ZasO5i-YNfuKfulLwAH6NjjiO8yn/view?usp=drivesdk).

### 2026-10-24T03:58:56.239-0300 — comentario 10160

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10160). Última edición informada: 2026-10-24T03:58:56.239-0300.

24/10/2026 — COMENTARIO 22 — ACTUALIZACIÓN: Conservación del evento antes de escribir y verificación USB final

Corregí un riesgo del registro asíncrono: un evento podía conservar referencias a listas o diccionarios que luego cambiaban antes de escribirse. Ahora guardo una copia profunda al emitir y devuelvo otra copia independiente. La prueba retiene al escritor, modifica el dato original y la copia devuelta y comprueba que el registro conserva el valor inicial. No atribuyo por esto corrupción a capturas históricas.

Pasaron las 22 pruebas unitarias del banco. Agregué un reloj inyectable para los ensayos; en operación normal se mantiene el reloj monotónico real. Repetí después la campaña USB: 131 registros válidos nuevos, contadores 1–131, CSV igual a los valores recibidos, 658 eventos brutos, escritores vaciados y sin pérdidas ni errores de almacenamiento. Verifiqué huellas de los originales publicados; conservé también la primera pasada.

La prueba previa de dos horas sigue como evidencia de aquella revisión. Esta modificación quedó cubierta por pruebas unitarias y una campaña física corta nueva; no la presento como otra prueba de dos horas. La tarea continúa con los criterios de formato e integración todavía pendientes.

[Corrección, procedimiento y comprobaciones](https://github.com/edulandoni/astra-cansat/blob/9735087c1074754895273c4109553f5b350c7faf/ground-station/docs/2026-10-24-bitacora-copias-y-verificacion-final.md)
[Copia verificada en Drive](https://drive.google.com/file/d/130V3pxXsMDwD4hM3tR3ewnrlnGu077PT/view)

[Ensayo USB y evidencia en GitHub](https://github.com/edulandoni/astra-cansat/blob/9735087c1074754895273c4109553f5b350c7faf/ground-station/docs/2026-10-24-ordenes-negativas-usb.md)
[Copia verificada en Drive](https://drive.google.com/file/d/1QplaMWPe9rHV-rlbhus5V2BN5VqaE4lY/view)

### 2026-10-25T23:29:09.180-0300 — comentario 10170

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10170). Última edición informada: 2026-10-25T23:29:09.180-0300.

25/10/2026 — COMENTARIO 23 — ACTUALIZACIÓN: cortes USB y alcance de los contadores

Separé conexión, identidad del emisor y antigüedad de la última muestra. Conservo el último dato como histórico durante un corte, sin mostrarlo como actual. Registro una interrupción por corte y distingo si vuelve el mismo arranque/ejecución, si la placa reinicia o si falta identidad suficiente. Esperando guardado cuenta datos recibidos pendientes de escritura; no cuenta mensajes ausentes. Mientras no puedo comparar contadores muestro faltantes por determinar. Los mensajes tardíos pueden reducir los huecos actuales.

Probé una desconexión física y reconexión del ESP32: corte detectado de 10,14 s, nuevo arranque confirmado y cantidad de mensajes ausentes desconocida. El tiempo incluye detección y reapertura de Windows; no lo presento como medición exacta del tiempo que estuvo desenchufado. En esa sesión guardé 312 muestras entre ejecuciones, con cero pendientes, errores o descartes al cerrar. Conservé una trama excesiva tras reconectar; su causa sigue pendiente.

En la versión final probé además cerrar y abrir el puerto desde la aplicación: corte detectado de 17,375 s, misma identidad y contador 65 → 84, hueco observable de 18 muestras. Al terminar llegaron 113 muestras hasta el contador 131; las 113 quedaron en CSV, con cero pendientes, errores y descartes de almacenamiento. No lo califico como campaña nominal sin pérdidas: el hueco fue provocado al cerrar el receptor. No hubo tramas excesivas en ese ensayo.

Pasaron 30 pruebas de software del banco, calidad e interfaz, incluyendo reinicio, identidad insuficiente, reparación de huecos, parada esperada y resultados de órdenes de otra ejecución. Publiqué métricas normalizadas, huellas y capturas; conservo diarios y CSV originales privadamente. No cambié firmware ni RF, no repetí las dos horas de la revisión anterior y no acredito resistencia eléctrica, autonomía ni copia externa simultánea. Mantengo la tarea en curso por la integración y criterios pendientes.

[Informe, pruebas y límites](https://github.com/edulandoni/astra-cansat/blob/caeac641b2e9c319c9430d9ea77429761487f898/ground-station/docs/2026-10-25-interfaz-y-cortes-usb.md) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/caeac641b2e9c319c9430d9ea77429761487f898) · [Copia verificada en Drive](https://drive.google.com/file/d/1VWU1Pd1KdSjfwjtSn-LmJwobT6fQLu5E/view)

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

