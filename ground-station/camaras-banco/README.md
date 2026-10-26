# Banco local de cámaras — experimental

Diario: [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39). Este banco prepara la comprobación de una ESP32-CAM por USB, sin modificar la aplicación de telemetría. [Diseño y alternativas](../docs/camaras/2026-10-25-energia-chequeo-dual.md) · [Preparación y límites del 26/10](../docs/camaras/2026-10-26-banco-local-preparacion-01.md).

## Estado

[Candidato de secuencia compilado](../docs/camaras/2026-10-26-candidato-secuencia-14.md): sketch experimental separado `AstraCameraSequenceBench`, solicitud explícita `sequence_request.py` y 31 pruebas del banco. El candidato agrega CLIP para doce cuadros con tiempos, archivos nuevos y cierre completo/parcial. No se cargó ni probó físicamente. El firmware instalado y el sketch probado de fotos se conservan; no atribuyo a esta compilación video, consumo o estabilidad.

[Preparación de grabación y energía](../docs/camaras/2026-10-26-preparacion-grabacion-13.md): incorporé `sequence_verify.py` para comprobar una secuencia JPEG desde archivos, con tiempos, integridad e identidad. El firmware instalado todavía no genera el perfil experimental `camera-sequence-0.1`; esta herramienta y sus pruebas preparan la aceptación, sin acreditar video físico. Uso: `python sequence_verify.py carpeta --expect-device IDENTIDAD_DEL_REGISTRO_PRIVADO` para origen cámara; las muestras de PC se identifican como `pc-fixture`. No escribe en la tarjeta.

La [lectura externa de toda la campaña](../docs/camaras/2026-10-26-lector-campana-panel-12.md) verifica nueve fotos, tres de ellas solicitadas desde el panel, y los 24 archivos originales intactos. Las nueve coinciden y abren desde la tarjeta después de desconectar las cámaras. No es video ni prueba de corte durante escritura.

El [ensayo físico del panel con ambas unidades](../docs/camaras/2026-10-26-panel-ambas-camaras-11.md) comprobó captura y guardado/lectura SD por turnos, con resultados y antigüedad separados. La campaña conserva cinco intentos incompletos y tres capturas correctas. El arranque requirió recuperación; no está acreditada su estabilidad. La lectura externa de estas fotos nuevas, video y energía siguen pendientes.

El [ensayo de ambas cámaras](../docs/camaras/2026-10-26-ambas-camaras-sd-y-lector-07.md) verifica dos fotos nuevas por unidad, guardado/lectura por cada cámara y comparación desde el lector después de desconectarlas. Los cuatro archivos coinciden y los 24 originales siguen intactos. Usé una tarjeta por turnos; no es una prueba simultánea ni de video. Las entradas siguientes conservan los cortes previos.

La [lectura independiente posterior](../docs/camaras/2026-10-26-lectura-independiente-camara-2-06.md) verifica desde el lector USB las dos fotos de la cámara 2 después de desconectarla: bytes, huellas y decodificación coincidentes, con los 24 archivos anteriores intactos. El ensayo SD de la otra cámara sigue pendiente. Los párrafos siguientes conservan el alcance de cortes anteriores.

La [actualización de guardado](../docs/camaras/2026-10-26-dos-fotos-sd-camara-2-05.md) acredita dos fotos nuevas escritas y leídas desde la cámara 2 con la tarjeta MBR/FAT32. La comparación independiente desde el lector USB y el ensayo SD de la otra cámara siguen pendientes. El párrafo siguiente describe el corte de diagnóstico previo.

El [ensayo de la cámara 1](../docs/camaras/2026-10-26-camara-a-prueba-fisica-02.md) conserva respaldo previo, fallos iniciales y cinco fotos USB válidas VGA/RGB. La [cámara 2](../docs/camaras/2026-10-26-camara-2-sd-03.md) entregó seis fotos válidas; dos intentos de guardado fallaron al montar una tarjeta GPT. La [preparación posterior](../docs/camaras/2026-10-26-microsd-mbr-restauracion-04.md) acredita MBR/FAT32 y 24 archivos repuestos/verificados, todavía sin nuevo ensayo de guardado. Grabación y control de energía siguen pendientes. Los LED encendidos no prueban captura.

El perfil `camera-usb-0.1` es exclusivo de mantenimiento local. No usa Wi-Fi/Bluetooth, no configura radio y no define los comandos de vuelo que desarrolla Edu. El firmware inicializa el sensor al encender y espera órdenes: todavía no implementa apagado de la placa, grabación continua ni disparo de misión.

## Componentes

- `camera_panel.py`: pantalla nativa para dos unidades registradas, con puerto explícito, fotos y estado por ronda. [Resultados y límites de la revisión](../docs/camaras/2026-10-26-panel-chequeo-dual-08.md).
- `camera_session.py`: conservación de cada petición, comprobación de evidencias y resultados independientes. `test_camera_session.py` verifica fallos y separación de rondas.

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

## Pantalla de comprobación

```powershell
python camera_panel.py --registry C:/BancoASTRA/registro-camaras.json --output C:/BancoASTRA/chequeos
```

Las rutas de ese ejemplo son configurables. El registro privado tiene `version: 1` y un objeto `cameras` con claves `camera1` y `camera2`: cada valor es la identidad de 16 dígitos hexadecimales ya comprobada para esa unidad. No invento identidades ni las deduzco del puerto. No publico el registro privado.

Elijo el puerto de la cámara conectada y pulso «Sólo foto» o «Foto + comprobar SD». No retiro la tarjeta ni desconecto durante una petición. «Ver un chequeo guardado» abre un `resultado.json` previo y vuelve a comprobar su foto; muestra evidencia histórica sin aprobar la ronda actual. «Nueva ronda» limpia confirmaciones, conservando fotos e historial. Una falla no aprueba la otra unidad. La fecha y antigüedad explican a qué momento pertenece la imagen.

La pantalla no reinicia, carga firmware, graba video ni controla alimentación. Una foto con lectura SD correcta acredita esa petición. La lectura independiente con lector externo sigue siendo un ensayo adicional, como el ya documentado para las cuatro fotos originales.

## Contrato de banco

Solicitudes ASCII terminadas en LF: `INFO <id>`, `INIT <id>`, `PHOTO <id>` y `SAVE <id>`. El ID tiene 16 dígitos hexadecimales. INIT reinicializa el sensor una vez y sólo se utiliza si INFO anuncia esa capacidad. El receptor no reenvía automáticamente. Es una herramienta de una petición por vez; no implementa todavía deduplicación persistente de órdenes ni grabación de misión.

`--expect-device` comprueba una identidad física previamente registrada antes de pedir foto o escritura. `--reset-once` solicita un reinicio RTS explícito y conserva los bytes previos en otro archivo; no corta alimentación ni carga firmware. `--init-once` solicita INIT una vez. Estas opciones son maniobras de diagnóstico, no recuperación automática ni comandos de vuelo. Un arranque en modo programación se informa con una explicación específica.

Respuestas: línea `@CAM ` seguida de JSON de versión 1. INFO incluye unidad, arranque, sensor y PSRAM. Una captura usa cabecera `frame` con ID, arranque, unidad, longitud y CRC32, seguida de exactamente esos bytes JPEG, salto de línea y control `end` con el mismo ID/arranque. El cuerpo binario no se interpreta como líneas. Rechazo más de 512 KiB por imagen, controles de más de 1024 bytes y registro de recepción de más de 2 MiB. Espero hasta 30 segundos por operación.

El firmware descarta cuadros pendientes y exige que la marca de captura sea posterior a la solicitud, en el mismo reloj desde arranque. La PC comprueba unidad/arranque, dimensiones y decodificación; no equipara frescura con exposición o enfoque correctos. Esos dos aspectos necesitan inspección de una escena real y ensayos de estabilización.

SAVE agrega montaje SD_MMC en un bit sin formateo, escritura y lectura. `saved=true` junto con `READBACK_OK` es el resultado reportado por el extremo que escribe; no es lectura independiente de la tarjeta desde la notebook. Si la SD falla pero la transferencia funciona, conservo la foto y el resultado de falla. La GUI de telemetría no muestra todavía este chequeo dual.
