# 19/10/2026 — Primera revisión del aula oficial CONAE

Diario: [ASTRA-37](https://astrateam2026.atlassian.net/browse/ASTRA-37). Esta entrada amplía las revisiones del 17/10 y los análisis del 19/10; no sustituye documentos anteriores. Registra mi lectura de fuentes y los efectos sobre mi área, sin modificar decisiones de otros responsables.

## Acceso y alcance comprobado

Ingresé al [aula oficial](https://educacion.conae.gov.ar/aulavirtual/) y al [curso CanSat Universitario 2026–2027](https://educacion.conae.gov.ar/aulavirtual/course/view.php?id=106). La identificación de la cuenta no define por sí sola el formato ni el valor del TEAM_ID del protocolo; eso sigue siendo un acuerdo de interfaz. No guardé contraseña, cookies ni enlaces con claves de sesión en esta documentación.

Revisé las tres secciones visibles del curso, las cuatro fuentes descargables, los seis debates técnicos visibles (13 mensajes: 6 preguntas, 6 respuestas y 1 repregunta), avisos, presentaciones, entrega, calendario y vista de calificaciones. La nómina mostraba 122 participantes/cuentas, lo que no equivale a 122 equipos; no exporté la nómina. No envié mensajes, no entregué trabajos ni marqué manualmente actividades. La lectura del foro puede actualizar su indicador de leído.

La grabación de apertura dura 51:45 y está enlazada por el aula. No encontré transcripción disponible en YouTube y no doy por revisado todo su audio. El video institucional incrustado también queda inventariado, sin análisis íntegro de audio. Esta revisión cubre el texto y los archivos descritos, no materiales futuros u ocultos a la cuenta.

## Fuentes y versiones

Conservé los cuatro originales con sus nombres, huellas y registro de movimientos en mi carpeta local de la revisión del aula. No los edité ni los republico completos aquí. El [inventario de fuentes](fuentes.json) enlaza cada recurso autenticado.

| Material | Comprobación |
| --- | --- |
| [Bases y condiciones](https://educacion.conae.gov.ar/aulavirtual/mod/resource/view.php?id=5139) | PDF de 12 páginas, SHA-256 d416ed8c463786b4c23196bec8b2e31002156f27126a3e7d9e14fe0dac6c39eb. |
| [Anexo A v2](https://educacion.conae.gov.ar/aulavirtual/mod/resource/view.php?id=5140) | SHA-256 27932c87654b64b443d41483c9b48adb06d7d1379dd7a01d54e4ea0035057bc7: idéntico byte por byte al que analizamos el 17/10. Las aclaraciones nuevas están en el foro, no en un PDF distinto. |
| [Plantilla PDR v2](https://educacion.conae.gov.ar/aulavirtual/mod/resource/view.php?id=5465) | 89 diapositivas; incluye portadas/cierre y 85 ítems numerados. No son 80 hojas Excel. |
| [Scoresheet v2](https://educacion.conae.gov.ar/aulavirtual/mod/resource/view.php?id=5466) | Una hoja llamada PDR. Revisé celdas, fórmulas, validaciones y filas ocultas. |

## Hallazgos de evaluación y entrega

La página de [entrega PDR](https://educacion.conae.gov.ar/aulavirtual/mod/assign/view.php?id=5467) pide un PDF cargado por una persona del equipo, nombre formado por usuario y PDR, y enlace al video dentro del formulario. Su texto anuncia del **17/11/2026 a las 00:00 al 21/11/2026 a las 23:59**, pero la tabla y el calendario fijan fecha de entrega **17/11/2026 a las 00:00**. Registro las dos referencias; no doy por resuelta su diferencia entre apertura, vencimiento y cierre. Planificar con el 17 como límite preventivo hasta aclaración es una recomendación interna, no cambio del plazo oficial.

El idioma obligatorio del entregable y el máximo del video no quedaron confirmados mediante una instrucción escrita nueva de las páginas inspeccionadas. La plantilla está en inglés y tiene una diapositiva para el enlace del video. Conservo la nota de nuestra reunión (PDR inglés, video español y unos 15 minutos) como antecedente del equipo, pendiente de cotejo del audio o aclaración escrita. No convierto esa nota en una cita textual del aula.

Las bases describen selección de 20 equipos tras PDR y 6 tras CDR; para el vuelo mencionan pruebas de caída, integración dimensional y batería, además de demostración real de tierra. La evidencia sintética que tenemos no reemplaza esa validación.

### Anomalías concretas del Scoresheet

La [revisión estructurada](revision-scoresheet.json) conserva coordenadas y fórmulas:

- Hay 86 filas de criterios visibles: 85 numeradas y una de calidad de presentación. La mayoría permite de 0 a 2, pero H175 fija máximo 10. Por eso no afirmo que todos los criterios valen exactamente dos puntos.
- Hay 41 filas de criterios ocultas. Algunas conservan contenidos de otra configuración, como geometrías mayores, huevo o parapente. No las adopto como requisitos nuestros por encontrarlas en el archivo.
- H177 suma H4:H176, incluidas las filas ocultas: el máximo aritmético es 262, frente a 180 de los criterios visibles. Ocultar filas no las elimina de SUM. No afirmo que así se calculará la evaluación oficial; lo dejo como inconsistencia que requiere aclaración.
- Hay columnas de tres jurados, pero G2 usa sólo D177 y E177; F177 tiene su propio total y queda fuera de esa fórmula. No lo corrijo sobre el archivo oficial ni uso G2 como autoevaluación fiable sin confirmación.
- El ítem 68 aparece en una fila oculta de simulación y en otra visible de plan de desarrollo. Las expectativas de los ítems 35 y 55 conservan referencias que las respuestas oficiales aclaran. No importo automáticamente todos los textos de la planilla como nuevos requisitos.

## Respuestas oficiales que cambian nuestra lectura

Las siguientes respuestas son de Pablo González en el foro del curso. Son aclaraciones identificadas y fechadas; no reescriben las versiones archivadas del anexo. En cada discrepancia conservo ambas fuentes y el pendiente.

### Telemetría y direccionamiento

En [2961, respuesta del 19/10](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2961#p50091) se permite definir y justificar nuestro formato. En [2963, respuesta del 19/10](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2963#p50093) se confirma que el destino del paquete satisface la interpretación de X2, según lo que defina el equipo. También se limita el uso de transmisores del equipo a los destinados al intercambio de telemetría.

Esto resuelve la ausencia de un formato oficial detallado en el anexo, pero no aprueba automáticamente nuestro ASCII22 ni fija bytes, CRC, direcciones o parámetros RF. Corresponde acordar el ICD con vuelo. No habilita equipos auxiliares de transmisión sin revisar esa limitación ni convierte el identificador en autenticación o inmunidad a interferencia.

### Inicio, espera y altitud

En [2960, respuesta del 19/10](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2960#p50090), el comienzo de misión lo comunica el CanSat al detectar separación real; se admite telemetría durante ascenso. STAND-BY significa equipo activado en espera. Las dos horas se describen como una espera hipotética en rampa con consumo mínimo, sin exigir transmisión continua; la cámara puede condicionar la grabación.

Se indica tolerancia de ±2 m para determinar el apogeo; siguen sin especificarse en esa respuesta la ventana exacta del promedio de descenso y otros detalles preguntados. En [2959, respuesta del 16/10](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2959#p50085) se pide ajustar el barométrico a cero al lanzamiento y considerar también GPS; la incertidumbre depende del sensor y calibración. La repregunta posterior sobre una tabla completa de errores permanece sin respuesta visible. No convierto ±2 m en tolerancia universal de todos los sensores.

### Panel solar

La respuesta [2963](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2963#p50093) permite cumplir informando la tensión del panel; no exige recargar batería. Debemos incluir esa medición y la consulta batería/solar de X6 en el acuerdo de datos y la pantalla. No considero resuelto el hardware ni el comando por esta aclaración.

### Contenedor, descenso y envolvente

En [2963](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2963#p50093) se aclara que contenedor y carga útil descienden juntos. Se acepta segundo paracaídas; [2961](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2961#p50091) admite un segundo sistema activo o pasivo. La respuesta menciona por error aparente el ítem 55 al contestar la duda sobre parapente: conservo esa referencia y no la corrijo como si hubiera sido publicada de otra manera.

Hay tres geometrías documentadas: bases 95 × 200 mm, anexo diámetro 90 y longitud 200–250 mm, y respuesta posterior máximo conjunto 90 × 200 mm. Para un estudio preventivo usaría la envolvente más restrictiva, pero falta reconciliar formalmente los documentos con el plano del vector. Se anuncia vuelo por encima de 500 m y por debajo de 1000 m; no es una altura nominal exacta para nuestro simulador.

La respuesta [2962](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2962#p50092) permite materiales y fabricación distintos de impresión 3D si cumplen los requisitos. No sustituye análisis ni ensayos estructurales.

### Innovación y presupuesto

La misión secundaria se considera opcional y se valoraría en igualdad de puntos, según [2963](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2963#p50093). Por eso el rotor generador se mantiene como investigación: primero debemos sostener los requisitos puntuables. La admisión general de sistemas de descenso activos o pasivos no aprueba un rotor específico ni demuestra su funcionamiento.

Sin ampliar ahora el análisis de presupuesto, registro la aclaración encontrada: gastos de importación, envíos e impuestos integran el costo final; equipos existentes quedan fuera y donaciones requieren estimación. Para moneda extranjera se indica cotización oficial al presentar el presupuesto. Son las respuestas de [2959](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2959#p50085) y [2963](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2963#p50093), no una interpretación nueva mía.

## Qué pide específicamente el PDR de tierra

El [mapa de ítems y evidencia](mapa-pdr-groundstation.csv) vincula ítem numerado, diapositiva real, fila de la planilla y tarea. Los ítems 69–74 están en diapositivas 72–77: arquitectura general, conexiones, comparación de al menos dos antenas con patrones, montaje, selección justificada y software de tierra. Los ítems 55/56 piden ejemplo de telemetría y lista de comandos; el 79 pide plan de simulación.

Disponemos de banco, GUI y evidencia sintética para explicar lo realizado. Faltan antena/selección, integración RF, comandos verificados, solar, unidades y pruebas de operación física. La expectativa del software menciona calibración de ángulos además de barómetro, sin un requisito equivalente claro en el anexo: queda TBR, no agrego un comando obligatorio unilateralmente.

## Inventario de páginas y pendientes reales

| Sección | Resultado de la revisión |
| --- | --- |
| Avisos y novedades | Sin novedades publicadas al consultar. |
| Presentación de equipos | Sin temas visibles al consultar. No publiqué presentación. |
| Consultas Etapa 2 | Seis debates revisados; la repregunta de precisión seguía abierta. |
| Grabación del 16/10 | [Video oficial enlazado](https://www.youtube.com/watch?v=m4-HQMSi2Wo), 51:45; sin transcripción accesible, audio completo pendiente. |
| Entrega y calendario | Diferencia 17/11 frente al intervalo escrito hasta 21/11. No entregué archivos. |
| Evaluación de la cuenta | Sin calificación publicada; no exporté datos personales. |
| Vector y ensayos ambientales | Se anuncian documentos para esta semana en respuestas 2960 y [2964](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2964#p50096); no aparecen como recursos nuevos en el curso inspeccionado. |
| CDR y etapas futuras | El curso explica que se habilitarán a quienes avancen. No doy por revisados documentos todavía no visibles. |

Pendientes prioritarios: confirmar fecha real de vencimiento/cierre; resolver envolvente; consultar tratamiento de filas ocultas, fórmula y jurados del Scoresheet; obtener documentos de vector/ensayos; cerrar formato/comandos con vuelo; cotejar idioma y duración del video. No envié esas consultas: esta entrada registra las preguntas para el canal del equipo.

## Efecto y continuidad por tarea

ASTRA-37 conserva revisión de fuentes, contradicciones y pendientes. ASTRA-18 recibe direccionamiento e interpretación de X3; ASTRA-24, formato y comandos; ASTRA-20, simulación y espera; ASTRA-21, registros/altitudes y versión del esquema; ASTRA-22, solar y evidencia de pantalla; ASTRA-25, expectativas de antena; ASTRA-36, alcance del rotor y prioridad de innovación. ASTRA-33 conserva sólo la publicación/respaldo. No modifico tareas de otras áreas.
