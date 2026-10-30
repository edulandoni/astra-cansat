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

### 2026-10-19T21:38:42.518-0300 — comentario 10083

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10083). Última edición informada: 2026-10-19T21:38:42.518-0300.

## 19/10/2026 — COMENTARIO 10 — Respaldo de la segunda lectura del aula

\[JIRA-GITHUB-SYNC\]

Publiqué una captura nueva de mis doce tareas, con 64 comentarios y 36 entradas de historial de cambios. Consulté todas las páginas y verifiqué pertenencia por creador/asignación. No hubo comentarios restringidos/internos que incluir; la copia mantiene exclusión de correos, identificadores innecesarios, binarios y reacciones. Conservo todas las capturas anteriores.

Captura: https://github.com/edulandoni/astra-cansat/tree/2540aa82dc9bcba7ac2c306968e6a8f2f1c8d632/ground-station/historial-jira/2026-10-20-00-37-57-UTC_73ad0027e522  
Cambio: https://github.com/edulandoni/astra-cansat/commit/2540aa82dc9bcba7ac2c306968e6a8f2f1c8d632  
Lectura temática: https://astrateam2026.atlassian.net/browse/ASTRA-37?focusedCommentId=10079

Comprobé doce manifiestos íntegros, enlaces locales, fuentes históricas conservadas, alcance exclusivo dentro de mi carpeta y ausencia de cadenas de credenciales en la revisión. El commit de respaldo agregó sólo archivos de historial-jira/. Verifiqué la referencia remota de groundstation y main sin cambios. La captura tiene fecha UTC 20/10; esta jornada sigue siendo 19/10 en Argentina.

El inventario documental se amplió a 22 recursos; el objetivo de cobertura 100% sigue activo por los límites audiovisuales registrados. Este aviso no genera otra captura por sí solo ni acredita ensayos físicos o una ejecución programada futura.

### 2026-10-19T22:06:51.852-0300 — comentario 10085

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10085). Última edición informada: 2026-10-19T22:06:51.852-0300.

## 19/10/2026 — COMENTARIO 11 — Publicación del cierre documental y referencias oficiales

Publiqué el informe de actualización 03, inventario de 30 entradas, huellas de fuentes actuales y controles de ambos audiovisuales. El cierre de investigación, métodos, límites y aclaraciones continúan en ASTRA-37, comentario 4: https://astrateam2026.atlassian.net/browse/ASTRA-37?focusedCommentId=10084. Aquí registro sólo publicación, configuración y respaldo.

Conservé los inventarios y entradas anteriores. Comprobé fuentes históricas, doce manifiestos y enlaces locales. La publicación agregó cuatro documentos y amplió el índice, sólo en ground-station/ de groundstation. Verifiqué el remoto y main sin cambios. No publiqué originales completos, grabaciones, transcripciones, capturas de participantes o credenciales.

La copia nueva en mi carpeta Drive fue verificada por metadatos y lectura. Los originales, copias de control, páginas de referencia y registros de movimientos permanecen en el conjunto local de esta revisión; los auxiliares de un intento de descarga incompleto se conservaron sin mover ni usar como evidencia.

Amplié la misma automatización para incluir las referencias oficiales enlazadas por las bases. Comprobé que mantiene ACTIVE, ejecución diaria 21:00 Argentina, chat de destino y política failed_runs_only; no creé otra programación. La confirmación acredita configuración, no una ejecución futura.

Cambio: https://github.com/edulandoni/astra-cansat/commit/3887c316d2a202f220ec687ed6a1fbfdba670124  
Informe: https://github.com/edulandoni/astra-cansat/blob/3887c316d2a202f220ec687ed6a1fbfdba670124/ground-station/docs/aula/2026-10-19/referencias-y-verificacion-actualizacion-03.md  
Drive: https://drive.google.com/file/d/1chQKLRid1GQzvK1oyajmSSrI74BeOtso/view?usp=drivesdk

A continuación conservo una nueva captura completa de mis doce tareas. No hubo cambios de código ni ensayos físicos. El seguimiento diario conserva las futuras publicaciones y aclaraciones pendientes.

### 2026-10-19T22:10:30.478-0300 — comentario 10086

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10086). Última edición informada: 2026-10-19T22:10:30.478-0300.

## 19/10/2026 — COMENTARIO 12 — Respaldo del cierre documental

\[JIRA-GITHUB-SYNC\]

Publiqué una captura completa de mis doce tareas, con 67 comentarios y 36 entradas de historial, tras consultar todas las páginas y verificar pertenencia por creador/asignación. La copia conserva las exclusiones de datos personales innecesarios, comentarios restringidos/internos, binarios y reacciones; no hubo comentarios excluidos en esta consulta.

Comprobé que los 64 comentarios de la captura anterior mantienen cuerpo y fechas, y que las doce tareas conservan título, descripción, creador, responsable y estado. El respaldo sólo agregó archivos dentro de historial-jira/. Verifiqué trece manifiestos, enlaces, fuentes históricas y publicación remota de groundstation; main conserva su referencia.

Captura: https://github.com/edulandoni/astra-cansat/tree/51c475eb2df8cf2ab5317c5e03455f8ad7c4b729/ground-station/historial-jira/2026-10-20-01-07-57-UTC_2dc0477ac15d  
Cambio: https://github.com/edulandoni/astra-cansat/commit/51c475eb2df8cf2ab5317c5e03455f8ad7c4b729  
Cierre de investigación y límites: https://astrateam2026.atlassian.net/browse/ASTRA-37?focusedCommentId=10084  
Informe: https://github.com/edulandoni/astra-cansat/blob/3887c316d2a202f220ec687ed6a1fbfdba670124/ground-station/docs/aula/2026-10-19/referencias-y-verificacion-actualizacion-03.md

El inventario vigente reúne 30 recursos revisados al corte, con métodos asistidos y dudas conservadas. La automatización mantiene la revisión diaria del aula y referencias oficiales. Esta captura no representa ensayos físicos ni acredita una ejecución programada futura. La fecha UTC de la captura es 20/10; corresponde a la jornada del 19/10 en Argentina.

Este aviso se incorporará con el próximo cambio real y no genera un respaldo adicional por sí solo.

### 2026-10-20T11:40:18.149-0300 — comentario 10087

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10087). Última edición informada: 2026-10-20T11:40:18.149-0300.

## 20/10/2026 — COMENTARIO 13 — Reorganización de Drive y mejora continua de groundstation

### Motivo y objetivo

La entrada de mi Drive seguía centrada en el laboratorio y la estación del 12/10. Después incorporé el banco USB, ensayos de recuperación, estudios de antecedentes y rotor y la revisión del aula. Necesitaba encontrar lo vigente sin confundirlo con versiones anteriores ni perder la historia.

Organicé mi espacio por temas que pueden mantenerse aunque cambien las herramientas: desarrollo; requisitos y aula; decisiones e interfaces; ensayos; investigación; material para PDR/video; e histórico. Aplico esto a groundstation y manejo de datos de mi área.

### Qué hice

Creé 11 carpetas, moví 18 elementos y renombré 2 carpetas existentes. Conservo los identificadores y enlaces originales. Los paquetes históricos se movieron completos con sus archivos y referencias. La estación v04 queda como antecedente DEPRECATED para la línea actual; el banco USB sigue siendo una herramienta experimental útil y conserva su advertencia de formato heredado.

Separé fuentes v1/v2 de análisis, trasladé las revisiones del aula a requisitos y los estudios de otros CanSat y rotor a investigación. Conservé el estado del 12/10, el inventario del 13/10, el antiguo instructivo y todas las revisiones fechadas. Los manifiestos anteriores siguen describiendo su fecha; un registro nuevo permite reconstruir las ubicaciones.

Publiqué 17 archivos de consulta: 9 guías, 6 copias de documentos versionados con enlaces utilizables desde Drive, un paquete de evidencias y experimentos de PC y el registro de movimientos. El paquete conserva 39 archivos de evidence/ y experiments/, con manifiesto SHA-256. No ejecuté nuevamente esos ensayos ni los contabilizo como trabajo nuevo.

La entrada principal es [00_EMPEZAR_ACA](https://drive.google.com/file/d/12H-VdifFyThzj4Tz-kXOLtM6EO0BBj49/view?usp=drivesdk). El [mapa Drive–Jira–GitHub](https://drive.google.com/file/d/1LIF_YtBnltenTIXojtHhaE4o8xGO4hWM/view) enlaza cada tema con su diario y sus archivos. Las investigaciones no se registran como implementación terminada.

### Cómo mantengo la estructura

Dejé una [pauta de mejora continua](https://drive.google.com/file/d/1CI3WMSbKoRgJsBWNnndZ4AgolJRQ-34V/view): agrego avances fechados dentro del tema, enlazo un mismo original desde otros lugares y actualizo los accesos cuando cambia qué conviene consultar. Reviso la estructura ante una confusión concreta o al preparar un hito; un ensayo o versión nueva no justifica renumerar o mover todo. Las conclusiones que cambian llevan una ACTUALIZACIÓN con referencia al original, sin borrarlo.

Amplié la automatización diaria existente para publicar nuevas revisiones del aula en su ubicación temática, conservando versiones y evitando duplicados. Verifiqué su configuración ACTIVE, el horario de 21:00 de Argentina, el mismo chat y la política de notificaciones anterior. Esto verifica la configuración, no una ejecución futura. El respaldo completo de Jira continúa en GitHub; desde Drive lo enlazo, sin crear una copia redundante diaria.

### Verificación y límites

Comprobé los nombres y carpetas de los 17 archivos publicados. Releí completos los 15 Markdown y comparé sus textos; comprobé igualdad semántica del registro JSON y SHA-256 idéntico del ZIP remoto. También verifiqué los 39 archivos del paquete y los 20 cambios de metadatos.

No reemplacé los bytes de los originales, no cambié permisos ni reorganicé HARDWARE, DOCUMENTOS u otras áreas. No cambié estados, responsables, descripciones ni comentarios anteriores de Jira. No modifiqué main ni protocol/. Los ensayos físicos, identificación exacta de la placa, TEAM_ID, interfaz acordada y enlace RF siguen pendientes. Ordenar documentos no acredita esas funciones.

### Publicación y evidencia

Publiqué la documentación, el registro de movimientos y los enlaces en [el commit 2a404c2](https://github.com/edulandoni/astra-cansat/commit/2a404c224882889f421d359f55c5bd9952a69a01), únicamente en groundstation/ground-station. Verifiqué el resultado remoto y main permanece en su revisión anterior.

El [informe de reorganización](https://github.com/edulandoni/astra-cansat/blob/2a404c224882889f421d359f55c5bd9952a69a01/ground-station/docs/organizacion-drive/2026-10-20/Reorganizacion_Drive_2026-10-20.md) enlaza los 17 archivos, sus huellas y el registro de ubicaciones. [Registro de movimientos en Drive](https://drive.google.com/file/d/1HzmyHC56TMmEU8mlIeICc2xucVqjt9JP/view).

Continúo las pruebas y cambios técnicos en sus tareas temáticas; esta entrada documenta organización, publicación y trazabilidad.

### 2026-10-20T12:08:12.757-0300 — comentario 10092

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10092). Última edición informada: 2026-10-20T12:08:12.757-0300.

## 20/10/2026 — COMENTARIO 14 — Análisis diario del aula e investigación en la automatización existente

Amplié la rutina existente para que el registro del aula produzca un panorama que podamos usar al trabajar y redactar el PDR. Creé ASTRA-38, asignada a mi cuenta y ya En curso por el primer informe. ASTRA-37 conserva fuentes y cobertura; ASTRA-35 los antecedentes/fotos; ASTRA-24 los efectos sobre interfaz. No moví el diario general al receptor ni cambié las descripciones o comentarios anteriores.

El orden diario es: revisar y registrar fuentes; generar informe priorizado; hacer una investigación complementaria acotada; respaldar todas mis tareas de Jira, incluida ASTRA-38. Conservo la automatización respaldo-diario-jira-github-groundstation, su ejecución de las 21:00 de Argentina, estado ACTIVE, mismo chat y política de notificaciones anterior. Verifiqué el texto guardado íntegro en UTF-8 y esos campos. No creé otra automatización ni afirmo una ejecución futura ya realizada.

El informe diario tendrá novedades separadas del panorama acumulado, preguntas/respuestas o publicaciones, prioridades justificadas, utilidad, fuentes, acciones propuestas y dudas. Se crea un corte aunque no haya novedades, identificándolo sin cambios; si falta acceso se marca parcial. Esa es la actualización específica de la pauta anterior para el informe de ASTRA-38. Los avisos de respaldo e investigación siguen evitando publicaciones repetidas sin avance real.

La investigación complementaria revisará hasta tres fuentes primarias nuevas o ampliará una ficha, con registro de lo ya consultado, resultados/fallas y referencias visuales con estado real, crédito y permisos observados. No transforma premios, renders o fotos en pruebas de nuestro hardware.

Publiqué [el informe del corte 11:56 ART](https://drive.google.com/file/d/13hQj8Ckp6KJv3cu1L5xeCX3Rwx4_NbLe/view?usp=drivesdk), [su método](https://drive.google.com/file/d/1vfcMYqX-nZhh_-icHyeb5jyx0g8puI_H/view?usp=drivesdk), [la investigación y actualización visual](https://drive.google.com/file/d/1b9XCAivqKZMcVMAbVtPAozInPlc2hu_O/view?usp=drivesdk) y [el catálogo](https://drive.google.com/file/d/18BSOE-_4108xSY262aXTrw4BSOr6CcaW/view?usp=drivesdk) en sus carpetas existentes. Verifiqué nombre, padre y contenido completo de las cuatro publicaciones Drive. Los controles y documentos están en [el commit 9208b92](https://github.com/edulandoni/astra-cansat/commit/9208b923e87ddc301a89951e6b362ccd861e0d93), confirmado en el remoto de groundstation; main permanece igual. No reorganicé otra vez las carpetas ni modifiqué otras áreas.

El primer corte detectó una respuesta nueva sobre comandos, siete debates/15 mensajes y cuatro archivos con huellas iguales. La investigación conserva cinco archivos de código leídos y siete referencias visuales, cuatro inspeccionadas. Es documentación y análisis; no repite ensayos ni acredita RF, energía o mecanismos físicos. El respaldo diario posterior capturará estas entradas con la consulta completa por creador/asignación, conservando todos los originales.

### 2026-10-20T12:11:25.048-0300 — comentario 10093

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10093). Última edición informada: 2026-10-20T12:11:25.048-0300.

## 20/10/2026 — COMENTARIO 15 — Respaldo del análisis diario y la investigación

\[JIRA-GITHUB-SYNC\]

Publiqué una captura nueva al corte UTC 20/10/2026 15:09:40, con las 13 tareas creadas por mí o asignadas a mi cuenta, 74 comentarios accesibles y 38 entradas de historial de campos. Incluye ASTRA-38, sus transiciones y primer informe; la novedad oficial en ASTRA-37; la investigación y referencias visuales de ASTRA-35; el efecto sobre interfaz en ASTRA-24; y las entradas recientes de organización/configuración en ASTRA-33.

Leí todas las páginas disponibles de tareas, comentarios e historial, verifiqué pertenencia y conservé originales y capturas anteriores. No descargué adjuntos binarios ni reacciones. El exportador aplica las exclusiones de comentarios restringidos/internos, correos e identificadores de cuenta. Verifiqué los manifiestos de las 14 capturas conservadas y los archivos nuevos; preservé también los espacios y saltos de línea de las citas históricas Markdown.

[Captura completa y archivos legibles](https://github.com/edulandoni/astra-cansat/tree/c07568d/ground-station/historial-jira/2026-10-20-15-09-40-UTC_c7500b092190) y [commit de respaldo](https://github.com/edulandoni/astra-cansat/commit/c07568d). Verifiqué el resultado remoto: este commit sólo agrega 16 archivos de ground-station/historial-jira/ en groundstation. Main permanece en su revisión anterior.

Este aviso queda fuera de esa captura, que corresponde al corte anterior a publicarlo. Su marca no disparará otro respaldo por sí sola. El respaldo conserva documentación y no representa ensayos nuevos de telemetría o hardware.

### 2026-10-20T21:08:09.727-0300 — comentario 10097

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10097). Última edición informada: 2026-10-20T21:08:09.727-0300.

20/10/2026 — COMENTARIO 16 — \[JIRA-GITHUB-SYNC\]

Conservé una captura nueva de mis 13 tareas, consultadas por creador/asignación verificados y con todas las páginas de comentarios e historial de campos. Captura UTC: 21/10/2026 00:07:08; corresponde al diario del 20/10 en Argentina. Incluye 78 comentarios y 38 cambios de campos, después del informe diario ASTRA-38, las novedades de fuentes ASTRA-37 y la ficha DJS ASTRA-35.

Verifiqué las huellas de los 15 manifiestos conservados y comprobé que los 74 comentarios de la captura anterior siguen intactos. La copia pública omite correos, identificadores de cuenta y comentarios restringidos/internos; no incluye adjuntos binarios ni reacciones. No se encontraron comentarios excluidos en esta consulta. Los originales permanecen en Jira.

[Captura y archivos legibles](https://github.com/edulandoni/astra-cansat/tree/256b5b568d32b143b9ac0073c74339ed85116887/ground-station/historial-jira/2026-10-21-00-07-08-UTC_9049b0b4a19e) · [Commit de respaldo verificado](https://github.com/edulandoni/astra-cansat/commit/256b5b568d32b143b9ac0073c74339ed85116887). Este commit sólo agrega archivos de historial-jira y está separado del análisis cc2b6fd. No cambié estados, responsables ni descripciones. Este aviso se ignora en la comparación semántica para evitar otro respaldo por sí solo.

### 2026-10-21T21:33:36.570-0300 — comentario 10102

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10102). Última edición informada: 2026-10-21T21:33:36.570-0300.

21/10/2026 — COMENTARIO 17 — \[JIRA-GITHUB-SYNC\]

Conservé una captura nueva de mis 13 tareas, con creador/asignación verificados y todas las páginas de comentarios e historial consultadas. Fecha UTC real: 22/10/2026 00:32:34, correspondiente al diario del 21/10 en Argentina. Incluye 83 comentarios y 38 cambios de campos, después del informe parcial del aula y el antecedente COSMOS.

Verifiqué los 16 manifiestos conservados y que los 78 comentarios de la captura anterior siguen intactos. La copia pública omite correos, identificadores de cuenta y comentarios restringidos/internos; en esta consulta no aparecieron comentarios excluidos. No incluye adjuntos binarios ni reacciones. Los originales permanecen en Jira. No cambié estados, responsables ni descripciones.

[Captura legible y manifiesto](https://github.com/edulandoni/astra-cansat/tree/39c6a8a1ac10ddc7bc6bfb52d76c65d251ee8ed5/ground-station/historial-jira/2026-10-22-00-32-34-UTC_4e66db07f308) · [Commit de respaldo verificado remoto](https://github.com/edulandoni/astra-cansat/commit/39c6a8a1ac10ddc7bc6bfb52d76c65d251ee8ed5). Sólo agrega archivos de historial-jira, separado del análisis 48b750d. Este aviso se ignora al comparar para evitar ciclos.

El respaldo Jira está completo dentro del alcance consultado; la revisión del aula está parcial por falta de respuesta del sitio, documentada en ASTRA-37/38. No confundo el éxito del respaldo con revisión de fuentes inaccesibles.

### 2026-10-22T21:11:24.100-0300 — comentario 10106

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10106). Última edición informada: 2026-10-22T21:11:24.100-0300.

22/10/2026 — COMENTARIO 18 — \[JIRA-GITHUB-SYNC\]

Conservé una captura nueva de mis 13 tareas por creador/asignación verificados, con todas las páginas de comentarios e historial de campos consultadas. Captura UTC real: 23/10/2026 00:10:17, correspondiente al diario del 22/10 en Argentina. Incluye 87 comentarios y 38 cambios de campos, después del corte diario y la investigación RSX/rotor.

Verifiqué los 17 manifiestos conservados y que los 83 comentarios de la captura anterior siguen intactos. La copia pública omite correos, identificadores de cuenta y comentarios restringidos/internos; no aparecieron comentarios excluidos en esta consulta. No incluye adjuntos binarios ni reacciones. Jira conserva los originales.

[Captura y archivos legibles](https://github.com/edulandoni/astra-cansat/tree/4c4481d8e2cbaf20c209adc3c4b99c363c33131d/ground-station/historial-jira/2026-10-23-00-10-17-UTC_105587ebc466) · [Commit de respaldo verificado remoto](https://github.com/edulandoni/astra-cansat/commit/4c4481d8e2cbaf20c209adc3c4b99c363c33131d). Sólo agrega archivos de historial-jira, separado del análisis b9a31b0. No cambié estados, responsables ni descripciones. Este aviso se ignora en la comparación para evitar ciclos.

El respaldo de Jira está completo dentro del alcance consultado; el informe del aula conserva su cobertura parcial. No uso el respaldo para dar por revisadas fuentes inaccesibles.

### 2026-10-23T21:05:26.003-0300 — comentario 10110

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10110). Última edición informada: 2026-10-23T21:05:26.003-0300.

23/10/2026 ART — COMENTARIO 19 — \[JIRA-GITHUB-SYNC\]

Conservé una nueva captura completa, consultada el 24/10/2026 a las 00:04:37 UTC (23/10 ART), después de registrar el corte diario y el contraste RSX. Incluye 13 tareas creadas por mí o asignadas a mí, 91 comentarios y 38 entradas del historial de cambios de campos. Leí todas las páginas y verifiqué pertenencia por cuenta. No limité la búsqueda a claves antiguas.

[Captura y archivos legibles](https://github.com/edulandoni/astra-cansat/tree/202b55a84f102abbdaabb0c2422e284382291183/ground-station/historial-jira/2026-10-24-00-04-37-UTC_180250a91c8f) · [Commit de respaldo verificado](https://github.com/edulandoni/astra-cansat/commit/202b55a84f102abbdaabb0c2422e284382291183).

Comprobé las 15 huellas del manifest, conservación del contenido anterior y ausencia de credenciales/correos/identificadores de cuenta en la copia pública. No hubo comentarios restringidos o internos en lo consultado; quedan excluidos del método, junto con adjuntos binarios y reacciones. No cambié estados, responsables o descripciones. El commit sólo agrega la nueva carpeta de historial-jira; conservé todas las capturas anteriores.

El análisis documental quedó en un commit separado: [ASTRA-38/35/34](https://github.com/edulandoni/astra-cansat/commit/48debe0bf52d52cabf90e3d88413b39995a79011), con copias de informes verificadas en Drive. El aula continúa con cobertura parcial, descrita en el corte; este respaldo no acredita acceso al aula. Este aviso posterior a la captura no genera otro respaldo por sí solo.

### 2026-10-23T23:31:21.427-0300 — comentario 10123

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10123). Última edición informada: 2026-10-23T23:31:21.427-0300.

23/10/2026 — COMENTARIO 20 — Publicación del banco02 y trazabilidad conservada

Publiqué tres bloques únicamente en groundstation/ground-station: implementación y evidencia114616a, propuesta de interfaz/antenas/antecedentesfc6e6d2 y control de publicaciónd35d978. No modifiqué main ni carpetas ajenas. La primera aceptación física sigue siendo parcial: cinco escenariosUSB y629paquetes guardados; RST/desconexión físicos dedicados, C:+microSD y ≥2hUSB conGUI todavía pendientes.

Agregué comentarios nuevos en ASTRA-20/21/22/24/25/34/35 según tema, sin usar receptor como diario general. Volví a leer todas sus páginas de comentarios y comprobé que las entradas anteriores conservan ID y texto; el control enlaza los nuevos comentarios. ASTRA-24 y25 pasaron a En curso por preparación/cálculo iniciados; no los cerré ni afirmé interoperabilidad oRF.

Publiqué y verifiqué texto completo/carpeta de cuatro informes nuevos enDrive, con enlaces deGit fijados al commit. Conservo estructura, originales y permisos:

* [2026-10-23-banco02-actualizacion-01.md](https://drive.google.com/file/d/1xvE1kleYV87FcYdauACFBdL49K941VCQ/view?usp=drivesdk)
* [2026-10-23-propuesta-banco-y-vuelo.md](https://drive.google.com/file/d/1oYWR-t__bDmwQAEvgOG-pSiADT5qDQOK/view?usp=drivesdk)
* [2026-10-23-antenas-y-link-budget-preliminar.md](https://drive.google.com/file/d/1KM8qlFtnFBjQaLrBYLvAhZ75QNc0jttZ/view?usp=drivesdk)
* [2026-10-23-antecedentes-a-pruebas.md](https://drive.google.com/file/d/1NiH9-b93CM91oOYWh8naujQ0lX7idqlQ/view?usp=drivesdk)

[Registro de enlaces, carpetas y verificaciones](https://github.com/edulandoni/astra-cansat/blob/d35d978f5f6e9edde47ee29238f4ae7a1474b4b6/ground-station/docs/historial/2026-10-23-publicacion-banco02-01.json) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/d35d978f5f6e9edde47ee29238f4ae7a1474b4b6).

Este comentario registra publicación y conservación del diario; no es una captura completa nueva de Jira ni sustituye el respaldo programado. Los avances técnicos continúan en sus tareas.

### 2026-10-24T00:30:40.532-0300 — comentario 10136

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10136). Última edición informada: 2026-10-24T00:30:40.532-0300.

24/10/2026 — COMENTARIO 21 — Ventanas de prueba y continuidad del chat

Dejé asentada una pauta persistente para mi área: después de observar u operar la interfaz del banco vuelvo al chat actual antes de pedir una maniobra o esperar respuesta. Otra ventana no debe tapar las preguntas. Uso la navegación propia de la app; no manipulo el contenido del chat mediante automatización de pantalla ni cierro una adquisición sólo para recuperar foco.

La pauta quedó en ground-station/AGENTS.md, conservando las instrucciones anteriores. Durante ensayos prolongados puedo mantener la ventana del banco minimizada entre observaciones; debo comprobar que continúen adquisición, archivo y actualizaciones de GUI. No doy por realizada una maniobra por tiempo transcurrido.

[Pauta versionada](https://github.com/edulandoni/astra-cansat/blob/44171403bd4ac59ee0657f96fc761d71dd14664a/ground-station/AGENTS.md) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/44171403bd4ac59ee0657f96fc761d71dd14664a).

También quedó publicada la actualización de reconexión y dos soportes en su tema de ensayos, con comentarios nuevos en ASTRA-20/21/22/34: [informe Drive verificado](https://drive.google.com/file/d/11qcMyyB8SE5QESRkXl5xLetJK-FeWNE2/view) y [commit técnico](https://github.com/edulandoni/astra-cansat/commit/2863fee267eeb3f48826e8876e279ca096ab091f). Este registro documenta metodología y publicación; no es una captura completa de Jira ni un nuevo ensayo.

### 2026-10-24T00:45:59.945-0300 — comentario 10141

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10141). Última edición informada: 2026-10-24T00:45:59.945-0300.

24/10/2026 — COMENTARIO 22 — ACTUALIZACIÓN COMENTARIO 21: Cierre de control de pantalla y publicación de la siguiente etapa

Amplié la pauta de ventanas: cierro la sesión de control de pantalla al terminar una operación y sólo la activo para una necesidad concreta de interfaz. Adquisición USB, procesamiento de archivos y consultas por API no requieren control del escritorio. Conservo la pauta de volver al chat antes de pedir maniobras.

[Pauta versionada](https://github.com/edulandoni/astra-cansat/blob/a8a6a76d5c7af279f4e64caaac8f4dddba222ca1/ground-station/AGENTS.md) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/a8a6a76d5c7af279f4e64caaac8f4dddba222ca1).

Publiqué en su tema la cadencia corta, identidad entre sesiones, fuentes congeladas e inicio del ensayo prolongado, con comentarios nuevos en ASTRA-20/21/22/34. Drive conserva un informe nuevo verificado dentro de Ensayos. La corrida larga está en curso: este registro de publicación no acredita su resultado ni reemplaza una captura de respaldo de Jira.

[Informe y evidencia por revisión](https://github.com/edulandoni/astra-cansat/blob/38ae9999af98395e376030089cf5f2c7447f409f/ground-station/docs/2026-10-24-cadencia-identidad-e-inicio-prolongado-actualizacion-05.md) · [Drive verificado](https://drive.google.com/file/d/1j6m_KdBn266iJZAxvZD4yM1B4rH_MkQ-/view?usp=drivesdk) · [Commit verificado](https://github.com/edulandoni/astra-cansat/commit/38ae9999af98395e376030089cf5f2c7447f409f). Conservo resultados, fuentes y comentarios anteriores.

### 2026-10-24T03:18:21.797-0300 — comentario 10156

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10156). Última edición informada: 2026-10-24T03:18:21.797-0300.

24/10/2026 — COMENTARIO 23 — Publicación y trazabilidad del cierre USB

Publiqué el cierre del banco USB con matriz completa, resultados, CSV sintético, serie de salud, gráfica, lanzador utilizado y procedimiento de reproducción. Trabajé únicamente en groundstation/ground-station, sin main, vuelo, protocol, HARDWARE, DOCUMENTOS o tareas del trabajo. Los diarios técnicos están en ASTRA-20/21/22/34; las revisiones de radio y antecedentes siguen en sus tareas temáticas.

Conservé la cronología: primer intento interrumpido, corrección del medidor, segundo intento aprobado y corrección offline de recuperación. No reescribí comentarios, descripciones, resultados o capturas previas. No cerré tareas con criterios de RF, vuelo o acuerdos pendientes.

El control de fuentes aclaró una diferencia de alcance del manifiesto: el árbol congelado contiene 22 productos de compilación ignorados. No se usan al adquirir ni son la referencia para volver a programar. Comprobé 29 archivos versionados idénticos al commit de fuente y que el CSV publicado conserva exactamente su huella. El manifiesto original permanece; la aclaración tiene documento nuevo y control enlazado. El diario original, la procedencia con rutas locales y la flash original siguen privados; no publiqué credenciales o identificadores de dispositivo.

Verifiqué contenido y carpeta de las copias Drive. La inhibición temporal de suspensión se liberó al cerrar; el control de pantalla quedó cerrado y el chat visible. Este comentario registra publicación y trazabilidad, no un respaldo Jira→GitHub ni una nueva configuración de la automatización.

[Informe final y matriz de la etapa](https://github.com/edulandoni/astra-cansat/blob/44bf6ea88a04acfa460dd77bdb8c62d4a6fb9a29/ground-station/docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md) · [Commit de resultados verificado](https://github.com/edulandoni/astra-cansat/commit/44bf6ea88a04acfa460dd77bdb8c62d4a6fb9a29) · [Drive: informe final](https://drive.google.com/file/d/1i-pRyjTcZRqRaD8nuIt3MrOW22W6Hu90/view?usp=drivesdk) · [Aclaración de reproducción](https://github.com/edulandoni/astra-cansat/blob/838e0a187472e0d7dcc2f6c4f8dee8abf5856c4d/ground-station/docs/2026-10-24-control-reproduccion-actualizacion-10.md) · [Drive: control de fuentes](https://drive.google.com/file/d/1fEv5ZasO5i-YNfuKfulLwAH6NjjiO8yn/view?usp=drivesdk).

### 2026-10-24T03:59:22.267-0300 — comentario 10165

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10165). Última edición informada: 2026-10-24T03:59:22.267-0300.

24/10/2026 — COMENTARIO 24 — ACTUALIZACIÓN: Revisión de mis trece tareas y publicación por tema

Revisé las trece tareas de mi alcance y sus páginas completas de comentarios. Avancé nueve tareas con entregables concretos: calidad, conservación de registros, GUI, controles USB, propuesta de destinatarios, cálculo de enlace y energía incremental. ASTRA-34 quedó Finalizado tras revisar sus criterios y recorrer En revisión → Finalizado; su implementación y acuerdos pendientes continúan en las tareas correspondientes.

Publiqué cuatro commits en groundstation, exclusivamente dentro de ground-station/, y seis informes nuevos en las carpetas temáticas existentes de Drive. Verifiqué contenido y carpeta de cada copia. La entrada del repositorio ahora orienta al banco v0.2 y distingue el estado histórico; conservé el banco anterior, informes, comentarios y evidencias originales.

El control registra 29 pruebas unitarias aprobadas, once vectores de destino, seis trazas de calidad y dos pasadas físicas de los mismos catorce controles USB, con 131 muestras por pasada. La prueba previa de dos horas conserva su fecha y revisión; no la atribuyo a los cambios nuevos.

Dejé cada avance en su tarea temática. No cambié tareas ajenas, responsables, descripciones ni parámetros RF; tampoco modifiqué la automatización. Este control no es una exportación completa del historial de campos de Jira. El acceso al aula volvió a fallar: no afirmo haber revisado novedades y no repetí el mismo impedimento en ASTRA-37/38. No registré avance de antecedentes sin evidencia primaria nueva.

[Revisión, matriz de pendientes y enlaces](https://github.com/edulandoni/astra-cansat/blob/9735087c1074754895273c4109553f5b350c7faf/ground-station/docs/historial/2026-10-24-revision-tareas-y-avances.md)
[Copia verificada en Drive](https://drive.google.com/file/d/1txyAJ7i1-vqQXnRKDA127hHJ_I4gu_ZU/view)
[Último commit verificado](https://github.com/edulandoni/astra-cansat/commit/9735087c1074754895273c4109553f5b350c7faf)

### 2026-10-24T21:06:30.980-0300 — comentario 10168

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10168). Última edición informada: 2026-10-24T21:06:30.980-0300.

24/10/2026 ART — COMENTARIO 25 — \[JIRA-GITHUB-SYNC\]

Conservé una captura nueva completa el 25/10/2026 a las 00:05:44 UTC (24/10 ART), después del informe diario y la investigación complementaria. Incluye las trece tareas de mi alcance, 149 comentarios y 42 entradas del historial de cambios de campos. Busqué por creador/asignación y comprobé pertenencia; leí todas las páginas de tareas, comentarios e historial. Incluye el cierre ya realizado de ASTRA-34, sin cambiar estados durante esta ejecución.

[Captura y archivos legibles](https://github.com/edulandoni/astra-cansat/tree/a4a8f9a59dfc548339a97e29aaea96ffd287a993/ground-station/historial-jira/2026-10-25T00-05-44Z_c4d32984e676) · [Commit de respaldo verificado remoto](https://github.com/edulandoni/astra-cansat/commit/a4a8f9a59dfc548339a97e29aaea96ffd287a993).

Verifiqué los 19 manifiestos conservados y que todos los comentarios y cambios de campos de la captura previa permanecen. Conservé también el formato de citas históricas, incluidos espacios originales: los avisos de estilo no justifican alterar los originales exportados. La copia omite correos e identificadores de cuenta y excluye comentarios restringidos/internos, adjuntos binarios y reacciones. No hubo comentarios excluidos en lo consultado. Jira conserva los originales.

El commit de respaldo sólo agrega una carpeta nueva de historial-jira y está separado del [commit de análisis ASTRA-38/35](https://github.com/edulandoni/astra-cansat/commit/2164cce77444a589264357d2a50ebc713043a633). Verifiqué las dos copias temáticas de Drive. El corte del aula sigue siendo parcial por falta de acceso: un respaldo completo de Jira no acredita lectura del aula.

No cambié responsables, estados, descripciones, permisos, software ni automatizaciones. Este aviso se ignora en la comparación para evitar ciclos.

### 2026-10-26T21:04:37.107-0300 — comentario 10201

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10201). Última edición informada: 2026-10-26T21:04:37.107-0300.

26/10/2026 ART — COMENTARIO 26 — \[JIRA-GITHUB-SYNC\]

Conservé una captura nueva completa el 27/10/2026 a las 00:01:43 UTC (26/10 ART), después de publicar el informe diario y el antecedente Peralta. Incluye las dieciséis tareas de mi alcance, 182 comentarios y 49 entradas de cambios de campos. Consulté por creador o asignación y comprobé los accountId antes de exportar; incluye ahora ASTRA-39, ASTRA-40 y ASTRA-41. Todas las páginas de tareas, comentarios e historial están completas. Volví a consultar las fechas de actualización y el conjunto de tareas permaneció estable durante la captura.

Captura y archivos legibles: https://github.com/edulandoni/astra-cansat/tree/ab4ceb4f4004031e9f7786970be81760fae4bfcc/ground-station/historial-jira/2026-10-27T00-01-43Z_3bab73918d0e  
Commit de respaldo verificado remoto: https://github.com/edulandoni/astra-cansat/commit/ab4ceb4f4004031e9f7786970be81760fae4bfcc

Verifiqué los veinte manifiestos conservados, sus huellas y la permanencia de todos los identificadores de comentarios/cambios de la captura anterior. El commit agrega únicamente diecinueve archivos en una carpeta nueva de historial-jira; no mezcla análisis ni modifica originales. La copia pública omite correos e identificadores de cuenta, excluye comentarios restringidos/internos y no descarga adjuntos binarios ni reacciones. No hubo comentarios excluidos entre los consultados. Jira conserva los originales.

El corte diario del aula es parcial por el mismo timeout de acceso: no afirmo ausencia de novedades ni cobertura total. El informe de 22 temas acumulados y las tres fuentes de Peralta están en su commit separado ASTRA-38/35: https://github.com/edulandoni/astra-cansat/commit/09553bba107b18f4f5b9b2c3ca2c23721ba699dc  
Informe aula verificado en Drive: https://drive.google.com/file/d/14I7h2fux9XhB-maQZWfET7yh4E0OiYHW/view?usp=drivesdk  
Antecedente verificado en Drive: https://drive.google.com/file/d/1yj-DzcviuXn_JcjYGfmU8oBECp3WYKyR/view?usp=drivesdk

No cambié estados, responsables, descripciones, permisos, software ni automatizaciones, ni usé el escritorio. El respaldo completo de Jira no acredita lectura del aula. Este aviso queda fuera de la comparación para evitar ciclos; no genero una copia redundante diaria del respaldo en Drive.

### 2026-10-28T00:53:26.254-0300 — comentario 10219

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10219). Última edición informada: 2026-10-28T00:53:26.254-0300.

28/10/2026 ART — COMENTARIO 27 — \[JIRA-GITHUB-SYNC\]

Conservé una captura nueva completa el 2026-10-28T03:51:14Z después de documentar el corte parcial del aula y la profundización de Peralta. Consulté las 16 tareas de mi alcance mediante JQL por creador/asignación y verifiqué su pertenencia por accountId. Leí todas las páginas de comentarios y cambios de campos: 200 comentarios y 49 entradas de historial. La lectura es por tarea, no una transacción atómica de Jira.

[Captura y archivos legibles](https://github.com/edulandoni/astra-cansat/tree/f68dcb8d3237c7d03c4198018a8000a04e91ce94/ground-station/historial-jira/2026-10-28T03-51-14Z_bd9e92c7967d) · [Manifest de huellas](https://github.com/edulandoni/astra-cansat/blob/f68dcb8d3237c7d03c4198018a8000a04e91ce94/ground-station/historial-jira/2026-10-28T03-51-14Z_bd9e92c7967d/manifest.json) · [Commit remoto verificado](https://github.com/edulandoni/astra-cansat/commit/f68dcb8d3237c7d03c4198018a8000a04e91ce94).

Comprobé las huellas de los 18 archivos enumerados en el manifiesto y la igualdad entre el árbol preparado localmente y el publicado. El commit agrega sólo esta carpeta de ground-station/historial-jira/, sin mezclar análisis ni software. Conservo las capturas anteriores. Los espacios y saltos del texto histórico no se normalizan para corregir avisos de formato.

La copia omite correos e identificadores de cuenta, comentarios restringidos/internos, adjuntos binarios y reacciones; no hubo comentarios restringidos o internos excluidos en esta consulta. No incluye fotos o videos nuevos del banco. Los avisos \[JIRA-GITHUB-SYNC\] no disparan otra captura por sí solos. No modifiqué estados, responsables, descripciones ni originales.

El informe diario y su análisis continúan en ASTRA-38; Peralta en ASTRA-35. Drive conserva acceso y explicación, sin duplicar la captura completa. El aula mantuvo el impedimento ya documentado: el corte es parcial y no acredita ausencia de novedades.

### 2026-10-28T22:24:12.691-0300 — comentario 10222

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10222). Última edición informada: 2026-10-28T22:24:12.691-0300.

28/10/2026 ART — COMENTARIO 28 — \[JIRA-GITHUB-SYNC\]

Conservé una captura nueva completa el 2026-10-29T01:22:34Z, después del informe diario y el análisis focal de KoNaR. Consulté las 16 tareas propias por creador/asignación, con pertenencia verificada por accountId; leí todas las páginas de comentarios e historial de cambios: 203 comentarios y 49 entradas de historial. La lectura es por tarea, no una transacción atómica de Jira.

[Captura y archivos legibles](https://github.com/edulandoni/astra-cansat/tree/52eae55d2a5f6f2c95c256a2a740b9a2d661ca03/ground-station/historial-jira/2026-10-29T01-22-34Z_6c1e439cbeb7) · [Manifest de huellas](https://github.com/edulandoni/astra-cansat/blob/52eae55d2a5f6f2c95c256a2a740b9a2d661ca03/ground-station/historial-jira/2026-10-29T01-22-34Z_6c1e439cbeb7/manifest.json) · [Commit remoto verificado](https://github.com/edulandoni/astra-cansat/commit/52eae55d2a5f6f2c95c256a2a740b9a2d661ca03).

Verifiqué las huellas de los 18 archivos enumerados en el manifiesto y la igualdad del árbol local y remoto. El commit sólo agrega esta carpeta de ground-station/historial-jira/, separado del commit de análisis. Conservo todas las capturas anteriores y los textos originales.

Excluyo correos, identificadores de cuenta y metadatos innecesarios; no incorporo comentarios restringidos/internos, adjuntos binarios ni reacciones. No hubo comentarios restringidos/internos excluidos en esta consulta. Comprobé ausencia de patrones de credenciales/sesión en la copia pública. Los avisos \[JIRA-GITHUB-SYNC\] no generan otra captura por sí solos.

El informe diario conserva el impedimento ya conocido del aula, por eso es parcial y no afirma ausencia de novedades. Queda en ASTRA-38; la investigación en ASTRA-35. No cambié estados, responsables o descripciones. Drive conserva acceso y explicación sin otra copia diaria del respaldo completo.

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

