# 27/10/2026 — Foto física desde Qt y preparación de grabación

[ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39) · [ASTRA-41](https://astrateam2026.atlassian.net/browse/ASTRA-41). Continúo la [integración del Laboratorio](../historial/2026-10-26-laboratorio-completo-04.md) y el [candidato de secuencia](2026-10-26-candidato-secuencia-14.md), conservando originales.

## Resultado físico

Solicité una foto de cámara 1 desde el mismo botón Qt del Laboratorio, con hardware real y SD conectados. Ejecuté la comprobación con widgets fuera de pantalla: la orden pasó por la app, el capturador existente y USB. Llegó un JPEG 640 × 480 RGB decodificable, con longitud, CRC y huella coherentes. La cámara reportó escritura y lectura correctas en SD; la imagen Qt quedó no vacía y el estado indicó foto capturada en esta sesión. Abrí también la imagen conservada y comprobé que se ve. La fotografía permanece privada.

Medí **3,172 s** desde activar el botón hasta completar el trabajo y actualizar la app. Incluye recepción, comprobación y guardado/lectura solicitados: no es garantía de latencia máxima ni transmisión de video. La imagen aparece al recibirla completa; no describo ese tiempo como transmisión instantánea.

La unidad arrancó en modo programación. El primer INFO lo detectó; apliqué una vez el reinicio RTS explícito existente y la siguiente identificación confirmó cámara preparada. No cargué firmware para conseguir esta foto. Conservo bytes/resultados privados y no presento ese reinicio como solución demostrada de estabilidad.

Después abrí el Laboratorio solicitado en Cámaras, con puerto privado recordado y la última imagen marcada como conservada. La repetición desde la ventana visible quedó solicitada, sin darla por confirmada por falta de respuesta. No controlé el escritorio ni pulsé botones mediante automatización de pantalla. El [control público](../../evidence/2026-10-27-camara-qt/control-01.json) separa evidencia física de software.

## Aplicación

Sacar foto solicita una captura nueva sin exigir tarjeta; Foto + microSD agrega el chequeo de escritura/lectura. Muestro captura en curso y tiempo de espera, bloqueo operaciones concurrentes y sustituyo la imagen al recibir el resultado. Un fallo mantiene la anterior identificada como tal; no la cuento como comprobación nueva. Agregué ampliación nativa y enumeración de puertos sin abrirlos, conservando la selección mientras exista. Abrir la app no inicia captura, reset ni grabación.

Incorporé Grabar prueba · 12 cuadros en SD, conectado al adaptador `sequence_session.py` y al solicitador CLIP existente. Comprueba identidad y capacidad antes de enviar; conserva el resultado y distingue cierre reportado, parcial y desconocido. No reinicia, reintenta, formatea ni borra. El cierre de app espera que termine el trabajo. La foto anterior no se presenta como video en vivo.

## Grabación: preparación y pendientes

Comprobé que los dos fuentes de firmware coinciden con el candidato compilado y que su binario conserva la huella. Los respaldos originales de ambas unidades siguen presentes. Este corte no acredita carga ni secuencia física: quedó solicitada la maniobra BOOT/RST necesaria antes de cargar. Conservo el programa de fotos probado.

La primera campaña prevista solicita doce imágenes con sus tiempos y una carpeta única. El candidato espera 500 ms después de escritura/lectura por cuadro; la cadencia efectiva debe medirse. No prometo 2 fps ni duración nominal exacta. Después necesito leer la tarjeta desde el lector, verificar manifiesto y cuadros, y reproducir con sus tiempos. Una secuencia JPEG breve no acredita grabación continua de misión, exportación de un archivo de video o audio.

## Verificación

Pasaron **38 pruebas del banco de cámaras y 15 del Laboratorio**. Las cuatro nuevas del adaptador comprueban cierre reportado sin atribuir lectura independiente, errores/timeout/parcial sin reintento, cierre contradictorio y selección explícita. La nueva prueba Qt verifica bloqueo de fotos durante la secuencia, unidad/puerto, mensaje de alcance y cierre sin terminar el trabajo. Las anteriores mantienen escenarios, recuperación, identidad e integridad.

Las imágenes de reproducción usadas en los tests son sintéticas. No convierto esos tests en video físico ni extiendo el resultado de cámara 1 a cámara 2. La foto actual sólo tiene lectura reportada por la cámara, no lectura independiente nueva desde el lector. Siguen pendientes estabilidad de arranque, secuencia real, duración, video/exportación, audio, consumo y apagado. Edu mantiene la definición del contrato de misión.
