# 24/10/2026 — ACTUALIZACIÓN 08: reconstrucción bloqueada por conflictos dentro de un diario

Diarios: [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21) y [ASTRA-34](https://astrateam2026.atlassian.net/browse/ASTRA-34). Amplío las pruebas de recuperación de la [actualización 01](2026-10-23-banco02-actualizacion-01.md); conservo esa entrada y sus resultados.

## Problema y efecto

El receptor identifica dos mensajes válidos con igual contador y diferente contenido como conflicto. Conserva el primero en CSV y deja la contradicción en el diario bruto mediante un evento validated/classification=conflict. No convierte la segunda versión en otra fila de telemetría única.

El recuperador comparaba correctamente filas contradictorias entre archivos, pero ignoraba esa marca interna al leer un solo diario. Podía reconstruir una fila y declarar salida limpia aunque el registro de adquisición ya avisara que existía otra versión. Es un límite distinto del conflicto entre dos copias que ya estaba probado.

Agregué el bloqueo ante esa marca, con archivo, línea, contexto y contador en el informe. No adjudico qué versión mide la realidad, no elijo silenciosamente la primera y no genero un CSV reconstruido mientras exista la contradicción. Conservo entradas y originales, y escribo sólo un resultado nuevo que explica el impedimento.

## Prueba reproducible

Generé una captura sintética con contador 1 y altitud 0,0 m, seguida por el mismo contador con altitud 999,0 m. El receptor conservó una fila candidata y registró el conflicto. Sobre el mismo diario, la versión anterior del recuperador escribió un CSV; la nueva dejó written=false y un conflicto, sin cambiar el original ni escribir un CSV reconstruido.

Pasaron las 18 pruebas de software, incluidas la nueva para el conflicto interno y las anteriores de copias contradictorias, reconstrucción limpia, CSV/JSONL y preservación de originales. [Comparación antes/después y huellas](../evidence/2026-10-24-banco02/recuperacion-conflicto-interno-12.json).

El límite sigue siendo la información disponible: si sólo selecciono un CSV y falta el diario donde estaba la marca, no puedo inferir esa contradicción ausente. No prometo recuperar datos que ninguna fuente conserva ni resolver discrepancias de medición automáticamente.

## Relación con la corrida USB

La herramienta de recuperación es offline. No cambié el firmware, el código cargado por la GUI en ejecución ni el snapshot de la [segunda corrida prolongada](2026-10-24-medidor-y-reinicio-prolongado-actualizacion-07.md). Su cierre verificará adquisición/archivo con sus huellas; la reconstrucción posterior se identificará con la versión nueva del recuperador. No atribuyo retrospectivamente esta corrección a ensayos anteriores.
