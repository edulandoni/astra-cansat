# ASTRA-34 — GND — Investigar calidad de datos y prevención de fallas

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-34)

Estado observado: En curso. Asignación: Cristian Ponsone. Creación: Cristian Ponsone.

## Descripción original consultada

## Objetivo

Evaluar mejoras de groundstation con datos sintéticos, distinguiendo mensaje válido de dato reciente, coherente y conservado. Seleccionar mejoras por evidencia antes de comprometer implementación.

## Trabajo y entregable

Investigar indicadores explicables, antigüedad, sesiones, contradicciones y campañas reproducibles de fallas. Conservar hipótesis, sondeos, resultados y alternativas. Separar del trabajo de receptor/parser/CSV y de la GUI; vincular esos entregables cuando corresponda.

## Estado real y límites

Ya ejecuté diez sondeos de software y publiqué sus resultados. El monitor propuesto no está implementado ni validado; no hay hardware ni prueba RF. Los ensayos concretos de almacenamiento y reconexión conservan su bitácora técnica en ASTRA-21. Las ideas enumeradas no se convierten automáticamente en compromisos de desarrollo.

## Criterio para completar esta investigación

Comparar comportamiento actual y mejoras candidatas, métricas de detección/demora/falsas alarmas, dependencias del ICD y recomendación justificada. Crear o actualizar una tarea de implementación sólo cuando el alcance esté asumido. Conservar los originales y registrar cambios mediante actualizaciones fechadas.

## Comentarios conservados

### 2026-10-19T20:41:08.837-0300 — comentario 10056

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10056). Última edición informada: 2026-10-19T20:41:08.837-0300.

## 19/10/2026 — COMENTARIO 1 — Incorporación de la investigación de calidad y prevención

### Procedencia y objetivo

Incorporo aquí la investigación que registré en ASTRA-21, comentario 6:  
https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10049  
Conservo ese original y su fecha; esta entrada ordena el tema y no representa una segunda ejecución. Busco elegir mejoras verificables antes de conectarnos al hardware.

### Trabajo y resultados ya obtenidos

Ejecuté diez sondeos con datos sintéticos, TEAM_ID 1000 ficticio y fallas inyectadas. El nominal aceptó 131 muestras y rechazó equipo ajeno. El parser aceptó números finitos pero deliberadamente anómalos (altura 3000 m, temperatura 999 °C, giro 9999 °/s), alturas y hora congeladas. Un mismo contador con contenido diferente no tuvo aviso específico de conflicto; ambos quedaron raw. Ante retroceso del contador, latest conservó un valor alto anterior. La excepción controlada de escritura raw terminó el worker con ERROR.

Estos resultados distinguen validación de estructura y evaluación de calidad; no fijan umbrales operativos ni demuestran qué sensor falló. Presión/altura del mismo sensor no son redundancia independiente.

### Propuesta y límites

Propongo evaluar avisos explicables de dato reciente, retenido, sospechoso o ausente, con métricas de demora, detecciones omitidas y falsas alarmas. También registré ideas de simulación coherente, pruebas de comandos y entrenamiento de operador como posibilidades, no compromisos ya implementados. No implementé el monitor, no probé hardware ni RF y no cambio ICD ni parámetros compartidos.

Las comprobaciones concretas de volumen, reconexión y recuperación de CSV siguen como avance técnico de ASTRA-21, comentario 8:  
https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10051  
Las utilizo como evidencia relacionada, sin duplicar su bitácora ni afirmar integración operativa del recuperador.

### Evidencia y próximos pasos

Informe: https://github.com/edulandoni/astra-cansat/blob/82a80614e186a5f8b50559eea8a293503154f02d/ground-station/docs/investigacion/2026-10-19-innovacion-y-prevencion.md  
Experimento: https://github.com/edulandoni/astra-cansat/tree/82a80614e186a5f8b50559eea8a293503154f02d/ground-station/experiments/2026-10-19-prevencion  
Resultados: https://github.com/edulandoni/astra-cansat/tree/82a80614e186a5f8b50559eea8a293503154f02d/ground-station/evidence/2026-10-19-investigacion-prevencion

Comparar alternativas y acordar sesiones, unidades y métricas antes de implementar. Dejé la investigación En curso porque ya tiene análisis y sondeos ejecutados; no cierro funciones pendientes.

### 2026-10-19T20:44:01.243-0300 — comentario 10062

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10062). Última edición informada: 2026-10-19T20:44:01.243-0300.

## 19/10/2026 — COMENTARIO 2 — Ubicación en GitHub corregida

La investigación y sus sondeos continúan aquí. Los ensayos de reconexión y recuperación CSV permanecen en ASTRA-21; los informes originales conservan sus referencias históricas.

Agregué un índice por tema, sin cambiar resultados, código ni originales. La reorganización no constituye otro ensayo.

Guía de esta tarea: https://github.com/edulandoni/astra-cansat/blob/a4c26b05bc66ef77efa702f03256e4bb3ba2d3c8/ground-station/docs/temas/calidad-de-datos/README.md  
Mapa vigente: https://github.com/edulandoni/astra-cansat/blob/a4c26b05bc66ef77efa702f03256e4bb3ba2d3c8/ground-station/docs/trazabilidad-vigente-2026-10-19.md  
Cambio: https://github.com/edulandoni/astra-cansat/commit/a4c26b05bc66ef77efa702f03256e4bb3ba2d3c8

El comentario 1 de esta tarea conserva el motivo, trabajo previo, resultados y límites. Las próximas actualizaciones temáticas se agregan aquí.

### 2026-10-21T21:32:11.259-0300 — comentario 10101

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-34?focusedCommentId=10101). Última edición informada: 2026-10-21T21:32:11.259-0300.

21/10/2026 — COMENTARIO 3 — ACTUALIZACIÓN de evidencia para prevenir falsos diagnósticos

El antecedente COSMOS de ASTRA-35 aporta un caso concreto: 525 filas, 89 identificadores ausentes en el intervalo de contador y campos GPS/giro a cero. No demuestra la causa de los huecos ni que cero sea una medición válida. La captura de GUI tampoco acredita el mismo conjunto completo que el CSV.

Para nuestras verificaciones propongo separar recibido, válido, guardado y faltante de contador; conservar origen y antigüedad; y evitar presentar GPS ausente como posición real o un hueco como pérdida RF confirmada. Las pruebas deberán indicar qué falla se inyectó y con qué registro contrastamos. Es una ampliación de criterios de investigación: hoy no cambié código ni ejecuté otro ensayo de ASTRA.

[Evidencia, método y límites](https://github.com/edulandoni/astra-cansat/blob/48b750db6e4ddadd9c2a5da429be37d7c82580b6/ground-station/docs/investigacion/2026-10-21-cosmos-csv-y-estacion.md) · [Métricas](https://github.com/edulandoni/astra-cansat/blob/48b750db6e4ddadd9c2a5da429be37d7c82580b6/ground-station/docs/investigacion/2026-10-21-cosmos-metricas.json) · [Informe Drive](https://drive.google.com/file/d/1-Wscr0q91TqCbbWjQxsjWEvwY-0xtl9g/view). No copio datos o parámetros extranjeros como requisito propio.

## Historial de cambios de campos

### 2026-10-19T20:39:34.384-0300 — cambio 10135

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Backlog

Después: Por hacer

### 2026-10-19T20:39:55.604-0300 — cambio 10139

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Por hacer

Después: En curso

