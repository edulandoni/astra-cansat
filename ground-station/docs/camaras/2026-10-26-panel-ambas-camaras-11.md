# 26/10/2026 — ACTUALIZACIÓN: ambas cámaras comprobadas desde el panel

Diario: [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39). Continúo el [ensayo de cámara 1 desde el panel](2026-10-26-panel-camara1-capturas-y-limites-10.md), conservando sus fallos de arranque y límites.

Pasé la misma tarjeta a cámara 2, con las placas desconectadas durante la maniobra. Seleccioné su ficha y COM7 en el panel que ya conservaba el resultado correcto de cámara 1. El primer intento de cámara 2 detectó espera de programación: no hubo identificación completa, foto ni escritura. La interfaz explicó el estado, mantuvo la foto anterior como histórica y el resumen permaneció en una de dos.

Fuera del panel apliqué una petición de consola con reinicio RTS explícito y la identidad esperada de cámara 2. Produjo un JPEG de 17481 bytes con guardado y lectura correctos. No cargué firmware ni agregué reinicio automático a la ventana.

Repetí explícitamente la solicitud desde «Foto + comprobar SD» de cámara 2: llegó un JPEG nuevo de 22497 bytes, CRC correcto, decodificación 640×480 RGB y READBACK_OK. Observé el resultado individual, la foto nueva, fecha y antigüedad actualizadas y el resumen de dos de dos comprobadas en esa misma ronda por turnos. Cámara 1 conserva su resultado anterior de la ronda; no afirmo que ambas estén conectadas simultáneamente.

El conjunto de registros del panel ahora contiene ocho peticiones: cinco incompletas y tres capturas correctas, dos de cámara 1 y una de cámara 2. Conservo también las peticiones de recuperación de consola por separado. El [control de esta actualización](../../evidence/2026-10-26-camera-panel/control-ambas-fisicas-actualizacion-03.json) conserva resultados, huellas y límites. Guardé una captura privada de la pantalla de dos de dos; no publico imágenes del entorno o personas automáticamente.

## Qué puedo afirmar y qué falta

El panel comprobó por turnos las dos unidades, recibió una foto nueva de cada una y obtuvo confirmación de escritura/lectura SD. La condición de una unidad no aprobó a la otra mientras su intento estaba fallido. Las explicaciones, resultados independientes, historial y antigüedad fueron observados durante la operación física. Las veintiuna pruebas de software del corte anterior corresponden al mismo código; esta pasada no cambió fuentes.

Los archivos nuevos del panel todavía necesitan lectura externa después de retirar alimentación; la verificación anterior de cuatro fotos conserva su alcance propio. Sigo sin acreditar arranque repetible: ambas unidades necesitaron el procedimiento de recuperación en esta campaña. No probé físicamente la selección de identidad equivocada, operación simultánea, video, recuperación de archivos incompletos, energía ni comandos de misión. El acceso desde la aplicación de telemetría permanece pendiente. ASTRA-39 sigue En curso.
