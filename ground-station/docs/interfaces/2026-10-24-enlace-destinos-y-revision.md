# 24/10/2026 — Enlace preliminar, destinos y paquete de revisión con vuelo

Diarios: [ASTRA-18](https://astrateam2026.atlassian.net/browse/ASTRA-18), [ASTRA-24](https://astrateam2026.atlassian.net/browse/ASTRA-24) y [ASTRA-25](https://astrateam2026.atlassian.net/browse/ASTRA-25). Preparación física pendiente en [ASTRA-23](https://astrateam2026.atlassian.net/browse/ASTRA-23). Amplío la [comparación anterior de antenas y fórmula](2026-10-23-antenas-y-link-budget-preliminar.md) y la [revisión de potencia/airtime](2026-10-24-radio-potencia-y-airtime-actualizacion-03.md), sin reemplazarlas.

## Cálculo que ya puedo reproducir

Implementé un calculador offline que exige procedencia para cada número conocido. Una entrada desconocida queda null y se informa como pendiente; no la sustituyo por cero. Sólo calculo potencia recibida si están frecuencia, distancia, potencia, ganancias y todas las pérdidas. El margen requiere además sensibilidad; la reserva sobre el objetivo necesita el objetivo explícito.

Revalidé la fórmula de espacio libre en [ITU-R P.525-5, sección 2.3, ecuación 5](https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.525-5-202411-I!!PDF-E.pdf). Uso distancia en metros, frecuencia en Hz y c=299792458 m/s; no mezclo la constante redondeada de la fórmula MHz/km con estas unidades. Esa referencia no modela por sí sola suelo, obstáculos, desalineación o interferencia.

| Ejecución | Resultado |
|---|---|
| ASTRA: once entradas todavía TBD | No invento potencia recibida ni margen; enumero las once faltantes |
| Ejemplo aritmético, NO ASTRA | A 915 MHz y 1000 m, FSPL=91,676205 dB |
| Mismo ejemplo: 10 dBm, ganancias 0/5 dBi, pérdidas 1+1+3+2 dB, sensibilidad hipotética −110 dBm | Prx=−83,676205 dBm; margen=26,323795 dB |
| Agrego 3/6/10 dB de pérdidas al ejemplo | El margen baja exactamente 3/6/10 dB; no es un margen garantizado de nuestro equipo |

Todas las cifras de la segunda ejecución son hipótesis declaradas, incluso sensibilidad, potencia y pérdidas. No combiné la mejor sensibilidad del SX1276 con una tasa incompatible ni elegí una antena definitiva. Pasaron tres pruebas nuevas de presupuesto y las dos existentes de tiempo de aire. Detecté y corregí una transcripción de la cifra esperada en el test antes de publicar; no ajusté la fórmula para aparentar una medición.

[Herramienta](../../tools/link_budget.py) · [Entrada ASTRA y resultado pendiente](../../evidence/2026-10-24-avances/enlace-01/astra-tbd-resultado.json) · [Hipótesis de ejemplo](../../evidence/2026-10-24-avances/enlace-01/ejemplo-input.json) · [Resultado ilustrativo y sensibilidad a pérdidas](../../evidence/2026-10-24-avances/enlace-01/ejemplo-resultado.json).

## Pruebas lógicas de destino que no eligen bytes de vuelo

Preparé once vectores sobre metadatos ficticios. Acepto sólo equipo, origen, destino y versión esperados, con política explícita sin broadcast e integridad ya comprobada por un futuro decodificador. Rechazo equipo/destino/origen/versiones ajenos, broadcast, política ausente o de tipo incorrecto, falta de destino e integridad no verificada. Los once resultados coinciden con lo esperado.

Esto es una prueba de política, no un protocolo codificado. TEAM_BENCH, ground y flight son etiquetas de fixture; no seleccionan tamaño, direcciones reales, Sync Word o Network ID. integrity_checked representa un resultado interno de validación; no es un bit recibido que debamos creer. Aquí no calculé CRC, no elegí algoritmo ni autentiqué emisores. Un remitente que copia etiquetas no queda autenticado. El filtro no impide recibir energía ajena ni evita una colisión física.

[Vectores completos](../../evidence/2026-10-24-avances/destinos-01/resultado.json) · [Política reproducible](../../experiments/2026-10-24-destinos/politica.py). La [campaña USB de órdenes](../2026-10-24-ordenes-negativas-usb.md) aporta por separado un caso físico de equipo ajeno en el banco; no lo convierto en prueba RF.

## Lo que dejo preparado para revisar con Edu

La [lista de campos pendientes](2026-10-24-perfil-radio-para-revisar.json) es DRAFT_NOT_APPROVED y no la consume un driver. Dejo sin rellenar frecuencia, modo, tasa/BW, potencia, sensibilidad del mismo modo, sincronización, CRC, identificadores/destinos, campos/unidades, reinicios/contadores, órdenes/confirmaciones y reintentos. No completé firmas de revisión ni envié el paquete a otra persona.

Primero necesitamos identificar las placas reales y cotejar su pinout: conservo la diferencia de 16 contactos en la foto frente a 14 en el manual localizado. Después debemos comprobar alimentación, desacoplo y antenas. El diagnóstico SPI sin transmisión sigue como paso futuro: no conecté un módulo ni escribí registros. ASTRA-23 continúa Por hacer para integración física.

Puedo mantener el catálogo de órdenes, las reglas de confirmación y estos vectores desde tierra. Para adoptar un contrato ambos extremos deben revisar el mismo documento y probar los mismos ejemplos, sin parches divergentes. La futura prueba debe rechazar destinatario incorrecto antes de ejecutar, separar aceptación/ejecución y conservar resultado desconocido tras un corte. No envío automáticamente una orden de nuevo por recibir timeout.

## Escalera de ensayo RF pendiente

| Etapa | Qué debo registrar | Condición para continuar |
|---|---|---|
| Mesa y comprobaciones sin TX | Unidad/revisión, pinout, alimentación medida, software y perfil | Hardware identificado y revisión compartida registrada |
| Primer enlace controlado | Bytes TX/RX, versiones, contador, destino, integridad, comandos y alimentación | Perfil autorizado para la prueba y ambas unidades disponibles |
| LOS corto e intermedio | Puntos crecientes de separación, alturas, entorno y orientación; ejemplo de planificación 25/50/100/250 m | Sitio, distancias finales y condiciones coordinados; no son puntos ya ejecutados |
| LOS largo y seguimiento | Ejemplos de planificación 500/1000 m, giro, polarización, paso alto y shadowing | Alcance del ensayo y perfil compatibles; no usar altura como distancia oblicua |
| Fallos y prolongado | Reset de cada extremo, interrupción, pérdida de ACK, órdenes repetidas y flujo continuo | Primero superar mesa; no heredar aprobación de dos horas USB como RF |

En cada punto necesito log del emisor para saber qué se intentó enviar y log del receptor para distinguir recibidos, válidos, únicos y guardados. Registraré RSSI/SNR sólo cuando el modo realmente entregue esas métricas; no relleno una inexistente con cero. Sin relojes sincronizados no llamaré latencia unidireccional a una resta de horas: puedo medir RTT desde un reloj y declarar qué incluye. Los criterios finales de tasa de pérdida, margen, duración y trayectoria siguen pendientes; no los invento para cerrar la tarea.

ASTRA-18/24/25 continúan abiertas: hay nuevos cálculos y casos reproducibles, pero no un modo aprobado, un margen real con entradas conocidas o interoperabilidad STM32/SX1276 demostrada.
