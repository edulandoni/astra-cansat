# 19/10/2026 — Antecedentes CanSat para orientar nuestras decisiones

Bitácora: [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21). Continúo la [investigación anterior](2026-10-19-innovacion-y-prevencion.md) y conservo sus conclusiones como historial.

## Qué revisé y qué falta

Preparé un [catálogo consultable de 35 registros equipo–edición](2026-10-19-catalogo-cansat.csv): los 10 finalistas escolares argentinos de 2022/2023, los 20 puestos primero a quinto de AAS 2023–2026, un premio específico de Ground Station, tres antecedentes europeos y un informe de generación eólica. Un mismo equipo en dos años cuenta dos veces. Es un relevamiento inicial delimitado, no todos los CanSat del mundo ni 35 auditorías completas.

Distingo cuatro evidencias: resultado oficial, diseño publicado, ensayo relatado por sus autores y datos crudos reproducibles. Un PDR describe lo previsto; un premio acredita su categoría. Ninguno garantiza que cada componente funcionó ni que sea seguro para nuestra misión. No reuní todavía un conjunto comparable de registros crudos de vuelo para todos estos equipos.

Las fuentes CONAE corresponden al certamen escolar: sirven como antecedentes, pero sus requisitos no reemplazan al universitario 2026/2027. Tampoco comparo puntajes de AAS entre años, porque cambian misión y evaluación.

## Qué ganó y qué puedo aprender

| Antecedente | Evidencia disponible | Qué podemos aprovechar y qué no afirmo |
| --- | --- | --- |
| SEDS ITBA, AAS 2025 | Primer puesto oficial; PDR localizado; entrevista posterior a un integrante | Estudiar integración y pruebas de un autogiro. El premio no acredita por sí solo generación eléctrica ni cada prestación del PDR. |
| PWr Aerospace, AAS 2024 | Primer puesto; repositorio de Ground Station y CDR públicos | Revisar separación de recepción, visualización y simulación. El código público no acredita que cada función se probó en vuelo. |
| Shockwave, AAS 2024 | Segundo puesto; CDR localizado | Contrastar alternativas documentadas. Revisión técnica integral del CDR pendiente. |
| Daedalus, AAS 2026 | Primer puesto; organizador enlaza PDR/CDR | Prioridad para ampliar revisión. No presento un documento localizado como leído completo. |
| DJS Arya, AAS 2026 | Premio específico Ground Station | Referencia prioritaria para tierra; falta obtener criterios del jurado y evidencia que expliquen el premio. |
| Cóndor Salvaje, Argentina 2023 | Artículo técnico con ensayos y vuelo; reconocimiento institucional | Los autores informan 98% de recepción en vuelo y despliegue parcial del parapente. La telemetría y la recuperación requieren indicadores separados. |
| gVIE, Argentina 2022 | Lanzamiento oficial; repositorio mCALCAN con fuentes y documentos | Revisar código y documentación conservando versiones y licencias. No deduzco fiabilidad de largo plazo de su sola publicación. |
| Astoria, Bélgica 2024 | Reconocimiento oficial; repositorio y sitio propios | Estudiar conservación de datos para análisis posterior. La documentación del equipo no sustituye registros verificables de cada ensayo. |
| WerndlExplorer y Astra Aether, ESA 2023 | Premios de divulgación y profesionalismo | La comunicación clara y explicar fallas también aportan. Son categorías distintas de rendimiento de radio. |
| ICARE, C’Space 2013 | Informe técnico previo al vuelo | Antecedente directo de hélice generadora. No encontré en ese informe energía medida durante vuelo. |

El artículo de Cóndor Salvaje relata ensayos de recepción a 50, 100 y 150 m y un vuelo desde aproximadamente 500 m. Informa unos 80,5 s de descenso, 6,2 m/s medios y aterrizaje a 67 m del objetivo. También describe dificultades de despliegue pese a numerosos ensayos de plegado. Son resultados comunicados por sus autores; no dispongo de los archivos crudos para repetir el cálculo. Su hélice motorizada para guiado no es una demostración de autorrotación generadora. No trasladamos sus baterías o parámetros a nuestro reglamento.

Los restantes casos argentinos amplían las misiones conocidas: atmósfera y calidad de aire, incendios, meteorología, ruido, iluminación, polvo y muestreo de microplásticos. El lanzamiento documentado no demuestra calibración, precisión ni cumplimiento completo de esas misiones secundarias. Los identifico en el catálogo para continuar con documentos técnicos propios.

## Qué incorporo a nuestro trabajo a partir de esto

1. Evaluar éxito por separado: datos recibidos, datos conservados, despliegue, descenso, localización y misión secundaria. Un sistema puede tener buena radio y fallar mecánicamente.
2. Mantener reproducción de vuelos y escenarios de falla en tierra. Guardar configuración, datos originales y resultado esperado; un video o una gráfica aislados no bastan para reconstruir un ensayo.
3. Mostrar explícitamente antigüedad del último dato, pérdidas, reinicios y GPS inválido. Son propuestas para evaluar contra nuestro estado actual, no funciones nuevas que dé por implementadas aquí.
4. Comparar alternativas con beneficio medido, masa, consumo, complejidad, modos de falla y esfuerzo de validación. Elegir algo porque ganó otro equipo sería insuficiente.
5. Tratar el rotor generador como experimento separado hasta obtener evidencia: [análisis específico](2026-10-19-rotor-y-generacion.md).

## Límites y siguiente revisión

Todavía faltan participantes fuera de los cinco primeros de AAS, más ediciones y países, informes posteriores al vuelo, causas de fallas y datos crudos. BioBit y los documentos históricos de Novationes ya aparecían en nuestro relevamiento anterior; no los declaro inexistentes ni completamente auditados por no completar aquí su revisión. Los PDR grandes de ITBA y Shockwave se localizaron y consultaron parcialmente; quedan pendientes de lectura íntegra y contraste con resultados posteriores.

Para ampliar cada ficha registraré: fuente, versión/fecha, requisito de su certamen, diseño, ensayo, resultado, falla y evidencia faltante. Una actualización futura se agrega con fecha, sin sustituir esta entrada. La investigación queda en mi área de documentación; no cambia decisiones ni tareas de otros subsistemas.

## Fuentes primarias

- [CONAE: finalistas y lanzamientos 2022](https://www.argentina.gob.ar/noticias/se-lanzaron-desde-la-conae-cinco-satelites-cansat-construidos-por-estudiantes-de-la) y [2023](https://www.argentina.gob.ar/noticias/cansat-2023-cinco-equipos-de-escuelas-secundarias-lanzaron-sus-satelites-en-el-centro).
- [AAS: clasificación 2023–2026 y premio Ground Station](https://www.cansatcompetition.com/winners.html).
- [PWr: Ground Station 2024](https://github.com/PWr-Aerospace/CanSat2024_Ground_Station) y [CDR](https://www.cansatcompetition.com/docs/teams/Cansat2024_2044_cdr_v01.pdf).
- [Shockwave: CDR 2024](https://cansatcompetition.com/docs/teams/Cansat2024_2078_cdr_v2.0.pdf).
- [Daedalus: PDR 2026](https://www.cansatcompetition.com/assets/docs/2026/cansat2026_1043_pdr_v07.pdf).
- [Cóndor Salvaje: artículo técnico](https://static.even3.com/anais/1443303.pdf?v=639041730014778153) y [reconocimiento UNT](https://medios.unt.edu.ar/2023/10/10/rector-vice-recibieron-alumnos-instituto-tecnico-aguilares-se-destacaron-final-cansat-2023/).
- [gVIE: mCALCAN](https://github.com/its-villada/mCALCAN).
- [Astoria: resultado belga](https://www.innoviris.brussels/nl/news/cansat-belgium-2024-de-winnaars-zijn) y [repositorio](https://github.com/pentakoron1/Astoria-CanSat).
- [ESA: premios 2023](https://www.esa.int/Education/CanSat/CanSat_2023_a_total_success).
- [ITBA: entrevista posterior a la competencia](https://www.iri.edu.ar/index.php/2025/09/15/del-aprendizaje-al-logro-el-triunfo-argentino-en-la-cansat-competition-2025/), [PDR 2025](https://cansatcompetition.com/docs/teams/cansat2025_3165_pdr_v01.pdf).
- [ICARE: informe técnico 2013](https://www.planete-sciences.org/espace/IMG/pdf/Icare_CanSat_T3_Milestone.pdf).
