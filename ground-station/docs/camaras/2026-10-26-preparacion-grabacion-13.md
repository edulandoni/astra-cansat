# 26/10/2026 — ACTUALIZACIÓN 13: preparar la aceptación de grabación y energía

[ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39) · Dependencia de interfaz: [ASTRA-24](https://astrateam2026.atlassian.net/browse/ASTRA-24). Cámaras continúa secundario respecto del Laboratorio.

## Qué nos aporta

Una foto correcta no demuestra una grabación. Para avanzar necesito comprobar varios cuadros consecutivos, sus tiempos, la integridad de cada archivo y el cierre de la secuencia. Preparé un verificador offline y el procedimiento para que, al ensayar, podamos separar una secuencia completa de una incompleta. No cargué firmware ni abrí puertos: el banco instalado sigue con INFO/INIT/PHOTO/SAVE y aún no produce este formato.

El primer ensayo propuesto será una secuencia breve VGA/JPEG en microSD, con cuadro móvil y una referencia de tiempo visible. El objetivo es medir lo que efectivamente se guarda, no prometer resolución o cuadros por segundo antes de ensayar. Eso es preparación para video: todavía faltan captura repetida en el firmware, visualización/exportación temporal y campaña física en ambas unidades.

## Diseño de aceptación preparado

El perfil experimental de archivos `camera-sequence-0.1` usa una carpeta nueva por intento, `sequence.json` y `frame_0001.jpg` consecutivos. No es un protocolo de vuelo ni fija órdenes a Edu. Manifiesto: versión 1, perfil, origen `pc-fixture` o `camera`, arranque de 16 hexadecimales, cantidad esperada 1–120, indicador de cierre y lista de cuadros. Cada cuadro declara índice, archivo, arranque, tiempo de captura desde arranque en microsegundos, longitud y CRC32. Para origen cámara se exige además identidad y comparación con una identidad esperada obtenida del registro privado.

El verificador rechaza rutas fuera de la carpeta, repetición de archivos, índices no consecutivos, cambio de arranque, tiempos no crecientes, archivos ausentes o corruptos y cantidades/cierre incompatibles. Limita el manifiesto a 128 KiB y cada JPEG a 512 KiB; comprueba JPEG VGA RGB mediante decodificación. Calcula huellas de los originales y tiempos entre cuadros. La tasa media usa `(N−1)/(último−primero)`: no cuento N intervalos para N cuadros ni supongo una duración nominal.

Herramienta: `camaras-banco/sequence_verify.py`. Sólo lee archivos y muestra JSON por salida estándar; no escribe en la SD. Códigos de salida: 0 para secuencia consistente, 1 para fallos encontrados y 2 para entrada incompatible/error de lectura. Una secuencia consistente de `pc-fixture` sigue siendo simulación. Las marcas temporales declaradas no prueban por sí solas exposición, reloj UTC ni continuidad de la escena.

## Base técnica

- [Controlador oficial esp32-camera](https://github.com/espressif/esp32-camera): recomienda JPEG y explica el compromiso entre un búfer —más control— y varios —mayor carga y cadencia—. Conservo un búfer como punto de partida del banco; no declaro que alcance la cadencia objetivo.
- [API de cámara de Espressif](https://github.com/espressif/esp32-camera/blob/master/driver/include/esp_camera.h): el cuadro informa longitud, dimensiones y marca temporal del primer búfer DMA desde arranque. Esa marca no es un reloj UTC ni la medida exacta del tiempo de exposición.
- [Modos de suspensión de ESP32](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/sleep_modes.html): quedan partes alimentadas en deep sleep. Dormir el procesador o desinicializar el controlador no demuestra alimentación nula de toda la placa.

Fuentes consultadas el 26/10/2026. No extrapolo prestaciones de ESP32-S3/P4 al ESP32 clásico ni convierto la ausencia de Wi-Fi en una medición de consumo. Audio queda sujeto a identificar micrófono/interfaz real; no lo atribuyo al sensor de imagen.

## Prueba física pendiente, por unidad

1. Conservar inventario y huellas de SD, identificar unidad y firmware; usar carpeta nueva.
2. Con la unidad preparada, pedir una secuencia breve mediante el banco candidato que falta implementar. Mover una escena con referencia temporal. Conservar todos los intentos, incluidos fallos y datos parciales.
3. Confirmar cierre; leer la tarjeta desde lector independiente, comprobar manifiesto/cuadros y comparar huellas con la declaración del emisor. Revisar movimiento, exposición y continuidad visual.
4. Medir latencia de inicio/parada, intervalos y ocupación de SD. Ensayar después una grabación prolongada y corte/reset controlado, preservando lo recuperable. No cortar alimentación durante una escritura como parte de esta preparación.
5. Medir tensión/corriente en espera, chequeo, grabación y cierre. Definir el circuito de alimentación con responsables de vuelo: evitar alimentación por señales cuando se corta la fuente. Ningún estado de software se rotula «0 % consumo» sin medición.

Edu define comandos y evento de misión. Mantengo separados chequeo momentáneo, habilitación de misión y confirmación de grabación. El arranque real, el circuito, el tratamiento de órdenes duplicadas y la conducta al reset siguen TBR con la interfaz compartida.

## Validación de software

Las nuevas pruebas usan imágenes creadas en PC. Verifican secuencia nominal a intervalos ficticios de 0,5 s, CRC, archivo ausente, secuencia abierta, cuadro faltante, arranque distinto, archivo repetido, tiempo invertido, ruta inválida e identidad esperada. La batería completa conserva también las pruebas anteriores del chequeo fotográfico. No acredita una sola secuencia capturada físicamente ni video, sonido o ahorro energético.
