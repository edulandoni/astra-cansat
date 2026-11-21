# Banco USB bidireccional v0.2 — experimental

## Pantalla y operación

La franja superior explica si recibo datos, espero identidad, terminé o tengo un corte. Vuelo, Energía, Ubicación GPS y Movimiento agrupan las mediciones; hago clic en un nombre con ⓘ para entender su significado y unidad. Los valores del banco son ficticios aunque los envíe el ESP32 físico.

Esperando guardado cuenta muestras ya recibidas pendientes de escritura. Faltantes detectados cuenta huecos observados en la ejecución: durante un corte queda por determinar. Si vuelve otra identidad de arranque, desconozco cuántos mensajes faltaron. Conservo la última muestra como histórica y no la muestro como actual. Cerrar conexión USB no detiene necesariamente al emisor; Conectar USB reabre y comprueba identidad, sin volver a iniciar automáticamente la misión.

[Pruebas de la interfaz y de ambos tipos de corte](../docs/2026-10-25-interfaz-y-cortes-usb.md). La historia de desarrollo está en el diario; las ayudas de la aplicación explican su uso actual. Para verificar software ejecuto `python -m unittest -q test_bench test_quality test_ui`.

Desarrollo mi estación resistente a fallos en una carpeta nueva. Conservo intacto el banco v0.1 y su sketch probado. Uso TEAM `1000` ficticio y datos sintéticos: no activo radio, sensores, borneras ni mecanismos. Este banco no aprueba el ICD con vuelo.

Diario: [ASTRA-20 firmware](https://astrateam2026.atlassian.net/browse/ASTRA-20), [ASTRA-21 adquisición y recuperación](https://astrateam2026.atlassian.net/browse/ASTRA-21), [ASTRA-22 pantalla](https://astrateam2026.atlassian.net/browse/ASTRA-22), [ASTRA-34 calidad](https://astrateam2026.atlassian.net/browse/ASTRA-34), [ASTRA-24 interfaz pendiente](https://astrateam2026.atlassian.net/browse/ASTRA-24).

## Ejecución

Python 3.12, Tk incluido y `pyserial==3.5` sólo para USB. Desde esta carpeta:

```powershell
python app.py --source pc --auto-run
python app.py --port COM5 --auto-run --reset-once
python campaign.py --port COM5 --reset-once --repeat-run --output C:/EnsayosASTRA/campana
python -m unittest -v test_bench
python app.py --source replay --replay C:/EnsayosASTRA/captura/journal.jsonl --speed 2 --output C:/EnsayosASTRA/reproduccion
python recover.py --input C:/EnsayosASTRA/captura/journal.jsonl --output C:/EnsayosASTRA/reconstruido-nuevo
```

Reemplazo COM5 por el puerto comprobado. Un solo proceso puede usarlo. `--reset-once` pulsa RTS una vez: inicia un nuevo arranque y debe quedar registrado; no equivale a desenchufar ni a presionar físicamente RST. Para recibir sin reiniciar omito esa opción. La redetección posterior busca un único CP210x: con varios candidatos detengo la elección automática y debo seleccionar el puerto explícitamente al relanzar.

Para la campaña prolongada uso `--auto-run --samples 7201 --duration 7220`: el firmware sigue a 1 Hz real y la aplicación cierra después de 7220 segundos de reloj monótono. El resultado se verifica con los tiempos de los datos y `gui_health`, no con la cantidad pedida. La fuente PC también admite esa ejecución, pero no acredita flujo USB físico.

`--backup E:/ASTRA/ensayo-nuevo` agrega otro destino. Antes verifico que E: sea el soporte externo esperado y otro disco físico; dos carpetas de C: no son respaldo independiente. No formateo ni altero otros archivos. Todos los destinos generan una carpeta única de sesión. Nunca paso como salida el archivo de entrada de reproducción o un directorio reconstruido existente.

## Organización

| Archivo | Función |
|---|---|
| wire.py | 22 campos compatibles y encuadre separado de metadatos |
| mission.py | Referencia sintética y resultados previstos |
| engine.py | Contextos, contadores, calidad y órdenes |
| journal.py | Escritores independientes, colas y confirmación por destino |
| sources.py | USB, emulador PC y reproducción |
| app.py | Pantalla con 22 campos y seis gráficos simultáneos |
| campaign.py | Cinco escenarios comparados con la declaración del emisor |
| recover.py | Reconstrucción nueva y procedencia por registro |
| firmware/AstraBench02/ | Sketch nuevo; el anterior permanece en v0.1 |

## Qué significa cada dato

Separo sesión PC, arranque `boot` y ejecución `run`. Un arranque o RUN nuevo crea segmento y vacía los valores actuales. Un resultado tardío de una orden no hace retroceder ese contexto. En el perfil antiguo, un retroceso sin identidad suficiente queda ambiguo y requiere declaración explícita; no invento continuidad.

Los contadores de pantalla distinguen válidos, únicos, huecos observados, duplicados, conflictos y rechazos. Cada escritor muestra confirmados, pendientes y descartados por separado. Un hueco de contador no demuestra su causa RF. Los totales de adquisición y las cantidades por segmento están en el diario.

Cada destino tiene escritores raw y CSV separados, con 600 eventos pendientes por escritor. Un fallo provoca reintento y un archivo `.recovery-N`, conservando posibles escrituras parciales. Si la cola se agota, registro los rangos de secuencias descartadas; si superan 256 rangos, declaro incompleto ese detalle. No prometo conservación ilimitada. El registro bruto conserva bytes, comandos, metadatos y diagnósticos; éstos no se cuentan como telemetría. La GUI conserva 300 muestras y el comparador 4096 huellas: un contador antiguo fuera de la ventana queda no verificado, no se inventa una comparación.

Confirmado significa escritura, `flush` y `fsync` completados; no certifica supervivencia a un corte eléctrico. Un error posterior a escritura parcial puede dejar duplicados inciertos: uso recuperación para reconciliarlos.

La edad de enlace y la edad de medición son independientes. GPS_SATS=0 indica sin solución sólo en este banco; mantengo posición anterior identificada y su edad. La constancia de un sensor no acredita avería. Advierto reloj congelado si avanza el contador con hora repetida. Muestro giro en rad/s convirtiendo explícitamente los °/s del perfil conocido; conservo los 22 valores originales en CSV. Otro perfil necesita unidades acordadas.

## Recuperación y reproducción

Acepto diarios JSONL y CSV dentro del árbol original `sesion/segments/segmento/Flight_1000.csv`. No asigno una identidad inventada a un CSV aislado. Combino por sesión, segmento, equipo y contador; reúno procedencia y bloqueo toda escritura de CSV reconstruido si hay conflicto o error de lectura. Sólo recupero datos presentes; nunca relleno pérdidas. Conservo huellas y originales. La herramienta es offline y puede usar memoria proporcional a los registros.

La reproducción genera una sesión y archivos nuevos, queda marcada REPLAY y no envía órdenes. La velocidad 1 respeta los intervalos registrados; un factor mayor acelera sólo reproducción. No acredita tiempo real de misión, RF ni hardware.

## Firmware y perfil

[Contrato exclusivo del banco](perfil-bench-usb-0.2.md). Compilado y cargado con Arduino-ESP32 3.3.12 / CLI 1.5.1, ESP32 clásico, DIO 40 MHz, flash 4 MB, carga 115200. Usa cJSON incluido en ESP-IDF. El original de la flash quedó conservado privadamente antes de la primera carga; no se publica ni se declara restauración probada.

Si falla entrada automática a programación: mantengo BOOT, pulso y suelto EN/RST, suelto BOOT y cargo sin nuevo reset previo. La luz no demuestra por sí sola modo ni recepción. Para correr después de programar uso EN/RST o el reinicio explícito de banco.

Resultados, límites y evidencia: [primera actualización de esta etapa](../docs/2026-10-23-banco02-actualizacion-01.md). Los ensayos pendientes continúan en entradas nuevas.

## Uso sin tapar el chat — 24/10/2026

`--start-minimized` deja la ventana en la barra de tareas y mantiene adquisición, archivo y actualizaciones de Tk activos. `Ctrl+M` minimiza la ventana del banco sin enviar órdenes al ESP32. Al terminar una inspección vuelvo al chat actual para mantener visibles las preguntas y maniobras pendientes. Una ventana minimizada no demuestra por sí sola que la GUI siga respondiendo: lo compruebo con observaciones y el registro `gui_health`.

## Conflictos de recuperación — 24/10/2026

Además de comparar filas entre copias, bloqueo reconstrucción si un diario seleccionado conserva una marca de conflicto detectado durante adquisición. Un CSV aislado no revela marcas que sólo quedaron en un diario ausente. [Caso antes/después](../docs/2026-10-24-recuperacion-conflicto-interno-actualizacion-08.md).

## Aceptación USB — 24/10/2026

[Resultado prolongado y matriz de toda la etapa](../docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md): 7261 paquetes en 7260,328 s reales entre primera y última muestra, escritores drenados y reconstrucción idéntica. El informe conserva el intento interrumpido, las versiones y los pendientes de RF/autonomía/STM32 y copia externa simultánea.

## Calidad y guardas — 24/10/2026

La pantalla avisa GPS sin actualizar aun con satélites declarados, siempre que la telemetría general siga fresca. Configuro edades con `--data-stale-seconds 3 --gps-stale-seconds 3`; son umbrales de banco, no de vuelo. [Métricas y captura](../docs/investigacion/2026-10-24-calidad-medida-y-cierre-investigacion.md) · [Prueba USB de órdenes inválidas](../docs/2026-10-24-ordenes-negativas-usb.md). Pruebo con `python -m unittest -v test_bench test_quality`.
