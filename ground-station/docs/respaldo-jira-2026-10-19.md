# 19/10/2026 — Respaldo Jira → GitHub

Relaciono este trabajo con [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20) y [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21).

## Qué automatizo

Preparo una lectura diaria a las 21:00 de Argentina, además del cierre de cada tanda. Uso el chat y sus conexiones autorizadas para leer Jira y publicar una captura nueva en la rama groundstation. La activación y su resultado quedan registrados en una entrada posterior de esta misma fecha.

No instalo una tarea de GitHub Actions en la configuración global del equipo. La ejecución programada depende de la disponibilidad de la aplicación, la máquina y sus conexiones; no promete un servicio independiente permanente.

Antes de exportar verifico las tareas creadas por mí o asignadas a mí. Consulto todas las páginas de tareas, comentarios e historial de cambios de campos. Si falta una página o falla el acceso, no publico una captura parcial como si estuviera completa. No modifico estados ni descripciones al hacer el respaldo.

Cada captura conserva fecha UTC de consulta y las fechas originales. Omite correos, identificadores de cuenta y comentarios restringidos o internos. No descarga adjuntos binarios ni reacciones. Si no hay cambios de contenido, conservo la captura anterior. Los comentarios marcados `[JIRA-GITHUB-SYNC]` y la fecha técnica de actualización por esos avisos no provocan nuevas capturas por sí solos.

## Cómo se guarda

El conector produce una lectura normalizada y verificada. Luego ejecuto:

```text
python ground-station/tools/guardar_bitacora.py --entrada CAPTURA_VERIFICADA.json
```

No guardo credenciales en el repositorio. El programa trabaja con una lectura ya obtenida: por sí solo no inicia sesión ni consulta Jira. Genera una carpeta nueva en ground-station/historial-jira/ con JSON, documentos por tarea, índice y huellas. No sobreescribe carpetas existentes.

El JSON de entrada tiene `captured_utc`, `complete: true` e `issues`. Cada tarea incluye `key`, `summary`, `description`, `status`, `assignee`, `creator`, `updated`, `owner_is_cristian: true`, `comments_complete: true`, `changelog_complete: true`, `comments`, `excluded_comments` y `changelog`. Los comentarios conservan `id`, `author`, `created`, `updated`, `body`; los cambios conservan `id`, `author`, `created` e `items` con `field`, `fromString`, `toString`. Solo marco verificada la pertenencia tras contrastar los identificadores reales de creador/asignación en el conector.

Publico únicamente nuevas capturas dentro de ground-station/, con una clave Jira en el mensaje del cambio. Agrego en mi tarea un comentario de respaldo con enlace a la captura y al cambio, marcado para evitar ciclos. Jira conserva el registro principal.

Referencias técnicas: [búsqueda paginada de Jira](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/) y [consulta de comentarios](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-comments/).
