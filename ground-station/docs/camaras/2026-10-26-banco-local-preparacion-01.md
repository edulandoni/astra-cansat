# 26/10/2026 — ACTUALIZACIÓN: preparación del banco local de cámaras

Diario: [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39). Continúo el [diseño del 25/10](2026-10-25-energia-chequeo-dual.md) y conservo sus pendientes. El objetivo completo sigue abierto: dos cámaras verificadas, fotos nuevas y guardado comprobado, control de energía y grabación, adaptación a la definición de Edu y evidencias de pruebas físicas.

## Qué preparé

Agregué un [banco separado](../../camaras-banco/README.md) con firmware para el pinout candidato AI-Thinker y receptor Python. No alteré el firmware ni la GUI de telemetría, no abrí COM5 y no cargué software en cámaras. La maniobra física quedó pendiente de revisar integridad y seguridad de placa/base/alimentación; no continúo ensayos sólo porque enciendan los LED.

El firmware informa identidad estable de unidad, identidad nueva por arranque, sensor detectado, PSRAM y flash. Solicita JPEG VGA y rechaza un cuadro cuya marca temporal sea anterior al pedido. PHOTO transfiere sin tocar la SD; SAVE escribe un archivo de nombre nuevo y comprueba longitud y CRC al leerlo desde la propia cámara. No formatea, no borra ni sobrescribe una ruta existente. Un fallo de SD no se disfraza de chequeo exitoso.

El receptor conserva bytes y resultado en una carpeta nueva por intento, valida encuadre, ID, arranque, unidad y CRC, y además abre/decodifica el JPEG con Pillow. Comparo dimensiones declaradas con las reales y exijo el perfil VGA en color. Un CRC correcto no basta para afirmar que existe una imagen legible. Separo foto comprobada con SD sin probar de foto con lectura SD reportada por el firmware. No atribuyo a esa lectura resistencia eléctrica ni video continuo.

Implementé límites de memoria/transferencia y espera, y no reenvío automáticamente al vencer el tiempo. Las respuestas viejas no satisfacen una solicitud nueva. El visor opcional es una ventana nativa independiente; no se integró aún a la app principal ni se comprobó visualmente con fotos de cámaras reales. Los archivos de captura quedan privados por defecto.

## Comprobaciones realizadas

Las pruebas automáticas usan un JPEG creado en PC, no la cámara: envío fragmentado en varios tamaños y en ráfaga, CRC alterado, truncamiento, cierre de otra orden/arranque, tamaños fuera de límite, diagnóstico excesivo, contenido inválido con CRC coincidente, dimensiones falsas, imagen monocroma, identidad o instante incorrectos, errores de SD, diagnóstico y respuesta antigua intercalados, y espera sin reintento.

El firmware candidato compila con Arduino CLI 1.5.1 y Arduino-ESP32 3.3.12. La primera compilación falló por las rutas largas del compilador en Windows al buscar cabeceras C++; conservé los intentos privados. Preparé un acceso corto al mismo directorio de herramientas y usé rutas de compilador/SDK y salida cortas, sin reemplazar el paquete ni cambiar el proyecto de telemetría. La compilación no implica carga, pinout confirmado ni funcionamiento físico. La evidencia de la revisión exacta está en el [control de preparación](../../evidence/2026-10-26-camera-preparacion/control.json).

## Qué sigue y qué no afirmo

1. Revisar integridad de ambas placas, base y fuente antes de conectarlas para ensayo; identificar cuál recibió un golpe. No hacer pruebas de contacto corporal.
2. Confirmar una unidad y su puerto, identificar chip y flash sin confundir la placa de telemetría, y conservar el firmware original antes de la primera escritura.
3. Probar PHOTO sin SD y revisar la imagen real; después identificar/preservar la tarjeta y probar SAVE. Repetir con la segunda unidad.
4. Medir latencia, exposición, consumo y picos; desarrollar doble chequeo, grabación continua recuperable y circuito de apagado/retención acordado.
5. Adaptar a comandos de Edu y ensayar la integración real. Los nombres de este banco no son protocolo de vuelo.

No acredité cámara sana, fotografía real recibida, SD física, consumo, apagado, autonomía, video o continuidad frente a reset. El sensor queda activo en este primer firmware de diagnóstico: no es la solución final de espera sin alimentación. Esta preparación permite avanzar sin manipular el equipo mientras se resuelve la condición previa del ensayo.
