# 26/10/2026 — ACTUALIZACIÓN 14: candidato de secuencia compilado, sin carga

[ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39) · Continúo la [preparación de aceptación](2026-10-26-preparacion-grabacion-13.md). Laboratorio sigue como objetivo primario en [ASTRA-41](https://astrateam2026.atlassian.net/browse/ASTRA-41).

## Qué preparé y para qué

Ya tengo un candidato para pedir una secuencia breve a una cámara y conservar cada imagen con su tiempo. Es un paso hacia grabación comprobable: puedo ensayar cuadros consecutivos sin hacer depender toda la evidencia de un archivo de video que sólo se complete al final. Todavía no es una cámara grabando demostrada ni un reproductor de video continuo.

Conservo intacto el sketch probado de fotos. Agregué `firmware/AstraCameraSequenceBench/` como copia experimental identificada, con `sequence_capture.h`. No cargué firmware ni abrí puertos. Las dos unidades conservan su estado físico anterior.

## Comportamiento del candidato

Anuncia la capacidad local `CLIP` junto con INFO/INIT/PHOTO/SAVE. `CLIP <id de 16 hexadecimales>` solicita hasta doce JPEG VGA en una carpeta nueva, con separación objetivo de 500 ms después de terminar cada escritura/lectura. La cadencia efectiva será menor y debe medirse; no prometo 2 fps ni seis segundos exactos. El tiempo del controlador y la SD se suma a esa espera.

Antes de grabar verifica cámara preparada, montaje SD de un bit sin formateo, espacio conservador para doce cuadros de hasta 512 KiB y ausencia de la carpeta. El flash LED queda bajo. Cada cuadro se cierra y se lee para comparar longitud/CRC; después conserva un archivo lateral con su tiempo. El manifiesto final incluye cuadros confirmados y cierre completo o parcial. Un fallo detiene la secuencia y conserva los archivos existentes. No borra ni sobrescribe nombres anteriores.

Un reset puede dejar cuadros o el marcador de inicio sin manifiesto final: eso es información parcial para diagnóstico, no cierre exitoso. Los archivos laterales preparan la reconstrucción posterior; todavía no implementé su reconstrucción automática. No atribuyo tolerancia física a reset o a corte eléctrico por este diseño.

## Solicitud y verificación desde PC

`sequence_request.py` requiere puerto e identidad esperada explícitos. Consulta INFO y sólo envía CLIP si la unidad coincide y anuncia la capacidad. No reinicia, no reintenta y conserva recepción/resultado en una carpeta nueva. Separa cierre reportado, secuencia parcial, error reportado y falta de confirmación. El cierre comunicado por la cámara no es verificación independiente.

La operación es breve y bloquea el procesamiento de otras órdenes del candidato hasta terminar o fallar. No hay STOP durante CLIP. No es la interfaz final de grabación de misión. Ante espera vencida, el resultado es desconocido: no repetir automáticamente ni retirar la SD hasta verificar el fin del trabajo. INFO puede servir después para comprobar que vuelve a responder, sin acreditar por sí solo archivos.

Después del ensayo, con unidad sin alimentación y tarjeta en lector, `sequence_verify.py` comprueba la secuencia con la identidad del registro privado. Los archivos que no pudo leer dejan `originals_unchanged` en desconocido, en vez de dar un sí general. Informa cuántos archivos tienen huella y cuántos fueron declarados. Un CRC incorrecto no impide conservar la huella del archivo que efectivamente leí.

Ejemplo de comandos de banco (sustituir puerto, identidad y carpetas con los datos privados verificados):

```text
python sequence_request.py --port COMx --expect-device IDENTIDAD --output CARPETA_NUEVA
python sequence_verify.py CARPETA_DE_LA_TARJETA --expect-device IDENTIDAD
```

No ejecutar sobre el firmware instalado sin comprobar capacidad; actualmente sólo el candidato experimental nuevo anuncia CLIP. Para volver a probar fotos puedo conservar el sketch original. La primera carga del candidato requiere procedimiento físico guiado y verificación de unidad, manteniendo los respaldos originales ya conservados.

## Validación y límites

Compiló con Arduino CLI 1.5.1, Arduino-ESP32 3.3.12, perfil ESP32-CAM con FlashMode dio y diagnóstico warn: 476739 bytes de programa y 35144 bytes estáticos de RAM. Es evidencia de compilación, no pinout, captura, cadencia o SD física. El [control de preparación](../../evidence/2026-10-26-secuencia-preparacion/control-01.json) conserva huellas y alcance.

Pasaron 31 pruebas Python del banco: incluyen las fotos/panel previos, verificación de secuencias y solicitud con respuestas fragmentadas, rechazo antes de CLIP por otra identidad o firmware sin capacidad, límites de controles, espera sin reintento, respuesta parcial, cambio de arranque y cierre/carpeta/unidad contradictorios. Los mensajes de cámara de esas pruebas son simulados; no prueban ejecución del C++ ni periféricos.

Pendiente físico: cargar el candidato con la unidad preparada, comprobar doce cuadros reales por unidad, revisar escena y tiempos, lectura independiente, ensayos de duración y recuperación. Falta reproducción/exportación temporal de la secuencia para evaluar video, además de audio sujeto a hardware, circuito/medición de energía y comandos de misión de Edu. No controlo alimentación ni habilitación de vuelo desde este banco.
