# 24/10/2026 — Órdenes de banco: rechazos físicos y misión completa

Diarios: [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20), [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21) y [ASTRA-24](https://astrateam2026.atlassian.net/browse/ASTRA-24). Amplío la [aceptación USB anterior](2026-10-24-aceptacion-banco-usb-actualizacion-09.md), sin reemplazarla.

## Qué ensayé

Ejecuté 14 comprobaciones entre las 03:28 y 03:31 ART del 24/10, con un único dueño de COM5, perfil bench-usb-0.2 y el ESP32 ya cargado. No solicité reinicio ni programación. El identificador de arranque siguió siendo 95eb1a8feb242968, igual al de las corridas previas; no deduzco estado por la luz. Antes de enviar órdenes de misión comprobé que el extremo se identificaba como sintético.

| Acción | Resultado observado |
|---|---|
| STOP, cero ficticio y hora válida | Ejecutadas |
| RUN con escenario INVALID | Rechazado BAD_ARGUMENT |
| RUN con cero muestras | Rechazado BAD_ARGUMENT |
| Hora 86400 | Rechazada BAD_TIME |
| RUN dirigido al equipo ficticio ajeno 1001 | Sin respuesta hasta timeout; cero muestras nuevas y mismo contexto |
| Consulta de alimentación propia posterior | Ejecutada: la recepción seguía operativa |
| RUN nominal de 131 muestras | Ejecutado |
| Repetir el mismo RUN después del contador 5 | Respuesta conservada; mismo run, contador no reiniciado |
| Cero y hora después del contador 12 | Ambas rechazadas NOT_LAUNCH_PAD |
| Fin y STOP | 131 únicos, sin huecos, rechazos de telemetría o avisos de calidad al final; STOP ejecutado |

No son 14 misiones independientes. Son 14 verificaciones dentro de una campaña, con una misión nominal completa. Diferencio un rechazo de orden de una trama de telemetría corrupta: los rechazos esperados no incrementaron el contador de telemetría inválida.

## Archivo y evidencia

Conservé 639 eventos brutos y 131 filas CSV. Verifiqué por separado la secuencia exacta 1..131, todas las clasificaciones new, CSV idéntico a los paquetes y escritores drenados sin descartes/errores. La herramienta final también exige cierre limpio de escritores para aprobar futuras pasadas; el resultado original de esta pasada queda intacto, con su verificación posterior separada.

[Resultado original](../evidence/2026-10-24-avances/usb-guardas-01/resultado.json) · [Diario original](../evidence/2026-10-24-avances/usb-guardas-01/journal.jsonl) · [CSV original](../evidence/2026-10-24-avances/usb-guardas-01/Flight_1000.csv) · [Verificación independiente](../evidence/2026-10-24-avances/usb-guardas-01/verificacion-captura.json) · [Herramienta reproducible](../tools/ensayar_ordenes_banco.py).

La versión de motor incorpora reloj inyectable para estudios de calidad; en esta campaña usó tiempo real. El firmware no cambió. Es una misión corta de la revisión nueva, no otra demostración de dos horas de la GUI nueva.

## Qué significa y qué falta

La prueba respalda validación de argumentos, guardas de banco, rechazo de equipo ajeno en esta implementación y duplicados sin reiniciar la misión. Un timeout aislado no acredita autenticación ni inexistencia universal de efectos; aquí conservo además ausencia de telemetría y continuidad del contexto y la verificación posterior con una orden válida.

No prueba unicast RF, destinos de vuelo, STM32 ni mecanismos físicos. El JSON, las direcciones de prueba, el estado LAUNCH_PAD y el timeout de banco no aprueban el ICD. ASTRA-24 sigue abierta hasta ejecutar el ensayo real entre ambos extremos.

## Segunda pasada con protección final de la bitácora

Después del [refuerzo de copias](2026-10-24-bitacora-copias-y-verificacion-final.md), repetí las 14 comprobaciones con la revisión final. Otra misión completa conservó 131 filas, todas new, sin huecos, errores o descartes; los escritores cerraron limpios. [Resultado de la segunda pasada](../evidence/2026-10-24-avances/usb-guardas-02/resultado.json) · [Contraste independiente](../evidence/2026-10-24-avances/usb-guardas-02/verificacion-captura.json). Son dos pasadas del mismo conjunto, no 28 clases diferentes de ensayo. Ambas conservan diario y CSV originales.
