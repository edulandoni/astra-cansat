# 26/10/2026 — Tamaño de paquete, perfil LoRa y confiabilidad para el PDR

Diario específico: [ASTRA-40](https://astrateam2026.atlassian.net/browse/ASTRA-40). Relaciono esta evaluación con ASTRA-18, ASTRA-25 y la interfaz de ASTRA-24. Continúo el [análisis de potencia y tiempo de aire](2026-10-24-radio-potencia-y-airtime-actualizacion-03.md); no lo sustituyo ni apruebo un Radio Profile.

## Motivo y alcance

En la conversación con Edu surgió una trama binaria estimada de unos 55 bytes frente al límite de 255 bytes de payload LoRa. Edu define el empaquetado y los comandos de vuelo; adapto tierra. Todavía necesito el desglose para saber si esos 55 incluyen todos los bytes de aplicación: versión, equipo/destino, sesión/contador, validez y controles acordados. No relleno el paquete hasta el máximo sólo porque exista espacio.

El costo demostrable aquí es el tiempo de transmisión. No medí costo de CPU ni energía de batería. El tiempo de propagación de la onda no aumenta por agregar bytes; aumenta el tiempo necesario para completar la transmisión. La latencia extremo a extremo agrega adquisición, espera, procesamiento y recepción. SF7/SF9/SF10 son factores de expansión, no bandas. Distingo portadora, ancho de banda y cadencia: 915 MHz no equivale a bitrate ni a una muestra por segundo. La hoja SX1276 especifica BW LoRa hasta 500 kHz; no supongo un perfil LoRa de 1 MHz.

## Matriz calculada, sin RF

Generé [108 hipótesis](../../evidence/2026-10-26-comparacion-lora/matriz-01.json) con [comparar_perfiles_lora.py](../../tools/comparar_perfiles_lora.py), reutilizando el calculador existente. Barro 50/55/60/100/124/255 bytes, SF7/9/10, BW125/250/500 kHz y CR4/5 o 4/8. Los 124 bytes son una muestra ASCII del banco, no el tamaño máximo de todos sus mensajes. Uso preámbulo 8, encabezado explícito y CRC físico activo; el CRC físico y encabezado LoRa ya están contemplados en la fórmula. El encabezado propio de aplicación sí integra el payload. No copio límites de LoRaWAN a este enlace propio.

Este recorte mantiene BW125 kHz, CR4/5, preámbulo 8, encabezado explícito y CRC activo:

| Payload completo | SF7 | SF9 | SF10 |
| --- | ---: | ---: | ---: |
| 55 bytes | 107,776 ms | 349,184 ms | 657,408 ms |
| 100 bytes | 174,336 ms | 553,984 ms | 1026,048 ms |
| 255 bytes | 399,616 ms | 1250,304 ms | 2295,808 ms |

Reducir de 100 a 55 bytes ahorra 38,18 % del tiempo de aire en SF7, 36,97 % en SF9 y 35,93 % en SF10, con esas hipótesis. El porcentaje usa como denominador el tiempo de 100 bytes. No es igual ahorro porcentual de batería completa. SF10/100 bytes supera el segundo de telemetría antes de comandos o guardas. SF10/55 bytes consume 65,74 % de ese segundo, sin acreditar que el resto alcance para operar. La duración aumenta por saltos de símbolos, no necesariamente por cada byte individual.

Mantener 55 bytes y cambiar CR4/5 a 4/8 lleva los tiempos a 160,000 / 508,928 / 952,320 ms para SF7/9/10. La redundancia tiene costo; no es aire gratis. Verifiqué tres resultados por aritmética independiente y pasaron las dos pruebas existentes del calculador. Son verificaciones de fórmula, no recepción real ni mediciones de desempeño.

## Qué significa más robusto

Semtech explica que aumentar SF mejora sensibilidad a costa de duración del símbolo; FEC agrega redundancia para tolerar pérdida parcial de información. Una transmisión más larga también ocupa más tiempo y puede quedar más expuesta a interferencia o desvanecimiento. No concluyo «SF más alto siempre gana». Comparo desempeño real en las condiciones del enlace y el presupuesto temporal completo.

Elijo candidatos que preserven toda la información y precisión requeridas, con margen para recibir órdenes. No reduzco campos necesarios para llegar a 55. Puedo justificar bytes adicionales de versión, identificación, sesión, contador o validez; falta acordarlos. CRC detecta errores, no los corrige. Repetir la misma información dentro de un paquete no protege contra perder el paquete entero. Repeticiones separadas también cuestan tiempo y pueden sufrir la misma perturbación; no las habilito por defecto.

## Campaña propuesta y decisión pendiente

1. Obtener de Edu el layout completo con longitudes, escala/unidades, signo, rango y orden de bytes; preparar vectores compartidos para extremos, inválidos y reinicios. La estimación de 55 bytes sigue TBR.
2. Presupuestar un segundo con la trama máxima, cambio TX/RX, órdenes/confirmaciones acordadas, guardas y recuperación. Definir umbrales de antigüedad, pérdidas y latencia con Edu; permanecen TBD.
3. Ensayar candidatos variando una condición a la vez y conservando alimentación, antenas, ubicación y configuración: PRR/PER, ráfagas, RSSI/SNR, latencia y antigüedad, órdenes y energía. Incorporar distancia/atenuación, orientación, movimiento y perturbaciones controlables; una prueba quieta no certifica vuelo. Registrar cantidad de muestras y suficiencia estadística, sin prometer porcentajes de recepción a partir del airtime.
4. Elegir conjuntamente la combinación que cumpla los requisitos con margen, documentando qué alternativas no cumplieron y por qué. La tabla de tiempos por sí sola no selecciona SF, BW, CR ni potencia.

Agrego potencia y régimen como una condición separada: revalidé en la hoja Semtech revisión 7, p.84, la restricción de ciclo TX de 1 % para operación a +20 dBm en las condiciones indicadas. No tomo el anuncio «100 mW» como permiso de uso continuo. La variante y circuitos del módulo, condiciones del fabricante y restricciones aplicables requieren revisión conjunta; no traslado el límite a toda potencia ni lo presento como una norma argentina.

## Fuentes y límites

- [Hoja Semtech SX1276 revisión 7, mayo de 2020](https://cdn.sparkfun.com/assets/7/7/3/2/2/SX1276_Datasheet.pdf): sección 4.1.1.7, p.31, fórmula y payload 1–255; p.10 BW; p.84 potencia/régimen. Es documento del fabricante servido por SparkFun. El enlace Salesforce desde la página oficial no entregó contenido legible; no afirmo igualdad binaria con ese servidor.
- [FAQ oficial: compromiso SF/FEC](https://www.semtech.com/design-support/faq/faq-lora).
- [FAQ oficial: payload largo, fading e interferencia](https://www.semtech.com/design-support/faq/P100).
- [Ficha oficial SX1276](https://www.semtech.com/products/wireless-rf/lora-connect/sx1276), usada para localizar la documentación.

No configuré ni transmití RF, no medí PER/CPU/batería y no fijé campos ni comandos de vuelo. Esta entrada aporta cálculos y una campaña verificable para decidir, no una afirmación de confiabilidad medida.
