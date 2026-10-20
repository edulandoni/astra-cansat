# 19/10/2026 — ACTUALIZACIÓN 1: control completo de los cuatro archivos

Diario: [ASTRA-37](https://astrateam2026.atlassian.net/browse/ASTRA-37). Continúo la [revisión inicial](revision-aula.md) y el [objetivo de cobertura](objetivo-cobertura-total.md), que conservo. Este control amplía la evidencia de lectura; no acredita ensayos de hardware ni resuelve contradicciones entre fuentes.

## Qué comprobé y cómo

Revisé el texto completo de las 12 páginas de bases, las siete del anexo, las 89 diapositivas y todas las filas con contenido de la única hoja del Scoresheet. Rendericé y revisé las 19 páginas PDF; inspeccioné también las seis imágenes incrustadas de la presentación. Son elementos gráficos institucionales, sin un requisito técnico adicional que faltara en la extracción textual. Revisé notas, relaciones externas, objetos, criterios ocultos, fórmulas, validaciones y comentarios del archivo de evaluación.

Los cuatro originales conservan los nombres y huellas publicados en [fuentes.json](fuentes.json). La lectura no modificó los originales. Los textos completos y las imágenes de inspección permanecen en la carpeta local de trabajo; publico mis conclusiones y controles, sin redistribuir completos los materiales del aula.

## Bases: cobertura por página

| Página | Contenido revisado y consecuencia |
| --- | --- |
| 1 | Objetivos del certamen y aprendizaje de ingeniería. Las afirmaciones del PDR necesitan justificación y evidencia. |
| 2 | Composición, pertenencia y modificaciones del equipo. Lo registro como contexto; no modifico integrantes. |
| 3 | Participación, inscripción y entrega PDR. Comparo el plazo con la actividad del aula; la discrepancia sigue abierta. |
| 4 | Selección PDR/CDR, revisiones de preparación y presentaciones. La estación debe llegar integrada, con evidencia disponible antes de la revisión. |
| 5 | Envolvente, altura y organización de evaluación. Conservo 95×200 mm como dato de bases, junto con los valores distintos de anexo y foro. |
| 6 | Evaluación PDR: requisitos, alternativas, prototipos, costos y planificación. No alcanza mostrar una interfaz atractiva. |
| 7 | CDR y preparación: resolver TBD/TBR y demostrar integración. Las decisiones compartidas de comunicaciones deben acordarse antes de esa etapa. |
| 8 | Operación de la estación, roles y revisión de vuelo. Distingo ensayos sintéticos de la demostración del enlace real. |
| 9 | Presentación posterior al vuelo y logística. Debemos conservar datos originales y procesados para explicar resultados y fallas. |
| 10–12 | Condiciones generales, autorizaciones, responsabilidades y premios. Lectura documental; no envié ni acepté formularios en nombre del equipo. |

## Anexo: 65 requisitos identificados

El inventario por prefijo es C1–C9 (9), S1–S9 (9), M1–M4 (4), E1–E9 (9), X1–X6 (6), SN1–SN8 (8), G1–G15 (15) y F1–F5 (5): **65 en total**. La referencia a 55 que conserva una fila oculta del Scoresheet es una discrepancia de esa planilla, no una reducción del anexo vigente.

| Grupo | Revisión y efectos sobre mi trabajo |
| --- | --- |
| C1–C9 | Misión, descenso en dos etapas, frecuencia de telemetría, videos, baliza y costo. El simulador debe representar eventos coherentes; no certifica velocidades ni mecanismos reales. |
| S1–S9 | Masa, dimensiones, vibración, choque, estructura, salida y montaje. El análisis de tierra conserva límites del conjunto para coordinar antena/interfaz; no aprueba el diseño mecánico. |
| M1–M4 | Restricciones de mecanismos, elementos calientes y contactos. Son dependencias de integración; no decisiones unilaterales de groundstation. |
| E1–E9 | Baterías, panel solar, acceso a encendido, indicación y alimentación de baliza. Debo registrar tensión solar y distinguir autonomía de espera de consumo durante misión. |
| X1–X6 | Bandas permitidas, destinatario, inicio, cadencia, campos y consultas de tensión. No equivalen a seleccionar LoRa, FSK, frecuencia o direccionamiento concretos. |
| SN1–SN8 | Altitud barométrica, temperatura, tensión, GPS, IMU, video y corriente. La GUI debe explicar unidades, vigencia y pérdida de datos; una señal ausente no debe convertirse en un cero válido. |
| G1–G15 | Cero por comando, CSV y copia, reloj, recepción/presentación, gráficos, estado, autonomía, portabilidad, antena, legibilidad, vista simultánea y telecomandos. Es el núcleo de mis criterios de aceptación. |
| F1–F5 | Contador, tiempo y calibración persistentes, UTC, comandos y estados. Una simulación del reinicio no demuestra persistencia física; debo acordar semántica y ensayos con vuelo. |

Para tierra, G14 exige contar recepción efectiva: el contador transmitido sirve para detectar saltos, pero no sustituye nuestro contador de paquetes recibidos. G12/G13 requieren legibilidad y visualización simultánea; no basta esconder telemetría en pestañas. G2 requiere conservar el CSV y una copia, que es un respaldo distinto del diario Jira.

## Presentación: 89 diapositivas, 85 ítems

Las diapositivas 1–3 son portada, introducción y enlace al video; las 4–88 corresponden a los ítems 1–85; la 89 cierra la presentación. Revisé cada ítem, incluidas expectativas y tablas, aunque su responsabilidad pertenezca a otra área. No impongo metodología ni cambios a esas áreas.

| Ítems | Cobertura |
| --- | --- |
| 1–3 | Índice, equipo y acrónimos. |
| 4–14 | Misión, requisitos, alternativas, configuración, dimensiones, disposición, operación y compatibilidad con vector. |
| 15–31 | Sensores: presión, temperatura, tensión/corriente, GPS, aceleración, giro y cámaras; comparación y selección. |
| 32–36 | Descenso: alternativas y elección de ambos sistemas. El texto heredado sobre parapente no invalida la aclaración oficial que admite otras soluciones. |
| 37–46 | Mecánica, componentes, mecanismos, masas, incertidumbre y margen. |
| 47–56 | Procesamiento y comunicaciones: CPU, memoria, interfaces, radio, control de transmisión, ejemplo de paquete y comandos. El formato debe acordarse y justificarse. |
| 57–65 | Energía: bloques, tensión, corriente máxima, capacidad, configuración, alternativas y presupuesto en Wh. |
| 66–68 | Arquitectura de software, estados, reinicios, muestreo y plan de desarrollo. |
| 69–74 | Estación de tierra: contexto, conexiones, dos alternativas de antena con patrones, soporte, elección y prototipo de software con comandos, gráficos y CSV. |
| 75–79 | Ensayos por subsistema, integración, ambiente y simulación. Se deben distinguir plan de prueba y resultado ejecutado. |
| 80–85 | Presupuestos, cronogramas, asignaciones y conclusiones. |

No encontré enlaces externos, notas con contenido adicional, gráficos de datos ni objetos incrustados que agreguen una segunda fuente técnica a la presentación. Algunos bloques de expectativas están vacíos; no invento criterios para completarlos como si fueran oficiales. El [mapa de groundstation](mapa-pdr-groundstation.csv) sigue siendo la entrada a mis ítems.

## Scoresheet: criterio visible y estructura heredada

Revisé las 177 filas con contenido y ocho columnas de la hoja PDR, incluidas las ocultas. Hay 127 filas con máximo numérico: 86 visibles y 41 ocultas. Los visibles reúnen los 85 ítems y la calidad de presentación. La suma de máximos visibles es 180; la suma que incluye ocultos es 262.

La fórmula de G2 usa D177 y E177, aunque existe F177 para un tercer jurado. H177 suma también las filas ocultas. La calidad de presentación admite hasta 10; la mayoría de los demás criterios llega a 2. Por eso no tomo el relato informal de «todo 0, 1, 2» ni el resultado de esa fórmula como regla definitiva de evaluación.

Las filas ocultas incluyen dimensiones y conceptos heredados, separación, parapente y referencias a otra cuenta de requisitos. También aparece repetida la numeración 68 entre un criterio oculto y el plan de desarrollo visible. El nombre definido PDRScore apunta a PDR!$G$2; los otros cinco nombres de puntuación conservan #REF!. No hay texto adicional en encabezados o pies. No eliminé filas ni corregí fórmulas del archivo oficial. No encontré comentarios, hipervínculos, gráficos ni vínculos externos de libro que aporten instrucciones adicionales. Estas anomalías requieren aclaración oficial; no impiden acreditar la lectura completa del archivo.

## Hasta dónde llegué

Completo el control documental de estos cuatro archivos. Continúo por separado con los audiovisuales y la revisión de novedades del aula. No declaro todavía cobertura total del curso. Mantengo abiertas las contradicciones de dimensiones, fecha de entrega, evaluación y cualquier aclaración pendiente; tampoco presento como ejecutadas pruebas físicas, de RF o autonomía.
