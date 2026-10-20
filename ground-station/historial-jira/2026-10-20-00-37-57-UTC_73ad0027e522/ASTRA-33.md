# ASTRA-33 — DOC — Mantener diario, trazabilidad y respaldo de groundstation

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-33)

Estado observado: En curso. Asignación: Cristian Ponsone. Creación: Cristian Ponsone.

## Descripción original consultada

## Objetivo

Conservar el diario y el respaldo Jira → GitHub de mi área con trazabilidad por tema. Jira es la fuente del razonamiento para el PDR; GitHub conserva código, evidencias y versiones.

## Alcance

Metodología sin sobrescritura, índices, mapa de comentarios y archivos, exportador de capturas y respaldo diario. Sólo mis tareas y ground-station/ en la rama groundstation. No regula cómo trabajan otras áreas.

## Resultado esperado y cierre

Cada avance tiene tarea temática, fecha, objetivo, resultados, límites y evidencia. Las correcciones enlazan originales; no se borran, editan ni trasladan físicamente comentarios históricos. El respaldo consulta todas las páginas y verifica pertenencia; conserva capturas y excluye datos privados. Sus avisos se registran aquí. La programación y la máquina deben estar disponibles; no prometo un servicio independiente permanente.

## Estado real al crear esta tarea

El método, exportador y respaldo ya están documentados y tienen verificaciones previas. Inicio esta tarea para ordenar la ubicación de sus registros; no atribuyo ensayos nuevos. Las entradas procedentes de ASTRA-20 y ASTRA-21 se incorporarán mediante comentarios nuevos con enlaces de origen. La tarea continúa como mantenimiento En curso.

## Comentarios conservados

### 2026-10-19T20:41:04.561-0300 — comentario 10054

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10054). Última edición informada: 2026-10-19T20:41:04.561-0300.

## 19/10/2026 — COMENTARIO 1 — Diario de mi área y corrección de ubicación

### Motivo y criterio

Separé el mantenimiento de la bitácora de las tareas de desarrollo. Antes registré metodología y avisos generales en el simulador ASTRA-20 y en el receptor ASTRA-21; esa ubicación mezcló sus objetivos. Desde esta entrada, esta tarea es la referencia para diario, trazabilidad y respaldo. No borro, edito ni traslado físicamente los originales. Estas incorporaciones son una reorganización de trabajo anterior, no avances nuevos repetidos.

### Método vigente

Escribo en primera persona por mi trabajo y en plural por el equipo. Registro fecha real y número correlativo dentro de cada tarea; para una actualización enlazo la entrada original y explico cambio, motivo, evidencia y efectos. Conservo descripciones, comentarios, adjuntos, archivos y versiones anteriores. Una copia no autoriza a sustituirlos.

Cada avance registra problema y requisitos, objetivo, trabajo y alternativas, configuración/versión, pruebas y resultados, evidencia, límites, pendientes y qué puedo afirmar en el PDR. Jira conserva el razonamiento; GitHub conserva código/evidencias y referencias de ida y vuelta. Un enlace aislado no reemplaza el relato.

Cada tema tiene su tarea. Backlog se reserva a ideas no asumidas; Por hacer a trabajo comprometido sin comenzar; En curso a trabajo iniciado. Sólo gestiono tareas creadas por mí o asignadas a mí, y sólo publico en mi rama groundstation y ground-station/. Este método se aplica a mi área, sin imponerlo al resto.

### Procedencia e historial

La metodología fija original sigue íntegra en ASTRA-20, comentario 5 del 17/10:  
https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10037  
La entrada previa sobre voz y estados se conserva:  
https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10036

Documento histórico: https://github.com/edulandoni/astra-cansat/blob/a1a7d383ed4498b540c0f7a12500a66f84bc3551/ground-station/docs/metodologia-2026-10-19.md  
La referencia histórica a ASTRA-20 se entiende como origen, no como ubicación futura de la metodología.

Creé y pasé esta tarea por las transiciones disponibles hasta En curso porque ya existe implementación/documentación y ahora estoy manteniendo su organización. No cierro los desarrollos por esta corrección.

### 2026-10-19T20:41:06.830-0300 — comentario 10055

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10055). Última edición informada: 2026-10-19T20:41:06.830-0300.

## 19/10/2026 — COMENTARIO 2 — Respaldo Jira → GitHub y antecedentes incorporados

### Trabajo que corresponde a esta tarea

El exportador guardar_bitacora.py recibe una lectura normalizada y verificada; no inicia sesión ni consulta Jira por sí solo. Guarda carpetas nuevas con JSON, documentos legibles, índice y manifiestos. Comprueba pertenencia y páginas completas. La copia pública omite correos, identificadores de cuenta y comentarios restringidos/internos; no incluye adjuntos binarios ni reacciones. Jira conserva los originales.

La automatización de este chat quedó programada diariamente a las 21:00 de Argentina y complementa el cierre de cada tanda. Depende de aplicación, máquina y conexiones. Hoy actualicé su destino de avisos a ASTRA-33, conservando horario, estado ACTIVE y política failed_runs_only. La confirmación del cambio acredita configuración, no una ejecución futura.

### Corrección técnica anterior que conservo

El primer control de deduplicación no reconocía la etiqueta del respaldo escapada por Jira y creó una captura adicional. Se corrigió para admitir formas normal/escapada y comparar huellas anteriores sin reescribir manifiestos. La verificación anterior informó cinco pruebas aprobadas y «Sin cambios» al repetir la lectura real. No repito esos ensayos en esta reorganización ni los atribuyo al simulador o al parser.

### De dónde provienen las entradas

ASTRA-20: comentarios 6 (parte de publicación general), 7, 8 y 9:  
https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10039  
https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10045  
https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10046  
https://astrateam2026.atlassian.net/browse/ASTRA-20?focusedCommentId=10048

ASTRA-21: comentario 4 (sólo exportador/respaldo), 5, 7 y 10:  
https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10040  
https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10047  
https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10050  
https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10053

Los apartados técnicos de simulador/parser de las entradas mixtas permanecen vinculados a sus tareas. El respaldo de documentación de Jira es distinto del respaldo de CSV de vuelo: este último sí corresponde a ASTRA-21.

### Evidencia conservada y pendientes

Exportador y pruebas: https://github.com/edulandoni/astra-cansat/tree/groundstation/ground-station/tools  
Capturas anteriores: https://github.com/edulandoni/astra-cansat/tree/groundstation/ground-station/historial-jira  
Corrección anterior: https://github.com/edulandoni/astra-cansat/commit/4fe04e377c9a786dc15dec4e406010c534b3a1bc

Falta verificar cada ejecución futura y mantener la clasificación al incorporar temas nuevos. No reescribo comentarios ni mensajes de commits históricos. Los avisos generales siguientes pertenecen exclusivamente a esta tarea.

### 2026-10-19T20:43:59.081-0300 — comentario 10061

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10061). Última edición informada: 2026-10-19T20:43:59.081-0300.

## 19/10/2026 — COMENTARIO 3 — Auditoría y mapa temático publicados

Revisé los 35 comentarios existentes en mis siete tareas antes de la corrección: 23 conservan su ubicación, 8 continúan en una tarea propia y 4 tenían temas mezclados que desglosé. No edité ni eliminé comentarios anteriores. ASTRA-20 recibió la aclaración 10059 y ASTRA-21 la 10060, ambas con enlaces al destino.

Creé ASTRA-33/34/35/36, asignadas a mí y En curso porque los trabajos ya comenzaron. Los ensayos concretos de reconexión, almacenamiento y recuperación CSV siguen en ASTRA-21. No cambié estados, responsables o descripciones de las siete tareas anteriores.

En GitHub consulté la lista del repositorio y los comentarios de conversación/revisión: el PR histórico 1 no tenía comentarios que reubicar. Conservé archivos fechados y mensajes de commits; agregué un mapa vigente, guías por tema y clasificación de cada comentario. La auditoría explica también la asociación corregida de los commits históricos, sin reescribirlos.

Comprobé 187 archivos preexistentes conservados byte por byte; sólo amplié README y AGENTS de mi área, además de crear los documentos nuevos. Revisé enlaces locales, manifiestos de las ocho capturas históricas y ausencia de cadenas de credenciales. No modifiqué código ni ejecuté ensayos técnicos nuevos.

Actualicé la automatización existente: sus avisos van exclusivamente a ASTRA-33. Verifiqué en la configuración guardada que mantiene ACTIVE, horario diario 21:00 y notificaciones failed_runs_only. Una ejecución futura sigue pendiente; esta revisión no la simula.

Auditoría completa: https://github.com/edulandoni/astra-cansat/blob/a4c26b05bc66ef77efa702f03256e4bb3ba2d3c8/ground-station/docs/historial/2026-10-19-orden-comentarios.md  
Clasificación: https://github.com/edulandoni/astra-cansat/blob/a4c26b05bc66ef77efa702f03256e4bb3ba2d3c8/ground-station/docs/comentarios-clasificados-2026-10-19.json  
Mapa vigente: https://github.com/edulandoni/astra-cansat/blob/a4c26b05bc66ef77efa702f03256e4bb3ba2d3c8/ground-station/docs/trazabilidad-vigente-2026-10-19.md  
Actualización del respaldo: https://github.com/edulandoni/astra-cansat/blob/a4c26b05bc66ef77efa702f03256e4bb3ba2d3c8/ground-station/docs/respaldo-jira-actualizacion-2026-10-19.md  
Cambio: https://github.com/edulandoni/astra-cansat/commit/a4c26b05bc66ef77efa702f03256e4bb3ba2d3c8

Esta entrada corrige la ubicación; los originales siguen visibles y enlazados como historial. Mantener este mapa al incorporar temas nuevos es trabajo de esta tarea.

### 2026-10-19T20:45:13.482-0300 — comentario 10065

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10065). Última edición informada: 2026-10-19T20:45:13.482-0300.

## 19/10/2026 — COMENTARIO 4 — Respaldo de cierre de la corrección temática

\[JIRA-GITHUB-SYNC\]

Publiqué una captura nueva de mis once tareas, con 46 comentarios y el historial consultado. Comprobé que los 35 comentarios previos conservan cuerpo y fechas, y que las siete tareas anteriores mantienen título, descripción, creador, responsable y estado. Las cuatro nuevas tareas están asignadas a mí y En curso.

Captura: https://github.com/edulandoni/astra-cansat/tree/c8596057d0cfcb04ffacef89819daa5f90b9f7a9/ground-station/historial-jira/2026-10-19-23-44-36-UTC_2ef2adf7fa77  
Cierre: https://github.com/edulandoni/astra-cansat/blob/c8596057d0cfcb04ffacef89819daa5f90b9f7a9/ground-station/docs/historial/2026-10-19-cierre-orden-comentarios.md  
Mapa vigente: https://github.com/edulandoni/astra-cansat/blob/c8596057d0cfcb04ffacef89819daa5f90b9f7a9/ground-station/docs/trazabilidad-vigente-2026-10-19.md  
Cambio: https://github.com/edulandoni/astra-cansat/commit/c8596057d0cfcb04ffacef89819daa5f90b9f7a9

Verifiqué la publicación remota de groundstation y que main conserva su referencia. Los nueve manifiestos de capturas y los enlaces revisados son coherentes. Los avisos generales siguientes quedan aquí; este aviso no genera otra captura por sí solo y se incluirá con el próximo cambio real. No se realizaron nuevos ensayos técnicos ni se modificaron áreas ajenas.

### 2026-10-19T21:04:40.376-0300 — comentario 10074

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10074). Última edición informada: 2026-10-19T21:04:40.376-0300.

## 19/10/2026 — COMENTARIO 5 — Publicación de la revisión del aula CONAE

La revisión de fuentes del aula tiene su propia tarea ASTRA-37, asignada a mí y En curso. Conserva el acceso oficial, cuatro materiales, versiones/huellas, seis debates técnicos, contradicciones y límites. Las consecuencias específicas se registraron en ASTRA-18/20/21/22/24/25/36, sin modificar sus descripciones ni resultados anteriores.

Publiqué sólo mis notas, inventario de huellas, revisión estructural de la planilla y mapa PDR de groundstation. No publiqué credenciales, cookies, enlaces de sesión, nómina ni los originales completos del aula. Los cuatro originales quedaron juntos en la carpeta local de revisión con nombres conservados y registro de movimientos. La copia del informe en mi Drive fue leída después de subirla.

Bitácora de fuentes: https://astrateam2026.atlassian.net/browse/ASTRA-37?focusedCommentId=10066  
Cambio: https://github.com/edulandoni/astra-cansat/commit/5f9d8c310ecbecc9e1b7d0cc8d29d5d43df7b406  
Informe: https://github.com/edulandoni/astra-cansat/blob/5f9d8c310ecbecc9e1b7d0cc8d29d5d43df7b406/ground-station/docs/aula/2026-10-19/revision-aula.md  
Drive: https://drive.google.com/file/d/1FA0LB32ekpHXlosXWMAVkTuWswSj9gKC/view?usp=drivesdk

Verifiqué enlaces locales, integridad de las fuentes históricas y manifiestos; no hice ensayos técnicos nuevos. La grabación está localizada sin transcripción accesible y su audio completo sigue pendiente. La captura de cierre debe incluir ahora las doce tareas propias, no limitarse a las siete iniciales.

### 2026-10-19T21:05:40.409-0300 — comentario 10075

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10075). Última edición informada: 2026-10-19T21:05:40.409-0300.

## 19/10/2026 — COMENTARIO 6 — Respaldo de la revisión del aula

\[JIRA-GITHUB-SYNC\]

Publiqué la captura completa de mis doce tareas, con 56 comentarios y el historial consultado. Incluye ASTRA-37 y las consecuencias técnicas de las aclaraciones del aula en sus tareas correspondientes. Conservo las capturas previas y los originales. La fecha UTC de la carpeta ya es 20/10; la revisión se realizó el 19/10 en Argentina.

Captura: https://github.com/edulandoni/astra-cansat/tree/9d611778c4fdc0b3de10ec4ac8fbbc6477ce24d6/ground-station/historial-jira/2026-10-20-00-05-20-UTC_198e451ab1ed  
Publicación y tareas: https://github.com/edulandoni/astra-cansat/blob/9d611778c4fdc0b3de10ec4ac8fbbc6477ce24d6/ground-station/docs/historial/2026-10-19-publicacion-aula-conae.md  
Cambio: https://github.com/edulandoni/astra-cansat/commit/9d611778c4fdc0b3de10ec4ac8fbbc6477ce24d6

Verifiqué la referencia remota de groundstation, main sin cambios, diez manifiestos íntegros y enlaces locales. No publiqué credenciales ni archivos completos del aula. No ejecuté ensayos físicos nuevos. Las contradicciones de plazo, envolvente y Scoresheet siguen pendientes en ASTRA-37, junto con el audio sin transcripción y los documentos aún no publicados.

Este aviso no genera otra captura por sí solo; se incorpora con el próximo cambio real.

### 2026-10-19T21:11:49.432-0300 — comentario 10077

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10077). Última edición informada: 2026-10-19T21:11:49.432-0300.

## 19/10/2026 — COMENTARIO 7 — Ampliación de la revisión diaria del aula

Amplié la automatización existente respaldo-diario-jira-github-groundstation; ahora se llama «Aula CONAE y respaldo diario · Groundstation». Conservé horario diario 21:00 Argentina, estado ACTIVE, chat de destino y política failed_runs_only. No creé otra programación.

Primero revisará el curso oficial y comparará recursos, versiones/huellas, respuestas editadas o nuevas y fechas/condiciones de entrega. Registrará novedades y avance real de cobertura en ASTRA-37 y los efectos específicos en su tarea técnica. Después respaldará todas mis tareas con el procedimiento existente. Sin novedades ni avance no creará comentarios o commits repetidos; los indicadores de leído y tokens de sesión no cuentan como cambio sustantivo.

Los avisos del respaldo siguen exclusivamente aquí. La revisión puede agregar documentación fechada dentro de docs/aula/ e historial de publicación, además de índices propios; el respaldo sigue limitado a historial-jira/. No se toca main ni otras áreas. No se guardan credenciales en prompt o archivos ni se envían mensajes/entregas en el aula. Si no puede ingresar, deberá informar el impedimento sin afirmar que revisó.

Comprobé la configuración guardada; confirma la ampliación, no una ejecución diaria futura. El objetivo de cobertura total sigue activo con archivos y audio pendientes.

Documento de alcance: https://github.com/edulandoni/astra-cansat/blob/88996d3c95fd1deb04760bdc08e778830bc7144d/ground-station/docs/aula/2026-10-19/objetivo-cobertura-total.md  
Cambio publicado: https://github.com/edulandoni/astra-cansat/commit/88996d3c95fd1deb04760bdc08e778830bc7144d

### 2026-10-19T21:12:49.921-0300 — comentario 10078

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10078). Última edición informada: 2026-10-19T21:12:49.921-0300.

## 19/10/2026 — COMENTARIO 8 — Respaldo del objetivo activo y ampliación diaria

\[JIRA-GITHUB-SYNC\]

Conservé una captura nueva de mis doce tareas con 59 comentarios y páginas completas de historial. Incluye el objetivo de cobertura total de ASTRA-37 y la ampliación de la automatización diaria, sin sustituir los originales. El objetivo sigue activo: esta captura no acredita que el contenido pendiente ya esté investigado.

Captura: https://github.com/edulandoni/astra-cansat/tree/0bdcd774edf8e759f60f8918084c834c1bf75455/ground-station/historial-jira/2026-10-20-00-12-35-UTC_91075934f729  
Cambio: https://github.com/edulandoni/astra-cansat/commit/0bdcd774edf8e759f60f8918084c834c1bf75455

Comprobé once manifiestos, enlaces y publicación de groundstation. La copia pública mantiene las exclusiones de datos personales, comentarios restringidos e internos. No contiene credenciales. Este aviso no produce otro respaldo por sí solo.

### 2026-10-19T21:37:05.068-0300 — comentario 10082

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10082). Última edición informada: 2026-10-19T21:37:05.068-0300.

## 19/10/2026 — COMENTARIO 9 — Publicación de la segunda lectura del aula

Publiqué cinco archivos de mi área: auditoría completa de los cuatro materiales, controles verificables, análisis asistido de audiovisuales, inventario ampliado de 22 recursos y enlace de entrada en README. Conservo entradas y fuentes anteriores. No cambié código ni carpetas ajenas.

Los hallazgos y sus límites están en ASTRA-37, comentario 3: https://astrateam2026.atlassian.net/browse/ASTRA-37?focusedCommentId=10079. Las actualizaciones RF y rotor continúan en ASTRA-18/36. Esta tarea registra solamente la publicación y el respaldo.

Verifiqué fuentes históricas, once manifiestos, enlaces locales y alcance de los cambios. Comprobé la publicación remota de groundstation y que main mantiene su referencia. No publiqué archivos completos del aula, audio, transcripción automática ni credenciales. La copia nueva en mi carpeta Drive fue comprobada por metadatos y lectura de contenido; no sustituye la anterior.

Cambio: https://github.com/edulandoni/astra-cansat/commit/5728978901d20b221c6cd5c50c9841ac357be0bb  
Copia Drive: https://drive.google.com/file/d/1-4LCEyCUqAB6JCbZGa0nUAeqlLz0HUfK/view?usp=drivesdk  
Inventario y pendientes: https://github.com/edulandoni/astra-cansat/blob/5728978901d20b221c6cd5c50c9841ac357be0bb/ground-station/docs/aula/2026-10-19/cobertura-actualizacion-02.json

El objetivo de 100% permanece activo por los límites audiovisuales expresamente documentados. La revisión diaria ampliada mantiene su configuración; esta entrada no acredita una ejecución programada futura. A continuación conservo una captura nueva de las doce tareas propias, con todas las páginas de comentarios e historial.

## Historial de cambios de campos

### 2026-10-19T20:39:31.912-0300 — cambio 10134

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Backlog

Después: Por hacer

### 2026-10-19T20:39:53.040-0300 — cambio 10138

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Por hacer

Después: En curso

