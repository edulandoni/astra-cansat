# 19/10/2026 — Actualización del destino del respaldo diario

Jira: [ASTRA-33, comentario 2](https://astrateam2026.atlassian.net/browse/ASTRA-33?focusedCommentId=10055).

Actualizo la ubicación indicada en [el documento anterior](respaldo-jira-2026-10-19.md) y [su activación](historial/2026-10-19-respaldo-diario.md), que conservo íntegros. La tarea del exportador y los avisos generales de respaldo es ahora ASTRA-33. No los agrego al simulador ASTRA-20 ni al receptor ASTRA-21.

Corregí la automatización existente `respaldo-diario-jira-github-groundstation`, sin crear otra. Conservé la frecuencia diaria de las 21:00 de Argentina, estado ACTIVE y política de notificaciones `failed_runs_only`. El cambio de configuración fue confirmado por la aplicación y comprobado en la configuración guardada. Esto no acredita todavía una ejecución futura con el nuevo destino.

Las reglas técnicas anteriores siguen vigentes: consultar todas mis tareas por creador/asignación verificados, todas las páginas de comentarios e historial, excluir datos privados, generar una carpeta nueva y manifiesto, conservar las anteriores y publicar sólo dentro de ground-station/historial-jira/ en groundstation. Si no cambia el contenido, no crear un commit ni otro aviso. Los avisos `[JIRA-GITHUB-SYNC]` no producen un ciclo por sí solos.

La consulta no debe limitarse a las siete tareas originales: las nuevas tareas propias también se incluyen. Antes de escribir un aviso verifico que ASTRA-33 siga dentro de mi alcance. Si no lo está, informo el impedimento; no elijo otra tarea por comodidad. No cambio estados ni descripciones como parte del respaldo.

Para saber dónde registrar un avance técnico uso el [mapa vigente](trazabilidad-vigente-2026-10-19.md). El horario, la disponibilidad de la aplicación, la máquina y las conexiones siguen siendo dependencias. El respaldo de CSV de vuelo es otro trabajo y permanece en ASTRA-21.
