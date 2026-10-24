# 24/10/2026 — ACTUALIZACIÓN04: reconexión USB y respaldo en dos discos

Diarios: [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20), [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21), [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22), [ASTRA-34](https://astrateam2026.atlassian.net/browse/ASTRA-34). Continúo el [ensayoRST](2026-10-23-rst-fisico-actualizacion-03.md), conservando las entradas y capturas anteriores.

## Corte y recuperación reales

Desenchufé y volví a conectar elESP32. El receptor registró el primer error de transporte el24/10 a00:09:15,934ART y reabrió el puerto a00:09:36,329ART. Son20,395s entre observaciones, incluyendo el tiempo físicamente desenchufado; no es una medición aislada de latencia automática de redetección.

Windows informó inicialmente acceso denegado al puerto retirado; después no había un candidatoCP210x disponible. La aplicación conservó los datos y siguió abierta. Todos los controlesgui_health durante el corte mostraron ausencia de medición actual. Al volver el único candidato, un sondeo nuevoPOWER_STATUS confirmó boot `58b338f4913b33d8`, distinto del anterior. La pantalla quedó sin datos ni gráficos de la misión anterior. No pulsé botones ni recargué firmware durante esta reconexión.

Después ejecuté cero ficticio, ajuste de hora yRUN. Recibí otra misión1..131/LANDED en su propio segmento, sin huecos, duplicados ni rechazos de telemetría. Quedaron262filas de las misiones anterior y posterior al corte; no las fusioné como una sola misión. La fuente esUSB_BENCH con datos ficticios, noRF.

## Anomalía conservada

Al reabrir apareció una secuencia malformada de12899bytes hastaCR. El límite del encuadre es2048bytes: el parser registró un desborde de trama, descartó ese encuadre y recuperó el siguiente mensaje válido. No fue un desborde de cola de archivo: los escritores cerraron sin descartes ni pendientes, conservando los bytes observados en bruto. No demostré la causa de esa ráfaga ni afirmo reconexión libre de anomalías.

La misión anterior ya había terminado antes del corte; no deduzco pérdidas de vuelo a partir del período sin generación. La misión posterior sí conserva todos sus131contadores previstos.

Agregué un aviso visible de trama excesiva, separado de rechazos y pérdidas de almacenamiento. Pasaron13pruebas de software: la nueva combina trama larga, equipo ajeno, diagnóstico y una muestra válida fragmentada; verifica recuperación sin mezclarlos. El proceso que produjo esta captura todavía no mostraba el aviso nuevo, aunque registró el desborde. No atribuyo retrospectivamente el cambio a esa pantalla.

## Reproducción con salida en dos soportes

Con el únicoUSB disponible, cerré la captura delESP32 y conecté el soporte externo. Comprobé con particiones/discos: C: está en disco0/NVMe y D: en disco1/USB, no de sistema y escribible. La particiónD: mide aproximadamente15,5GB. USB no distingue por sí solo microSD con adaptador de un pendrive; registro soporteUSB y dejo ese subtipo sin confirmar. No formateé, moví ni modifiqué archivos ajenos.

Usé únicamente la carpeta nueva `D:/ASTRA_Groundstation_2026-10-24_replay_01/`, sesión `20261024T031642_848997Z_255bfdbfbbc3`. Derivé una entrada con las131tramas aceptadas de la misión posterior a reconectar, conservando sus bytes reensamblados y tiempos de recepción. La procedencia conserva huella del diario original, segmento y secuencias de eventos. No es una reproducción de todos los diagnósticos o bytes malformados de la captura completa.

EjecutéREPLAY a velocidad1 conGUI, salida localC: y respaldoD:. Los cuatro escritores(raw/CSV por destino) confirmaron todos los registros sin pendientes, errores o descartes al cerrar. AmbosCSV contienen1..131. Los tres archivos comparados de cada destino(diario,CSV y resumen) tienen huellas idénticas entreC:yD:.

Reconstruí después unCSV nuevo a partir de los dos diarios. La herramienta reunió131candidatos únicos, conservó los originales y elCSV reconstruido coincide byte a byte con elCSV guardado. No ejecuté extracción en caliente ni corte eléctrico. Tampoco huboESP32 conectado durante esta reproducción; recepción física con respaldo externo simultáneo sigue pendiente de conectividad suficiente.

## Temporización: siguiente carga preparada

La primera campaña mostró acumulación del tiempo de emisión sobre cada segundo. Preparé una agenda de vencimientos absolutos de1000ms y la identifico enhello como `fixed-deadline-1000ms`. La compilación pasó conCLI1.5.1/core3.3.12:311008bytes de programa y25324de variables. Conservo fuentes/artefactos anteriores y el respaldo original de flash.

En este corte todavía no cargué esa revisión ni medí su temporización física. Compilar no demuestra1Hz exacto sin jitter. Después de cargarla debo comprobar sus intervalos y ejecutar la campaña real de≥2hUSB conGUI/memoria medida; no la sustituyo por las reproducciones ni por tiempo de ventana abierta sin flujo.

## Evidencia y estado

- [Resultado de reconexión y anomalía](../evidence/2026-10-24-banco02/reconexion-01/resultado-reconexion-01.json), [diario normalizado](../evidence/2026-10-24-banco02/reconexion-01/journal-sin-rutas-locales.jsonl) y [CSV físicos separados](../evidence/2026-10-24-banco02/reconexion-01/segments/). Sólo retiro rutasroot de metadatos de la copia pública; conservo bytes/fechas y huella del original.
- [Dos discos, huellas, procedencia y reconstrucción](../evidence/2026-10-24-banco02/doble-soporte-04.json).
- [Entrada derivada reproducible](../evidence/2026-10-24-banco02/replay-tramas-aceptadas-entrada-04.jsonl) y [CSV de reproducción](../evidence/2026-10-24-banco02/replay-Flight_1000-04.csv).
- [Trece tests y fuentesPython](../evidence/2026-10-24-banco02/software-framing-03.json).
- [Compilación de cadencia, todavía sin cargar](../evidence/2026-10-24-banco02/firmware-cadencia-preparacion-02.json).

Quedan demostradas recuperación del puerto/contexto y otra misión completa, más escritura de reproducción en dos discos y reconstrucción equivalente. Siguen abiertos causa de ráfaga malformada, carga/temporización nueva, dos horas continuas, respaldo externo simultáneo con recepción física,RF, autonomía y acuerdos de vuelo. Mantengo las tareas en curso y continúo cada resultado en una actualización nueva.
