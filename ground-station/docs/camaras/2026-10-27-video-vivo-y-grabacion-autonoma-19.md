# 27/10/2026 — ACTUALIZACIÓN 19: video, vista en vivo y grabación autónoma

[ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39) · interfaz pendiente en [ASTRA-24](https://astrateam2026.atlassian.net/browse/ASTRA-24). Continúo la [primera secuencia física](2026-10-27-primera-secuencia-y-mp4-18.md) y el [estudio de energía y chequeo](2026-10-25-energia-chequeo-dual.md). Esta entrada es análisis y propuesta de verificación; no es otra prueba física ni firmware cargado.

## Qué tenemos y qué necesitamos

La cámara sí puede proporcionar imágenes sucesivas para video. Nuestro ensayo guardó doce JPEG y después construí un MP4 en la PC: 6,077584 s entre el primer cuadro y el último, aproximadamente 1,81 cuadros/s. No es todavía una grabación continua de vuelo ni una vista en vivo fluida. Todos los videos se componen de cuadros; lo que nos falta es capturarlos con continuidad suficiente, conservar sus tiempos y sostener la operación completa sin depender de la notebook.

Separo tres funciones: **grabar el viaje en la SD**, **ver una imagen actual en el Laboratorio** y **conocer desde tierra si cada cámara sigue guardando**. Pueden fallar de manera independiente. Ver una foto no demuestra que la SD funciona; recibir «inicio aceptado» no demuestra que se escribió el primer cuadro; perder la radio no significa que la grabación local se detuvo.

Para el PDR, esta propuesta define cómo obtendremos evidencia. Hoy sólo puedo afirmar las fotos verificadas y la secuencia corta ya documentada. No doy por aprobados video continuo, autonomía, apagado de potencia, grabación simultánea de dos unidades ni supervivencia a reset.

## Capacidad de estas placas y sonido

El controlador oficial de [Espressif](https://github.com/espressif/esp32-camera) admite adquisición JPEG con OV2640 y ESP32. PSRAM, formato y cantidad de buffers afectan el funcionamiento; aumentar buffers también exige más memoria/procesamiento. El ejemplo oficial [CameraWebServer](https://raw.githubusercontent.com/espressif/arduino-esp32/master/libraries/ESP32/examples/Camera/CameraWebServer/app_httpd.cpp) implementa un flujo de imágenes JPEG por HTTP multipart. Es una base para estudiar vista en vivo; no garantiza una tasa concreta en nuestras unidades.

El diseño estándar ESP32-CAM de las fotos no incorpora un micrófono identificado. La [ficha de Ai-Thinker V1.0, conservada por un distribuidor](https://gzhls.at/blob/ldb/9/5/1/c/fa48c01c284d3f9299f1b92f2286d6c6314a.pdf) documenta cámara, tarjeta, interfaces y Wi-Fi/Bluetooth, sin identificar un micrófono. La uso como referencia de diseño, no como certificación de la revisión exacta de nuestros clones ni de su consumo o capacidad máxima de tarjeta. Nuestros programas actuales no adquieren audio. Tener Bluetooth o una interfaz de audio en el chip no incorpora el sensor acústico. Sonido requiere hardware e integración adicionales; lo mantengo como extra después de asegurar el video.

No confundo extensión con capacidad: el MP4 H.264 que exporté se codifica en la PC. No lo presento como un codificador H.264 instalado en la cámara. Para el próximo grabador estudiaré JPEG continuo con índice y segmentos recuperables, o contenedor MJPEG/AVI, midiendo rendimiento e integridad antes de elegir. Un archivo único enorme y una tasa nominal no prueban continuidad.

## Vista en vivo: camino propuesto

Propongo **Wi-Fi local de mantenimiento para banco**, mostrando el flujo dentro de la misma aplicación Qt, sin una interfaz HTML. La grabación local tendrá prioridad; un espectador lento no deberá bloquearla. Usaré una cola acotada para vista previa que descarte imágenes viejas y muestre la más reciente, contabilizando descartes. La aplicación mostrará unidad, origen, cuadros/s recibidos y antigüedad; ante corte conservará la última imagen con aviso, sin llamarla actual. Si no hay una referencia de reloj medida, no presentaré tiempo desde recepción como latencia de captura.

Como objetivo inicial de ensayo propongo vista previa de al menos 10 cuadros/s a 320×240 y latencia p95 menor de 500 ms mediante escena/reloj de referencia. Es una hipótesis de aceptación de banco, no una prestación garantizada ni requisito CONAE. La grabación exigida se evalúa aparte a la resolución aplicable: bajar la vista previa no autoriza bajar la evidencia del vuelo. Si el procesador no sostiene ambos caminos, mediré degradación y priorizaré grabación; no ocultaré el problema cambiando la velocidad de reproducción.

El USB actual a 115200 bit/s y 8N1 tiene un techo teórico de 11520 bytes/s antes de nuestro protocolo. Una foto medida de 14733 bytes demanda al menos 1,279 s sólo de transmisión. Diez fotos de ese tamaño por segundo exigirían unos 147330 bytes/s: no entran en ese canal. El tamaño cambia según escena/calidad. Podemos estudiar un baudrate mayor, pero necesitará ensayo completo de errores, receptor y estabilidad. No basta acelerar el reproductor.

| Transporte | Utilidad | Condición y límite |
| --- | --- | --- |
| USB actual | Foto puntual, diagnóstico y control de banco | Ya probado; insuficiente para el objetivo anterior con esos tamaños |
| Wi-Fi local | Encuadre y vista previa cerca del banco | Candidato; medir energía, demora y coexistencia con SD; apagado explícito fuera de mantenimiento |
| Bluetooth | Alternativa por estudiar sólo si aparece una necesidad concreta | No agrega una ventaja demostrada y suma otro camino de prueba |
| SX1276 | Estado ligero de cámaras en vuelo; miniatura eventual | Perfil/bytes con Edu, prioridad de telemetría, permiso y presupuesto de aire; no prometo video en vivo |

La capacidad del chip no autoriza otro transmisor en misión. La última revisión diaria del aula fue parcial y no revalidé hoy una autorización para Wi-Fi/Bluetooth en vuelo. Conservo la [cobertura conocida](../aula/2026-10-26/Informe_aula_2026-10-26_2059_ART.md). Wi-Fi local es una propuesta para banco; cualquier uso en preparación oficial o misión necesita confirmar las condiciones aplicables. Una miniatura recibida por radio será una comprobación puntual con fecha e identidad, nunca prueba de continuidad.

## Funcionamiento autónomo propuesto

1. **Espera:** alimentación de cámaras cortada por un circuito adecuado, si ésa es la arquitectura acordada. Sin alimentación la cámara no puede escuchar órdenes: el OBC debe controlar su encendido. Medir fugas y alimentación accidental por señales; no prometer 0 mA sin medir.
2. **Chequeo previo:** encender cada unidad, identificar arranque y tarjeta, verificar espacio, capturar una imagen nueva y un tramo corto, cerrar y leer para comprobar integridad. Revisar encuadre en el montaje real. Guardar resultados individuales con vencimiento. Si ya está grabando, la consulta no debe reiniciarla ni apagarla.
3. **Armado:** definir con Edu evento, margen de arranque y ventana que debemos filmar. Poner altura en cero no iniciará automáticamente cámaras por una asociación implícita. La cámara debe alcanzar grabación antes del comienzo exigido; la reserva de tiempo y energía se mide.
4. **Grabación:** cada cámara escribe con su propio programa y SD, sin PC ni conexión Wi-Fi necesaria. La orden local vendrá del OBC con el formato definido por Edu. Una vez iniciada, la continuidad no debe depender de mantener una orden por radio ni del proceso de tierra. El circuito y la política frente a reset del OBC deben sostener alimentación y evitar reinicios de cámaras; todavía es una dependencia sin verificar.
5. **Supervisión:** cada unidad reporta progreso de captura y escritura, errores y espacio. Tierra interpreta los reportes recientes; si dejan de llegar muestra «estado desconocido». La autonomía de grabación continúa según la política local, aun sin enlace.
6. **Finalización y recuperación:** cerrar segmentos y registrar resultado antes de cortar energía. Acordar parada, tiempo máximo y política ante aterrizaje/falla; un corte brusco no debe invalidar todos los segmentos ya cerrados. Verificar luego las tarjetas con un lector independiente, decodificando los cuadros y buscando huecos.

La continuidad ante reinicio de cámara es un problema distinto: identificar un arranque nuevo, recuperar archivos cerrados e informar el intervalo perdido. No prometo recuperar cuadros que nunca se guardaron. El proyecto necesitará dos tarjetas para demostrar operación simultánea; las pruebas anteriores usaron una por turnos.

## Qué debe confirmar una cámara

Propongo estos conceptos para revisar con Edu; **no fijo nombres de comandos, bytes ni campos de la trama de vuelo**:

| Información por unidad | Para qué sirve |
| --- | --- |
| Identidad, arranque, misión y segmento | No mezclar una respuesta vieja con la grabación actual |
| Estado solicitado y estado observado | Separar orden enviada, aceptada, primer cuadro guardado y grabación en progreso |
| Cuadros capturados, guardados y descartados; bytes escritos | Detectar que la cámara captura pero la tarjeta dejó de progresar |
| Instante del último cuadro/escritura y contador del reporte | Detectar información detenida; no mantener un verde indefinido |
| Espacio, error de cámara/SD y motivo de reset | Explicar una interrupción en vez de un «OK» genérico |
| Segmentos cerrados e integridad comprobada | Distinguir bytes aceptados por el sistema de archivos de contenido verificado |

«Escribiendo» requiere progreso reciente de escritura; un LED, un bucle vivo o una bandera `recording=true` no alcanzan. Un CRC calculado antes de guardar tampoco acredita lectura posterior. Durante grabación evaluaré sincronización/cierre por segmentos y controles de lectura que no perjudiquen continuidad. La comprobación independiente de recuperación sigue siendo la prueba más fuerte de lo conservado; ningún reporte garantiza por sí solo todos los cuadros futuros.

Las consultas y reintentos deberán ser idempotentes: consultar no inicia otra grabación; repetir inicio no borra archivos ni crea una misión distinta sin intención; un timeout no equivale a rechazo. Definir con Edu códigos de falla y qué contadores mínimos caben en la telemetría, preservando su prioridad y cadencia. El resto puede quedar en el log local.

## Campaña para pasar de propuesta a evidencia

| Ensayo | Evidencia y criterio |
| --- | --- |
| Video con movimiento controlado | Ambas unidades, color/resolución aplicable, tiempos reales, cuadros decodificables y huecos medidos; fijar fps objetivo después de caracterizar |
| Vista previa y SD simultáneas | Cadencia, antigüedad, latencia medida con referencia, descartes, memoria y escritura; cerrar/reabrir espectador sin detener grabación |
| Funcionamiento sin notebook | Alimentación de vuelo representativa y disparador local, grabación completa y posterior lectura independiente |
| SD ausente, llena, lenta o con fallo | Error visible y localizado; no declarar grabación sana porque sigan llegando imágenes |
| Pérdida de telemetría | Estado desconocido en tierra y continuidad local comprobada después |
| Reinicio del OBC | Mantener alimentación y continuidad de cámaras con el circuito real; medir huecos, no sólo observar LEDs |
| Reset de cámara/corte de energía | Detectar nuevo arranque y segmentos incompletos; preservar lo cerrado, informar pérdidas |
| Montaje y ambiente | Ver encuadres sin obstáculos, fijación, cables/SD retenidos, luz, vibración y temperatura en condiciones definidas |
| Duración y batería | Cubrir espera, arranque, misión y margen acordado; medir corriente/picos y tensión con ambas cámaras, no inferir autonomía del USB |

Cada ensayo dejará versiones, condiciones, criterio previo, registros, resultado y límites. La estructura y el video recibidos se analizan [en una entrada separada](2026-10-27-estructura-y-banco-de-vuelo-20.md). No modifiqué firmware, RF, cableado ni archivos de vuelo para este análisis.

## Próximo bloque implementable

Primero desarrollar un candidato separado de adquisición continua y vista previa local, preservando PHOTO/SAVE y el programa probado. Medir una cámara con y sin SD antes de prometer dos flujos. Después incorporar el disparador autónomo y supervisión acordados, ensayar ambas con dos tarjetas y alimentación representativa. El control de energía se prueba con su circuito; no se simula como si fuera una medición eléctrica. Esta secuencia evita hacer depender el video del viaje de la notebook que lo muestra.
