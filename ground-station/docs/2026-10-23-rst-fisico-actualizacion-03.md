# 23/10/2026 — ACTUALIZACIÓN03: RST físico y arranque sin identidad

Diarios: [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20), [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21), [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22), [ASTRA-34](https://astrateam2026.atlassian.net/browse/ASTRA-34). Amplío la [actualización01](2026-10-23-banco02-actualizacion-01.md), conservando sus pendientes tal como estaban al corte.

## Ensayo y resultado físico

Conservé abierta la GUIUSB y pulsé EN/RST. La primera pulsación reportada quedó registrada a23/10/2026 23:39:19ART como DOWNLOAD_BOOT y `waiting for download`. No arrancó el simulador ni recibí hello nuevo. No demostré por qué GPIO0 fue muestreado en ese estado; no atribuyo la causa a BOOT, cable o controlador sin prueba.

Dejé BOOT suelto y volví a pulsar EN/RST. A23:40:16ART apareció un hello con boot `db40b035fbb715d0`, diferente del anterior `cdd083adc284734f`. La GUI creó segmento nuevo, dejó campos/gráficos vacíos y mantuvo el CSV anterior con131muestras. No recargué firmware entre pulsaciones.

Inicié explícitamente otroRUN. Recibí contadores1..131 y LANDED en otro segmento, sin huecos, duplicados ni rechazos. Al cerrar, el escritor confirmó262filas de ambos segmentos; conservo los dosCSV. El reset devolvió el offset ficticio a12m y hora inicial13:00:00: no recalibré antes de eseRUN, por eso su altitud final es12m. No confundo esa señal sintética con altura medida ni con persistencia de configuraciónF1/F2.

## Incidencia detectada y corrección

El proceso que estaba abierto sabía limpiar valores al recibir un hello de arranque diferente, pero no invalidaba inmediatamente el contexto sólo por el mensajeROM. En el primer intento sin hello permanecían valores antiguos identificados como viejos. Era una limitación del receptor, que debía explicar el arranque pendiente sin esperar al firmware.

Agregué reconocimiento acotado del diagnósticoROM del ESP32 sólo en el perfil de banco. Al detectarlo invalido identidad/medición actuales, GPS y alimentación; las órdenes pendientes quedan con resultado desconocido. No invento un boot nuevo a partir del texto. Conservo el histórico y espero anuncio o respuesta a un sondeo nuevo.

Después de0,5s preparo un únicoPOWER_STATUS para recuperar identidad si se perdió hello. No repito comandos anteriores ni hago reintentos indefinidos. Si quedó en bootloader, ese sondeo puede vencer sin respuesta y la identidad sigue desconocida. EnREPLAY no envío nada.

También distingo en pantalla edad del último mensaje válido y edad de medición, y marco como histórica una respuesta de orden perteneciente a otro contexto. El número de guardados por escritor acumula la sesiónPC, mientras únicos/huecos corresponden al segmento actual.

## Verificación de la corrección

Pasaron12pruebas de software, incluidas dos nuevas: arranqueROM sin hello que invalida valores/pendientes y recuperación del anuncio perdido mediante un sondeo único. Reproduje los bytes reales de la captura con el receptor corregido: después de `waiting for download`, identidad y medición quedan vacías y el contexto ambiguo. La reproducción completa conserva262paquetes únicos.

La corrección se cargó en un proceso nuevo dePC; no requiere cambiar el firmwareESP32. La captura física anterior corresponde al proceso anterior a esta corrección. No afirmo que ese proceso ya tuviera el arreglo ni cuento la reproducción como otra pulsación física.

- [Resultado del ensayo, contextos y límites](../evidence/2026-10-23-banco02/rst-fisico-05/resultado-rst-05.json).
- [Diario normalizado conservando bytes y fechas](../evidence/2026-10-23-banco02/rst-fisico-05/journal-sin-rutas-locales.jsonl): sólo retiro clavesroot de metadatos de almacenamiento; el original local conserva su huella publicada.
- [CSV separados](../evidence/2026-10-23-banco02/rst-fisico-05/segments/).
- [Resultado de12tests y huellas de fuentes](../evidence/2026-10-23-banco02/software-tests-rom-06.json).

RST físico y recepción posterior quedan demostrados en este banco, con la incidencia y límites anteriores. La desconexión/reconexiónUSB se ensaya en la siguiente captura con el proceso corregido. Siguen pendientesC:+microSD, dos horas continuasUSB conGUI/memoria medida y cualquier pruebaRF/autonomía/corte eléctrico. Una GUI abierta durante25minutos con gran parte del tiempo sin flujo no acredita continuidad de recepción.
