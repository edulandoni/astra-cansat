# 23/10/2026 — ACTUALIZACIÓN: primera misión completa desde el ESP32 físico

Continúo la [preparación y secuencia BOOT](2026-10-23-banco-esp32-usb.md), que conservo. Diarios: [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20), [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21) y [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22). La preparación anterior estaba compilada y pendiente de carga: esta entrada agrega los resultados físicos posteriores.

## Respaldo y carga

Repetí BOOT apretado → pulsar y soltar EN/RST → soltar BOOT. La conexión volvió a funcionar sin reinicio automático. Repetí la lectura completa a 115200 baudios: terminó correctamente en 383,1 segundos y guardó 4.194.304 bytes. Conservo el archivo local `flash_original_intento03.bin`, SHA-256 `a312ead25e36d3ab004b4fea46efae0fa43274c45631514b6cac47b30e809472`, en Descargas/06 Documentos/CanSat_Universitario/2026-10-23_banco_esp32_usb_01. No sustituye un respaldo en disco independiente ni acredita una restauración efectiva. No publico el binario original.

Cargué los cuatro componentes compilados del simulador a 115200 baudios. Esptool terminó correctamente y verificó las cuatro escrituras por hash. No solicité un borrado completo de flash. El sketch sigue sin cambios, con SHA-256 `1e0d78499cb05bbae38c07a2655b37c75c9519cc7bbf4ddcac56de571d9d0c81`; se conserva la configuración Arduino CLI 1.5.1 / Arduino-ESP32 3.3.12, DIO, flash a 40 MHz y capacidad de 4 MB. Esos 40 MHz son del acceso a la flash, no una frecuencia de radio. [Procedencia, direcciones y huellas de los archivos de entrada](../evidence/2026-10-23-esp32-usb/respaldo-carga-02.json).

El resultado muestra que esta lectura a menor velocidad funcionó; no identifica por sí solo la causa física del fallo del intento anterior. Conservo los errores anteriores como parte del diario.

## Primera captura USB sin pantalla

Ejecuté el capturador con COM5, 115200, TEAM_ID ficticio 1000, escenario NOMINAL, reinicio EN/RTS y ventana de captura de 137 segundos. La sesión comenzó el 23/10 a las 21:53:09 ART y terminó a las 21:55:27 ART. El reinicio y preparación agregan tiempo a la ventana de captura; no son un corte de alimentación.

Recibí 131 paquetes únicos, contadores 1–131, cero duplicados, cero huecos observados, cero rechazos y cero desbordes de framing. No se informaron errores de captura ni de archivo. Recorrí LAUNCH_PAD → ASCENT → APOGEE → DESCENT → PROBE_RELEASE → PAYLOAD_RELEASE → LANDED. El intervalo de llegada mediano fue 1,000 s, mínimo 0,891 s y máximo 1,109 s, medidos desde la PC; no es una medición de latencia RF ni calibración del reloj del micro.

Conservo el [resultado](../evidence/2026-10-23-esp32-usb/nominal-01/resultado.json), el [Flight_1000.csv](../evidence/2026-10-23-esp32-usb/nominal-01/Flight_1000.csv), los [131 eventos de telemetría recibida](../evidence/2026-10-23-esp32-usb/nominal-01/recepcion-telemetria.jsonl) y sus [huellas](../evidence/2026-10-23-esp32-usb/nominal-01/manifest-publico.json). Los bytes originales USB, los eventos de arranque completos y la flash original permanecen en la copia local. La copia pública excluye el binario de arranque y sus eventos; no modifica los originales.

## Qué encontré al abrir la pantalla

La primera sesión de la GUI recibió datos y graficó, pero empezó en el contador 2 y registró siete rechazos. Revisé el arranque: el texto de diagnóstico y su CR/LF llegaban al parser de telemetría, contaminando también la primera muestra. No lo atribuyo a pérdida RF. Esa sesión conserva 76 muestras, contadores 2–77; la cerré voluntariamente para probar la corrección. No fue una misión completa ni un ensayo de interrupción de enlace.

Agregué la opción explícita `--bench-reset-once` a la pantalla y la adquisición. Sólo para el sketch conocido: reinicio EN/RTS una vez al conectar y conservo los primeros 0,5 segundos de arranque como eventos `startup_window`, fuera del parser. Ese sketch empieza a emitir al segundo; si cambia esa condición hay que revisar la ventana. El parser estricto y el formato no cambian. Sin la opción, el receptor conserva su comportamiento normal: no activo este descarte ni este reinicio de banco. En una reconexión no repito deliberadamente el reinicio de la opción; esto no elimina los posibles efectos de DTR/RTS del sistema/controlador, que requieren ensayo físico separado.

Abrí una sesión nueva con la opción y comprobé visualmente COM5, datos recientes, tablas y gráficos. La segunda sesión guardó los contadores 1–131 y llegó a LANDED con cero rechazos, duplicados o huecos observados. [CSV y resultado comparativo de la GUI](../evidence/2026-10-23-esp32-usb/gui-02/resultado.json) · [CSV](../evidence/2026-10-23-esp32-usb/gui-02/Flight_1000.csv). La copia corresponde al corte de esa sesión; la ventana permanece abierta. El sketch deja de emitir después de sus 131 muestras, por lo que luego aparece la indicación de datos antiguos: no lo interpreto automáticamente como falla de enlace.

Pasaron once pruebas con `python -m unittest -v test_ground test_usb_startup`: las nueve existentes y dos nuevas sobre conservación del arranque, reinicio opcional y no repetición del reinicio al reconectar. Las pruebas de reconexión usan un puerto simulado; no acreditan una desconexión física del USB.

Para repetir desde una terminal con las dependencias instaladas, dentro de `banco-usb-v0.1/`:

```powershell
python app.py --port COM5 --team 1000 --bench-reset-once
```

Para conservar cada ejecución con sus contadores desde el inicio, cierro la sesión y abro una nueva. No abro simultáneamente otro monitor del mismo puerto. Esta opción es de banco, no un comando para el vehículo ni configuración para el gateway RF.

## Observaciones de la luz

Al conectar inicialmente observé una luz azul fija. Después del procedimiento BOOT/EN observé que se apagó, encendió aproximadamente medio segundo y volvió a apagarse; al repetirlo vi el mismo comportamiento. Durante la nueva lectura volvió a quedar fija. Durante la recepción de la misión observé que empezó a titilar. Conservo [la secuencia inicial](../evidence/2026-10-23-esp32-usb/observaciones-led-02.json) y [la observación posterior](../evidence/2026-10-23-esp32-usb/observaciones-led-03.json). Son observaciones visuales aproximadas: no identifiqué el circuito del LED ni acredité correspondencia entre destellos y paquetes.

## Qué puedo afirmar y qué queda pendiente

Puedo afirmar que esta placa ejecutó el simulador cargado y entregó por USB una misión sintética completa, que el parser la aceptó y que el CSV se guardó. También comprobé la pantalla con una segunda misión sintética completa después de corregir su inicio de banco.

No son mediciones reales de altitud, GPS, presión, IMU o batería. No probé SX1276, antena, alcance, RF, autonomía de dos horas, corte de alimentación, restauración de la flash original o respaldo en disco independiente. TEAM_ID 1000 y los 22 campos siguen siendo convenciones experimentales heredadas; no constituyen un ICD aprobado ni formato obligatorio de CONAE v2. Las borneras y su mapa eléctrico permanecen sin usar ni verificar.

Quedan ensayos físicos de escenarios de fallo, reconexión, reinicio y recuperación de sesión, además del trabajo de interfaz acordado con vuelo. Mantengo las tareas en curso; esta evidencia no cierra todos sus criterios.
