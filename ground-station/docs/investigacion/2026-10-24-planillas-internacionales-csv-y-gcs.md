# 24/10/2026 — Planillas internacionales: distinguir pantalla de archivo

Diario: [ASTRA-35](https://astrateam2026.atlassian.net/browse/ASTRA-35). Continúo los [antecedentes convertidos en pruebas](2026-10-23-antecedentes-a-pruebas.md) y los [criterios generales del premio](2026-10-24-criterios-premio-groundstation.md), conservándolos.

## Tres fuentes y su edición

Abrí la [página Mission del organizador](https://cansatcompetition.com/mission.html): ahora se identifica para 2027, con guía y scoresheet anunciadas como actualizadas el 23/10/2026. No comparé una copia binaria anterior de esa página ni de la guía. Su contexto ya es PocketQube y dos emisores; no es una descripción de nuestra misión CONAE ni prueba de lo que usaron los ganadores de 2025/2026.

Leí completo el texto de dos planillas de una página enlazadas allí. No inspeccioné imágenes de estaciones de equipos. Pedí capturas de las planillas, pero no recibí píxeles inspeccionables: mantengo pendiente su revisión visual.

La [planilla GCS](https://cansatcompetition.com/assets/docs/competition/Ground%20Station%20Scoresheet.pdf) separa comprobaciones antes y durante el vuelo. Revisa órdenes, gráficos, datos simultáneos y recepción; distingue enviar una orden de comprobar el mecanismo. El contenido incluye acciones de PocketQube propias de ese contexto. No contiene resultados de un equipo ni demuestra robustez ante pérdida o reinicio.

La [planilla CSV](https://cansatcompetition.com/assets/docs/competition/CSV%20Data%20Score%20Sheet.pdf) revisa nombre y orden de columnas, estados presentes, efecto de calibración, conteos y eventos. Indica una revisión del archivo con el equipo y conservación del soporte por el jurado. No publica aquí datos crudos, puntajes aplicados ni tolerancias de pérdida; su lista no prueba que una implementación la haya superado.

## Qué extraigo para nuestro banco

Esta es mi interpretación para preparar evidencia; no una incorporación de obligaciones internacionales a CONAE. Mantengo nuestro formato de práctica y el ICD pendiente con Edu.

| Antecedente | Riesgo propio | Comprobación útil | Evidencia actual / límite |
|---|---|---|---|
| Pantalla y archivo tienen controles separados | Dar por guardado lo que sólo vimos | Contrastar emisor, parser, CSV y registro bruto | Dos campañas USB de 131 muestras: contraste documentado; no RF |
| Enviar y ejecutar se revisan por separado | Confundir envío con resultado | Mostrar aceptación/rechazo/ejecución o desconocido | Catorce controles repetidos en dos pasadas; simulación, sin actuadores |
| El CSV debe permitir recorrer eventos | Un resumen no explica qué pasó | Conservar identidad, orden original y procedencia | Recuperación y sesiones de banco; formato final compartido pendiente |
| La evaluación distingue fases | Una captura aislada oculta regresiones | Procedimiento de inicio, misión y cierre con evidencia | GUI de reproducción observada; campo y legibilidad al sol pendientes |

Los enlaces a nuestras [guardas USB](../2026-10-24-ordenes-negativas-usb.md), [conservación del evento](../2026-10-24-bitacora-copias-y-verificacion-final.md) y [calidad medida](2026-10-24-calidad-medida-y-cierre-investigacion.md) muestran trabajo ya realizado. Leer estas planillas no constituye otra campaña ni prueba nueva de ASTRA. No modifiqué software o tareas técnicas por esta pasada.

## Conservación y faltantes

Calculé SHA-256 sobre los PDF públicos leídos en memoria, sin guardar ni republicar binarios: GCS, 59.879 bytes, `00b377cd4d25db98065f97b41117c9b782e8239d18838b681c5667db55c0f55d`; CSV, 54.799 bytes, `9debcdc145cb9cbabe294e32d7fe6bdca20c3bdeee6fd91eb6c7ebd4fb6eede7`. Son huellas de esta consulta, no prueba de igualdad con una edición previa. La referencia visual queda en el [catálogo nuevo](2026-10-24-catalogo-visual-planillas.csv).

Sigue faltando documentación técnica y puntuación aplicada de DJS para atribuir el premio a funciones concretas; tampoco encontré en esta pasada un PFR/dataset nuevo de Daedalus. Las fuentes localizadas por búsqueda que no abrí no se cuentan como leídas. La investigación del rotor continúa separada en ASTRA-36; estas planillas no demuestran energía generada.
