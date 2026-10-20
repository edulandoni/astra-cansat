# Ensayos y evidencia que puedo mostrar
20/10/2026 — [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21), [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20), [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22) y [ASTRA-34](https://astrateam2026.atlassian.net/browse/ASTRA-34).

Esta incorporación organiza pruebas anteriores; no ejecuté otra campaña ni repetí los resultados como si fueran nuevos. El paquete Evidencias_y_experimentos_PC_2026-10-19 conserva la estructura evidence/ y experiments/ y un manifiesto SHA-256. Sus datos son sintéticos. El código del banco necesario para repetir los ensayos está fijado en el [repositorio revisado](https://github.com/edulandoni/astra-cansat/tree/51c475eb2df8cf2ab5317c5e03455f8ad7c4b729/ground-station/banco-usb-v0.1).

| Conjunto | Resultado registrado | Cómo lo reproduzco y dónde miro |
| --- | --- | --- |
| Banco USB | 9 pruebas aprobadas | [Instrucciones](https://github.com/edulandoni/astra-cansat/blob/51c475eb2df8cf2ab5317c5e03455f8ad7c4b729/ground-station/banco-usb-v0.1/README.md), evidence/2026-10-19/pruebas-banco-python.txt |
| Estación histórica v04 | 13 pruebas de lógica aprobadas | [Archivo completo](https://github.com/edulandoni/astra-cansat/tree/51c475eb2df8cf2ab5317c5e03455f8ad7c4b729/ground-station/archive/DEPRECATED/estacion-v04), evidence/2026-10-19/pruebas-estacion-v04.txt |
| Escenarios del 17/10 | NOMINAL 131 válidos; pérdida 118 y 13 huecos; corrupción 121 y 10 rechazos | evidence/2026-10-17/VERIFICACION.txt y sus cinco sesiones originales |
| Prevención | Sondeos de extremos, datos congelados, equipo ajeno y falla raw | [Experimento](https://github.com/edulandoni/astra-cansat/tree/51c475eb2df8cf2ab5317c5e03455f8ad7c4b729/ground-station/experiments/2026-10-19-prevencion), evidence/2026-10-19-investigacion-prevencion/ |
| Resiliencia | 7200 paquetes registrados sin consumidor de pantalla; fallo CSV y reconexión virtual | [Instrucciones](https://github.com/edulandoni/astra-cansat/blob/51c475eb2df8cf2ab5317c5e03455f8ad7c4b729/ground-station/experiments/2026-10-19-resiliencia/README.md), evidence/2026-10-19-resiliencia/ |
| Reconciliación | 31 filas reconstruidas con procedencia; control negativo bloquea contradicción | Misma carpeta de experimento y evidence/2026-10-19-resiliencia-reconciliacion/ |

7200 mensajes procesados en segundos prueban volumen de software, no dos horas reales de autonomía. Un puerto sustituido no prueba USB físico. Dos carpetas en el mismo disco no acreditan dos soportes independientes. No ensayé radio, alcance, alimentación ni cortes eléctricos en estas pruebas.

Las verificaciones del exportador Jira se conservan en el paquete como evidencia documental, relacionadas con ASTRA-33; no las cuento como pruebas de vuelo. Para preparar una demostración leo también los límites de cada informe y uso el commit fijado, sin sustituirlo por una versión futura sin registrar el cambio.
