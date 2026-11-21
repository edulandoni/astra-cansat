# 21/10/2026 — COSMOS 2025: CSV publicado y estación de tierra

Diario: [ASTRA-35](https://astrateam2026.atlassian.net/browse/ASTRA-35). Continúo los antecedentes sin reemplazar el [caso DJS](2026-10-20-djs-arya-vuelo-y-recuperacion.md). Esta pasada profundiza una ficha; no ejecuté código ajeno ni cambié el software de ASTRA.

## Fuentes y alcance

Revisé README, GCS/Flight_3195.csv y GCS/communication.py del [repositorio publicado por sus autores](https://github.com/BarrettT123/CanSat-Team-Cosmos-Software/tree/5f33675e6a7439da6f12d4411a9cb3b0d64353b9), fijado en `5f33675e6a7439da6f12d4411a9cb3b0d64353b9`. El repositorio es un fork y presenta a COSMOS/team 3195 como edición AAS 2025. No verifiqué aquí su puesto con el organizador ni certifico que ese commit exacto voló. El CSV es evidencia publicada por el equipo, sin cadena independiente que garantice captura completa o sensores calibrados.

## Qué medí en el archivo

Con un análisis propio de sólo lectura conté 525 filas de datos y 26 columnas; todas las filas indican modo F. PACKET_COUNT va de 418 a 1031, sin duplicados ni retrocesos. Hay 22 saltos hacia adelante: faltan 89 identificadores dentro de las 614 posiciones de ese intervalo. Esto describe huecos del archivo; no es una tasa de pérdida RF medida. Pueden intervenir recepción, guardado, recorte u otras causas que este CSV no permite separar.

Los estados son LAUNCH_PAD 473, ASCENT 3, APOGEE 7, DESCENT 14, PROBE_RELEASE 24 y LANDED 4. GPS_SATS, coordenadas y AUTO_GYRO_ROTATION_RATE son cero en todas las filas. El cero puede ser marcador de ausencia o un valor del circuito de adquisición: no lo convierto en posición válida, rotor detenido ni prueba de generación. La altitud máxima de la columna es 616,2; no certifica altura física real ni precisión.

Las [métricas y huella](2026-10-21-cosmos-metricas.json) permiten reproducir conteos. Para repetirlos uso csv.DictReader, convierto PACKET_COUNT a entero y sumo max(siguiente−anterior−1,0) en pares consecutivos; compruebo retrocesos/duplicados por separado. SHA-256 del CSV: `ef63242c60000adaeeec81f40d5ba03b1629907390191d38e13909e3e2f3a276`. No republico el CSV completo ni coordenadas.

## Qué muestra el módulo, sin ejecutarlo

En [communication.py](https://github.com/BarrettT123/CanSat-Team-Cosmos-Software/blob/5f33675e6a7439da6f12d4411a9cb3b0d64353b9/GCS/communication.py), read() busca el terminador COSMOS, incrementa receivedPacketCount antes de parsear y escribe la línea dividida en CSV. parse_csv_data() separa por comas y conserva las últimas veinte entradas; en esa función no valida todos los campos. Por eso recibido y válido no son equivalentes.

flush_csv() abre y cierra otro manejador, mientras read() mantiene el suyo abierto. La lectura estática no demuestra que esa llamada vacíe el buffer del escritor activo; no hice una prueba de corte ni afirmo que perdieron datos en vuelo por esto. En comandos, _write_serial() captura errores y puede retornar sin confirmación al llamador; send_commands() registra envío tras llamar al método. Una cola procesada o un mensaje de log no demuestra recepción ni ejecución a bordo.

## Captura visual inspeccionada

Abrí la [captura groundstation.png](https://raw.githubusercontent.com/BarrettT123/CanSat-Team-Cosmos-Software/5f33675e6a7439da6f12d4411a9cb3b0d64353b9/groundstation.png). Es una captura de GUI identificada COSMOS/team 3195, no una foto del equipo físico. Muestra estado LANDED, gráficos, controles SIM/CSV y varios valores GPS ausentes. Su contador de recibidos muestra 958 y el CSV consultado tiene 525 filas: no pruebo que sean la misma sesión completa ni atribuyo la diferencia a pérdida. El gráfico visible conserva un tramo de descenso; no acredita por sí solo todo el vuelo.

La registro como F10 en el [suplemento visual](2026-10-21-catalogo-visual-cosmos.csv). Crédito: repositorio de COSMOS; creador individual de la imagen y licencia de reutilización no confirmados. Conservo el enlace y no copio el binario a GitHub/Drive.

## Qué propongo para nuestra área

Este caso vuelve concreta la necesidad de distinguir contador embarcado, recibidos, válidos y guardados, además de última posición válida y antigüedad. Me interesa preparar pruebas con huecos antes y durante ascenso, GPS ausente y confirmación real de escritura/comandos. Son propuestas relacionadas con ASTRA-34/21/24, no ensayos nuevos ni decisión del ICD. No copio su identificador, comandos, baudrate o parámetros extranjeros a CONAE. No infiero electricidad generada por un campo de giro o una imagen.
