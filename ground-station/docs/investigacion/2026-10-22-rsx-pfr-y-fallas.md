# 22/10/2026 — RSX 2025: PFR, fallas y contradicciones

Diario: [ASTRA-35](https://astrateam2026.atlassian.net/browse/ASTRA-35). Profundicé una ficha a partir del [repositorio de RSX](https://github.com/adam-kabbara/RSX-CANSAT-2025/tree/da327893982c1afd6e480e9cf3d89b43ebca273e) y su [PFR de 31 páginas](https://github.com/adam-kabbara/RSX-CANSAT-2025/blob/da327893982c1afd6e480e9cf3d89b43ebca273e/competition_documentation/deliverables/Cansat2025_3114_PFR.pdf), fijados en `da327893982c1afd6e480e9cf3d89b43ebca273e`. Leí todo el texto extraído; observé la imagen de conjunto de p.5 y el gráfico de p.13. No revisé todos los elementos visuales, videos enlazados, datos crudos ni planilla de misión. No certifico sus resultados ni el puesto que declara el README.

## Qué relatan los autores después del vuelo

Las pp.16,23,27 atribuyen el mal despliegue del autogiro a una secuencia de pérdida del paracaídas y vuelco; reportan descenso medio de 19,5 m/s. La posible temporización de expulsión se presenta como hipótesis, no como causa probada. P.13 atribuye el corte de telemetría al desprendimiento del XBee en el impacto. P.22 relata un GPS sustituido a último momento que no obtuvo fix durante lanzamiento. Pp.24–28 proponen sobrecalentamiento para las cámaras y reconocen que omitieron su ensayo térmico. P.28 propone reforzar retención y ensayar más allá de condiciones nominales. Son relatos/análisis del equipo; no los repetí experimentalmente.

## Discrepancias que conservo

P.14 marca liberación a 441 m, aproximadamente 70% del máximo 622,8 m. P.30 describe éxito al 75% y elevación de las palas, mientras p.16 describe despliegue incorrecto y p.23 trabado del rotor. No convierto el texto de lecciones en aprobación del descenso completo. El objetivo, el estado del software, la liberación mecánica y el régimen estable son eventos diferentes.

P.13 muestra tanto máximo 622,8 m como altitud calibrada 826,3 m, sin que esta pasada reconstruya las bases. Conservo ambas referencias sin elegir una como altura real. Tampoco adopto la afirmación de recepción de todos los paquetes como tasa independiente medida. La crítica general a ESP32 en p.30 es experiencia declarada de ese equipo, no evidencia para descartar nuestra placa.

## Qué sí pude observar visualmente

P.5 contiene una vista de conjunto con palas desplegadas y electrónica; su aspecto es de render/modelo digital. La imagen sola no certifica hardware construido ni materiales. P.13 contiene gráfico de altitud barométrica frente a hora UTC, puntos y bandas de estado. La transición de estado mostrada no certifica por sí sola un evento físico. Las referencias F11/F12 se registran en el [suplemento visual](2026-10-22-catalogo-visual-rsx.csv), sin republicar binarios. Autor individual/licencia de imagen pendientes.

## Para qué me sirve y qué falta

Para groundstation propongo separar transmisión recibida, sensor válido y evidencia de evento; una radio puede seguir recibiendo aunque GPS o cámara fallen. La recuperación debe conservar último dato válido y antigüedad. Para nuestra idea del rotor, el [análisis específico](2026-10-22-rotor-estabilidad-y-evidencia.md) incorpora estabilidad previa y evidencia de despliegue, sin aprobar mecanismos ajenos a mi área.

En nuestro PDR conviene mostrar qué se esperaba, qué pasó, datos y límites, y mantener contradicciones pendientes. No copio alturas, porcentajes, transmisores ni reglas de AAS a CONAE. No hay datos de energía eléctrica generada en lo revisado; el Hall mide paso/giro y no demuestra generación neta. Queda contrastar la planilla cruda y las secuencias de video en otra pasada delimitada, si aporta evidencia útil.

## Control de fuente

PDF: 31 páginas, 1.726.125 bytes, SHA-256 `07fbced5a643a71f9707966f6983476e4e09cde232d33d0c87b4ca03ff0524c9`. Original guardado directamente en Descargas, en la carpeta temática de esta ejecución, con registro origen/destino. La lectura textual no equivale a auditoría de todos sus gráficos ni escucha de grabaciones. No ejecuté software ajeno, no modifiqué ASTRA ni ensayé RF, descenso o generación.
