# 26/10/2026 — ACTUALIZACIÓN 02: recuperación demostrable y gráfico sin continuidad inventada

[ASTRA-41](https://astrateam2026.atlassian.net/browse/ASTRA-41) · Continúo la [primera entrega](2026-10-26-laboratorio-entrega-01.md), que permanece conservada.

Agregué Recuperación como octava sección del Laboratorio. Puedo explicar y demostrar qué pasa cuando dos archivos se complementan, cuando falta una medición en ambas fuentes o cuando discrepan. Reutilizo el recuperador del banco; cada clic crea fuentes sintéticas y una carpeta nueva. No abro datos reales ni altero originales.

## Resultados

- Copias complementarias: diez candidatos, CSV nuevo con diez filas de datos y procedencia por cada registro.
- Ausente en ambas: nueve candidatos, CSV parcial con nueve filas. La aplicación informa que falta una; no fabrica el décimo dato.
- Conflicto: diez candidatos pero una discrepancia; reconstrucción bloqueada, sin CSV. Conservo fuentes y diagnóstico.
- Las huellas de los originales permanecen iguales en los tres casos. Son dos archivos en el mismo disco: no demuestra respaldo en soportes independientes.

Cuatro pruebas de integración pasan: reconstrucción/procedencia/conflicto, separación de huecos e identidades en gráfico, paquete/tiempo de aire y las cinco misiones completas. Dos pruebas nativas adicionales verifican cierre durante misión y durante recuperación: esperan terminar los escritores y el trabajo iniciado. No se abren puertos físicos.

## Gráfico

La primera integración tomaba sólo el último valor de cada actualización de pantalla y podía dibujar una línea atravesando contadores faltantes. Ahora consumo todas las muestras disponibles de la cola acotada del motor, conservo contador y segmento y corto las líneas ante huecos o cambio de identidad. El eje horizontal representa contador; el gráfico mantiene como máximo 180 muestras. Los archivos siguen conservando todas las muestras aceptadas según su estado de escritura.

Esta corrección mejora la demostración visual; no constituye una campaña USB o RF. La recuperación sintética acredita el algoritmo sobre esos casos, no recuperación de información ausente ni resistencia física de un soporte. El objetivo de cámaras continúa secundario y sin nuevos ensayos físicos en esta actualización.
