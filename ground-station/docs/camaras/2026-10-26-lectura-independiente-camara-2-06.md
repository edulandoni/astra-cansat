# 26/10/2026 — ACTUALIZACIÓN: fotos de la cámara 2 verificadas desde el lector

Diario: [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39). Completo la lectura independiente que quedó pendiente en [dos fotos guardadas desde la cámara](2026-10-26-dos-fotos-sd-camara-2-05.md), sin modificar aquel corte.

Después de desconectar la cámara, pasé la microSD al lector USB. Comprobé la misma tarjeta por identidad, capacidad, tabla MBR y volumen FAT32 `ASTRA_CAM`. La lectura desde la notebook encontró los dos archivos escritos por la cámara: 23862 y 22935 bytes.

Comparé cada archivo completo de la tarjeta con su foto recibida por USB: los bytes coinciden exactamente. Verifiqué además longitud, CRC32 y SHA-256 contra los registros de las solicitudes. Ambos archivos abren como JPEG 640×480 RGB desde el propio lector. Esto aporta comprobación independiente del reporte READBACK_OK del firmware.

Revisé también los 24 archivos repuestos después de preparar la tarjeta: todos conservan sus SHA-256 originales. No borré ni reescribí archivos durante esta lectura. Las fotos y los nombres/contenidos ajenos al ensayo permanecen privados. El [control de esta actualización](../../evidence/2026-10-26-camera-b/control-lector-actualizacion-03.json) conserva tiempos, huellas y resultados sin publicar esos originales.

Puedo afirmar que estas dos fotos completas quedaron guardadas y legibles después de desconectar la cámara. No corté alimentación mientras escribía: no es una prueba de recuperación de archivo incompleto ni de tolerancia a un corte arbitrario. Tampoco demuestra video continuo, autonomía, consumo, apagado electrónico ni funcionamiento dual simultáneo.

Sigo con la cámara 1 usando la misma tarjeta, conservando los dos archivos de esta prueba. Cada unidad mantiene identidad y resultados separados; una foto válida de una no verifica la otra. El objetivo completo y ASTRA-39 siguen abiertos.
