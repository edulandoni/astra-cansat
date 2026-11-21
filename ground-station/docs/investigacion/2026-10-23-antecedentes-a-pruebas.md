# 23/10/2026 — De antecedentes a decisiones verificables

Diario: [ASTRA-35](https://astrateam2026.atlassian.net/browse/ASTRA-35). Continúo el catálogo existente, sin presentar sus35 registros como auditorías completas. Priorizo tierra y pruebas sobre agregar funciones sin evidencia. Mi [implementación y resultados](../2026-10-23-banco02-actualizacion-01.md) se registran por separado.

## Daedalus2026 — lectura enfocada

Leí el texto de GCS en páginas PDF121–137 y las páginas de verificación139/140/143/146/147/150/151 del [PDR1043v07](https://www.cansatcompetition.com/assets/docs/2026/cansat2026_1043_pdr_v07.pdf). Inspeccioné visualmente123/129/131/135. Identifiqué módulos separados, ventana acotada, comandos asíncronos y raw/CSV. La prueba de comunicación propone contrastar registros de emisor/receptor y recuperar pérdida temporal. Es un diseño/plan, no datos crudos de vuelo. El texto oscila entre RPi y notebook: conservo esa inconsistencia. Su mención de flush no demuestra resistencia eléctrica. No incorporo acceso remoto de su arquitectura. La clasificación del organizador confirma primer puesto2026; no valida aisladamente su GCS.

## ITBA2025 — lectura enfocada

Leí GCS112–126 y verificación128–132/135 del [PDR3165v01](https://cansatcompetition.com/docs/teams/cansat2025_3165_pdr_v01.pdf). Inspeccioné113/117/118/119. Encontré GUI PyQt, calibraciones diferenciadas y pruebas propuestas de radio con orientación, movimiento y bloqueo. Su simulación sustituye presión de barómetro; no equivale a nuestra reproducción offline. Exportar a USB no prueba copia externa continua. Hay discrepancia de conector de la Yagi respecto del fabricante; la marco TBR en la comparación de antenas. Sus pruebas están planificadas: no encontré allí resultados crudos que las cierren. Primer puesto2025 es clasificación oficial, no certificación de cada función ni requisito CONAE.

## DJS Arya — premio y documentación faltante

Revalidé [ganadores oficiales](https://cansatcompetition.com/winners.html) y la [publicación de AAS](https://astronautical.org/events/cansat/): premio Ground Station2026 a DJS Arya. El [portafolio del autor](https://kshayik.com/projects/djs-arya-cansat-gcs/) describe aproximadamente1Hz y22+variables; no entrega criterios del jurado, código fijado a commit, campaña de fallos o CSV de vuelo. Su galería sigue enlazando Unsplash y no la tomo como captura técnica comprobada. Conservo el [análisis previo del artículo institucional2025](2026-10-20-djs-arya-vuelo-y-recuperacion.md); no confundo edición2025 con premio2026. El faltante técnico queda abierto, sin inventar la causa del premio.

## Antecedente → prueba propia

| Antecedente / evidencia | Riesgo para mi estación | Prueba propia y resultado al corte |
|---|---|---|
| Daedalus147: contrastar TX/RX | Recibir no equivale a guardar | Oráculo USB vs629 filas válidas: coinciden cinco escenarios |
| Daedalus143/147: larga operación y recuperación | Bloqueo o memoria creciente | Colas y ventanas acotadas implementadas; ≥2h físicas pendientes |
| Daedalus135: raw y CSV | Un destino falla y silencia todos | Fallo raw inyectado: CSV y otro destino siguen; reintento recupera |
| ITBA132: orientación/bloqueo | Concluir alcance sólo por enlace quieto | Plan RF de orientaciones; no ejecutado sin radio/antenas |
| ITBA131: conservar tras reset | Mezclar contador de arranques distintos | Contextos y handshake ensayados en software; RST físico pendiente |
| [RSX2025](2026-10-23-rsx-datos-y-calidad.md): GPS sin solución y diagnósticos | Mostrar coordenadas o estados como evidencia física | GPS_LOSS15 muestras sin fix, retención comprobada; diagnóstico separado |
| [PWr/COSMOS](2026-10-20-antecedentes-codigo-y-fotos.md): recepción/buffers/archivo | Confundir llegada, validez y archivo | Escritores independientes y contadores por etapa; tests de fallo/desborde |
| DJS: premio confirmado, criterio técnico no publicado aquí | Copiar una función sólo por prestigio | No selecciono arquitectura por premio; documento faltantes |

El diferencial que evalúo es explicar y reconstruir datos ante fallos con resultados medidos. Su valoración como innovación del concurso sigue pendiente. El rotor continúa en ASTRA-36: estos PDR no demuestran energía eléctrica generada, y no incorporo mecanismos a esta etapa.

## Cobertura, visuales y conservación

Los PDF completos fueron extraídos para búsqueda local; no afirmo haber leído todas sus diapositivas. Daedalus185p, SHA256 `7eb5f9863ceeb4b3ce773ccf526eef1b40235bef1a8606fd285d2635809ef04c`; ITBA176p, SHA256 `e5ebddd650c651dbd64a9cb13ee653bb2a3c7ae1c08556af981`. Las páginas visuales se registran en el [catálogo de esta pasada](2026-10-23-catalogo-visual-gcs.csv). No republico PDF ni imágenes ajenas; licencia/permiso de reutilización no confirmados. Originales y render propio de lectura quedan en Descargas/06 Documentos/CanSat_Universitario/2026-10-23_etapa02_fuentes_01, conservando nombres/versiones; no moví archivos ajenos. Extracción de texto no acredita OCR integral ni video revisado.
