# 26/10/2026 — ACTUALIZACIÓN: nueve fotos verificadas desde el lector

Diario: [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39). Completo la lectura externa que quedó pendiente en el [chequeo de ambas cámaras desde el panel](2026-10-26-panel-ambas-camaras-11.md).

Después de desconectar cámara 2, pasé la microSD al lector USB y comprobé la tarjeta por capacidad, bus USB, tabla MBR y volumen FAT32 `ASTRA_CAM`. Comparé todas las fotos guardadas que tienen un resultado correcto conservado en el banco: nueve archivos en total, seis solicitados desde consola y tres desde el panel. Los nueve coinciden byte por byte con sus recepciones, además de longitud, CRC32 y SHA-256, y abren desde la tarjeta como JPEG 640×480 RGB.

No encontré archivos `ASTRA_CHECK_*.jpg` ajenos a esos nueve registros. Revisé también los 24 archivos originales repuestos tras la preparación de la tarjeta: todos mantienen sus huellas. Esta pasada sólo leyó la tarjeta; no borró ni reescribió fotos o archivos anteriores.

El [control de lectura de campaña](../../evidence/2026-10-26-camera-panel/control-lector-campana-actualizacion-04.json) conserva las nueve fotos por unidad y origen, tamaños, huellas y comprobaciones. Las imágenes nuevas y la captura del panel permanecen privadas; esta actualización no agrega adjuntos a Jira automáticamente.

## Resultado de esta etapa y límites

Quedan comprobadas identificación, fotos nuevas, color y dimensiones, escritura/lectura local y recuperación de archivos completos desde el lector en ambas unidades. El panel permitió comprobarlas por turnos en la misma ronda con resultados y antigüedad propios. Los fallos se conservan y no se convierten en confirmaciones. Los registros de consola y panel siguen separados.

No es grabación de video ni un ensayo de corte durante escritura. No acredita arranque repetible, consumo, apagado, funcionamiento simultáneo o continuidad ante reset del controlador de vuelo. Usé una sola tarjeta compartida por turnos; falta una tarjeta por cámara para una campaña simultánea. La prueba física de selección equivocada y la integración del acceso desde la aplicación de telemetría siguen pendientes, al igual que el contrato de misión definido por Edu. El objetivo completo y ASTRA-39 permanecen abiertos.
