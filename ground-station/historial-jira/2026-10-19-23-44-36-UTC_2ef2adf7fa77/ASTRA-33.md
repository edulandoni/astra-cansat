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

