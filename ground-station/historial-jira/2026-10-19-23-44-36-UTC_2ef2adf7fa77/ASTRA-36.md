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

