# 27/10/2026 — Vista Wi-Fi confirmada y siguiente etapa de grabación

[ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39) · [ASTRA-41](https://astrateam2026.atlassian.net/browse/ASTRA-41). Actualizo el [candidato de vista previa](2026-10-27-vista-previa-wifi-banco.md) y conservo sus pruebas, pendientes y configuración originales.

## Resultado físico nuevo

Pudimos activar la red de mantenimiento de cámara 1, conectar la notebook y ver su imagen en vivo dentro del Laboratorio. Esta confirmación de uso de la aplicación es evidencia de vista previa física; no es una medición de cuadros/s, latencia, consumo, estabilidad prolongada ni escritura simultánea de video. No publiqué la clave temporal ni las capturas que la muestran.

El primer intento desde la app indicó que la placa esperaba programación. Después de pulsar solamente RST, con BOOT suelto, se pudo activar la red y ver la imagen. No atribuyo el incidente a abrir/cerrar el puerto, a la base o a un botón sin aislar la causa. El arranque correcto después de la carga documentado antes se conserva como ese ensayo, no como una garantía general. La dependencia de intervención manual sigue abierta y requiere los ciclos de alimentación sin USB previstos.

Al terminar, desactivé Wi-Fi por el control USB después de comprobar identidad y recibí `wifi_off`. No cambié la conexión de red de Windows ni inicié otra red para continuar. No medí emisiones o consumo: el resultado es una desactivación reportada por el firmware, distinta de una comprobación eléctrica.

## SD después de la vista previa

Con la vista previa desactivada solicité otra secuencia CLIP de cámara 1. La operación informó doce cuadros y cierre `COMPLETE`. El programa realiza escritura y lectura con CRC en cámara; conservo su respuesta y el registro serial en una carpeta nueva. No leí esta secuencia desde el lector ni decodifiqué sus JPEG en PC, por lo que no la presento como verificación independiente. No formateé ni borré la tarjeta.

Después hice tres aperturas/consultas INFO consecutivas por USB, sin solicitar reset. Las tres respondieron con una misma identidad de arranque y cámara preparada; no apareció espera de programación. Es una comprobación breve favorable, no veinte ciclos de encendido ni aislamiento del fallo anterior. No demuestra que el problema de arranque esté resuelto.

La secuencia continúa siendo de doce cuadros. **Ver una imagen en vivo y obtener un CLIP cerrado no acredita todavía grabación autónoma continua del viaje.** Esa diferencia es central para no confundir la demostración con el criterio del PDR.

## Dos cámaras y conexión de trabajo

El candidato actual crea una red por cámara activada. Dos redes aisladas no ofrecen por sí solas una vista simultánea desde la única conexión Wi-Fi de la notebook. Además, conectarnos al punto de acceso de la cámara puede dejarnos sin el acceso habitual a Internet.

Para el uso cercano propongo un modo de mantenimiento **cliente de una red compartida**: cámara 1, cámara 2 y notebook conectadas al mismo router. Cada unidad tendrá su dirección y su identidad esperada en el Laboratorio. Esto permite conservar Internet en la PC si el router lo proporciona y la red permite comunicación entre clientes. La [API oficial de Espressif](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/wifi.html) distingue Soft-AP, donde la placa crea la red, de STA, donde se conecta a un punto de acceso existente. El modo STA compartido aún no está implementado ni probado en nuestro candidato.

Antes de usar esa opción necesito elegir una red autorizada, revisar compatibilidad/aislamiento de clientes y gestionar credenciales sin publicarlas, incluirlas en el código o guardarlas en logs. No cambiaré la configuración de la red de trabajo por iniciativa propia. Una red de laboratorio sin salida a Internet no resuelve por sí sola el inconveniente de la notebook.

La aplicación también necesita una vista dual con conexión y antigüedad independientes: el panel actual muestra una unidad seleccionada. No presentaré una cámara conectada como dos verificadas ni una sola imagen como ronda dual. Cuando el modo compartido exista, mediré la carga conjunta sobre ambas placas, red y aplicación; no duplico una tasa nominal y la llamo rendimiento medido.

## Orden del siguiente bloque

1. Desarrollar grabación continua local a SD, con duración/límites explícitos, inicio/parada idempotentes y cierre por segmentos recuperables. La cámara sigue grabando aunque no haya notebook o enlace de vista previa.
2. Conectar supervisión real de cuadros/bytes guardados, último progreso, espacio y errores al modelo ya probado. Una confirmación de inicio no reemplaza progreso; reportes vencidos quedan desconocidos.
3. Ejecutar pruebas por USB con Wi-Fi apagado mientras usamos la PC, conservando archivos y luego leyendo con lector independiente. Medir cadencia y huecos, sin crear video más rápido para simular fluidez.
4. Incorporar modo compartido y vista dual de mantenimiento en un candidato posterior; ensayar streaming y escritura simultáneos sin bloquear la grabación.
5. Verificar ambas unidades con sus SD, alimentación representativa, arranque sin botones y continuidad ante reset del computador de vuelo. Eventos y comandos de misión se acuerdan con Edu; no modifico su implementación ni parámetros RF.

El sonido sigue al final y fuera de esta etapa. La [evidencia normalizada](../../evidence/2026-10-27-camara-wifi/control-02-vista-confirmada.json) separa confirmación de la vista física, reportes de SD y límites de verificación. La cámara quedó conectada y su radio fue desactivada según su respuesta; no depende de mantener la notebook conectada a la red del banco para desarrollar el próximo bloque.
