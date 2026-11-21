# 26/10/2026 — ACTUALIZACIÓN: cámara 1 captura y guarda desde el panel

Diario: [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39). Continúo el [primer ensayo del panel](2026-10-26-panel-error-arranque-09.md), conservando sus intentos incompletos.

## Ensayo y resultados

El conjunto de registros del panel contiene seis peticiones: una detectó modo programación, otra agotó la espera de identificación, dos identificaron la cámara y sensor pero fallaron al adquirir el primer cuadro de preparación, y las dos últimas capturaron, guardaron y leyeron fotos nuevas correctamente. No oculto los cuatro intentos incompletos bajo un resultado nominal.

Después del arranque normal con RST, las dos fallas de adquisición fueron WARMUP_1_FAILED. La identidad y el sensor respondían, pero no llegó una imagen y no se alcanzó la escritura SD. La interfaz mantuvo las fotos previas como históricas y no contó la operación como aprobada. Mejoré sus explicaciones para distinguir fallo de imagen, tarjeta que no monta, espera de programación y falta de respuesta, conservando el error original en los registros.

Para comparar con el procedimiento anterior, cerré el panel y ejecuté una petición de consola con el reinicio RTS explícito ya utilizado en banco. Esa petición produjo un JPEG de 12066 bytes con guardado y lectura correctos. No cargué firmware. El resultado demuestra recuperación en ese intento; no identifica por sí solo la causa del arranque fallido ni acredita arranque repetible.

Volví a abrir el panel y pedí captura desde «Foto + comprobar SD», sin reinicio automático. Los registros conservaron dos fotos nuevas, de 9599 y 14379 bytes, con CRC, decodificación JPEG 640×480 RGB y READBACK_OK. Observé en pantalla una foto actualizada, fecha y antigüedad propias, resultado individual correcto y resumen de una de dos cámaras comprobadas. La foto conservada de cámara 2 no pasó a contar como prueba nueva. No ejecuté la prueba física de selección de identidad equivocada; esa condición tiene cobertura de software, sin atribuirle una prueba física.

El [control del corte](../../evidence/2026-10-26-camera-panel/control-camara1-fisica-actualizacion-02.json) conserva las seis peticiones y sus huellas. Pasaron veintiuna pruebas de software, incluida la regresión del error de identificación y las explicaciones entendibles. Las fotos nuevas permanecen privadas; no las agrego automáticamente a GitHub ni a los adjuntos anteriores de Jira.

## Límites y continuidad

La captura desde el panel quedó comprobada para cámara 1 en el arranque recuperado. Falta cámara 2 en esa interfaz, lectura externa de estas fotos nuevas, prueba física de selección equivocada e integración del acceso desde la estación de telemetría. No doy por solucionada la estabilidad del arranque. Los ensayos de consola y lectura externa anteriores conservan su alcance propio.

Video continuo, recuperación de archivos incompletos, consumo, apagado y la interfaz de misión que define Edu siguen pendientes. La app permanece como banco USB y no altera fuentes de telemetría, radio ni código de vuelo. ASTRA-39 sigue En curso.
