# 26/10/2026 — ACTUALIZACIÓN: primeras fotos físicas de cámara A

Diario: [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39). Continúo la [preparación de software](2026-10-26-banco-local-preparacion-01.md). El objetivo completo permanece abierto; esta entrada acredita una unidad y capturas USB, sin sustituir pruebas de SD, grabación o alimentación.

## Identificación, respaldo y carga

Identifiqué COM7 como CH340 de la base USB, diferente del CP210x/COM5 usado antes para telemetría. El ESP32 respondió como ESP32-D0WD-V3, revisión 3.1, cristal 40 MHz y flash de 4 MB. El pinout candidato permitió detectar OV2640, PID decimal 38/hexadecimal 0x26, y 4 MB de PSRAM. Conservo la identidad física en el registro privado para diferenciar unidades.

Antes de escribir leí los 4194304 bytes de flash, conservé el original privado y calculé su huella. La lectura informó 103,4 s a 460800 baud. No probé restauración. Cargué bootloader, particiones, boot_app0 y aplicación en los offsets previstos; esptool verificó la huella escrita. No volví a leer toda la flash al cambiar después el diagnóstico.

Trabajé con la notebook informada en batería y sin tarjeta microSD en esta cámara. Esto describe las condiciones del ensayo, no una medición de seguridad eléctrica o autonomía.

## Resultados completos, sin ocultar los intentos fallidos

| Intento | Resultado | Qué permite afirmar |
|---|---|---|
| 1 y 2, firmware inicial | Sensor y memoria identificados; CAPTURE_FAILED al pedir foto, mismo arranque | El sensor responde a configuración, pero no produjo una imagen recibida en esos intentos |
| 3, después de desconectar/reconectar | Timeout de INFO; bytes conservados con DOWNLOAD_BOOT y waiting for download | Quedó en modo de programación, no ejecutando el diagnóstico; no fue una falla de transferencia JPEG |
| 4, firmware con diagnóstico por fase y nuevo arranque | JPEG de 9713 bytes, 640×480 RGB, CRC y decodificación correctos | Primera foto USB válida, escena gris sin detalle suficiente para evaluar enfoque |
| 5, apuntando a una escena reconocible | JPEG de 23164 bytes, 640×480 RGB, CRC y decodificación correctos | Observé monitor, objetos y colores reconocibles; no apliqué un criterio cuantitativo de nitidez o lectura de texto fino |
| 6, 7 y 8 | Tres fotos nuevas correctas, de 16379, 21076 y 20416 bytes | Repetición corta en el mismo arranque; no ensayo prolongado ni de video |

El [control normalizado](../../evidence/2026-10-26-camera-a/control.json) conserva tiempos, tamaños, CRC, validación y huellas por intento. No publico fotos del entorno ni la flash original; sus huellas permiten vincular el resultado con los originales privados. Las cinco fotos correctas pertenecen a solicitudes distintas y tienen marca de captura posterior al pedido. No presento una foto retenida como respuesta nueva.

Agregué mensajes de fase para distinguir primer cuadro de calentamiento, segundo y cuadro solicitado. Habilité avisos del controlador únicamente durante adquisición y los deshabilité antes de transmitir el JPEG binario. La nueva compilación ocupa 453895 bytes de programa y 35016 bytes estáticos. Después de esa carga y nuevo arranque obtuve cinco capturas válidas, pero no aislé la causa de los dos fallos iniciales: no atribuyo la mejora sólo a los mensajes o a un conector. Sigue TBR.

El modo de programación tras reconexión coincide con el [comportamiento de arranque documentado por Espressif](https://docs.espressif.com/projects/esptool/en/latest/esp32/advanced-topics/boot-mode-selection.html). Falta verificar arranque repetible después de desconexión real; una carga seguida de reinicio correcto no satisface ese caso.

## Estado y siguiente paso

La cámara A captura y transfiere fotos VGA en color por USB en las condiciones observadas. No hay microSD y no ejecuté SAVE, por lo que no afirmo almacenamiento local. No medí consumo, exposición/enfoque de forma cuantitativa, temperatura, video, apagado ni continuidad ante reset. No habilité Wi-Fi, RF ni un protocolo de vuelo. El puerto quedó liberado al terminar cada captura.

Sigo con identificar y respaldar la segunda cámara, obtener sus fotos y comparar unidades. Después necesitaremos tarjetas para probar escritura/lectura y grabación, y el circuito e interfaz acordados para control de energía. ASTRA-39 continúa en curso. Conservo todos los intentos previos y no cierro el objetivo por este resultado parcial.
