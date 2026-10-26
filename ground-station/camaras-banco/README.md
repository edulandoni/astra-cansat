# Banco local de cámaras — experimental

Diario: [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39). Este banco prepara la comprobación de una ESP32-CAM por USB, sin modificar la aplicación de telemetría. [Diseño y alternativas](../docs/camaras/2026-10-25-energia-chequeo-dual.md) · [Preparación y límites del 26/10](../docs/camaras/2026-10-26-banco-local-preparacion-01.md).

## Estado

El [ensayo de cámara A del 26/10](../docs/camaras/2026-10-26-camara-a-prueba-fisica-02.md) conserva respaldo previo, fallos iniciales y cinco fotos USB válidas VGA/RGB. La segunda unidad, microSD, grabación y control de energía siguen pendientes. La preparación anterior conserva su revisión propia. No usar un equipo con integridad o alimentación dudosas; los LED encendidos no prueban seguridad ni captura.

El perfil `camera-usb-0.1` es exclusivo de mantenimiento local. No usa Wi-Fi/Bluetooth, no configura radio y no define los comandos de vuelo que desarrolla Edu. El firmware inicializa el sensor al encender y espera órdenes: todavía no implementa apagado de la placa, grabación continua ni disparo de misión.

## Componentes

- `firmware/AstraCameraBench/`: candidato para pinout AI-Thinker/ESP32 clásico, PSRAM requerida, JPEG 640×480. Hay que confirmar cada placa antes de cargarlo.
- `camera_check.py`: identifica el firmware, solicita una foto nueva, conserva bytes y resultado, valida CRC y decodifica JPEG. Abre únicamente el puerto indicado, sin búsqueda ni carga automática.
- `test_camera_check.py`: fragmentación, corrupción, truncamiento, identidad, frescura, imagen, SD y falta de respuesta sin reenvío.

## Operación futura, después de revisar el hardware

Con Python 3.12 instalo `requirements.txt` en un entorno del banco. Cierro otro receptor que use ese mismo puerto. Identifico la cámara física con una etiqueta; no reutilizo COM5 por suposición ni confundo la placa de telemetría con una cámara.

```powershell
python camera_check.py --port COM_CAMARA --label camara-a --output C:/EnsayosASTRA/camaras
python camera_check.py --port COM_CAMARA --label camara-a --output C:/EnsayosASTRA/camaras --save-sd --show
python -m unittest -v test_camera_check
```

`COM_CAMARA` es un marcador que reemplazo por el puerto comprobado. La primera orden pide una foto sin montar ni escribir la SD. Sólo uso `--save-sd` después de identificar la tarjeta y conservar su contenido. Nunca formateo ni borro archivos; cada captura usa otro directorio de PC y otro nombre en la tarjeta. La lectura después de escritura se compara por longitud y CRC; no acredita supervivencia a corte eléctrico. Un archivo parcial se conserva y se informa, no se reemplaza para aparentar éxito.

`--show` abre una ventana nativa con la foto de ese chequeo y su fecha. No es video en vivo. Las fotos y el registro recibido son privados por defecto: pueden mostrar el entorno de trabajo, así que no los publico automáticamente en GitHub.

## Contrato de banco

Solicitudes ASCII terminadas en LF: `INFO <id>`, `PHOTO <id>` y `SAVE <id>`. El ID tiene 16 dígitos hexadecimales. El receptor no reenvía automáticamente. Es una herramienta de una petición por vez; no implementa todavía deduplicación persistente de órdenes ni grabación de misión.

Respuestas: línea `@CAM ` seguida de JSON de versión 1. INFO incluye unidad, arranque, sensor y PSRAM. Una captura usa cabecera `frame` con ID, arranque, unidad, longitud y CRC32, seguida de exactamente esos bytes JPEG, salto de línea y control `end` con el mismo ID/arranque. El cuerpo binario no se interpreta como líneas. Rechazo más de 512 KiB por imagen, controles de más de 1024 bytes y registro de recepción de más de 2 MiB. Espero hasta 30 segundos por operación.

El firmware descarta cuadros pendientes y exige que la marca de captura sea posterior a la solicitud, en el mismo reloj desde arranque. La PC comprueba unidad/arranque, dimensiones y decodificación; no equipara frescura con exposición o enfoque correctos. Esos dos aspectos necesitan inspección de una escena real y ensayos de estabilización.

SAVE agrega montaje SD_MMC en un bit sin formateo, escritura y lectura. `saved=true` junto con `READBACK_OK` es el resultado reportado por el extremo que escribe; no es lectura independiente de la tarjeta desde la notebook. Si la SD falla pero la transferencia funciona, conservo la foto y el resultado de falla. La GUI de telemetría no muestra todavía este chequeo dual.
