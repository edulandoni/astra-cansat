# 27/10/2026 — Grabación segmentada y supervisión USB

[ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39) · [ASTRA-41](https://astrateam2026.atlassian.net/browse/ASTRA-41) · [ASTRA-24](https://astrateam2026.atlassian.net/browse/ASTRA-24). Continúo la [vista Wi-Fi confirmada](2026-10-27-vista-wifi-confirmada-y-red-compartida.md), conservando sus resultados.

## Qué aporta este bloque

La cámara puede recibir un inicio y seguir capturando y guardando en su propia SD hasta una parada o una duración límite. Ya no depende de pedir una foto o un grupo de doce cuadros cada vez. Puedo consultar progreso real de archivos, cerrar el seguimiento USB y volver a consultar. La vista previa y el Wi-Fi quedan apagados durante estos ensayos.

La grabación se conserva como JPEG con tiempos e índices, agrupados en segmentos. La PC puede verificar la grabación completa, reproducirla y exportar un MP4 con los tiempos originales. No presento ese MP4 como H.264 codificado en la cámara ni una tasa nominal de reproducción como tasa de captura. La continuidad y fluidez se evalúan por los tiempos de los cuadros, no por la extensión del archivo.

Para el PDR este bloque aporta control, trazabilidad y evidencia de banco. **Cerrar el puerto no es desenchufar la alimentación USB.** No prueba todavía autonomía con batería, arranque del sistema completo, vuelo, funcionamiento de ambas cámaras juntas ni continuidad ante reset del OBC.

## Implementación del candidato

Creé `AstraCameraRecorderBench` separado de los candidatos de fotos, secuencia corta y vista previa anteriores. Conserva esas funciones cuando está inactivo; durante grabación rechaza operaciones que puedan interrumpir el sensor o disputar el almacenamiento. El inicio exige Wi-Fi desactivado. No cambia redes de Windows ni configura SX1276.

El banco tiene REC_START, REC_STOP y REC_STATUS, con identidad de orden, arranque y ejecución. Son órdenes ASCII locales experimentales; no son la interfaz de vuelo aprobada. Edu define los comandos de vuelo y adapto tierra a su contrato.

En reposo el candidato mantiene el sensor preparado. No implementa todavía el corte de alimentación ni demuestra el consumo mínimo de espera; apagar Wi-Fi no equivale a apagar la cámara.

Cada inicio declara de 1 a 3600 segundos. Es un límite de banco atendido por el bucle de cámara: no un temporizador externo capaz de interrumpir una operación de SD bloqueada. Repetir el mismo inicio conserva su ejecución; cambiar su duración con el mismo ID se rechaza. La parada debe identificar el arranque y ejecución correctos. El historial acotado de órdenes no se presenta como persistencia ante reinicio; un comando de otro arranque se rechaza.

La captura tiene objetivo de 200 ms entre intentos, sin recuperar atrasos en ráfagas. Cada JPEG VGA en color se escribe, cierra y lee para comprobar longitud/CRC. Después guardo y verifico su índice lateral con tiempo y CRC. Los contadores de guardado avanzan después de esas comprobaciones, no al aceptar la orden ni al capturar sin guardar. Verifico espacio antes del cuadro y no sobrescribo rutas existentes. No formateo ni borro archivos.

Un segmento reúne hasta 60 cuadros y cierra su manifiesto. Un segmento final más corto es válido al detenerse correctamente. Mantengo en memoria sólo los metadatos del segmento actual, no toda la misión. Los segmentos cerrados y los índices individuales conservan evidencia si se interrumpe otro segmento, pero todavía no hice un ensayo de corte de energía ni implementé recuperación automática de cualquier carpeta incompleta. El verificador completo rechaza cierres ausentes, índices en conflicto y discrepancias de tiempo o totales; no inventa cuadros.

## Aplicación y estados

En Cámaras agregué duración límite, Iniciar grabación, Consultar grabación, Detener y cerrar, Cerrar seguimiento USB y Copiar grabación a PC por USB. Un único trabajador conserva el puerto durante el seguimiento; el panel bloquea fotos, Wi-Fi y telemetría sobre ese puerto. No abre hardware al iniciar el Laboratorio.

El progreso distingue capturados, guardados/leídos por cámara, bytes, segmentos cerrados, espacio disponible y edad de la última escritura. El modelo preparado antes ahora recibe esos reportes reales. No muestra confirmación de continuidad por una bandera aislada: espera avance entre reportes del mismo contexto y deja el estado desconocido al vencer la información. Una orden rechazada se distingue de un timeout cuyo resultado desconocemos; no hay reintentos automáticos de inicio o parada.

Cerrar seguimiento o cerrar la aplicación no envía STOP por detrás: la cámara puede continuar hasta el límite que ya recibió. La pantalla lo explica. No retiro alimentación mientras graba. Una copia en curso puede cancelarse conservando originales y archivos parciales; los parciales no se presentan como una copia completa.

## Pruebas físicas con cámara 1

Compilé el primer candidato con Arduino CLI 1.5.1 y Arduino-ESP32 3.3.12: 1123203 bytes de programa y 60084 bytes estáticos. La aplicación binaria ocupa 1123344 bytes y tiene SHA-256 `2c4eef60d2de49497186d961e820b73d86a62989539c8c685aeb57e2814a707b`.

Comprobé identidad antes de escribir sólo la aplicación en 0x10000. Las particiones coinciden con el candidato probado; no reescribí bootloader ni tabla y no formateé la SD. Esta carga y el arranque se realizaron automáticamente, sin pedir BOOT/RST. Es un caso nuevo favorable; no elimina los fallos de arranque registrados ni sustituye los ciclos de alimentación pendientes.

| Ensayo | Resultado reportado por la cámara |
| --- | --- |
| Duración límite de 30 s | COMPLETE / DURATION_LIMIT; 123 capturados, guardados y leídos; 1753920 bytes de JPEG; tres segmentos |
| Puerto cerrado durante 8 s | Mismo arranque y ejecución al volver; avance de 10 a 48 cuadros mientras no había seguimiento |
| Repetición de inicio | Misma ejecución; no volvió a cero ni creó otra grabación |
| Mismo inicio con otra duración | Rechazado |
| Parada dirigida a otra ejecución | Rechazada; la grabación continuó |
| Nueva grabación detenida explícitamente | COMPLETE / STOP_REQUESTED; 16 cuadros; 227713 bytes; un segmento |
| Repetición de esa parada | Mismos cuadros y ejecución; no inició otra grabación |

Esos valores proceden de respuestas físicas y registros USB. La ausencia de seguimiento no equivale a ausencia de alimentación. El tiempo límite solicitado tampoco es por sí solo la separación medida entre primer y último cuadro: esa medición se obtiene de los archivos.

## Lectura sin extraer la tarjeta

Para completar comprobaciones sin maniobras físicas agregué REC_READ y un copiador acotado. Sólo acepta selectores de archivos del banco y contextos hexadecimales; no recibe rutas arbitrarias ni permite escribir o borrar SD. Rechaza lectura durante grabación o vista previa. El origen de una carpeta puede pertenecer al arranque de captura anterior a una actualización, separado del arranque actual que atiende la lectura.

El cliente comprueba identidad, longitud y CRC de cada transferencia. Crea una carpeta nueva, conserva nombres y metadatos y mantiene parciales ante fallo. Después decodifica los JPEG en PC y contrasta manifiestos, índices laterales, orden temporal, segmentos y totales. La copia de banco tiene un límite explícito de 512 MiB; no la presento como descarga ilimitada de una misión de cualquier tamaño.

Esta revisión usa el mismo controlador SD de la cámara y **no es una lectura independiente con otro lector**. La validación en PC sí agrega decodificación e integridad de la copia recibida. Nunca doy por comprobada una transferencia física sólo porque pasó un test con archivos de PC.

Compilé la ampliación con 1125171 bytes de programa y 60132 bytes estáticos. El binario ocupa 1125312 bytes, SHA-256 `87aef759d94e6c9fded0d5d21b8d34cdcad204dfcc78d6b0298c3b43080b221a`. Antes de cargar comprobé que no hubiera grabación activa. Verifiqué otra vez identidad y particiones, escribí sólo aplicación y comprobé hash. La carga volvió a ser automática. Los archivos de las grabaciones anteriores permanecieron en SD y se recuperaron después del cambio de arranque; conservo el binario y las fuentes de la iteración de captura por separado del candidato final.

Recuperé las dos primeras grabaciones completas por USB, conservando sus nombres e índices. El verificador contrastó todos los JPEG, CRC, tiempos, índices laterales y totales; los archivos locales permanecieron iguales durante la comprobación. Exporté ambos MP4 y volví a decodificarlos. No envié imágenes o videos a repositorios públicos.

| Comprobación desde archivos copiados | Límite de 30 s | Parada explícita |
| --- | --- | --- |
| Archivos recibidos | 251 | 35 |
| Cuadros JPEG VGA RGB decodificados | 123 | 16 |
| Segmentos comprobados | 3 | 1 |
| Separación primero–último cuadro | 29,828024 s | 3,038722 s |
| Cadencia media por N−1 intervalos | 4,090113 cuadros/s | 4,936286 cuadros/s |
| Mayor intervalo entre marcas | 0,479809 s | 0,239837 s |
| Cuadros decodificados del MP4 | 123 | 16 |
| Diferencia temporal máxima del MP4 | 0 µs | 0 µs |

No uniformé intervalos ni añadí cuadros para aparentar más fluidez. La duración de presentación final del MP4 puede incluir el último cuadro; no la confundo con la separación medida entre extremos. Inspeccioné el primer y último JPEG de la grabación larga: muestran techo y luminaria, sin patrón de movimiento controlado. La prueba no valida comportamiento con movimiento de vuelo, estabilización, exposición exterior ni vibración.

Después accioné por código los botones Qt con hardware real y plataforma fuera de pantalla: inicio de cinco segundos, progreso de escritura visible en el estado, cierre reportado, copia USB, apertura del archivo verificado y exportación. Esa tercera grabación reportó 24 cuadros y completó la copia y exportación. No tomé control del escritorio ni afirmo que hubo una observación manual de esos botones. Conservo sus registros por separado de las dos primeras sesiones.

## Verificación de software

Pasaron 58 tests del banco de cámaras y 29 del Laboratorio, con salida correcta del proceso. Cubren fragmentación, arranque/unidad incorrectos, contradicciones de reportes, timeout sin reintento, rechazo conocido, cierre de seguimiento sin parada oculta, grabaciones de varios segmentos, CRC/archivos faltantes, conflictos de índices, conservación de fuentes, copia cancelable y exportación con tiempos irregulares. La lectura de archivos ya guardados no exige que el sensor esté listo; sí exige identidad y capacidad de lectura correctas. Los casos de archivo generados en PC se identifican como sustitutos de hardware.

Al ejecutar juntos los tests Qt apareció un fallo nativo al terminar el proceso. Detecté widgets de pruebas cerrados pero todavía vivos y agregué limpieza explícita entre casos, antes de destruir QApplication. La suite volvió a terminar correctamente. No presento un resultado «OK» seguido de caída del proceso como una validación satisfactoria.

La interfaz se prueba fuera de pantalla, sin controlar el escritorio. Las maniobras de la campaña física se ejecutaron mediante el mismo cliente USB utilizado por el panel; la observación manual de los botones nuevos es un alcance separado.

## Límites y siguientes ensayos

Quedan pendientes pruebas largas y con movimiento controlado, caracterización de cadencia y huecos bajo carga, SD llena/lenta/ausente en hardware, corte de energía y recuperación, alimentación representativa, arranque sin USB/botones en ambas unidades, continuidad ante reset del OBC, modo compartido de Wi-Fi y streaming simultáneo con prioridad de escritura. Sonido permanece fuera de esta etapa. Mantengo los ensayos de vuelo y los acuerdos de comandos abiertos.

[Control de la primera campaña](../../evidence/2026-10-27-grabacion-segmentada/control-01.json) · [Copia USB y MP4](../../evidence/2026-10-27-grabacion-segmentada/control-02-copia-usb.json) · [Integración Qt con cámara real](../../evidence/2026-10-27-grabacion-segmentada/control-03-qt-fisico.json). Conservo las tres capturas y sus alcances separados.

[Control final de software](../../evidence/2026-10-27-grabacion-segmentada/control-04-software-final.json): incluye cancelación de copia, conserva parciales y originales.

[Huellas de las fuentes publicadas](../../evidence/2026-10-27-grabacion-segmentada/control-05-fuentes-publicadas.json). Los controles anteriores conservan el estado de sus propias iteraciones. El acceso de la app se denomina Ver grabación conservada, porque el archivo seleccionado no implica que sea la última captura cronológica.
