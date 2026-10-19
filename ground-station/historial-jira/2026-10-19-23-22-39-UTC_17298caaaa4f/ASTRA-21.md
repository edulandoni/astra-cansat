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

