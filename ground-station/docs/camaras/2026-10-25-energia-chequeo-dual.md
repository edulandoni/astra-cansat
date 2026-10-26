# 25/10/2026 — Cámaras: energía, grabación y comprobación dual

Diario: [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39). Comencé el estudio y desarrollo de mi extremo de cámaras y su integración en tierra. El [reparto de comandos](../interfaces/2026-10-25-comandos-definidos-desde-vuelo.md) queda en ASTRA-24: Edu define vuelo y yo adapto groundstation.

## Qué tenemos y qué cambió

En las tres fotos recibidas veo dos placas rotuladas ESP32-CAM, lectores microSD y una base ESP32-CAM-MB con micro-USB. En un flexible se lee OV2640. Esto coincide con los dos kits que registra [ASTRA-16](https://astrateam2026.atlassian.net/browse/ASTRA-16), pero no acredita fabricante, revisión, PSRAM, sensor de ambas unidades ni su funcionamiento. La base USB es herramienta de banco; la arquitectura previa no la incluye en vuelo.

ASTRA-16 conserva una propuesta de dos cámaras autónomas, cenit/nadir, cada una con microSD, alimentación de 5 V y señal START del OBC, sin Wi-Fi/Bluetooth en misión. Allí se había preferido mantenerlas encendidas sin grabar durante espera y no conmutar potencia por complejidad. Ahora evalúo apagarlas completamente en espera y encenderlas para comprobar o grabar. Es una revisión propuesta que necesita mediciones y acuerdo; no reescribo esa tarea ajena ni doy por probado su margen energético anterior.

La copia archivada del anexo v2 exige video del descenso hacia cenit y nadir (C6/C7), evidencia del despliegue (SN6) y video en color de al menos 640×480 (SN7). E4/E7 y la aclaración del 19/10 vinculan standby con CanSat activado y espera de bajo consumo. Cámaras apagadas no significa OBC/radio de mando apagados: alguna electrónica debe permanecer capaz de recibir y actuar.

Fuentes CONAE: [anexo v2](https://www.argentina.gob.ar/sites/default/files/2026/08/anexo_requerimientos_tecnicos_-_cansat_universitario_2026-2027_v2.pdf), [aclaración oficial archivada](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2960#p50090) y [análisis previo de fuentes](../aula/2026-10-19/revision-aula.md). Leí las copias locales existentes; el PDF público no respondió en esta consulta y no revalidé hoy el aula. No incorporo una exigencia nueva de transmitir imágenes ni una tasa mínima de cuadros que no haya identificado en esas fuentes.

## Mi recomendación inicial

Empezaría con las dos ESP32-CAM que ya tenemos, cada una grabando en su tarjeta. Primero verificaría una y después las dos juntas. Propongo alimentación conmutable independiente por cámara, comprobación temporal y una acción explícita de armado/inicio distinta de calibrar altura. No selecciono todavía el circuito, sus pines ni el instante de disparo.

La grabación debe estar funcionando antes de toda la secuencia de descenso. Encender por primera vez justo en separación puede perder el comienzo mientras arrancan el procesador, sensor y SD. Mediré tiempo desde alimentación hasta primer cuadro guardado y exposición estable; con eso dimensionaremos margen y evento con Edu. Preparar en tierra puede ahorrar menos energía, pero ofrecer más seguridad de inicio. No usaré «altura cero» como disparador implícito: repetir una calibración no debe reiniciar ni cortar video.

## Opciones de hardware y ahorro

| Opción | Qué aporta | Límite y verificación necesaria |
|---|---|---|
| ESP32-CAM existentes, OV2640 por confirmar en ambas | Aprovecho kits disponibles; captura JPEG y tarjeta local | Confirmar PSRAM, pinout real, sensor, consumo y grabación sostenida; resolución máxima no acredita video útil |
| XIAO ESP32-S3 Sense, alternativa de comparación | Fabricante documenta cámara, PSRAM y microSD | Cambia montaje, sensor según lote y software; no justifica compra antes de medir las placas disponibles |
| ESP32-CAM encendida, sin grabar | Menor demora para iniciar; menos conmutación externa | Sigue consumiendo; margen de batería no medido aquí |
| Deep sleep y sensor en reposo | Reduce consumo y permite despertar mediante señal compatible | No equivale a alimentación cortada: quedan dominios/consumos de placa; no mantiene recepción Wi-Fi dormida |
| Corte de alimentación con interruptor electrónico | Se aproxima mejor a cámaras realmente apagadas; puedo aislar y reiniciar una | Fugas no son cero, requiere conmutación, control de señales y arranque fiable; puede comprometer autonomía ante reset del OBC |

El [controlador oficial de Espressif](https://github.com/espressif/esp32-camera) soporta OV2640 y captura JPEG. Advierte necesidad de PSRAM salvo casos limitados y carga adicional de RGB/YUV, especialmente junto con Wi-Fi. Es una base de software, no certificación de estas placas ni grabador de video completo. El [ejemplo oficial de pines](https://raw.githubusercontent.com/espressif/arduino-esp32/master/libraries/ESP32/examples/Camera/CameraWebServer/camera_pins.h) permite contrastar la variante AI-Thinker; no autoriza copiar pines a un clon sin revisión. PWDN del sensor no apaga automáticamente toda la placa.

[Espressif documenta deep sleep y sus despertares](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/sleep_modes.html): quedan dominios activos y la conexión inalámbrica no se mantiene. Debemos medir el conjunto con sensor, regulador y SD, no copiar el consumo del chip desnudo.

Para comparar otro modelo consulté [Seeed XIAO ESP32-S3 Sense](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/): incorpora cámara, soporte SD y 8 MB de PSRAM; el sensor cambia según lote. No traslado sus cifras de consumo a nuestras placas. Su [ejemplo de grabación](https://wiki.seeedstudio.com/xiao_esp32s3_camera_usage/#record-short-videos-and-save-to-microsd-card) es didáctico y advierte limitaciones de exportación/reproducción: no copiaré un bucle que concatena JPEG y llama .avi al archivo como prueba de video correctamente temporizado. Necesitamos formato recuperable, marcas temporales y reproducción verificada.

## Cómo apagar sin efectos secundarios

Evaluaré interruptor de carga en el positivo y masa común, un canal por cámara. Un GPIO da la orden de habilitación; no alimenta la cámara. Como ejemplo de familia, [TI TPS22918](https://www.ti.com/product/TPS22918) ofrece subida controlada y descarga de salida. No lo seleccioné ni supongo que incluya limitación de corriente o bloqueo inverso completo: esas funciones deben comprobarse en el componente final. Corriente admisible, disipación, habilitación, fuente real y protecciones siguen TBD.

Antes de retirar alimentación, cierro y confirmo los archivos. Las líneas START/UART/estado tampoco pueden inyectar corriente a una cámara apagada. Debemos elegir aislamiento o niveles de reposo documentados y verificarlos; masa compartida y una resistencia por sí solas no acreditan aislamiento. La [nota TI sobre protección con alimentación apagada](https://www.ti.com/document-viewer/lit/html/SCDA015) describe cómo señales activas pueden realimentar circuitos por protección ESD. Bloqueo inverso en potencia y aislamiento de señales resuelven rutas distintas.

Hay otra condición crítica: ASTRA-16 quería que una cámara ya grabando continuara si el STM32 se reinicia. Si el reset deja su habilitación de potencia en cero, perdemos esa autonomía. Debemos resolver retención de habilitación, secuencia de reset y recuperación antes de aprobar el corte de alimentación; el estado seguro no tiene por qué ser el mismo antes del armado y durante grabación. Un pull-down permanente no resuelve ambas necesidades. La electrónica y política finales quedan para revisión conjunta, sin asignar trabajo en tareas ajenas.

## Qué hará «Comprobar cámaras»

Es el nombre entendible de una función propuesta, no sintaxis de telecomando acordada. En espera, el proceso sería:

1. Identificar la solicitud y el estado previo; encender primero una cámara y después la otra para evaluar picos sin sumarlos innecesariamente.
2. Esperar identidad, arranque y estabilización medidos. Cada respuesta pertenece a una cámara y un arranque concretos.
3. Capturar un JPEG nuevo, guardar un archivo nuevo en su tarjeta y leerlo para comparar integridad. Informar SD ausente, llena, fallo de escritura o captura sin convertirlos en «cámara OK».
4. Transferir una foto o miniatura por el transporte de mantenimiento acordado; validar tamaño/integridad y que la PC pueda decodificarla. Registrar las dos por separado.
5. Mostrar ambas con cámara, hora/ID de chequeo, antigüedad y resultado. La ventana puede ser temporal, pero conservo la evidencia: una imagen vieja no sirve como confirmación nueva.
6. Cerrar archivos y volver a apagado sólo si la prueba partió de espera. Si ya graba, no aplico un ciclo de alimentación ni interrumpo grabación por un chequeo; su política queda por definir.

Separaré «encendida», «capturó», «guardó», «imagen recibida» y «grabación verificada». También tendrá sentido recibir un resultado ligero por radio aunque no se pueda traer la foto. Un chequeo positivo acredita ese instante; no garantiza el vuelo posterior, la estabilidad térmica, todos los cuadros ni la energía restante.

## Cómo llegan las fotos a tierra

| Camino | Uso que estudiaría | Qué falta |
|---|---|---|
| Cable/serie con base USB de mantenimiento | Primera comprobación cerca de la notebook, sin ocupar RF | Firmware de captura y encuadre binario, identificación de dos puertos, integridad y alimentación; el conector USB solo no es una webcam |
| Wi-Fi local temporal | Vista previa de banco/preparación si el equipo y la competencia lo admiten | Permiso aplicable, alcance, energía, modo de mantenimiento y evidencia de apagado antes de misión; no lo habilito por defecto |
| Miniaturas por SX1276 | Evaluación posterior si necesitamos revisar sin acceso local | Perfil acordado, fragmentación, prioridad de telemetría, reensamble, integridad, tiempo límite y presupuesto de aire/energía |
| Video completo en microSD | Evidencia del descenso recuperada después | Formato, continuidad, espacio, temperaturas, montaje y recuperación ante corte |

Una foto «mostrada por un toque» puede haber tardado mucho en llegar. Dos imágenes supuestas de 20 KiB suman 327680 bits: a una tasa útil hipotética de 9600 bit/s requieren como mínimo 34,13 s, y a 1000 bit/s 327,68 s. No son tamaños medidos ni perfiles elegidos. El cálculo no incluye reintentos ni reservas; sirve para no prometer instantaneidad.

[NiceRF informa tasas LoRa que dependen del perfil](https://www.nicerf.com/news/lora-module-sx1276.html); una tasa física máxima no equivale a caudal útil disponible. Conservo el [análisis previo de tiempo de aire y potencia](../interfaces/2026-10-24-radio-potencia-y-airtime-actualizacion-03.md). No cambiaré RF o potencia para meter imágenes ni retrasaré telemetría requerida de 1 Hz. La vista previa en misión sigue sin aprobarse.

## Plan de implementación y ensayos

| Paso | Resultado que necesito guardar | Estado |
|---|---|---|
| Inventario individual | Sensor detectado, revisión, PSRAM, firmware original respaldado cuando corresponda y SD identificada | Pendiente |
| Una foto de una cámara | Archivo nuevo decodificable, color, dimensiones, tiempo y escritura/lectura coincidente | Pendiente |
| Doble chequeo | Dos identidades y fotos nuevas; una falla no vuelve verde a la otra | Pendiente |
| Grabación local | ≥640×480 color, cuadros y tiempos comprobados; conservar intervalos sin datos, no rellenarlos | Pendiente |
| Segmentación | Archivos consecutivos reproducibles, sin perder la transición entre ellos; recuperación del último tras corte | Pendiente |
| Potencia | Corriente apagada/espera/arranque/chequeo/grabación, picos y tensión en terminales; dos cámaras y radio simultáneos | Pendiente |
| Control y resets | Standby, chequeo, armado/inicio y finalización repetidos; reset de OBC no corta cámaras ya grabando | Pendiente |
| Entorno | Espera de diseño, vibración/montaje y temperatura dentro del CanSat; encendido con batería en condición de diseño | Pendiente |
| Adaptación a comandos de Edu | Vectores acordados y resultados medidos; sin confundir enviada con ejecutada | Pendiente |
| Integración en interfaz | Estados y antigüedad individuales, imagen completa o transferencia fallida explicada | Propuesta, sin cambios de app |

Mediré energía en una referencia común. Si tomo corriente del bus de 5 V, calcularé energía por tiempo y convertiré a batería con eficiencia del convertidor; no sumaré mAh de buses distintos como si fueran equivalentes. Incluiré arranques y chequeos, no sólo minutos de grabación. FPS, duración máxima, tiempo de arranque, temperatura, consumo, capacidad SD, criterio de exposición y presupuesto de enlace quedan TBD/TBR con evidencia.

Como antecedente ya documentado, [RSX relata fallas de cámara y una hipótesis térmica sin ensayo térmico previo](../investigacion/2026-10-22-rsx-pfr-y-fallas.md). Lo uso para priorizar nuestro ensayo dentro del volumen de vuelo, no como causa demostrada ni para descartar ESP32.

## Hasta dónde llegué

Identifiqué visualmente las placas, comparé documentación primaria, revisé requisitos archivados y la arquitectura previa, abrí mi tarea y preparé esta propuesta. No cargué firmware en cámaras, conecté potencia, tomé fotos con ellas ni medí consumo. No hay todavía botón operativo de cámara en groundstation. Conservo el banco de telemetría que ya funciona y no modifico código de vuelo ni archivos de otras áreas.
