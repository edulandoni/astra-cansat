# Groundstation y manejo de datos

## Fotos verificadas desde el lector — 26/10/2026

[Lectura independiente de las dos fotos de la cámara 2](docs/camaras/2026-10-26-lectura-independiente-camara-2-06.md): coinciden byte por byte con las recibidas por USB después de desconectar la cámara; los 24 archivos anteriores también permanecen intactos. Falta comprobar SD en la otra unidad, video y control de energía. Las entradas siguientes conservan los cortes anteriores.

## Guardado de fotos desde la cámara 2 — 26/10/2026

[Dos fotos nuevas con escritura y lectura desde la cámara](docs/camaras/2026-10-26-dos-fotos-sd-camara-2-05.md): el montaje y guardado funcionaron con MBR/FAT32, sin cambiar firmware. Falta lectura independiente con el lector, ensayo de la otra cámara, video y control de energía. Las entradas siguientes conservan los cortes anteriores.

## Dos cámaras con fotos USB y tarjeta preparada — 26/10/2026

[Cámara 2: seis fotos válidas y diagnóstico del montaje SD](docs/camaras/2026-10-26-camara-2-sd-03.md) · [Preparación MBR/FAT32 y reposición verificada de los 24 archivos](docs/camaras/2026-10-26-microsd-mbr-restauracion-04.md). Ambas unidades ya produjeron fotos USB; el guardado desde la cámara, video y control de energía siguen pendientes. Las entradas siguientes conservan los cortes anteriores.

## Primeras fotos de cámara A — 26/10/2026

[Ensayo físico, intentos fallidos y cinco fotos USB correctas](docs/camaras/2026-10-26-camara-a-prueba-fisica-02.md), con respaldo original conservado. Todavía no acredita segunda cámara, microSD, video ni control de energía.

## Preparación local de cámaras — 26/10/2026

[Banco USB de cámaras](camaras-banco/README.md) y [control de preparación](docs/camaras/2026-10-26-banco-local-preparacion-01.md): firmware candidato compilado y receptor probado con JPEG de PC. La carga, fotos de ambas cámaras, SD, energía y grabación física siguen pendientes; el objetivo completo continúa en ASTRA-39.

## Cámaras y definición de comandos — 25/10/2026

Inicié [el estudio de apagado en espera, grabación y chequeo dual de ESP32-CAM](docs/camaras/2026-10-25-energia-chequeo-dual.md) en [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39), con fuentes y ensayos pendientes. La [decisión de coordinación de comandos](docs/interfaces/2026-10-25-comandos-definidos-desde-vuelo.md) establece que Edu define vuelo y adapto groundstation; el banco USB conserva su perfil experimental.

## Interfaz y cortes USB — 25/10/2026

[Pantalla explicada, reconexión física y cierre manual del puerto](docs/2026-10-25-interfaz-y-cortes-usb.md): cuatro grupos de mediciones con ayuda, seis contadores con su alcance, datos históricos identificados y huecos visibles. El informe conserva resultados, capturas y límites de esta revisión nativa.

## Lectura vigente — 24/10/2026

Desarrollo en [banco USB v0.2](banco-usb-v0.2/README.md). El [estado de mis 13 tareas y los avances de esta pasada](docs/historial/2026-10-24-revision-tareas-y-avances.md) enlaza implementación, pruebas y pendientes. La [aceptación prolongada previa](docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md) conserva sus versiones; no se atribuye a cambios posteriores. El banco v0.1 y las entradas iniciales siguen como referencia histórica.

## Incorporación del 23/10/2026 — banco experimental v0.2

[Banco resistente a fallos y USB bidireccional](banco-usb-v0.2/README.md) · [Resultados y pendientes de aceptación](docs/2026-10-23-banco02-actualizacion-01.md). Conservo v0.1 y todas las entradas anteriores. La línea nueva distingue simulación, USB físico y pruebas aún pendientes; no aprueba RF ni el protocolo de vuelo.

También preparé la [propuesta de interfaz para revisar con Edu](docs/interfaces/2026-10-23-propuesta-banco-y-vuelo.md), la [comparación preliminar de antenas y enlace](docs/interfaces/2026-10-23-antenas-y-link-budget-preliminar.md) y la [tabla de antecedentes a pruebas](docs/investigacion/2026-10-23-antecedentes-a-pruebas.md).

La [actualización02 del módulo y los comandos](docs/interfaces/2026-10-23-modulo-radio-y-comandos-actualizacion-02.md) agrega la referencia informada por Edu, la discrepancia de pinout con la foto y un cálculo reproducible de tiempo de aire. No configura RF ni confirma aún la variante física.

La [actualización03 del ensayo RST](docs/2026-10-23-rst-fisico-actualizacion-03.md) conserva la incidencia de modo descarga, la recepción posterior1..131 y la corrección del receptor cuando no llega una identidad nueva.

La [actualización04 del24/10](docs/2026-10-24-reconexion-y-doble-soporte-actualizacion-04.md) agrega reconexiónUSB, una anomalía de encuadre conservada, reproducción enC:+otro discoUSB y reconstrucción coincidente; las dos horas y la nueva carga siguen pendientes en ese corte.

La [actualización 05](docs/2026-10-24-cadencia-identidad-e-inicio-prolongado-actualizacion-05.md) verifica la cadencia corta y la identidad entre sesiones e inicia el ensayo prolongado. Su inicio no acredita el resultado de dos horas.

Me encargo de recibir, registrar y mostrar la telemetría en tierra. Esta carpeta reúne mi código, pruebas y decisiones. La rama `groundstation` es mi línea de trabajo del subsistema; no establece reglas para las otras áreas del equipo.

La [actualización de potencia y tiempo de aire del 24/10](docs/interfaces/2026-10-24-radio-potencia-y-airtime-actualizacion-03.md) contrasta la hoja Semtech de 2020 y explicita el riesgo de suponer máxima potencia y telemetría de un paquete por segundo sin evaluar el perfil conjunto.

La [actualización 06](docs/2026-10-24-gps-presentacion-actualizacion-06.md) corrige la presentación sin solución GPS y verifica que el dato original se conserve. Es posterior al snapshot del ensayo prolongado.

La [actualización 07](docs/2026-10-24-medidor-y-reinicio-prolongado-actualizacion-07.md) conserva un intento prolongado interrumpido, identifica una acumulación del medidor de memoria y registra la corrección y el segundo intento. No declara todavía dos horas aprobadas.

La [actualización 08](docs/2026-10-24-recuperacion-conflicto-interno-actualizacion-08.md) evita declarar limpia una reconstrucción cuando el propio diario ya registra un conflicto entre mensajes del mismo contador.

La [actualización 09: aceptación del banco USB](docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md) reúne el resultado prolongado de 7261 paquetes en 2 h 1 min reales, reconstrucción coincidente, matriz completa de la etapa y límites para el PDR.

La [actualización 10](docs/2026-10-24-control-reproduccion-actualizacion-10.md) aclara qué archivos del manifiesto pertenecen a Git y qué artefactos ignorados quedaron copiados sin usarse durante la adquisición.

## Por dónde empezar

| Necesidad | Ubicación |
| --- | --- |
| Probar sin placa ni antena | [Banco USB v0.2](banco-usb-v0.2/README.md) |
| Saber qué funciona y qué falta | [Revisión vigente del 24/10](docs/historial/2026-10-24-revision-tareas-y-avances.md) |
| Entender cómo guardo la historia | [Metodología](docs/metodologia-2026-10-19.md) |
| Revisar las pruebas | [Matriz de aceptación y límites](docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md) |
| Entender el cambio de reglamento | [Comparación v1/v2 para tierra](docs/requisitos/v1-v2-groundstation-2026-10-19.md) |
| Entender qué necesito acordar con vuelo | [Ficha de interfaz pendiente](docs/interfaces/pendientes-groundstation-2026-10-19.md) |
| Ir del código a su motivo en Jira | [Mapa de trazabilidad](docs/trazabilidad-2026-10-19.md) |
| Leer las capturas de Jira | [Historial de Jira](historial-jira/README.md) |
| Revisar simuladores anteriores | [Archivo DEPRECATED](archive/DEPRECATED/README.md) |
| Entender el respaldo diario | [Automatización](docs/respaldo-jira-2026-10-19.md) |
| Investigar mejoras sin hardware | [Prevención de fallas y oportunidades](docs/investigacion/2026-10-19-innovacion-y-prevencion.md) |
| Revisar desconexiones y recuperación de archivos | [Ensayos de resiliencia](docs/investigacion/2026-10-19-resiliencia-y-recuperacion.md) |

## Estado histórico de la incorporación del 19/10 — conservado

Conservo el banco Python y el sketch ESP32 del 17/10 sin alterar sus fuentes. El banco puede generar datos ficticios en la computadora. El sketch todavía no tiene compilación ni prueba física acreditadas. No hay validación de radio, antena, alcance, dos horas de autonomía ni persistencia ante corte real.

El formato de 22 campos y TEAM_ID de cuatro dígitos es una convención heredada de v1 para practicar; no lo presento como formato obligatorio del anexo v2 ni como protocolo acordado con Edu. `1000` es ficticio.

Las entradas fechadas y las capturas se conservan. Una conclusión nueva se agrega en otro documento o comentario con referencia al anterior. Este índice puede incorporar enlaces a nuevas entradas; su versión inicial queda en Git.

Jira es la bitácora principal: [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20), [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21), [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22).

## Investigación agregada el 19/10/2026

- [Antecedentes CanSat y catálogo de 35 registros](docs/investigacion/2026-10-19-antecedentes-cansat.md).
- [Autorrotación y generación eléctrica: antecedentes, límites y cálculo](docs/investigacion/2026-10-19-rotor-y-generacion.md).

## Ubicación de los temas — actualización del 19/10/2026

Para continuar el diario uso el [mapa vigente](docs/trazabilidad-vigente-2026-10-19.md). Los enlaces de las entradas anteriores conservan su contexto histórico.

- [ASTRA-33: diario, trazabilidad y respaldo](docs/temas/diario-y-respaldo/README.md).
- [ASTRA-34: investigación de calidad de datos](docs/temas/calidad-de-datos/README.md).
- [ASTRA-35: antecedentes CanSat](docs/temas/antecedentes-cansat/README.md).
- [ASTRA-36: rotor y generación eléctrica](docs/temas/rotor-y-energia/README.md).
- [Revisión de los 35 comentarios y corrección de referencias](docs/historial/2026-10-19-orden-comentarios.md).

El receptor y los ensayos de CSV siguen en ASTRA-21; el respaldo de documentación de Jira continúa en ASTRA-33. Los originales permanecen íntegros.

## Incorporación del 19/10/2026 — Aula CONAE

[Revisión del aula oficial, plantillas PDR y aclaraciones](docs/aula/2026-10-19/revision-aula.md), con bitácora propia en [ASTRA-37](https://astrateam2026.atlassian.net/browse/ASTRA-37). Los informes anteriores se conservan.

## Objetivo activo — documentación oficial completa

[Inventario de cobertura y revisión diaria del aula](docs/aula/2026-10-19/objetivo-cobertura-total.md). La revisión inicial no se considera 100%; el audio y la auditoría exhaustiva de archivos siguen abiertos en ASTRA-37.

## Avance de cobertura — segunda lectura del 19/10/2026

Completé la [auditoría de los cuatro archivos](docs/aula/2026-10-19/auditoria-archivos-actualizacion-01.md), con [controles verificables](docs/aula/2026-10-19/control-archivos-actualizacion-01.json). Agregué el [análisis asistido de los audiovisuales y una consulta nueva](docs/aula/2026-10-19/audiovisuales-y-foro-actualizacion-02.md). El [inventario ampliado](docs/aula/2026-10-19/cobertura-actualizacion-02.json) reúne 22 recursos y conserva los límites del reconocimiento de voz y el muestreo visual. El objetivo de 100% sigue activo; no se presenta una revisión audiovisual asistida como certificación exhaustiva.

## Cierre documental del corte del 19/10/2026

La [actualización 03](docs/aula/2026-10-19/referencias-y-verificacion-actualizacion-03.md) incorpora las referencias oficiales enlazadas desde bases, el reglamento de participación, la segunda lectura íntegra del audio y el control de toda la línea visual. El [inventario vigente de 30 entradas](docs/aula/2026-10-19/cobertura-actualizacion-03.json) registra el material disponible analizado y conserva métodos, límites y dudas. La revisión diaria sigue activa para cambios y publicaciones pendientes. Este cierre documental no certifica hardware, cumplimiento de la misión o exactitud infalible de las herramientas.

## Organización de Drive — actualización del 20/10/2026

La [entrada actual de Drive](https://drive.google.com/file/d/12H-VdifFyThzj4Tz-kXOLtM6EO0BBj49/view?usp=drivesdk) reúne el acceso por temas de groundstation. La [actualización de organización](docs/organizacion-drive/2026-10-20/Reorganizacion_Drive_2026-10-20.md) conserva las ubicaciones anteriores, el mapa Drive–Jira–GitHub, las verificaciones y la pauta de mejora continua. Las entradas anteriores siguen describiendo sus fechas; para continuar uso esta navegación y las actualizaciones posteriores.

## Análisis diario del aula e investigación — actualización del 20/10/2026

El [primer panorama priorizado del 20/10](docs/aula/2026-10-20/Informe_aula_2026-10-20_1156_ART.md) explica preguntas, respuestas, publicaciones y pendientes. El diario de ese análisis continúa en [ASTRA-38](https://astrateam2026.atlassian.net/browse/ASTRA-38); [ASTRA-37](https://astrateam2026.atlassian.net/browse/ASTRA-37) mantiene fuentes y cobertura. La [metodología del corte diario](docs/aula/2026-10-20/Metodo_analisis_diario_2026-10-20.md) actualiza la cadencia sin borrar las entradas anteriores. La [revisión de antecedentes, código y fotos](docs/investigacion/2026-10-20-antecedentes-codigo-y-fotos.md) y su [catálogo visual](docs/investigacion/2026-10-20-catalogo-visual-cansat.csv) documentan el avance en ASTRA-35.

## Primera placa física — actualización del 23/10/2026

[Identificación, controlador, secuencia BOOT y herramientas de banco USB](docs/2026-10-23-banco-esp32-usb.md). El registro distingue preparación y compilación de carga y recepción física; conservo el estado histórico anterior. Diario en ASTRA-20 y ASTRA-21.

## Misión USB física — actualización posterior del 23/10/2026

[Primera misión completa, respaldo original y corrección del inicio de la GUI](docs/2026-10-23-prueba-usb-fisica-actualizacion-02.md). Recibí 131 muestras sintéticas desde la placa y otras 131 en la pantalla; conservo la preparación y el primer intento de GUI por separado.
