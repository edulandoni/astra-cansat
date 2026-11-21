# 24/10/2026 — ACTUALIZACIÓN: potencia y tiempo de aire antes del enlace RF

Diario: [ASTRA-18](https://astrateam2026.atlassian.net/browse/ASTRA-18) y [ASTRA-25](https://astrateam2026.atlassian.net/browse/ASTRA-25). Amplío la [actualización 02](2026-10-23-modulo-radio-y-comandos-actualizacion-02.md); conservo el análisis anterior.

## Qué pude verificar

Leí la portada y la página 84 de la [hoja Semtech SX1276/77/78/79, revisión 7, mayo de 2020](https://cdn.sparkfun.com/assets/7/7/3/2/2/SX1276_Datasheet.pdf). El documento mantiene para operación a +20 dBm el límite de 1 % de ciclo de transmisión y VSWR máximo 3:1, en el rango de temperatura indicado; especifica alimentación 2,4–3,7 V para ese modo. Por lo tanto, la observación de la revisión 4 no desaparece en esta copia de 2020. Es una condición del componente, distinta de los permisos y límites regulatorios que también debemos verificar.

Es un PDF de Semtech servido por SparkFun. El enlace directo del fabricante no entregó un PDF legible; no afirmo igualdad binaria con ese servidor ni que haya revisado toda la hoja o sus erratas. La variante física del módulo y su circuito siguen TBR; la potencia anunciada en una venta no acredita el uso continuo a ese nivel.

## Efecto sobre mi propuesta

Con el [calculador existente](../../tools/airtime_lora.py), repetí cálculos ilustrativos para 134 bytes de payload, preámbulo de 8 símbolos, CRC activo y CR4/5. No son parámetros seleccionados para el equipo. El tamaño procede del banco ASCII; la trama de vuelo y su sobrecarga siguen pendientes.

| Hipótesis LoRa | Tiempo de aire por paquete | Fracción de aire si envío uno por segundo | Intervalo aritmético para 1 % |
|---|---:|---:|---:|
| SF6, BW500kHz, encabezado implícito | 31,392 ms | 3,1392 % | 3,1392 s |
| SF7, BW125kHz, encabezado explícito | 220,416 ms | 22,0416 % | 22,0416 s |
| SF9, BW125kHz, encabezado explícito | 697,344 ms | 69,7344 % | 69,7344 s |
| SF12, BW125kHz, encabezado explícito y DE activo | 5087,232 ms | 508,7232 % | 508,7232 s |

La última columna es tiempo de aire dividido por 0,01; no define una ventana normativa ni valida un régimen de operación. No incluye órdenes, ACK, guardas o reintentos. El caso SF12 ni siquiera cabe en un segundo. El ejemplo rápido tampoco satisface por sí solo el 1 % a máxima potencia. Estos ejemplos bastan para descartar la suposición «915 MHz, 100 mW y un paquete por segundo funcionan automáticamente juntos»; no prueban que ningún perfil posible sirva.

Voy a revisar con Edu la trama máxima, modulación, tasa, potencia y confirmaciones como un único presupuesto de tiempo de aire. Si evaluamos FSK/GFSK, hay que calcular su encuadre y desempeño propios; no aplico la fórmula LoRa ni reduzco datos requeridos sin acuerdo. No elegí una alternativa, no configuré registros, no transmití RF y no cambié el contrato de vuelo.

## Evidencia y límites

[Entradas, resultados y huella del PDF](../../evidence/2026-10-24-banco02/radio-rev7-08.json). La hoja tiene 132 páginas, 5257370 bytes y SHA256 `330745f933df00015d2de3efd582608339350ba3a21001d11b9d449839ce016b`. Conservo el original privado en la carpeta temática de Descargas y el registro de procedencia, sin movimientos ni republicación del PDF.

Siguen pendientes confirmar ambas placas, pinout, antenas, fuente y desacoplo, restricciones aplicables y acuerdo de Radio Profile/ICD. Esta actualización es preparación verificable para esa discusión; no cierra integración ni presupuesto de enlace medido.
