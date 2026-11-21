# 23/10/2026 — Propuesta para revisar con Edu

Diario: [ASTRA-24](https://astrateam2026.atlassian.net/browse/ASTRA-24). Amplío [los pendientes de interfaz](pendientes-groundstation-2026-10-19.md). Preparé y probé mi extremo USB experimental; todavía no ejecuté interoperabilidad STM32 ↔ ESP32/SX1276. Esta propuesta no aprueba el ICD compartido.

Quiero que ambos extremos entiendan lo mismo cuando reciben un dato o una orden. El ICD es ese acuerdo escrito: qué bytes mandamos, qué significan, cómo identificamos equipo/misión, qué hacemos si faltan y cómo sabemos si una orden se ejecutó. Lo que falta acordar queda TBD; lo que ya tiene una propuesta pero necesita revisión queda TBR.

## Datos y unidades por acordar

Mantengo un perfil compatible de 22 campos para poder probar ahora. La [comparación v1/v2](../requisitos/v1-v2-groundstation-2026-10-19.md) conserva que el formato detallado v1 no aparece como obligación en v2. Debemos confirmar contenido y semántica final, no adoptar columnas sólo por herencia.

| Campos del banco | Unidad / significado actual | Revisión necesaria |
|---|---|---|
| TEAM_ID | 1000 ficticio | ID real, ubicación y direccionamiento TBD |
| MISSION_TIME | HH:MM:SS UTC ajustada a PC | Fecha, precisión, sincronización y persistencia TBD |
| PACKET_COUNT | Entero creciente por RUN | Rollover, alcance y persistencia TBD |
| MODE / STATE | S y estados ilustrativos | Estados de vuelo/eventos reales TBR |
| ALTITUDE | m AGL, offset calibrable ficticio | Referencia, cero y validez TBR |
| TEMPERATURE / PRESSURE | °C / kPa | Resolución, frecuencia y estado sensor TBR |
| VOLTAGE / CURRENT | V / A sintéticos | Punto de medida, rango y validez TBD |
| GYRO_R/P/Y | °/s en wire heredado; rad/s en pantalla | Ejes, referencia corporal y SI de wire TBR |
| ACCEL_R/P/Y | m/s² ilustrativos | Ejes, gravedad incluida/retirada TBD |
| GPS_TIME/ALTITUDE/LATITUDE/LONGITUDE/SATS | UTC / m MSL / grados / conteo | Datum, precisión, edad y fix explícito TBD |
| CMD_ECHO | NONE heredado | Confirmación final por ID y resultado TBR |

No uso cero como sinónimo universal de error. Propongo calidad por medición: valor, instante de medición, validez y motivo; la hora de recepción PC se guarda aparte. Una última posición válida sigue siendo histórica cuando se pierde fix. Mensajes de diagnóstico se conservan aparte y no incrementan telemetría. No aseguro sincronización de reloj a partir de recibir una orden.

## Identidad y reinicios

Propongo separar sesión PC, arranque del emisor y misión. En USB tengo boot aleatorio/run; para vuelo falta acordar generación, persistencia y reset del contador. Un retroceso sin contexto suficiente se trata como ambiguo. No quiero que una reconexión convierta automáticamente una muestra vieja en dato actual.

## Órdenes y confirmaciones

En [bench-usb-0.2](../../banco-usb-v0.2/perfil-bench-usb-0.2.md) ensayé RUN/STOP, calibración ficticia, hora y consulta sintética de alimentación. Sólo preparan el receptor y la pantalla. Propongo discutir ID único, recibido/aceptado/ejecutado/rechazado, resultado desconocido tras corte, deduplicación, expiración y límites de reintento. La confirmación de ejecución debe provenir del extremo que ejecuta, no del botón de la GUI.

El banco espera3s y no reenvía automáticamente. Ese timeout no queda seleccionado para vuelo: depende de airtime, turno, latencia y estado del sistema. Tampoco doy por aprobado el JSON de USB para radio. El payload solar de banco es un mensaje separado, no una medición física ni una nueva columna acordada.

## RF y separación de equipos

Eliminar NetID heredado no habilita broadcast. Poner TEAM_ID al comienzo permite rechazar datos ajenos en nuestra aplicación, pero no impide que una antena reciba físicamente energía de otros transmisores ni resuelve por sí solo acceso al canal. Debemos acordar identificación, destino, Sync Word, filtrado y política de telecomandos con Edu conforme a CONAE y al módulo real. No configuro ninguno unilateralmente.

Frecuencia exacta, LoRa/FSK/GFSK, BW/bitrate, potencia, CRC, Sync Word, red/direcciones y parámetros de enlace: TBD/TBR en el Radio Profile compartido. No activo Wi-Fi/Bluetooth como sustituto de este acuerdo.

## Ensayo conjunto propuesto

1. Fijar versión de ICD y juego de mensajes de ejemplo válidos/ inválidos.
2. Comparar bytes recibidos, unidades y contadores con el origen; probar fragmentación, diagnósticos y equipos ajenos.
3. Ejecutar órdenes duplicadas, inválidas, tardías y sin respuesta; medir tiempos reales de cada extremo.
4. Reiniciar/desconectar cada extremo por separado; verificar identidad, pendientes y que la pantalla conserve el histórico sin hacerlo actual.
5. Integrar RF sólo después del acuerdo y conservar perfil, versiones, capturas y resultados en ambas áreas.

Esta lista es propuesta, no trabajo asignado a Edu ni prueba realizada. Mi extremo USB ya permite preparar esos casos. La tarea continúa abierta por integración y acuerdo externos.
