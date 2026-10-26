# 26/10/2026 — ACTUALIZACIÓN: dos fotos guardadas y leídas por la cámara sin caída

Diario: [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39). Continúo la [preparación MBR/FAT32](2026-10-26-microsd-mbr-restauracion-04.md) y conservo los [fallos con GPT](2026-10-26-camara-sin-caida-sd-03.md).

Con la microSD preparada dentro de la cámara sin caída, comprobé su identidad antes de enviar SAVE. La primera petición incluyó un reinicio RTS explícito; la segunda no reinició la placa. Ambas corresponden al mismo arranque y a identificadores de solicitud distintos. No recargué firmware ni cambié la frecuencia del bus SD entre el fallo con GPT y estos ensayos.

| Inicio UTC | JPEG recibido | CRC32 | Resultado |
| --- | --- | --- | --- |
| 04:27:45,516 | 23862 bytes | c4bc4edf | Guardado y lectura por la cámara: READBACK_OK |
| 04:27:56,994 | 22935 bytes | b70728f3 | Guardado y lectura por la cámara: READBACK_OK |

La cámara creó un nombre nuevo para cada archivo, cerró la escritura y comparó longitud y CRC al leerlo. La PC recibió las fotos, comprobó identidad, arranque y frescura, validó CRC y decodificó ambos JPEG 640×480 RGB. Observé en la segunda foto objetos y colores reconocibles del entorno; no medí nitidez ni exposición cuantitativamente. Las fotos y los registros completos permanecen privados.

El [control nuevo](../../evidence/2026-10-26-camera-b/control-sd-capturas-actualizacion-02.json) conserva tiempos, tamaños, huellas y alcance. El cambio de GPT a MBR/FAT32 permitió superar el montaje y completar escritura/lectura en estos dos intentos con el mismo firmware; no generalizo este resultado a toda tarjeta o a una prueba prolongada.

Este corte acredita dos fotos con lectura desde la propia cámara. La verificación independiente desde el lector USB después de retirar alimentación sigue pendiente. Tampoco acredita grabación continua, apagado, consumo, recuperación de archivos incompletos ni chequeo simultáneo de ambas cámaras. El puerto quedó cerrado después de cada solicitud. Continúo con leer los archivos desde la notebook y después ensayar el guardado en la cámara que se cayó, sin borrar estos resultados.
