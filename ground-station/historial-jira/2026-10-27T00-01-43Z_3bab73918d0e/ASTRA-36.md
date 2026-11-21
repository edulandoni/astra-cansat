# ASTRA-36 — INV — Evaluar autorrotación y generación eléctrica en descenso

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-36)

Estado observado: En curso. Asignación: Cristian Ponsone. Creación: Cristian Ponsone.

## Descripción original consultada

## Objetivo

Estudiar la posibilidad de un rotor de descenso que produzca electricidad y comparar beneficio energético, masa, estabilidad, despliegue y modos de falla. Es investigación conceptual, no autorización de un sistema de recuperación.

## Alcance y estado real

Antecedentes de autogiro y generación eólica CanSat localizados; cálculo gravitatorio reproducible publicado. El ejemplo de 0,5 kg, 400 m de tramo y conversión global hipotética del 10% da 0,05448 Wh; no demuestra rendimiento real. No hubo ensayo físico, CFD ni validación aerodinámica.

## Requisitos y dependencias

La v2 exige paracaídas C3 y otro sistema C4; estudiar admisibilidad del rotor para C4 sin darla por aprobada. No sustituye paneles E3 ni autonomía dentro del cohete E7. Las decisiones de recuperación y alimentación se coordinan con sus responsables; no modifico sus tareas ni carpetas.

## Entregable y cierre de la investigación

Informe con fuentes, hipótesis, balance energético, alternativas y criterios de prueba; recomendación justificada de continuar, descartar o ensayar. Faltan geometría, coeficientes respaldados, consumo real, presupuesto de masa y condiciones de falla. No afirmo novedad mundial ni implementación de vuelo. Registro futuras conclusiones como actualizaciones nuevas.

## Comentarios conservados

### 2026-10-19T20:41:12.926-0300 — comentario 10058

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-36?focusedCommentId=10058). Última edición informada: 2026-10-19T20:41:12.926-0300.

## 19/10/2026 — COMENTARIO 1 — Autorrotación, energía y pendientes de viabilidad

### Procedencia y objetivo

Separo el análisis del rotor del comentario 9 de ASTRA-21:  
https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10052  
No borro el original ni modifico sus resultados. Estudio beneficio energético frente a masa, estabilidad, descenso y despliegue; no apruebo un diseño de recuperación.

### Qué hice y qué concluyo

La misión AAS 2025 exigía autogiro, y SEDS ITBA ganó esa edición. ICARE documentó generación eólica en un CanSat en 2013, pero su informe es previo al vuelo: no demuestra energía obtenida. No puedo afirmar novedad mundial.

Revisé C3/C4 de nuestra copia v2: primera etapa con paracaídas; la segunda admite estudiar otro sistema, sujeto a confirmar admisibilidad. No reemplazo paneles de E3 ni alimentación durante la espera E7. No envié consultas ni tomé decisiones por los responsables de recuperación.

Ejecuté un cálculo reproducible con masa constante 0,5 kg, apogeo ficticio 500 m, rotor desde 400 m y descenso supuesto 5 m/s. El tramo duraría 80 s y representa 0,5448 Wh gravitatorios. Con conversión global hipotética del 10% serían 0,05448 Wh y 2,452 W medios: unos 3,27 minutos ideales a 1 W. Verifiqué las relaciones aritméticas entre potencia, energía y tiempo. La eficiencia y las alturas del ejemplo no son prestaciones medidas ni requisitos confirmados.

### Límites y próximos pasos

El cálculo no resuelve aerodinámica ni predice rpm, arranque o estabilidad. Cargar eléctricamente el eje frena el rotor y puede modificar el descenso. No hubo prueba física, CFD ni comprobación de despliegue. Debemos comparar rotor libre/cargado, energía neta, masa y fallas de carga abierta, cortocircuito o trabado. La investigación queda En curso; no significa que asumimos construirlo para vuelo.

### Evidencia

Informe: https://github.com/edulandoni/astra-cansat/blob/f5fda9162f8b67d3ad70b086f3d3613f9f814434/ground-station/docs/investigacion/2026-10-19-rotor-y-generacion.md  
Reproducción: https://github.com/edulandoni/astra-cansat/tree/f5fda9162f8b67d3ad70b086f3d3613f9f814434/ground-station/experiments/2026-10-19-rotor  
Resultados: https://github.com/edulandoni/astra-cansat/tree/f5fda9162f8b67d3ad70b086f3d3613f9f814434/ground-station/evidence/2026-10-19-rotor-escala  
Copia Drive: https://drive.google.com/file/d/1gn-23kr-wZz9REoaCJ5ZivTevtMtpFoc/view?usp=drivesdk  
Antecedentes comparativos: ASTRA-35.

### 2026-10-19T20:44:05.419-0300 — comentario 10064

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-36?focusedCommentId=10064). Última edición informada: 2026-10-19T20:44:05.419-0300.

## 19/10/2026 — COMENTARIO 2 — Ubicación en GitHub corregida

La viabilidad del rotor, el cálculo ilustrativo y sus evidencias continúan aquí. El informe inicial conserva su referencia histórica a ASTRA-21; esta tarea no implica aprobación de un diseño de vuelo.

Agregué un índice por tema, sin cambiar resultados, código ni originales. La reorganización no constituye otro ensayo.

Guía de esta tarea: https://github.com/edulandoni/astra-cansat/blob/a4c26b05bc66ef77efa702f03256e4bb3ba2d3c8/ground-station/docs/temas/rotor-y-energia/README.md  
Mapa vigente: https://github.com/edulandoni/astra-cansat/blob/a4c26b05bc66ef77efa702f03256e4bb3ba2d3c8/ground-station/docs/trazabilidad-vigente-2026-10-19.md  
Cambio: https://github.com/edulandoni/astra-cansat/commit/a4c26b05bc66ef77efa702f03256e4bb3ba2d3c8

El comentario 1 de esta tarea conserva el motivo, trabajo previo, resultados y límites. Las próximas actualizaciones temáticas se agregan aquí.

### 2026-10-19T21:03:49.962-0300 — comentario 10073

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-36?focusedCommentId=10073). Última edición informada: 2026-10-19T21:03:49.962-0300.

## 19/10/2026 — COMENTARIO 3 — ACTUALIZACIÓN de admisibilidad general y prioridad del rotor

Amplío el comentario 1 con dos respuestas oficiales del 19/10: https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2961#p50091 y https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2963#p50093

Se acepta un segundo sistema de descenso activo o pasivo; puede ser otro paracaídas. No hay aprobación específica de nuestro rotor ni comprobación de despliegue, estabilidad o C4. Contenedor y carga útil bajan juntos. La envolvente conjunta se aclara como máximo 90×200 mm, en discrepancia con los 200–250 mm del anexo conservado; falta reconciliarla con el plano anunciado.

La misión secundaria es opcional y se valoraría a igualdad de puntos. Distingo usar un rotor para cumplir C4 de agregar generación como misión extra: son aportes distintos. Esa respuesta no garantiza puntuación por nuestra generación; conviene priorizar requisitos demostrables antes de asumir complejidad adicional.

La espera de dos horas se aclara con consumo mínimo en rampa, sin transmisión obligatoria continua. Por eso la comparación energética anterior de 1 W durante dos horas sigue siendo sólo un ejemplo, no el consumo que CONAE exige. El cálculo de 0,05448 Wh al 10% hipotético no cambia, pero tampoco predice energía real.

No cambié el diseño ni hice ensayos nuevos. Mantengo la investigación En curso. El detalle y sus fuentes están en ASTRA-37 y https://github.com/edulandoni/astra-cansat/blob/5f9d8c310ecbecc9e1b7d0cc8d29d5d43df7b406/ground-station/docs/aula/2026-10-19/revision-aula.md

### 2026-10-19T21:37:03.021-0300 — comentario 10081

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-36?focusedCommentId=10081). Última edición informada: 2026-10-19T21:37:03.021-0300.

## 19/10/2026 — COMENTARIO 4 — ACTUALIZACIÓN de rotor y despliegue con la apertura

Amplío los comentarios 1 y 3 con la grabación oficial del 16/10: https://www.youtube.com/watch?v=m4-HQMSi2Wo&t=1637 (aproximadamente 27:20–28:25). Se menciona expresamente estudiar un segundo paracaídas, un rotor o un sistema activo; hay que justificar que no se despliegue dentro del fuselaje ni trabe la expulsión. Esto abre una alternativa de investigación, no aprueba nuestro rotor ni la generación eléctrica.

Conservo una contradicción: alrededor de 32:45–33:55 la charla admite separar partes; la respuesta posterior del 19/10 exige que contenedor y carga bajen juntos: https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2963#p50093. No uso el audio anterior para dar por aprobada la separación. También conservo las diferencias de longitud hasta el plano anunciado.

La apertura confirma que la misión secundaria se valora ante igualdad y no aporta por sí sola una puntuación ordinaria garantizada. El cálculo energético anterior permanece hipotético; no hice ensayos ni cambié el diseño. Para evaluar una propuesta necesitamos comparar despliegue, estabilidad, masa y energía neta con rotor libre/cargado, y justificar que sigue cumpliendo el descenso.

Fuente y método de análisis asistido: https://astrateam2026.atlassian.net/browse/ASTRA-37?focusedCommentId=10079  
Informe con timestamps y límites: https://github.com/edulandoni/astra-cansat/blob/5728978901d20b221c6cd5c50c9841ac357be0bb/ground-station/docs/aula/2026-10-19/audiovisuales-y-foro-actualizacion-02.md

### 2026-10-22T21:09:53.147-0300 — comentario 10105

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-36?focusedCommentId=10105). Última edición informada: 2026-10-22T21:09:53.147-0300.

22/10/2026 — COMENTARIO 5 — ACTUALIZACIÓN: estabilidad previa y evidencia de rotor

Amplío el estudio anterior con el PFR RSX registrado en ASTRA-35. Sus autores vinculan pérdida del paracaídas y vuelco con despliegue incorrecto/trabado del autogiro. El documento contiene conclusiones contradictorias y no verifiqué videos/datos crudos: no afirmo causa probada ni que todo rotor se comporte así.

La consecuencia para nuestra investigación es estudiar si el mecanismo necesita orientación estable para abrirse y cómo responde si falla la etapa anterior. Propongo una futura matriz con descenso estabilizado, orientación desfavorable, apertura parcial, giro trabado y generador conectado/desconectado. Apertura, giro sostenido, estabilidad, descenso y energía deben verificarse por separado. Hoy no ejecuté esos ensayos ni fijé valores aerodinámicos o diseño de recuperación.

Un pulso Hall o palas abiertas no prueban generación neta. Para sostener esa afirmación necesitamos tensión/corriente con tiempo, energía útil y efecto de carga sobre giro, además de masa y cumplimiento. El antecedente no aporta esa medición: mantengo la idea como investigación sin beneficio energético acreditado, conservando el cálculo gravitatorio anterior.

[Actualización Drive](https://drive.google.com/file/d/1ZL9LAkGOirKYrtgR-eC2yJXTcJRbLsFb/view) · [GitHub](https://github.com/edulandoni/astra-cansat/blob/b9a31b09aea7da3a2e8e027c41f6e6088c0f1eb3/ground-station/docs/investigacion/2026-10-22-rotor-estabilidad-y-evidencia.md) · [PFR y límites de fuente](https://github.com/edulandoni/astra-cansat/blob/b9a31b09aea7da3a2e8e027c41f6e6088c0f1eb3/ground-station/docs/investigacion/2026-10-22-rsx-pfr-y-fallas.md), commit b9a31b0 verificado. La semántica de estado, apertura confirmada y régimen estable queda como propuesta para el acuerdo de interfaz, no ICD aprobado. No adopto porcentajes extranjeros ni decido tareas ajenas.

### 2026-10-24T03:59:18.363-0300 — comentario 10164

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-36?focusedCommentId=10164). Última edición informada: 2026-10-24T03:59:18.363-0300.

24/10/2026 — COMENTARIO 6 — ACTUALIZACIÓN: Energía incremental: incluir lo que cuesta el agregado

Amplié el análisis con consumo adicional y admitiendo resultados negativos. En un ejemplo hipotético fijo de 0,5 kg, 400 m, descenso de 5 m/s y eficiencia global del 10 %, el máximo convertido del modelo es 0,05448 Wh sin consumo auxiliar. Con 0,2 W adicionales durante los 80 s de descenso queda 0,05004 Wh; si ese consumo también permanece 7.200 s antes de liberar, el balance incremental pasa a −0,34996 Wh.

Son supuestos de exploración, no componentes elegidos ni energía medida. Las pérdidas ya incluidas en la eficiencia no se descuentan dos veces. El consumo común sólo se cancela al comparar duraciones iguales; si el rotor modifica el tiempo de descenso hay que incorporar también esa diferencia de consumo. El modelo actual no resuelve aerodinámica ni cambios de trayectoria. Pasaron las dos pruebas del cálculo y conservé el análisis anterior.

Recomiendo sostenerlo como investigación opcional y no presupuestar generación no demostrada. Faltan geometría, masa real, consumo, despliegue, estabilidad y ensayos. La tarea permanece abierta y no sustituye requisitos de energía o autonomía.

[Modelo, casos y límites en GitHub](https://github.com/edulandoni/astra-cansat/blob/9735087c1074754895273c4109553f5b350c7faf/ground-station/docs/investigacion/2026-10-24-rotor-energia-incremental.md)
[Copia verificada en Drive](https://drive.google.com/file/d/1eKQxEkvz1YpKhs5bEKdukatljL_bncNy/view)

## Historial de cambios de campos

### 2026-10-19T20:39:39.171-0300 — cambio 10137

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Backlog

Después: Por hacer

### 2026-10-19T20:40:00.670-0300 — cambio 10141

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Por hacer

Después: En curso

