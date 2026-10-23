# ASTRA-38 — DOC — Análisis automatizado del aula CONAE y prioridades al corte

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-38)

Estado observado: En curso. Asignación: Cristian Ponsone. Creación: Cristian Ponsone.

## Descripción original consultada

## Motivo

Necesito convertir el registro de fuentes del aula en un informe entendible para trabajar y preparar el PDR: qué preguntaron, qué respondió CONAE, qué se publicó, por qué nos sirve y qué sigue pendiente. No alcanza con un listado de enlaces ni con el contador de mensajes no leídos.

## Alcance y relación con otras tareas

Esta tarea conserva el análisis priorizado y el diario de cortes completos del aula. [ASTRA-37](https://astrateam2026.atlassian.net/browse/ASTRA-37) conserva las fuentes, control de versiones, cobertura, aclaraciones y contradicciones. [ASTRA-33](https://astrateam2026.atlassian.net/browse/ASTRA-33) conserva metodología, publicaciones y respaldo. Los efectos sobre nuestros desarrollos se vinculan a su tarea técnica. No reorganizo ni cambio tareas ajenas.

## Resultado de cada corte diario

Después de revisar el aula genero un informe nuevo con fecha y hora de corte en Argentina: resumen de novedades desde el corte anterior; panorama acumulado por prioridades; preguntas y respuestas explicadas con fuentes y fechas; entradas, archivos, videos y avisos; motivo de la prioridad, efecto para groundstation/PDR y acción sugerida; pendientes sin respuesta, contradicciones y límites de la consulta. Una duda de un participante no se transforma en requisito confirmado.

Publico en [Requisitos y aula CONAE de mi Drive](https://drive.google.com/drive/folders/1-bP1G1SJQ0rPiITxEWzIyLK3W5qofIK0), dentro de análisis y aclaraciones, y en ground-station/docs/aula/ de la rama groundstation. Dejo un comentario nuevo con el corte, conclusiones y enlaces. Conservo todos los informes y comentarios anteriores. Si no hubo novedades lo indico como corte sin cambios; no presento como nuevo el contenido acumulado.

## Prioridades

Uso prioridad alta cuando afecta cumplimiento, entrega, interfaces o un bloqueo real; media para decisiones y pruebas próximas; informativa para contexto. Justifico cada clasificación. Ordeno la información sin asignar tareas ni parámetros RF a otros integrantes.

## Criterios de verificación

* Recorrer todas las secciones, foros, páginas, mensajes completos y archivos disponibles; comparar cuerpos, versiones y huellas.
* Separar fecha de publicación, fecha de detección y hora de corte.
* Explicar qué cambió respecto del informe previo y enlazar la fuente estable.
* Diferenciar respuesta oficial, interpretación propia, pregunta abierta y resultado de prueba.
* No afirmar que el corte está completo ante lectura fallida, truncada, archivo no verificado o acceso faltante; registrar la limitación.
* Mantener originales y actualizaciones fechadas, sin borrar ni reemplazar el diario.
* No publicar credenciales, sesiones, transcripciones completas ni material técnico/personal de otros equipos; no enviar consultas o entregas.
* El éxito de configuración de la automatización no acredita su ejecución futura.

## Investigación complementaria

Los antecedentes de otros CanSat, fotos de referencia y sus resultados se investigan y documentan en [ASTRA-35](https://astrateam2026.atlassian.net/browse/ASTRA-35). Rotor y generación siguen en [ASTRA-36](https://astrateam2026.atlassian.net/browse/ASTRA-36). Desde este informe los enlazo cuando tengan relación, sin mezclarlos con requisitos CONAE.

## Comentarios conservados

### 2026-10-20T12:07:56.375-0300 — comentario 10088

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-38?focusedCommentId=10088). Última edición informada: 2026-10-20T12:07:56.375-0300.

## 20/10/2026 — COMENTARIO 1 — Primer informe priorizado del aula, corte 11:56 ART

### Objetivo y alcance

Inicié esta tarea y la pasé a En curso porque ya hice el primer corte: releí las tres secciones, los siete debates completos, los foros adicionales y la entrega, y volví a descargar los cuatro archivos oficiales. El análisis tiene 18 temas explicados, con origen, pregunta/publicación, respuesta, prioridad justificada, utilidad, acción sugerida y pendiente. Conservo el registro de fuentes en ASTRA-37.

### Novedad de este corte

El foro técnico pasa de 14 a 15 mensajes, con las mismas siete discusiones. La respuesta oficial nueva es [p50098](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2965#p50098), del 20/10 a las 08:28 según el aula: podemos enviar comandos para acciones específicas, justificando su utilización y cumpliendo la misión primaria. Actualiza la pregunta que seguía sin respuesta en el corte del 19/10. No habilita control manual irrestricto ni resuelve nuestro contrato de comandos con vuelo.

Comparé los cuerpos completos de los otros seis debates: siguen iguales tras normalizar espacios y excluir la navegación inferior. Las cuatro huellas SHA-256 coinciden con las del 19/10. No confundí un cambio de navegación o el indicador de no leídos con contenido nuevo.

### Panorama acumulado por prioridades

Prioridad alta, por cumplimiento, entrega o interfaz:

1. La entrega pide PDF llamado username - PDR y enlace al video. El texto dice 17–21/11, pero el vencimiento configurado sigue el 17/11 a las 00:00. Mantengo la contradicción; no asumimos que la plataforma estará abierta hasta el 21.
2. La nueva respuesta sobre comandos permite estudiar acciones concretas justificadas. Falta acordar qué puede ordenar tierra y cómo distingue enviado, recibido, rechazado y ejecutado.
3. El formato de telemetría es propio y debe justificarse. Para X2 se admite dirección de destino. La sintaxis heredada del banco no se convierte en formato obligatorio; filtrar por equipo no hace que la antena reciba sólo nuestra señal.
4. El comienzo de misión lo envía el CanSat al detectar separación real. Se permite telemetría durante ascenso. No se infiere separación sólo por recibir el primer paquete.
5. La aclaración posterior exige contenedor y carga útil unidos, dentro de 90 mm × 200 mm totales. Conservo las diferencias con otros textos y la grabación; nuestra investigación de rotor debe considerar esta restricción.
6. Vector y perfiles ambientales fueron anunciados, pero no apareció un documento nuevo con ellos. No inventamos ensayos, curva de ascenso ni puntos de sujeción para cerrar requisitos.
7. Sensores, calibración y referencias de altura importan. La tolerancia de apogeo respondida es ±2 m; no la aplicamos a todas las magnitudes. La tabla completa de precisión y las ventanas de promedios siguen sin aclaración.
8. Plantilla y scoresheet mantienen sus archivos. Siguen abiertas las inconsistencias sobre filas heredadas y cálculo con dos columnas de jurado frente a las tres mencionadas en apertura. No corregí la planilla oficial ni declaré puntajes validados.

Prioridad media, por decisiones y pruebas próximas:

9. STAND-BY es espera con el CanSat activado y consumo mínimo; no exige transmisión continua. Procesar 7200 mensajes acelerados no prueba dos horas de autonomía.
10. El segundo descenso puede ser activo o pasivo, incluido otro paracaídas. Eso abre alternativas, sin aprobar nuestro rotor ni demostrar su despliegue.
11. Las alturas anunciadas del vector son superiores a 500 m e inferiores a 1 km; no fijan apogeo nominal ni canal RF asignado.
12. No se admiten radios auxiliares ajenas a telemetría. Basta telemedir tensión solar; medir tensión no prueba energía útil ni carga de batería.
13. La entrada PDR pide requisitos, diseño, alternativas, prototipos/pruebas, presupuesto y cronograma. Podemos mostrar evidencia de PC con sus límites sin presentarla como vuelo validado.
14. La apertura, analizada el 19/10, menciona video de 10–20 minutos, documento en inglés y relato en español. No repetí hoy la transcripción.

Información y contexto:

15. Otros materiales y métodos de fabricación están permitidos si cumplen requisitos; la elección y validación de estructura siguen en su área.
16. La misión opcional se valora para desempatar. Conservo las aclaraciones de costos sin reabrir el análisis de presupuesto que dejamos para después.
17. Avisos sigue sin publicaciones y presentaciones sin temas. Ambos espacios se revisaron, no sólo el foro técnico.
18. La bienvenida y video institucional aportan contexto; no fijan parámetros RF ni demuestran prestaciones de ASTRA.

### Evidencia, límites y continuidad

Publiqué el [informe completo en Drive](https://drive.google.com/file/d/13hQj8Ckp6KJv3cu1L5xeCX3Rwx4_NbLe/view?usp=drivesdk) y el [método de cortes](https://drive.google.com/file/d/1vfcMYqX-nZhh_-icHyeb5jyx0g8puI_H/view?usp=drivesdk), dentro de Requisitos y aula CONAE/Análisis y aclaraciones. [Documentación y controles en GitHub](https://github.com/edulandoni/astra-cansat/commit/9208b923e87ddc301a89951e6b362ccd861e0d93). Verifiqué publicación remota, nombres, carpetas y texto completo de las copias de Drive.

Los audios y la auditoría estructural se heredan del análisis completo documentado del 19/10; no afirmo revalidación binaria de videos ni otra lectura total de las seis páginas públicas hoy. Los originales nuevos quedaron ordenados en Descargas con registro de movimientos. No envié preguntas, entregas ni formularios; no marqué actividades manualmente.

Amplié la automatización existente: después de revisar fuentes generará un informe por corte a las 21:00 de Argentina, aun sin novedades, diciéndolo expresamente. Conservará informes y comentarios previos; si falta acceso o lectura, identificará corte parcial. La configuración está verificada, pero la ejecución futura aún no se acredita.

La investigación de otros CanSat y sus referencias visuales continúa en ASTRA-35; los efectos concretos sobre interfaz están en ASTRA-24. Este informe no completa pruebas de radio, energía o hardware.

### 2026-10-20T21:06:30.375-0300 — comentario 10094

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-38?focusedCommentId=10094). Última edición informada: 2026-10-20T21:06:30.375-0300.

20/10/2026 — COMENTARIO 2 — Informe diario al corte 21:03 ART

Revisé once discusiones completas y 19 mensajes. Desde las 11:56 aparecieron cuatro preguntas de participantes, sin respuesta oficial: promedio de velocidad de descenso; liberación/recuperación de paracaídas y partes; carcasa/fibra de vidrio; presentación PDR y dos transmisores simultáneos. No las convierto en permisos ni requisitos. Los siete debates anteriores conservan sus cuerpos, fechas y autores; los cuatro archivos oficiales conservan sus SHA-256.

Prioridad alta: aclarar la ventana de promedio para no demostrar cumplimiento con un cálculo equivocado; mantener abierta la duda sobre desprendimientos; no incorporar una segunda radio por una consulta sin respuesta. También sigue la contradicción de entrega: texto 17–21/11 frente a vencimiento configurado 17/11 00:00. El material del vector y ensayos todavía no apareció; avisos y presentaciones siguen vacíos.

El informe conserva el panorama acumulado, explica cada pregunta/respuesta, utilidad y acción propuesta. Corte parcial respecto de revalidación total audiovisual: videos analizados el 19/10, sin nueva escucha ni huellas binarias hoy. Releí cronograma y cómo me inscribo en navegador. No envié consultas ni entregas y no cambié parámetros RF.

[Informe en Drive](https://drive.google.com/file/d/1IEjo_KDtY_J644xVQJyVwiDvvggk9Q5G/view) · [Informe y control en GitHub](https://github.com/edulandoni/astra-cansat/blob/cc2b6fd43bb544540e21837098d9aa1e0a142b65/ground-station/docs/aula/2026-10-20/Informe_aula_2026-10-20_2103_ART.md). Commit cc2b6fd43bb544540e21837098d9aa1e0a142b65 verificado remoto. Fuentes en ASTRA-37; antecedente DJS separado en ASTRA-35. Conservo los cortes anteriores.

### 2026-10-21T21:31:59.044-0300 — comentario 10098

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-38?focusedCommentId=10098). Última edición informada: 2026-10-21T21:31:59.044-0300.

21/10/2026 — COMENTARIO 3 — Corte diario PARCIAL, 21:30 ART

No pude acceder al curso ni al ingreso oficial: ambas navegaciones finalizaron por tiempo de espera. No ingresé credenciales ni modifiqué seguridad. No puedo afirmar sin novedades, conteos actuales ni que las cuatro preguntas de ayer sigan sin respuesta. El último acceso válido fue 20/10 21:03, con once debates y 19 mensajes; esos valores son históricos.

Leí las páginas públicas de cronograma e inscripción: sin cambio sustantivo detectado en sus textos relevantes. No sustituyen al aula ni resuelven la configuración contradictoria de entrega observada ayer. Prioridad alta: recuperar lectura completa de foros/adjuntos, entrega/calendario, archivos y eventual publicación del vector/perfiles. Mientras falta evidencia mantengo abiertas las decisiones sobre promedio, recuperación y dos transmisores.

El informe conserva todo el panorama acumulado, con fechas, fuentes, motivos y acciones, identificado como no revalidado hoy. No revisé grabaciones ni huellas de los cuatro archivos en esta ejecución. [Informe Drive](https://drive.google.com/file/d/1Igtm2qN_9OmHCEonSFouNK9jtkigdsji/view) · [GitHub](https://github.com/edulandoni/astra-cansat/blob/48b750db6e4ddadd9c2a5da429be37d7c82580b6/ground-station/docs/aula/2026-10-21/Informe_aula_2026-10-21_2130_ART.md), commit 48b750db6e4ddadd9c2a5da429be37d7c82580b6 verificado. El siguiente corte debe comparar desde la última lectura válida. Fuentes/impedimento en ASTRA-37; ficha COSMOS en ASTRA-35.

### 2026-10-22T21:09:44.937-0300 — comentario 10103

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-38?focusedCommentId=10103). Última edición informada: 2026-10-22T21:09:44.937-0300.

22/10/2026 — COMENTARIO 4 — Corte diario PARCIAL, 21:07 ART

El curso y la página de ingreso volvieron a finalizar por tiempo de espera. Es el mismo impedimento del 21/10: no duplico aviso en ASTRA-37. No llegué al formulario ni ingresé credenciales. No puedo afirmar sin novedades ni conocer las respuestas actuales del foro. La última lectura válida sigue siendo el 20/10 a las 21:03, con once discusiones y 19 mensajes, valores históricos.

Sí leí completas las páginas públicas de cronograma e inscripción; sin cambio sustantivo detectado en texto relevante. Conservan PDR 17–21/11 y anexo v2 del 16/10; no resuelven la configuración de entrega del aula registrada antes. No revalidé binarios públicos.

Prioridad alta: recuperar cobertura completa de secciones, foros/adjuntos, calendario/entrega, archivos, audiovisuales y eventual vector/perfiles. Mantengo las dudas e interpretaciones pendientes; el panorama acumulado está explicado por tema y marcado como no revalidado. No fijé parámetros RF ni envié consultas/entregas.

[Informe Drive](https://drive.google.com/file/d/1izbBRPsiI0f5BSQVKcYKK_BIkiX7sh3e/view) · [Informe y controles GitHub](https://github.com/edulandoni/astra-cansat/blob/b9a31b09aea7da3a2e8e027c41f6e6088c0f1eb3/ground-station/docs/aula/2026-10-22/Informe_aula_2026-10-22_2107_ART.md), commit b9a31b09aea7da3a2e8e027c41f6e6088c0f1eb3 verificado remoto. Conservo el corte anterior. Investigación RSX y efecto sobre rotor en ASTRA-35/36, separados de requisitos CONAE.

## Historial de cambios de campos

### 2026-10-20T11:49:38.574-0300 — cambio 10146

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Backlog

Después: Por hacer

### 2026-10-20T11:50:25.422-0300 — cambio 10147

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Por hacer

Después: En curso

