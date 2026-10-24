# 24/10/2026 — ACTUALIZACIÓN 05: cadencia, identidad e inicio del ensayo prolongado

Diarios: [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20), [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21), [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22) y [ASTRA-34](https://astrateam2026.atlassian.net/browse/ASTRA-34). Amplío la [actualización 04](2026-10-24-reconexion-y-doble-soporte-actualizacion-04.md), que conservó el estado previo a estas cargas.

## Cadencia medida en el ESP32

Cargué la revisión con agenda de vencimientos absolutos. Verifiqué que bootloader y tabla de particiones coinciden con los anteriores y escribí sólo la aplicación en0x10000:311152bytes, hash verificado. No repetí la lectura de flash original ni cambié radio o periféricos.

Recibí una misión USB completa de131muestras. Entre primera y última transcurrieron129,985347s para130intervalos, media0,999887s; mínimo0,947197s y máximo1,041331s. La mediana fue1,017362s: no la confundo con deriva acumulada. En la revisión anterior el mismo tramo ocupaba132,573s. La agenda nueva evita sumar el tiempo de emisión a cada período; las llegadas a PC siguen teniendo jitter y esta medición no es calibración metrológica de un reloj.

[Evidencia de carga y cadencia corta](../evidence/2026-10-24-banco02/cadencia-nominal-05.json). Esta corrida todavía tenía el identificador de ejecución anterior; no le atribuyo la corrección siguiente.

## Identidad entre sesiones de PC

Al revisar el inicio del ensayo prolongado detecté que `run=seq` podía repetirse si abría otra sesión PC sin reiniciar el emisor. Conservé los resultados anteriores y cambié el banco para usar `run=client + "_" + seq`. El cliente es único por sesión PC y el anuncio identifica `run_identity=client-sequence`. La identidad de arranque sigue separada.

Compilé la corrección con CLI1.5.1/core3.3.12:311336bytes de programa y25332de variables. El intento de entrada automática falló con Wrong boot mode0x13 antes de escribir. Repetí BOOT apretado → pulsar y soltar EN/RST → soltar BOOT. La carga manual de311488bytes de imagen en0x10000 terminó con hash verificado; conservé ambos diagnósticos y artefactos anteriores.

Ejecuté dos sesiones físicas de PC consecutivas, cada una de12muestras, sin reiniciar el ESP32 entre ellas. Comprobé mismo boot y distintos run que contienen sus clientes. Cada corrida coincidió con el oráculo, sin huecos, duplicados ni rechazos; repetir RUN no volvió a ejecutarlo. Son dos pruebas cortas, no dos misiones completas ni dos horas.

[Resultado de identidad y carga](../evidence/2026-10-24-banco02/identidad-dos-sesiones-06.json). La memoria de deduplicación corresponde al cliente activo y se limpia al cambiarlo o reiniciar el emisor: no garantizo ejecución única entre clientes alternados o después de perder esa memoria. La PC no retransmite órdenes anteriores automáticamente. El [perfil actualizado](../banco-usb-v0.2/perfil-bench-usb-0.2.md) conserva la explicación y los formatos históricos.

## Tiempo monotónico y software

Agregué a cada evento el tiempo transcurrido desde el inicio del almacenamiento, medido con reloj monotónico. Conservo también UTC. Uso el primero para duración/intervalos y, cuando está disponible, para ritmo de reproducción; un ajuste de hora de Windows no debe inventar ni borrar tiempo de ensayo.

Pasaron15pruebas de software, incluidas identidad entre sesiones y reproducción que conserva ritmo pese a un retroceso de hora UTC. La prueba de duración rechaza una captura USB real de12muestras y10,969s: no acredita dos horas por tener fuente física o cantidad configurada. Los registros viejos sin marca monotónica se conservan; no les invento una.

## Ensayo prolongado iniciado, todavía sin resultado

Inicié la corrida el24/10 a00:36:19ART, desde una copia congelada del código y firmware. Pedí7261muestras a la cadencia normal y una ventana de7280s para incluir el cierre. Son algo más de dos horas reales, sin aceleración. El resultado se decidirá por duración monotónica efectivamente registrada, secuencia, archivos y GUI; esta entrada no declara aprobación.

Mantengo la GUI minimizada entre observaciones para no tapar el chat. Adquisición, archivo y callbacks siguen activos; no dejo una sesión de control de pantalla en espera. El lanzador obtiene una inhibición transitoria de suspensión por inactividad y la libera al salir; no cambia ajustes persistentes ni demuestra autonomía. Un cierre anticipado, falta de datos o error se conservará como tal.

El [analizador](../tools/resumir_usb_prolongado.py) exige captura cerrada, fuente USB, al menos7200s monotónicos entre datos, secuencia esperada, CSV equivalente, escritores drenados y ausencia de errores de la corrida nominal. Registra memoria residente, tamaños de contenedores y progreso de GUI; un intervalo superior a10s entre controles de GUI impide aprobar continuidad por este analizador. No extrapolo ausencia de fugas a tiempo ilimitado ni equiparo memoria residente a todo el heap.

[Inicio real, parámetros, fuentes congeladas y validación del analizador](../evidence/2026-10-24-banco02/inicio-prolongado-07.json). Un observador local generará el resultado al cerrar; tengo que revisarlo antes de publicar una conclusión. Esta corrida usa sólo el disco interno mientras el único USB está ocupado por el ESP32. La prueba en dos discos se conserva separadamente en la actualización04.

Siguen pendientes el resultado prolongado, causa de la ráfaga malformada de reconexión, recepción física con respaldo externo simultáneo, RF, autonomía y acuerdos con vuelo. No cierro tareas con esos criterios externos todavía abiertos.
