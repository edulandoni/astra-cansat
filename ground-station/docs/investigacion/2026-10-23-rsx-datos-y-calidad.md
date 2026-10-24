# 23/10/2026 — ACTUALIZACIÓN RSX: datos de misión y calidad

Diarios: [ASTRA-35](https://astrateam2026.atlassian.net/browse/ASTRA-35) y [ASTRA-34](https://astrateam2026.atlassian.net/browse/ASTRA-34). Amplío el [análisis del PFR del 22/10](2026-10-22-rsx-pfr-y-fallas.md), sin reemplazarlo. Hoy contrasté la [planilla publicada](https://github.com/adam-kabbara/RSX-CANSAT-2025/blob/da327893982c1afd6e480e9cf3d89b43ebca273e/competition_documentation/3114_mission_data_cansat_2025.csv.xlsx), fijada al commit `da327893982c1afd6e480e9cf3d89b43ebca273e`. Leí sus celdas con openpyxl en modo de lectura; no ejecuté programas del equipo ni modifiqué la planilla. No analicé los videos.

## Qué contiene y cómo lo conté

La hoja `cansat_data` ocupa A1:AA108, con 27 columnas, encabezado y 107 filas no vacías. Separé 93 filas de telemetría mediante PACKET_COUNT numérico; las otras 14 son diagnósticos en CMD_ECHO (filas 2–14 y 68). No las cuento como paquetes corruptos ni como muestras de sensores. No hay fórmulas. Los [resultados agregados y método](2026-10-23-rsx-metricas.json) permiten revisar el cálculo sin republicar el archivo ajeno o coordenadas.

Los contadores van de 1 a 93 sin huecos, duplicados o retrocesos dentro de ese intervalo publicado. No demuestra ausencia de pérdida RF fuera de él ni captura de toda la misión. PACKET_RECV coincide con PACKET_COUNT en las 93 muestras; sin conocer cómo se produce esa columna, no lo tomo como prueba independiente del receptor.

## Estados, tiempo y eventos: son cosas distintas

La primera muestra es de 18:03:50 y la última de 18:05:22. Hay 53 LAUNCH_PAD, 11 ASCENT, una APOGEE, siete DESCENT y 21 PROBE_RELEASE; no hay LANDED. La última altitud publicada es 50,2. Esto limita la cobertura: no alcanza para atribuir la ausencia a una causa de radio, impacto o exportación por sí sola.

El máximo de ALTITUDE es 622,8 en F78, a las 18:04:52 y todavía con estado ASCENT. APOGEE aparece en la fila 80, dos segundos después, con 608,1. La primera PROBE_RELEASE está en la fila 88, a las 18:05:02, con altitud 441, aproximadamente 70,81% de 622,8. Coincide aproximadamente con el relato del 70% del PFR, pero el estado enviado no certifica el instante mecánico de liberación. Conservo la discrepancia con el 75% mencionado en otra parte del PFR.

El PFR sitúa el fin de telemetría en 18:05:20; esta planilla llega a 18:05:22. Registro la diferencia sin elegir una versión ni atribuir causa. La referencia de 826,3 m del PFR continúa sin reconstrucción de su base. No convierto esas diferencias en requisitos CONAE.

GPS_SATS es cero en todas las muestras; las coordenadas también son cero. No encuentro evidencia de fix válido. AUTO_GYRO_ROTATION_RATE pasa de cero a 0,6 en la fila 88 y conserva ese valor hasta la 108. El valor constante no permite distinguir por sí solo giro físico sostenido, resolución, actualización del sensor o dato retenido. No demuestra generación eléctrica.

## Referencia visual que sí observé

Abrí e inspeccioné el [gráfico publicado de giro](https://raw.githubusercontent.com/adam-kabbara/RSX-CANSAT-2025/da327893982c1afd6e480e9cf3d89b43ebca273e/pfr_plots/png_plots/payload_auto-gyro_rotation_rate_plot.png), de 800 × 500 píxeles. Muestra el escalón de cero a 0,6 con eje rotulado °/s y bandas de estado. Es un gráfico de datos, no una foto del mecanismo, ni validación independiente de la planilla. La fecha original y licencia individual no están confirmadas; conservo sólo el enlace. Se incorpora como F13 en el [catálogo nuevo](2026-10-23-catalogo-visual-rsx.csv).

## Qué propongo para nuestro manejo de datos

Propongo separar telemetría, diagnóstico y rechazo de formato con contadores distintos. También conservar el instante de recepción, el tiempo de misión y la antigüedad de cada dato válido; mostrar estado declarado y evento físico confirmado como conceptos distintos. Un valor plano debe poder investigarse sin declararlo automáticamente válido o fallado. La ausencia de LANDED debe exponerse como captura incompleta, sin inventar una causa de pérdida.

Son criterios para diseñar pruebas futuras de ASTRA-34 y el parser/GUI, no funciones implementadas hoy ni ensayos aprobados. No cambié código, ICD o perfil RF. Queda revisar semántica/unidades desde el productor y contrastar videos si aportan evidencia útil. Esta pasada profundiza una ficha; no valida toda la solución RSX ni su clasificación.

## Procedencia y conservación

Fuente de 21.542 bytes, SHA-256 `b5c99bd15782dc2428ad97f408d73ee5616a5c426ab3e4d40cbd7662ba20b87d`. El original queda en Descargas, carpeta temática del 23/10, con registro de origen/destino y sin cambios de huella después del análisis. Referencias de celdas: A2:AA108; máximo F78; estado E80; liberación E88/F88; giro S88:S108. No republico el binario ni datos personales. Conservo el análisis previo completo y agrego esta actualización.
