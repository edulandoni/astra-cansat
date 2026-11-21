# 26/10/2026 — ACTUALIZACIÓN: fotos de ambas cámaras verificadas en microSD

Diario: [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39). Continúo la [lectura independiente de cámara 2](2026-10-26-lectura-independiente-camara-2-06.md) y el [ensayo inicial de cámara 1](2026-10-26-camara-a-prueba-fisica-02.md). Uso cámara 1 para la primera unidad identificada y cámara 2 para la segunda; la correspondencia física queda en el registro privado.

## Qué probé

Usé la misma tarjeta MBR/FAT32, por turnos. Verifiqué la identidad de cámara 1 antes de pedir escritura y conservé su firmware de diagnóstico ya instalado. La primera petición incluyó un reinicio RTS explícito y la segunda no; ambas pertenecen al mismo arranque y a solicitudes diferentes. La cámara creó dos archivos nuevos, informó READBACK_OK y entregó sus JPEG por USB. No recargué firmware ni repetí el respaldo original de flash.

Después de desconectar cámara 1, pasé la tarjeta al lector USB y comparé los cuatro archivos completos de ambas unidades con sus respectivas recepciones. Todos coinciden byte por byte, por longitud, CRC32 y SHA-256; los cuatro abren desde la tarjeta como JPEG 640×480 RGB.

| Unidad | Captura UTC | Tamaño | Resultado desde lector independiente |
| --- | --- | --- | --- |
| Cámara 1 | 04:35:11,770 | 27951 bytes | Coincide y decodifica |
| Cámara 1 | 04:36:02,475 | 21420 bytes | Coincide y decodifica |
| Cámara 2 | 04:27:45,516 | 23862 bytes | Coincide y decodifica |
| Cámara 2 | 04:27:56,994 | 22935 bytes | Coincide y decodifica |

También volví a verificar los 24 archivos anteriores: sus huellas originales se conservan. La lectura desde el lector no escribió ni borró archivos. El [control normalizado](../../evidence/2026-10-26-camera-a/control-sd-y-lector-actualizacion-01.json) conserva tiempos, resultados y huellas. Conservo originales de las fotos y registros en el banco privado. Adjunto en ASTRA-39 las cuatro fotos, con nombres de unidad y número de captura; no publico sus imágenes en el repositorio público.

## Alcance para el PDR

Ambas cámaras identificadas producen fotos nuevas en color 640×480, las escriben y leen en una tarjeta local y permiten recuperar los mismos archivos desde un lector independiente después de desconectarlas. Es un ensayo corto, con una sola tarjeta compartida por turnos y alimentación USB de banco. No demuestra chequeo simultáneo ni que tengamos una tarjeta por unidad.

No retiré alimentación durante escritura. Quedan pendientes video continuo y temporización, recuperación de archivos incompletos, consumo y control de energía, arranque repetible, chequeo dual en la aplicación e interfaz de misión acordada con Edu. El perfil USB local sigue siendo experimental; no configura RF ni redefine los comandos de vuelo. La tarea permanece En curso.
