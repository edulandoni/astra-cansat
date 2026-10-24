# bench-usb-0.2 — contrato experimental de banco

Trabajo relacionado: ASTRA-20/21/22/24/34. Lo uso exclusivamente entre el simulador USB y mi PC. No sustituye el futuro ASTRA-COMMS-ICD ni autoriza parámetros RF o comandos de vuelo.

Telemetría: los 22 campos originales de v0.1, ASCII, separados por coma, terminador CR. Modo S, TEAM1000 ficticio. No agrego metadatos a sus columnas. Diagnósticos y ROM CRLF se conservan en bruto y se distinguen de telemetría.

Control: prefijo ASCII `@BENCH `, objeto JSON compacto, terminador CR. `v` es `bench-usb-0.2`, `team` es `1000`; metadatos del emisor incluyen `boot` y `run`. `boot` cambia al reiniciar; `run` empieza idle y cambia con RUN. La identidad aleatoria tiene colisión teórica y no es autenticación. Sin CRC de aplicación ni garantías RF: el transporte actual es UART/USB.

Ejemplo ilustrativo de solicitud, que debe enviarse con CR final:

```json
{"v":"bench-usb-0.2","kind":"command","team":"1000","client":"sesion_pc","seq":1,"id":"sesion_pc:1","op":"RUN","args":{"scenario":"NOMINAL","samples":131}}
```

| Orden | Efecto sintético |
|---|---|
| RUN | Nueva ejecución, escenario y cantidad 1..100000 |
| STOP | Detengo generación; no acciona periféricos |
| CAL_ZERO | Llevo offset ficticio de altitud de 12 m a cero, sólo antes de ascenso |
| SET_TIME | Hora UTC de PC en segundos desde medianoche 0..86399, sólo antes de ascenso |
| POWER_STATUS | Consulto batería y tensión solar sintéticas; no mide ADC |

Respuestas `kind=result`, mismo `id`, `phase=accepted`, `executed` o `rejected` con motivo. Separo cola local, enviado, aceptado y ejecutado en simulación. Espero 3 segundos configurables en Engine, sin reintentos automáticos. Interrupción de transporte o arranque cambia pendientes a unknown. Una respuesta tardía se registra como tal, conservando el timeout previo en el diario. Enviar no demuestra ejecución.

El emisor memoriza 64 resultados por cliente, con secuencia creciente. Repetir exactamente el mensaje conocido devuelve el resultado sin ejecutar de nuevo; cambiar el contenido con el mismo ID rechaza ID_CONFLICT. Un ID antiguo fuera de memoria rechaza ID_EXPIRED. Tras reinicio se pierde esa memoria: la PC no reenvía pendientes automáticamente. No es un mecanismo seguro frente a clientes maliciosos ni aprobación para vuelo.

Otros metadatos: `hello` anuncia contexto; `oracle` declara por contador si se genera, omite o corrompe la muestra; `done` termina la ejecución. El oráculo sirve para contrastar el receptor con el emisor del ensayo; no certifica física ni independencia de algoritmos compartidos. Al reconectar, una consulta POWER_STATUS nueva puede recuperar contexto si se perdió el anuncio inicial. Una respuesta antigua no cambia el contexto vigente.

Modelo ilustrativo: espera 10 s, ascenso hasta 500 m en t=30 s; descenso a 15 m/s hasta 400 m (80 %), luego 5 m/s; aterrizado desde t=117 s. No representa el vector real ni prueba despliegues. IMU, GPS, presión y alimentación son señales ilustrativas, sin un modelo aerodinámico integral. Estados y separación temporal siguen siendo convenciones de banco por revisar con Edu.

Escenarios de 131 instantes: NOMINAL 131 válidos; PACKET_LOSS 13 omisiones; CORRUPTED_PACKET 10 presiones inválidas; GPS_LOSS sin fix t=50..64, última posición válida retenida; RESET omite t=60..62 y conserva contexto. Este RESET lógico es distinto del botón RST, desenchufado y caída eléctrica.

Antes de integrar vuelo necesito acordar campos y unidades, semántica de validez y estados, TEAM_ID y direccionamiento, identidad persistente de arranque/misión, comandos, confirmaciones, duplicados, CRC y perfil de radio. Todo ello permanece propuesto o TBD/TBR; no copio esta envoltura USB a RF por defecto.
