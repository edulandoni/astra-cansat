# 27/10/2026 — Vista previa Wi-Fi y supervisión propuesta de grabación

[ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39) · [ASTRA-41](https://astrateam2026.atlassian.net/browse/ASTRA-41) · conceptos de interfaz en [ASTRA-24](https://astrateam2026.atlassian.net/browse/ASTRA-24). Continúo el [análisis de grabación autónoma](2026-10-27-video-vivo-y-grabacion-autonoma-19.md), sin reemplazarlo.

## Alcance de este bloque

Confirmamos que las dos cámaras disponen de su propia microSD. Eso permite preparar pruebas simultáneas; no convierte los ensayos previos por turnos en una prueba simultánea. El sonido queda al final y no forma parte de este desarrollo.

Implementé un camino local para ver imágenes nuevas dentro del Laboratorio Qt y un modelo separado para interpretar progreso de grabación. Son funciones distintas: **la imagen de la red no acredita guardado en SD**. Mantengo las fotos USB y el ensayo corto CLIP; todavía no implementé el grabador autónomo continuo ni el circuito de potencia.

## Firmware candidato de mantenimiento

Creé `AstraCameraPreviewBench` separado de `AstraCameraSequenceBench`. Conserva INFO/INIT/PHOTO/SAVE/CLIP y agrega WIFI_ON/WIFI_OFF exclusivamente para mantenimiento local por USB, con identidad comprobada antes de activar la red. Estos nombres no son comandos de vuelo aprobados. Edu define esa interfaz y yo adapto tierra.

El programa no inicia Wi-Fi al arrancar. La activación explícita crea una red local protegida por una clave temporal generada en memoria por la app; la clave se muestra para conectar Windows y no se guarda en archivos ni se incluye en documentos o logs. Desactivar Wi-Fi no corta alimentación ni finaliza una grabación por una asociación implícita. Reiniciar vuelve a dejar la radio sin iniciar. No habilito esta red como enlace de misión ni doy por confirmado su permiso en preparación oficial.

El productor de imágenes usa dos buffers de cámara y un único último JPEG de vista previa en PSRAM. La tarea de red toma una copia y la envía sin retener el buffer de captura; no acumula una cola indefinida de cuadros. El objetivo de adquisición se solicita cada 100 ms, pero no es una tasa conseguida. El servidor atiende un flujo en el puerto 81, ruta `/stream`, con separador `astra-frame`. Cada parte incluye longitud, unidad, arranque, contador e instante de captura. El uso de JPEG/HTTP multipart se apoya en el [ejemplo de Espressif](https://github.com/espressif/arduino-esp32/tree/master/libraries/ESP32/examples/Camera/CameraWebServer); el control de buffers se fundamenta en el [controlador oficial](https://github.com/espressif/esp32-camera).

No presento escritura y streaming simultáneos como probados: PHOTO/SAVE/CLIP se ejecutan en el bucle principal y pueden detener temporalmente la actualización de vista previa. Primero desconecto el visor para medir fotos/SD. Separar adquisición y almacenamiento con prioridad de grabación sigue siendo trabajo del próximo candidato. La vista previa conserva VGA; no implementé un escalador independiente a QVGA ni medí todavía fps, latencia, energía o alcance de Wi-Fi.

## Laboratorio nativo

En Cámaras agregué Vista previa Wi-Fi con selección de unidad y dirección, activación/desactivación por el puerto USB elegido y conexión/desconexión de imagen explícitas. Abrir el Laboratorio no abre una conexión a la cámara. El control USB comparte las exclusiones de fotos y telemetría: no admite dos operaciones simultáneas sobre el puerto.

Después de activar, conecto Windows a la red indicada y pulso Conectar vista previa. Esto es una red local: no necesita Internet y puede interrumpir el acceso a Internet de la notebook mientras esté seleccionada. Vuelvo a la red habitual al terminar. No cambio la configuración de Windows automáticamente.

El cliente utiliza la identidad privada registrada por unidad. Rechaza otra cámara, cambios de arranque, retrocesos, igual contador con contenido diferente, JPEG inválido, tamaños excesivos y respuestas/redirecciones incompatibles. Un duplicado idéntico no renueva la antigüedad. Limito bloques a 64 KiB, cabeceras a 4 KiB y JPEG a 512 KiB, con dimensiones máximas de 1600×1200 antes de decodificar. Uso sólo dirección IP local explícita, sin credenciales en URL, proxy ni caché.

Si pasan dos segundos sin otra imagen válida, la vista deja de marcar recepción actual. Una desconexión conserva la imagen identificada como anterior. Muestro tiempo desde recepción y promedio recibido; **no los llamo latencia de captura ni rendimiento de la SD**. El visor no inicia grabación, no guarda fotos por rutina ni confirma continuidad del video local.

## Supervisión de grabación: modelo preparado

`camera_health.py` interpreta reportes sintéticos con identidad, arranque, segmento, secuencia, cuadros/bytes escritos, tiempo de funcionamiento, última escritura, estado y error. Es una propuesta de software para revisar con Edu, no un formato de vuelo ni un receptor conectado a cámaras.

| Resultado del modelo | Interpretación |
| --- | --- |
| UNKNOWN | No hay reporte o venció el tiempo configurado |
| START_UNCONFIRMED | Se declara grabación sin cuadros/bytes guardados |
| PROGRESS_UNCONFIRMED | Hay un reporte, pero falta observar progreso entre reportes del mismo contexto |
| WRITING_REPORTED | Progresan cuadros y bytes, con escritura reciente; es reporte del emisor, no lectura independiente |
| WRITE_STALLED | No progresa la escritura o envejeció el último guardado |
| ERROR / NOT_RECORDING | Falla reportada / grabación no declarada |

Un duplicado no renueva el vencimiento. Rechazo contadores regresivos y tiempos contradictorios; un arranque/segmento nuevo necesita confirmar progreso nuevamente. No convierto un estado reportado en garantía futura ni un corte de radio en prueba de que la cámara dejó de grabar. Falta recibir el contrato de Edu, implementar su adaptador y medir la supervisión con escritura real.

## Compilación, carga y arranque observados

Compilé con Arduino CLI 1.5.1 y Arduino-ESP32 3.3.12 para `esp32:esp32:esp32cam`: 1118015 bytes de programa y 58540 bytes estáticos. El binario de aplicación tiene 1118160 bytes, SHA-256 `ba24abe39077f5002a509a5efc238b8bee0e042f4404f5e75ff169d9050f18b6`.

Verifiqué por el cargador la identidad de cámara 1 y la igualdad de tablas de partición respecto del programa probado. Escribí sólo la aplicación en 0x10000, con hash verificado. No reescribí bootloader/particiones ni formateé o borré la SD. Los respaldos y el firmware anterior siguen conservados.

Después del reset de carga, INFO respondió sin pedir otra maniobra: identidad correcta, sensor listo, 4194304 bytes de PSRAM y capacidades WIFI_ON/WIFI_OFF. Esa observación demuestra un arranque en esta condición, no estabilidad autónoma. La consulta previa a la carga no obtuvo respuesta; conservo ese resultado sin atribuirle una causa que no aislé.

BOOT/IO0 se utiliza para entrar al cargador. **No es aceptable depender de BOOT o de pulsar RST para operar durante la misión.** Aún faltan encendidos desde alimentación representativa sin USB ni botones, arranque de ambas cámaras, inicio de grabación y continuidad ante reset del OBC. Como campaña inicial propongo 20 ciclos por unidad, registrando tensión, tiempo de arranque, identidad, primer cuadro escrito y fallos; esa cantidad es un criterio de banco propuesto, no una demostración estadística de confiabilidad de vuelo.

## Verificación y límites

Pasaron 43 tests del banco de cámaras y 26 del Laboratorio. La prueba de red del visor usa un servidor PC explícitamente identificado como sustituto: entrega JPEG fragmentados a Qt, comprueba decodificación, antigüedad y cierre. Las pruebas del modelo de salud usan reportes ficticios. Estas pruebas no acreditan rendimiento de las ESP32-CAM, coexistencia con SD, consumo, ausencia de emisiones en espera ni autonomía.

La comprobación de interfaz se realizó fuera de pantalla, sin controlar el escritorio. La activación y la imagen física de Wi-Fi requieren sus resultados propios; no las doy por realizadas porque el firmware compiló o la app recibió imágenes del servidor PC. El [control de este bloque](../../evidence/2026-10-27-camara-wifi/control-01.json) distingue software, carga y pendientes.

## Procedimiento y siguiente bloque

1. Elegir cámara 1 y su puerto USB, sin capturas en curso.
2. Activar Wi-Fi por USB; conservar en pantalla la red/clave temporal, sin publicarla.
3. Conectar Windows a esa red y pulsar Conectar vista previa. Mover una escena/reloj de referencia y medir demora/cadencia; comprobar imagen detenida y desconexión.
4. Desconectar el visor y desactivar Wi-Fi por USB. Volver a la red habitual. Repetir fotos/SD y verificar los archivos desde lector cuando corresponda.
5. Después de caracterizar este camino, desarrollar grabación continua independiente con prioridad de escritura, consultas de progreso y cierre/recuperación de segmentos. Recién entonces ensayar simultáneamente ambas cámaras con sus tarjetas y alimentación representativa.

Las decisiones de activación en vuelo, armado, evento de inicio/parada y conservación de potencia ante reset siguen pendientes de acuerdo y circuito. No cambié `protocol/`, vuelo, parámetros SX1276 ni tareas ajenas.
