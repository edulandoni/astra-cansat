# 26/10/2026 — ACTUALIZACIÓN: primer ensayo físico del panel y explicación del arranque

Diario: [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39). Continúo el [panel de comprobación](2026-10-26-panel-chequeo-dual-08.md), conservando su corte de preparación.

Con cámara 1 conectada, elegí COM7 y pulsé «Foto + comprobar SD» en la ventana. El receptor detectó que la placa estaba esperando programación y terminó sin completar INFO. No llegó a enviar PHOTO ni SAVE; no solicitó escritura en la tarjeta. Conservé el resultado y diagnóstico originales en la carpeta nueva de la petición.

El panel mostró una clave `info` ausente en lugar de la explicación del receptor. Corregí el lector de evidencia: cuando falta identificación o foto, propaga el error registrado, sin intentar acceder a campos inexistentes. Una prueba nueva reproduce exactamente ese resultado incompleto y exige conservar la explicación de modo programación. Pasaron veinte pruebas en total, sin errores ni fallas.

Los registros conservan además una segunda petición desde la ventana, iniciada a las 04:57:35,928 UTC, que agotó su espera de identificación sin respuesta completa. Tampoco envió captura ni escritura SD. Cada petición tiene su propio directorio; no descarto ese segundo intento al resumir el resultado físico.

El [control de esta actualización](../../evidence/2026-10-26-camera-panel/control-error-arranque-actualizacion-01.json) conserva tiempos del intento, huella privada, motivo y regresión. El ensayo no verifica una captura nueva desde el panel; los ensayos físicos correctos de consola siguen documentados por separado.

Cerré la ventana y preparé repetir después de un arranque normal mediante RST, sin BOOT/IO0. No cargué firmware ni apliqué reinicio automático. La repetición física con la corrección sigue pendiente en este corte. No declaro averiado el sensor ni la tarjeta a partir de un arranque que no ejecutaba el programa de cámara.
