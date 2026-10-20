# ASTRA-37 — DOC — Revisar aula CONAE, materiales PDR y aclaraciones oficiales

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-37)

Estado observado: En curso. Asignación: Cristian Ponsone. Creación: Cristian Ponsone.

## Descripción original consultada

## Objetivo

Revisar los materiales accesibles de CanSat Universitario 2026/2027 y registrar versiones, fuentes, aclaraciones, contradicciones y efectos sobre mi trabajo. Separar el texto del anexo, las respuestas oficiales y nuestras decisiones de implementación.

## Alcance

Curso oficial, bases/anexo, plantilla y planilla PDR, foro de consultas, avisos, grabación y entrega/calendario. Conservar originales y registrar cambios con entradas nuevas. No enviar mensajes ni entregar documentación desde esta revisión. No guardar credenciales, cookies ni enlaces de sesión en Jira o GitHub.

## Estado real

Ingreso correcto al curso. Cuatro archivos oficiales descargados y conservados; seis debates técnicos revisados. La grabación de apertura se localizó, pero no tiene transcripción accesible y no se da por analizada íntegramente. Detecté contradicciones de fecha de entrega, envolvente y fórmulas de la planilla que requieren aclaración.

## Entregable y cierre

Inventario verificable, informe de hallazgos y pendientes, selección de evidencias y efecto sobre mis tareas. Actualizaciones específicas en sus tareas técnicas. No modifica tareas ni decisiones de otros responsables. Una documentación futura del vector/ensayos, anunciada en el foro, requiere otra revisión cuando se publique.

## Comentarios conservados

### 2026-10-19T21:03:34.992-0300 — comentario 10066

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-37?focusedCommentId=10066). Última edición informada: 2026-10-19T21:03:34.992-0300.

## 19/10/2026 — COMENTARIO 1 — Revisión inicial del aula oficial y materiales PDR

### Motivo y alcance

Ingresé al aula oficial y revisé los materiales visibles del curso CanSat Universitario 2026/2027 para contrastar nuestro trabajo con fuentes actuales. No publiqué mensajes ni entregué archivos; no guardo credenciales o datos de sesión en la documentación.

Revisé las tres secciones del curso, cuatro archivos oficiales, seis debates técnicos (13 mensajes), avisos, presentación, entrega/calendario y vista de calificaciones. No exporté la nómina ni deduzco TEAM_ID del nombre de cuenta. La grabación de apertura dura 51:45; no tiene transcripción accesible y no doy por analizado todo su audio. El video institucional incrustado también queda inventariado sin revisión íntegra de audio.

### Archivos y versión

Conservé originales y registro de movimientos en la carpeta local de esta revisión. La plantilla tiene 89 diapositivas y 85 ítems numerados. El Scoresheet tiene una hoja PDR. El anexo v2 tiene SHA-256 27932c87654b64b443d41483c9b48adb06d7d1379dd7a01d54e4ea0035057bc7: coincide con el PDF revisado el 17/10; lo nuevo son plantillas y respuestas del foro.

### Hallazgos principales

La respuesta oficial del 19/10 admite formato de telemetría propio justificado, dirección de destino para X2 y transmisión durante ascenso. El CanSat comunica inicio cuando detecta separación real. STAND-BY es espera activada; las dos horas se aclaran como espera en rampa con consumo mínimo, sin exigir transmisión continua. No equivale a dos horas de consumo de misión completa.

Contenedor y carga útil bajan juntos. Se acepta segundo paracaídas y, en general, un segundo sistema activo o pasivo. No se aprueba por eso un rotor específico. El panel solar puede cumplir con enviar su tensión; no se exige carga de batería. La misión secundaria se valoraría a igualdad de puntos.

### Contradicciones y pendientes de aclaración

1. Entrega: la descripción dice 17/11 a las 00:00 hasta 21/11 a las 23:59, pero la fecha configurada y el calendario indican 17/11 a las 00:00. Conservo ambas; trabajar con el 17 como límite preventivo es una recomendación interna, no una modificación oficial.
2. Envolvente: bases 95×200 mm; anexo 90 mm y longitud 200–250; respuesta posterior máximo conjunto 90×200. Falta reconciliar documentos con el plano anunciado.
3. Scoresheet: 86 criterios visibles y 41 ocultos. Los máximos visibles suman 180; H177 incluye ocultos y suma 262. G2 promedia sólo D177/E177 aunque hay tercera columna y total F177. H175 permite máximo 10, distinto de la mayoría 0–2. No modifiqué ni recalculé el original ni tomo esas fórmulas como confirmación del criterio efectivo del jurado.
4. La respuesta sobre altitud indica ±2 m para apogeo y calibración barométrica a cero al lanzamiento. La repregunta por incertidumbres completas sigue sin respuesta visible; no generalizo esa tolerancia.
5. Se anunciaron documentos de vector y ensayos ambientales para esta semana; no aparecen como recursos nuevos en el curso inspeccionado.
6. El idioma obligatorio y duración máxima del video no quedaron confirmados en una instrucción escrita nueva de estas páginas. Conservo nuestras notas de reunión como antecedente, sin atribuirlas a una revisión íntegra del audio.

### Efecto sobre mi área y evidencia

Preparé un mapa entre ítems del PDR, diapositivas, filas y tareas. Tierra ocupa ítems 69–74 (diapositivas 72–77); faltan alternativas de antena/patrones, montaje y selección, comandos verificados, solar, unidades y pruebas físicas. El banco sintético no cierra esos criterios.

Las actualizaciones técnicas se registran en ASTRA-18/20/21/22/24/25 y la investigación del rotor en ASTRA-36. ASTRA-33 conserva sólo el respaldo. Mantengo esta tarea En curso por las aclaraciones y materiales pendientes; esta entrada no modifica tareas ajenas.

Informe, inventario y fuentes: https://github.com/edulandoni/astra-cansat/blob/5f9d8c310ecbecc9e1b7d0cc8d29d5d43df7b406/ground-station/docs/aula/2026-10-19/revision-aula.md  
Mapa PDR: https://github.com/edulandoni/astra-cansat/blob/5f9d8c310ecbecc9e1b7d0cc8d29d5d43df7b406/ground-station/docs/aula/2026-10-19/mapa-pdr-groundstation.csv  
Celdas y fórmulas inspeccionadas: https://github.com/edulandoni/astra-cansat/blob/5f9d8c310ecbecc9e1b7d0cc8d29d5d43df7b406/ground-station/docs/aula/2026-10-19/revision-scoresheet.json  
Copia Drive verificada: https://drive.google.com/file/d/1FA0LB32ekpHXlosXWMAVkTuWswSj9gKC/view?usp=drivesdk  
Las rutas relativas de la copia Markdown se navegan desde GitHub. No republico completos los archivos del aula en el repositorio público.

### 2026-10-19T21:11:47.075-0300 — comentario 10076

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-37?focusedCommentId=10076). Última edición informada: 2026-10-19T21:11:47.075-0300.

## 19/10/2026 — COMENTARIO 2 — Objetivo de cobertura total de la documentación oficial

Amplío el objetivo de esta tarea: investigar el 100% de toda la documentación oficial disponible para nuestra cuenta, incluidos archivos, aclaraciones, plantillas, evaluación y audiovisuales. Conservo la revisión inicial y sus resultados; no la declaro cobertura total.

Preparé un inventario inicial de 17 recursos ya identificados. La primera lectura de los cuatro archivos queda como revisión parcial hasta completar control exhaustivo por página/diapositiva/criterio e imágenes/referencias. Los seis debates y cinco páginas tienen lectura textual acreditada al corte anterior. Las dos piezas audiovisuales siguen abiertas; la reunión no tiene transcripción accesible por la vía comprobada. No calculo un porcentaje global con recursos heterogéneos ni cuento un video como revisado por su título.

Cada recurso conservará URL estable, versión/fecha o huella, evidencia, estado y pendiente. Registraré segmentos efectivamente revisados de los audiovisuales y ampliaré el inventario al aparecer recursos nuevos. Los documentos anunciados pero todavía no publicados quedan separados del material disponible. El objetivo permanece activo mientras exista contenido sin analizar; la falta de una transcripción automática no lo da por completado.

Amplié la automatización diaria existente para revisar también el aula, sus foros, archivos reemplazados, fechas y condiciones. Conservé 21:00 Argentina y política failed_runs_only. Las novedades o avances reales se registran aquí y los efectos técnicos en su tarea propia; ASTRA-33 conserva sólo respaldo y configuración. No habrá envíos ni entregas desde el aula.

Objetivo e inventario: https://github.com/edulandoni/astra-cansat/blob/88996d3c95fd1deb04760bdc08e778830bc7144d/ground-station/docs/aula/2026-10-19/objetivo-cobertura-total.md  
Inventario estructurado: https://github.com/edulandoni/astra-cansat/blob/88996d3c95fd1deb04760bdc08e778830bc7144d/ground-station/docs/aula/2026-10-19/cobertura-inicial.json  
Cambio: https://github.com/edulandoni/astra-cansat/commit/88996d3c95fd1deb04760bdc08e778830bc7144d

Esta entrada registra el objetivo y alcance; no presenta análisis nuevo del audio ni una ejecución futura de la automatización.

### 2026-10-19T21:36:34.543-0300 — comentario 10079

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-37?focusedCommentId=10079). Última edición informada: 2026-10-19T21:36:34.543-0300.

## 19/10/2026 — COMENTARIO 3 — ACTUALIZACIÓN de cobertura y lectura de apertura

Amplío los comentarios 1 y 2, sin sustituirlos. Completé el control de las 12 páginas de bases, siete de anexo, 89 diapositivas y seis imágenes incrustadas, y 177 filas con contenido de la hoja PDR. Revisé los 127 criterios con máximo numérico, incluidos 41 ocultos. El anexo enumera 65 requisitos; la referencia oculta a 55 es heredada. Cinco nombres definidos de puntuación conservan #REF! y PDRScore apunta a G2. No modifiqué los originales.

Pude obtener el audio completo de apertura (51:45) y leí toda la transcripción automática local, que no es una transcripción oficial. Inspeccioné 53 muestras visuales de esa reunión y 30 del institucional (2:26); el reconocimiento del audio institucional no produjo voz. Registro esos límites: no declaro 100% audiovisual exhaustivo ni confundo ausencia de voz reconocida con prueba de silencio. El objetivo sigue activo. El inventario ampliado reúne 22 recursos, incluidos siete debates y páginas auxiliares; no calculo un porcentaje mezclando recursos heterogéneos.

La apertura precisa: video 10–20 minutos; documentación/diapositivas en inglés y exposición en español (inglés oral permitido sin puntaje adicional); promedio de tres evaluadores y calidad de presentación hasta 10. Esto resuelve la duda sobre la excepción del máximo 10, pero no las filas ocultas ni la fórmula que promedia dos jurados. Se retiraron exigencias heredadas de Net ID/XBee; no se impone LoRa ni se elimina X2. El banco de simulación sigue siendo útil aunque no se exijan los comandos/modo heredados.

Hay diferencias que conservo expresamente: la charla admite separar partes y menciona margen de longitud, mientras el foro posterior indica conjunto unido y máximo 90×200 mm. No uso la grabación anterior para dar por aprobada otra configuración. Para el rotor se permite estudiar alternativas de descenso y se exige garantizar que no se abran dentro del cohete; no hay aprobación ni prueba de nuestra generación.

Volví a comprobar la entrega: acepta desde 17/11 00:00 y muestra vencimiento en ese mismo instante, aunque descripción y charla dicen 17–21. Mi recomendación inicial de anticipar al 17 no soluciona una actividad que todavía no permite entregar: hay que preparar antes y aclarar la configuración. No envié consultas ni entregas.

Encontré una séptima discusión, mensaje 50097, sobre autonomía/control desde tierra, sin respuesta oficial. Es una consulta de otro equipo, no una regla nueva. Avisos/presentaciones siguen vacíos; insignias/competencias/calificaciones no aportan documentación adicional. El plano del vector y perfiles anunciados siguen pendientes.

Publiqué mis notas y controles en groundstation, exclusivamente ground-station/. No hubo cambios de código ni ensayos físicos. La continuación es verificar íntegramente los audiovisuales y seguir las aclaraciones/versiones. Las consecuencias RF y rotor se registran en ASTRA-18 y ASTRA-36; el respaldo en ASTRA-33.

Auditoría: https://github.com/edulandoni/astra-cansat/blob/5728978901d20b221c6cd5c50c9841ac357be0bb/ground-station/docs/aula/2026-10-19/auditoria-archivos-actualizacion-01.md  
Audiovisuales, timestamps y novedades: https://github.com/edulandoni/astra-cansat/blob/5728978901d20b221c6cd5c50c9841ac357be0bb/ground-station/docs/aula/2026-10-19/audiovisuales-y-foro-actualizacion-02.md  
Inventario y pendientes: https://github.com/edulandoni/astra-cansat/blob/5728978901d20b221c6cd5c50c9841ac357be0bb/ground-station/docs/aula/2026-10-19/cobertura-actualizacion-02.json  
Copia Drive leída después de subirla: https://drive.google.com/file/d/1-4LCEyCUqAB6JCbZGa0nUAeqlLz0HUfK/view?usp=drivesdk  
Cambio: https://github.com/edulandoni/astra-cansat/commit/5728978901d20b221c6cd5c50c9841ac357be0bb

## Historial de cambios de campos

### 2026-10-19T21:01:21.876-0300 — cambio 10143

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Backlog

Después: Por hacer

### 2026-10-19T21:01:27.216-0300 — cambio 10144

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Por hacer

Después: En curso

