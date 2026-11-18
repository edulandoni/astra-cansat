# ACTUALIZACIÓN — Nuestra contribución al PDR, 17/11/2026, versión 2

ASTRA-24 / ASTRA-22 / ASTRA-25 / ASTRA-39 / ASTRA-40. Redacté 23 diapositivas en la familia visual de la plantilla oficial archivada; no reemplazo el aporte de apoyo publicado anteriormente. El original editable y las figuras de fabricantes están en Drive, fuera del repositorio público.

## 1. ASTRA ground segment — PDR contribution

Criterio de plantilla: GS. Design baseline and verification status · 17 November 2026

| Contribution | Deck pages | Official template items |
| --- | --- | --- |
| Ground control system | 2–9 | 69–74 |
| Telemetry, commands and RF timing | 10–12 | 53–56; support to C&DH |
| Camera trade, recording and supervision | 13–16 | 28–31; support to payload |
| Evidence and verification plan | 17–21 | 76, 77, 79; support to I&T |
| Closure checklist and source register | 22–23 | Cross-cutting dependencies |

Design proposals are identified. Bench results are not presented as flight qualification.

Notas para exposición:

Esta es nuestra contribución editable, no el PDR completo del equipo. Mantiene la familia visual de PDR Template V2 y sus números de criterio. Las páginas indicadas son internas a este aporte; al integrarlo se renumera el índice general. Las diapositivas 2–16 contienen el diseño y 17–23 pueden usarse como respaldo. La plantilla oficial y Scoresheet V2 son las copias archivadas el 19/10; su disponibilidad actual detrás del aula no pudo revalidarse. No afirmamos que el equipo haya aprobado las propuestas abiertas.

Fuentes:

- [O1](https://educacion.conae.gov.ar/aulavirtual/course/view.php?id=106)
- [O2](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/aula/2026-10-19/mapa-pdr-groundstation.csv)
- [D1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/pdr/2026-11-17/Interfaz_para_completar_con_Edu.json)

## 2. GCS overview

Criterio de plantilla: 69. Proposed flight-to-ground architecture · RF integration pending

Telemetry is received over RF; flight video remains on two independent camera cards.

Notas para exposición:

El OBC STM32 y la radio de vuelo pertenecen al diseño compartido con Edu. Nuestra propuesta usa una pasarela ESP32 con SX1276 y USB hacia la notebook. Lo comprobado es el banco USB con datos sintéticos, no la cadena RF STM32–radio–tierra. Cada cámara conserva su propio registro local. Wi-Fi es mantenimiento cercano y no se usa como garantía de enlace durante el descenso. La ausencia de enlace con tierra no debe detener la grabación, pero esa condición sobre alimentación de vuelo sigue pendiente de ensayo.

Fuentes:

- [E1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md)
- [E3](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/historial/2026-10-26-laboratorio-completo-04.md)
- [E5](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/camaras/2026-10-27-grabacion-segmentada-y-supervision-usb.md)
- [D1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/pdr/2026-11-17/Interfaz_para_completar_con_Edu.json)

## 3. GCS components and connections

Criterio de plantilla: 70. Interface inventory · implemented USB path and proposed RF gateway

| Component / connection | Role and interface | Status / closure |
| --- | --- | --- |
| Flight OBC → flight radio | SPI, IRQ, reset; final pins and levels from Edu | Shared design; pinout not frozen |
| Flight radio ↔ ground radio | LoRa at a proposed 915 MHz carrier | Profile / addressing / antennas open |
| Ground radio → ESP32 | SPI plus interrupt and reset lines | Proposed; module revision to confirm |
| ESP32 → PC | USB serial → acquisition / decoder | USB bench physically exercised |
| PC → two storage destinations | Original journal, CSV, health and manifest | Software supported; independent-media mission test open |
| Camera 1 / camera 2 | Own microSD; proposed OBC control / health return | Two still-photo units; recording proof on camera 1 |

No final RF pin mapping is claimed before the exact radio module and shared ICD are confirmed.

Notas para exposición:

Los módulos informados son SX1276/915 MHz; no se debe cablear por intuición porque hubo diferencias entre fotos y documentación del módulo. La placa de desarrollo y el módulo de radio no comparten necesariamente tolerancia a 5 V. Verificar tensión de lógica, regulación, desacople, IRQ y RESET contra la revisión física antes del montaje. Dos carpetas en un mismo disco no son dos medios independientes. El receptor mantiene trazabilidad de fuentes y errores; los binarios originales de terceros y datos privados no se publican en GitHub.

Fuentes:

- [E1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md)
- [E2](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/2026-10-25-interfaz-y-cortes-usb.md)
- [D1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/pdr/2026-11-17/Interfaz_para_completar_con_Edu.json)

## 4. Ground antenna trade

Criterio de plantilla: 71. Two manufacturer-documented candidates · 902–928 MHz, linear polarization

| Criterion | Taoglas TI.92.2113 | Taoglas OMB.915.B05F21 |
| --- | --- | --- |
| Configuration | Hinged terminal dipole, SMA male | Outdoor omnidirectional, N female |
| Published peak gain | 1.21 dBi straight; 2.14 dBi bent | 5.9 dBi |
| Length / mass | 198 ± 3.3 mm / 22.5 g | 1,094 ± 30 mm / 500 g, plus 70 g mount |
| Pattern evidence | Datasheet pp. 8–9; position-dependent nulls | Datasheet p. 8; plane-dependent lobes / nulls |
| Operational trade | Compact, lower setup and cable burden | Higher peak gain; larger support and wind load |
| PDR proposal | First portable prototype candidate | Alternative for a fixed ground mount |

Peak gain is not gain in every direction. Neither candidate has been tested on ASTRA.

Notas para exposición:

Comparamos dos modelos concretos, no dos rótulos genéricos. TI.92: ficha SPE-19-8-076/A del 12/06/2019, tabla p.4 y patrones pp.8–9. OMB: SPE-22-8-119-A del 02/08/2022, patrón p.8. La página comercial de TI.92 muestra otra cifra máxima; para este análisis usamos los valores y la configuración de la ficha versionada. La propuesta de selección es de diseño y debe contrastarse con las antenas que ya tiene el equipo, los conectores y disponibilidad. No es una orden de compra ni una decisión del enlace de vuelo.

Fuentes:

- [M1](https://www.taoglas.com/datasheets/TI.92.2113.pdf)
- [M2](https://www.taoglas.com/datasheets/OMB.915.B05F21.pdf)

## 5. Antenna radiation patterns

Criterio de plantilla: 71. Manufacturer reference at approximately 915 MHz · not ASTRA measurements

Match the datasheet axis system and physical orientation before using a directional gain in a link budget.

Notas para exposición:

Extractos de figuras de Taoglas, conservados con crédito y enlaces al original para la revisión técnica de este PDR. Arriba: TI.92.2113 recta, p.8. Abajo: OMB.915.B05F21, p.8. Las escalas y ejes son los del fabricante; no están normalizados entre modelos ni medidos por nosotros. No interpretar el término omnidireccional como cobertura esférica uniforme. La posición articulada de TI.92 tiene otro patrón, en p.9 del original, y también debe evaluarse si se usa esa geometría. Los originales y extractos no forman parte del repositorio público.

Fuentes:

- [M1](https://www.taoglas.com/datasheets/TI.92.2113.pdf)
- [M2](https://www.taoglas.com/datasheets/OMB.915.B05F21.pdf)

## 6. Ground antenna mounting design

Criterio de plantilla: 72. Portable, restrained tabletop / tripod concept · dimensions to be confirmed

Place the antenna away from the operator, laptop and metal; document the tested orientation.

Notas para exposición:

Este es un esquema conceptual propio, no un plano mecánico construido ni una medición. Proponemos fijar el terminal en un soporte no conductor con alivio de tracción del coaxial, base estable y zona libre para el operador. El receptor y el USB se mantienen próximos a la PC; el cable RF debe ser tan corto como resulte compatible con la separación y la estabilidad. La mesa o trípode, soportes y lastre reales deben dimensionarse con la antena definitiva. Comprobar el conector de cada extremo: TI.92 es SMA macho y OMB es N hembra; el adaptador y sus pérdidas no se presuponen cero. Antes del campo: inspección mecánica, movimiento del cable, viento y repetibilidad de orientación.

Fuentes:

- [M1](https://www.taoglas.com/datasheets/TI.92.2113.pdf)
- [M2](https://www.taoglas.com/datasheets/OMB.915.B05F21.pdf)
- [E7](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/interfaces/2026-10-24-enlace-destinos-y-revision.md)

## 7. Antenna selection and link-budget closure

Criterio de plantilla: 73. Preliminary choice: TI.92 portable prototype · final hardware selection pending

| Decision / calculation | Rationale or value | Remaining evidence |
| --- | --- | --- |
| Portable candidate: TI.92 | Small size, low mass, no active pointing | Connector compatibility and field comparison |
| Fixed alternative: OMB | Higher published peak gain | Mount size, cable losses and angular coverage |
| Free-space loss illustration | 915 MHz, 1 km slant range → 91.676 dB | Actual geometry and RF profile |
| Received-power model | Ptx + Gtx(θ) + Grx(θ) − cable / path / other losses | Directional gains, polarization and installation losses |
| Link margin | Received power − sensitivity at selected profile | Unknown for ASTRA; no guaranteed range claimed |

A higher spreading factor changes airtime and sensitivity; it does not change the carrier frequency.

Notas para exposición:

La selección preliminar favorece portabilidad y una primera campaña controlada. Debe cambiar si el inventario real, ensayo o geometría indican otra solución. FSPL = 20 log10(4πdf/c), c=299792458 m/s, d=1000 m, f=915e6 Hz. No es la altura por sí sola: se usa distancia oblicua. El margen real exige potencia, sensibilidad del mismo SF/BW, ganancias en los ángulos de operación, cables, polarización, obstáculos y margen objetivo. No trasladar un ejemplo teórico al alcance garantizado del CanSat.

Fuentes:

- [M1](https://www.taoglas.com/datasheets/TI.92.2113.pdf)
- [M2](https://www.taoglas.com/datasheets/OMB.915.B05F21.pdf)
- [E7](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/interfaces/2026-10-24-enlace-destinos-y-revision.md)

## 8. GCS software prototype

Criterio de plantilla: 74. Native Qt application · explicit PC simulation shown, no hardware connected

22 telemetry fields and 11 plots. Source, freshness, packet counters and recording health remain visible.

Notas para exposición:

Captura nueva del Laboratorio Qt actual, obtenida fuera de pantalla con el emisor sintético de PC. No es una foto de recepción RF ni de sensores físicos. Python y PySide6/Qt Widgets, adquisición y almacenamiento reutilizan el motor de banco. Los datos se actualizan desde una fuente elegida explícitamente: USB, simulación de PC o reproducción. No hay datos sintéticos de reemplazo cuando se pierde un enlace real. Hay once gráficas para quince canales numéricos; ejes de IMU se agrupan. Todas las variables disponibles pueden verse en la tabla con su condición. Falta ensayo de legibilidad exterior a pleno sol.

Fuentes:

- [E3](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/historial/2026-10-26-laboratorio-completo-04.md)
- [https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/laboratorio/qt_app.py](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/laboratorio/qt_app.py)

## 9. Acquisition, quality and recording

Criterio de plantilla: 74. Implemented separation of responsibilities · independent backup is a field-test gate

Retained values become historical; graph segments do not bridge counter gaps or different sessions.

Notas para exposición:

La recepción conserva los bytes originales y el diario de eventos, clasifica trama y perfil, valida campos y actualiza las vistas sin bloquear el registro. El CSV es una salida derivada; el original y la procedencia permiten reconstruir y comparar. Los contadores recibidos, inválidos, saltos observados, duplicados y errores de escritor son conceptos diferentes; un salto observado no permite inferir todas las pérdidas después de un reinicio. La recuperación no inventa muestras faltantes ni resuelve conflictos silenciosamente. Preparar Flight_<ID>.csv y una copia en medio independiente para los jueces; ID definitivo y semántica final se ajustan al ICD. Entrega práctica: CSV legible, diario, manifest, versiones y explicación de límites.

Fuentes:

- [E1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md)
- [E2](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/2026-10-25-interfaz-y-cortes-usb.md)
- [E3](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/historial/2026-10-26-laboratorio-completo-04.md)

## 10. Command transmission and verification

Criterio de plantilla: 56. Bench commands implemented · flight command encoding awaits the shared ICD

| Function | Implemented bench behavior | Flight closure / verification |
| --- | --- | --- |
| Altitude zero | CAL_ZERO transaction and returned result | Define reference and allowed states; verify resulting altitude |
| UTC setting | SET_TIME with validated time argument | Define clock source / persistence; compare reported UTC |
| Power / solar status | POWER_STATUS response in bench profile | Define measured channels, units and validity |
| Run / stop | RUN and STOP for test source control | Not flight arming / deployment commands |
| Execution confirmation | Accepted / executed / rejected; request identity | Agree response fields, deadlines and duplicate handling |
| Roll / pitch calibration | No verified flight implementation | Only include if required by actual sensor / approved interface |

An ACK of receipt is not proof of execution. Replayed data cannot transmit commands.

Notas para exposición:

No mostramos un formato de órdenes de vuelo inventado para completar la plantilla. El banco usa prefijo @BENCH y JSON perfil bench-usb-0.2; es un protocolo experimental y está separado del ICD de vuelo. Flujo previsto: operador valida destino y estado, emite solicitud identificada, obtiene aceptación y luego resultado o timeout; verificar en telemetría el efecto físico o de configuración. Cero altimétrico debe comprobar la referencia y su persistencia; hora UTC debe contrastarse con una referencia. La plantilla menciona roll/pitch: no asumir que gyro en rad/s sea ángulo de orientación ni fingir una calibración inexistente. La gestión de comandos críticos debe acordarse con Edu, sin accionar mecanismos desde este trabajo.

Fuentes:

- [E3](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/historial/2026-10-26-laboratorio-completo-04.md)
- [D1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/pdr/2026-11-17/Interfaz_para_completar_con_Edu.json)
- [https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/banco-usb-v0.2/wire.py](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/banco-usb-v0.2/wire.py)

## 11. Telemetry definition and working example

Criterio de plantilla: 55. Bench example only · 22 ASCII fields with a carriage-return delimiter

The ~55-byte flight payload is an estimate, not this ASCII frame and not an approved final format.

Notas para exposición:

Este ejemplo se obtiene del generador de banco existente, no se inventa una muestra de vuelo. La lista de campos y el CSV permiten verificar orden y parser. Incluye TEAM_ID de prueba 1000, hora de misión y GPS, contador, modo y estado, altura relativa y GPS, temperatura, presión, tensión/corriente, tres velocidades angulares, tres aceleraciones, latitud/longitud, satélites y eco. Los nombres R/P/Y del gyro no significan ángulos. Edu debe definir el wire de vuelo, versión, origen/destino, tipos, escalas, orden de bytes, límite de longitud y validez. Eliminar el Net ID heredado no autoriza broadcast ni define direccionamiento. La cabecera y CRC de la capa física LoRa se contabilizan en el modelo de airtime, no se suman otra vez como campos de aplicación.

Fuentes:

- [D1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/pdr/2026-11-17/Interfaz_para_completar_con_Edu.json)
- [https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/banco-usb-v0.1/protocol.py](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/banco-usb-v0.1/protocol.py)
- [https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/laboratorio/runtime.py](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/laboratorio/runtime.py)

## 12. Radio timing and transmission control

Criterio de plantilla: 54. Calculated LoRa airtime · BW 125 kHz, CR 4/5, explicit header, CRC, preamble 8

A 1 Hz design must also allocate commands, responses, turnaround and guard time. Final scheduler remains open.

Notas para exposición:

Cada barra usa payload completo de aplicación de 55, 100 o 255 bytes. SF7:107.776/174.336/399.616 ms; SF9:349.184/553.984/1250.304 ms; SF10:657.408/1026.048/2295.808 ms. Son cálculos con fórmula de Semtech, no mediciones de radio. La frecuencia de ejemplo es 915 MHz pero el airtime depende de SF/BW/CR, cabecera, CRC y preámbulo. El intervalo restante no es capacidad garantizada de comandos. Aterrizaje, inicio de telemetría, estado de baja potencia y recuperación tras reset se acuerdan con vuelo; no se fija apagado automático por pérdida de señal. La limitación indicada por el fabricante para +20 dBm requiere revisar condiciones de operación y no debe generalizarse como norma regulatoria para toda potencia.

Fuentes:

- [E6](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/interfaces/2026-10-26-payload-sf-confiabilidad-04.md)
- [M4](https://cdn.sparkfun.com/assets/7/7/3/2/2/SX1276_Datasheet.pdf)
- [D1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/pdr/2026-11-17/Interfaz_para_completar_con_Edu.json)

## 13. Camera sensor trade — release and ground views

Criterio de plantilla: 28. Same sensor trade applies to template items 28 and 30

| Criterion | OV2640 on ESP32-CAM | OV5640 alternative |
| --- | --- | --- |
| Sensor capability in driver | Colour, up to 1600 × 1200 | Colour, up to 2592 × 1944 |
| 640 × 480 recording target | Within sensor capability; bench images checked | Within sensor capability; ASTRA unit not tested |
| Integration evidence | Two actual units; PSRAM identified | Driver support only; not plug-and-play approval |
| Storage / throughput | Measured on camera 1 at VGA | No ASTRA throughput or power measurements |
| Decision criterion | Existing hardware and reproducible VGA evidence | Extra resolution adds integration / resource risk |

Select OV2640 for both preliminary views. Lens field of view and mechanical orientation still require integration tests.

Notas para exposición:

La comparación se basa en la tabla del controlador oficial de Espressif 2.1.7 y en ensayos propios. Soporte del controlador no implica que un módulo OV5640 sea eléctricamente intercambiable en nuestras placas. No atribuimos fps máximos, consumo ni óptica sin medición. Elegimos preliminarmente OV2640 porque ya hay dos unidades y fotos VGA color verificadas; aumentar resolución no resuelve por sí solo la misión. Para una reutilización directa en el PDR general, esta diapositiva puede cubrir el trade de ambos puntos 28 y 30, manteniendo las dos selecciones siguientes en el mismo diseño si el editor decide dividirlo.

Fuentes:

- [M3](https://components.espressif.com/components/espressif/esp32-camera/versions/2.1.7/readme)
- [E4](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/camaras/2026-10-26-ambas-camaras-sd-y-lector-07.md)
- [E5](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/camaras/2026-10-27-grabacion-segmentada-y-supervision-usb.md)

## 14. Dual-camera recording architecture

Criterio de plantilla: 29. Selected preliminary concept for items 29 and 31 · each camera has its own microSD

Required views: release / zenith and ground / nadir. Verify the lens is unobstructed throughout the mission.

Notas para exposición:

Dos ESP32-CAM con OV2640, PSRAM identificada y tarjeta propia. La finalidad es guardar el viaje localmente aunque no haya notebook ni enlace. OBC inicia/controla según la interfaz que Edu confirme. Se propone devolver salud por cámara al OBC para telemetría, pero el bus y los pines no están aprobados. Un pulso START por sí solo no permite saber desde tierra si se escribe en la SD. La alimentación debe impedir que un reset del OBC interrumpa ambas cámaras, y eso debe comprobarse sobre el esquema EPS real. Cámara 2 aún no tiene validación del grabador nuevo; la evidencia conjunta existente es fotografía secuencial, no video simultáneo. Audio fuera de alcance por decisión del equipo.

Fuentes:

- [E4](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/camaras/2026-10-26-ambas-camaras-sd-y-lector-07.md)
- [E5](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/camaras/2026-10-27-grabacion-segmentada-y-supervision-usb.md)
- [D1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/pdr/2026-11-17/Interfaz_para_completar_con_Edu.json)

## 15. Recording lifecycle and failure supervision

Criterio de plantilla: 31. Proposed autonomous behavior · camera 1 provides short bench evidence

| Phase | Camera behavior to verify | Ground indication |
| --- | --- | --- |
| Power on / ready | Cold boot, mount card, capture / write self-check | Ready only after verified initialization |
| Start event | OBC event starts an identified recording run | Command result is distinct from stored frames |
| Recording | Append frames / index; close segments periodically | Frames, bytes and last successful write age |
| Link loss / OBC reset | Recording continues on flight power | State unknown if reports become stale |
| Stop / recovery | Close segment and manifest; preserve valid prior data | Final counts and errors; incomplete segment flagged |
| Post-flight | Independent reader decodes both cards | Compare duration, gaps, counts, hashes and views |

A preview image or a “recording” flag alone does not prove continuous SD writing.

Notas para exposición:

El candidato de banco segmenta hasta 60 cuadros y conserva un índice por cuadro, con manifiesto de cierre. La recuperación de un segmento interrumpido por corte no está validada; es un caso de prueba, no una función que damos por aprobada. Las condiciones de inicio, parada, duración y modo de fallo dependen del diseño compartido. Proponemos que los reportes incluyan identidad de cámara, arranque y corrida, cuadros y bytes guardados, edad de última escritura, espacio disponible y errores. Los umbrales de frescura y frecuencia de reporte se fijan a partir del presupuesto del enlace. No confundir ausencia de reporte con cámara detenida: el estado desde tierra pasa a desconocido.

Fuentes:

- [E5](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/camaras/2026-10-27-grabacion-segmentada-y-supervision-usb.md)
- [D1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/pdr/2026-11-17/Interfaz_para_completar_con_Edu.json)

## 16. Local preview and flight video are separate paths

Criterio de plantilla: 31. Wi-Fi maintenance was demonstrated near the PC · no flight-range video claim

| Path | Purpose / observed status | Design boundary |
| --- | --- | --- |
| USB photograph | Capture and inspect a current scene | Bench tool; not the autonomous mission link |
| Wi-Fi preview | Camera 1 local live image confirmed by operator | FPS and latency not characterized |
| Two local access points | Each camera may expose its own network | Current PC cannot assume both at once |
| Shared Wi-Fi network | Possible future maintenance design | Not implemented or validated |
| microSD recording | Local image sequence plus timestamps / segment index | Wi-Fi preview and SD recording not concurrently validated |
| Ground health telemetry | Small status packets via OBC / main RF | Return interface must be defined with Edu |

No continuous downlink of flight video is assumed. Recording must not depend on the PC Wi-Fi connection.

Notas para exposición:

La vista previa local de cámara 1 se confirmó en una comprobación operativa. Esa comprobación no da una latencia ni tasa de cuadros medida. Usar una red local de cámara puede interrumpir la conexión Wi-Fi habitual de la PC. El grabador de banco requiere Wi-Fi apagado; no damos por hecho coexistencia ni agregamos consumo de RF no medido al EPS. La secuencia de JPEG con tiempos es captura de video; el MP4 H.264 se genera en la PC, no se atribuye codificación H.264 al ESP32. El producto de vuelo puede definirse luego como secuencia recuperable o contenedor compatible, conservando la temporalidad y sin interpolar cuadros.

Fuentes:

- [E5](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/camaras/2026-10-27-grabacion-segmentada-y-supervision-usb.md)
- [D1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/pdr/2026-11-17/Interfaz_para_completar_con_Edu.json)

## 17. Physical USB bench evidence

Criterio de plantilla: 76. Recorded on 24 October 2026 · synthetic telemetry emitted by an ESP32

| Metric / check | Observed result | Scope / limitation |
| --- | --- | --- |
| Valid packets / CSV rows | 7,261 / 7,261 | One prolonged USB bench configuration |
| Monotonic elapsed time | 7,260.328 s (~2 h 1 min) | Does not validate PC battery autonomy |
| Mean / min / max interval | 1.000045 s / 0.937 s / 1.063 s | Host-observed timing, not RF airtime |
| CSV reconstruction | Original and reconstructed SHA-256 equal | Evidence and immutable source manifest retained |
| Nominal writer counters | No drops / duplicates / writer errors reported | No guarantee for untested field conditions |
| Disconnect / reconnect test | Separate campaign detected ~10.14 s outage | Missing samples after power / reset may be unknown |

This is not a two-hour test of the current Qt build, flight sensors or the RF link.

Notas para exposición:

La evidencia prolongada pertenece a la revisión de adquisición ce3220891ece63d2fcaa0c7990ec8d3eaa63181f y documentación consolidada en 44bf6ea88a04acfa460dd77bdb8c62d4a6fb9a29. CSV SHA256 f62404025543b6391957352b5de0c081f91557d6c41f6d1e6fd83643f243e1c2. El perfil inicial incluye una misión sintética corta y muchas muestras posteriores de estado LANDED; no equivale a dos horas de vuelo. La prueba de corte y reapertura es otra campaña, con límites distintos; no mezclarla con el segmento nominal para anunciar cero pérdidas globales. Un nuevo ensayo de aceptación debe usar las versiones finales de aplicación, receptor y almacenamiento.

Fuentes:

- [E1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md)
- [E2](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/2026-10-25-interfaz-y-cortes-usb.md)

## 18. Camera bench evidence

Criterio de plantilla: 76. Physical results recorded on 26–27 October 2026

| Test | Observed result | What it does not establish |
| --- | --- | --- |
| Both camera units: still images | Each: two 640 × 480 colour JPEGs | No simultaneous dual-camera recording |
| Independent SD reader | Image bytes / CRC / SHA matched in sequential checks | Same card used by turns in that campaign |
| Camera 1 recording | 123 frames; 3 segments; 1,753,920 JPEG bytes | No mission-length, dual-unit or thermal qualification |
| Measured frame interval | 29.828024 s first-to-last; 4.090113 fps mean | Not a guaranteed flight frame rate |
| Monitoring interrupted | Counts advanced 10 → 48 during 8 s without monitor | USB power remained connected |
| Recorded files checked | USB copy, frame decode and checksums consistent | Independent reader check of these recordings pending |

No cold boot on flight battery, OBC-reset tolerance or environmental video test has been completed.

Notas para exposición:

Estas cifras corresponden a la prueba de grabación corta de cámara 1. Tasa media calculada como (123−1)/(t_último−t_primero), no 123 dividido por una duración de interfaz. Mayor hueco reportado: 0.479809 s. Hubo además un STOP de 16 cuadros y una prueba de botones de 24 cuadros, pero no se suman como una misión continua. Las fotografías de ambas cámaras fueron verificadas mediante lector; las grabaciones nuevas se copiaron por el controlador de cámara vía USB y no recibieron aún esa verificación independiente. La verificación independiente de estas grabaciones sigue pendiente.

Fuentes:

- [E4](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/camaras/2026-10-26-ambas-camaras-sd-y-lector-07.md)
- [E5](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/camaras/2026-10-27-grabacion-segmentada-y-supervision-usb.md)

## 19. Simulation and fault-injection test plan

Criterio de plantilla: 79. Repeatable software cases · existing bench results and final-build revalidation

| Case | Expected observable behavior | Acceptance evidence |
| --- | --- | --- |
| Nominal sequence | 131 synthetic samples accepted in the reference run | Oracle, journal and CSV agree; no writer drops |
| Packet omission | Observed counter gaps, no fabricated values | Missing set equals injected omissions |
| Corrupt frame | Invalid count increases; invalid data not graphed as valid | Original bytes and rejection reason retained |
| GNSS invalid / unavailable | Invalidity visible; no false valid fix | State and timestamps preserve the distinction |
| Logical reset | New identity / segment; plots do not bridge sessions | No false duplicate or continuous trajectory |
| Storage conflict / failed copy | Explicit degraded state; no silent overwrite | Recovery preserves originals and flags conflicts |

Simulation results demonstrate software behavior. Physical resets, RF loss and power faults need separate tests.

Notas para exposición:

Estos escenarios ya existen en el emisor de PC y pruebas de integración. En la campaña de referencia: nominal 131, pérdida 118 con 13 omitidas, corruptas 121 válidas y 10 inválidas, GNSS 131 y reset lógico 128 con 3 omitidas. No trasladar sin más esos totales a toda versión: el ensayo final debe fijar commit, configuración y oráculo, y comprobar que no quedan errores ni colas pendientes. El reset lógico no valida el arranque del hardware ni la persistencia en flash. Los casos de recuperación comparan fuentes complementarias, una muestra ausente en ambas y conflicto; no rellenan datos por interpolación.

Fuentes:

- [E3](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/historial/2026-10-26-laboratorio-completo-04.md)
- [https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/laboratorio/test_laboratory.py](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/laboratorio/test_laboratory.py)
- [https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/laboratorio/runtime.py](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/laboratorio/runtime.py)

## 20. Integrated mission verification plan

Criterio de plantilla: 77. Proposed gates before claiming flight readiness

| Gate | Procedure | Acceptance / retained evidence |
| --- | --- | --- |
| ICD interoperability | Send known real flight frames and commands through both radios | Byte-exact decode; destination isolation; execution result and effect |
| Complete mission recording | Both cameras, own cards, flight EPS, no notebook | Full required interval; both views decode; gaps and resets reported |
| OBC reset / lost ground link | Reset OBC and interrupt monitoring while recording | No unintended camera stop; ground state becomes unknown when stale |
| Independent storage | PC plus distinct backup medium; induce one writer failure | Raw / CSV compare; failure alarm; originals preserved |
| RF and mounting | Representative range / angles / setup with final profile | RSSI/SNR/PER, gaps, cable losses and orientation documented |
| Recovery and handover | Read both cards independently; export telemetry and media | Hashes, duration, file readability and judge-facing copy checked |

Environmental and endurance acceptance conditions must be taken from the complete team test plan.

Notas para exposición:

No fijamos por nuestra cuenta las condiciones de vibración, impacto o térmicas del vector. Nuestro aporte es instrumentar y conservar datos antes, durante y después de los ensayos que el equipo defina conforme a la documentación oficial aplicable. Para autonomía, registrar tensión/corriente y consumo de cámara/grabación/radio, picos y duración, sobre alimentación real. No derivar consumo promedio del tamaño del JPEG ni de la potencia nominal del transmisor. Los umbrales cuantitativos de PER, margen, gaps y duración se fijan y aprueban antes de la ejecución; no se escogen después para hacer pasar un resultado.

Fuentes:

- [E1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md)
- [E5](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/camaras/2026-10-27-grabacion-segmentada-y-supervision-usb.md)
- [D1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/pdr/2026-11-17/Interfaz_para_completar_con_Edu.json)

## 21. Requirement coverage and remaining risks

Criterio de plantilla: 74. Ground-segment checks · documentary coverage is distinct from acceptance

| Requirement / need | Current contribution | Remaining gate |
| --- | --- | --- |
| G2 recording and independent backup | Journal, CSV and recovery workflow | Final system on independent media for mission duration |
| G12 display in direct sunlight | Native high-contrast display prototype | Outdoor readability test |
| G13 simultaneous data display | 22 fields in table; grouped plots selectable | Confirm final mandatory fields and judge-facing layout |
| G14 received packet counter | Receiver totals and loss / invalid diagnostics | Verify with final RF counter semantics |
| Camera full required interval | Autonomous dual-recording concept / short single-unit proof | Flight EPS, cold boot, two views and independent readback |
| RF / commands | Trade, airtime and verification plan | Shared ICD and physical interoperability |

Main risks: undefined interfaces, unmeasured RF coverage, flight power and incomplete dual-camera validation.

Notas para exposición:

Los identificadores G se usan conforme al mapa de requisitos oficial analizado previamente; no se declara una revalidación completa del aula en noviembre. La tabla de 22 campos es un prototipo de banco y debe adaptarse a la telemetría final. No declaramos satisfecho G13 por mostrar sólo una parte de la tabla en una captura: hay que verificar el conjunto visible y la presentación final pedida. Tampoco se da G2 por cumplido con dos rutas en un único disco. El checklist expone claramente dónde existe diseño, implementación o evidencia física y dónde hace falta aceptación.

Fuentes:

- [O2](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/aula/2026-10-19/mapa-pdr-groundstation.csv)
- [E3](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/historial/2026-10-26-laboratorio-completo-04.md)
- [D1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/pdr/2026-11-17/Interfaz_para_completar_con_Edu.json)

## 22. Shared decisions required to close integration

Criterio de plantilla: ICD. Prepared ground-side interfaces · seven decisions awaiting flight-system definition

| Decision | Needed from Edu / shared design | Ground-side closure action |
| --- | --- | --- |
| D01 telemetry | Fields, encoding, full size, IDs and real example | Adapt parser; generate byte-exact vectors |
| D02 RF | Exact module, profile, addressing and TX/RX timing | Configure gateway; redo airtime / link budget |
| D03 commands | Operations, arguments, state guards, result / timeout | Bind controls and verify execution effects |
| D04 state / reset | Mission and boot identity, counter / clock persistence | Align segmentation, gaps and freshness |
| D05 / D06 cameras | Start / stop / power and progress-return interface | Integrate autonomous recorder and stale-state checks |
| D07 physical integration | Antennas, cables, EPS and mission geometry | Freeze mount / losses; run acceptance campaign |

These decisions are not assigned or approved by this deck. Preserve evidence and version each agreed baseline.

Notas para exposición:

Mensaje listo para copiar a Edu: estoy preparando ya nuestra parte del PDR. Necesito tu definición actual de paquete y ejemplo, perfil/módulo de radio y tiempos, comandos/respuestas, estados/reset, control y retorno de salud de ambas cámaras, y antenas/cables/alimentación/geometría. Separá lo implementado, lo propuesto y lo pendiente. Con esa versión adapto tierra y la dejamos consistente para integrar. No hace falta que todo esté construido para documentar el diseño preliminar, pero no podemos presentar parámetros compartidos como acordados si no lo están. El archivo de interfaz adjunto conserva null donde falta una definición real, en vez de usar un valor que parezca válido.

Fuentes:

- [D1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/pdr/2026-11-17/Interfaz_para_completar_con_Edu.json)
- [https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/pdr/2026-11-17/decisiones_para_Edu.csv](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/pdr/2026-11-17/decisiones_para_Edu.csv)

## 23. Evidence and source register

Criterio de plantilla: REF. Versioned project records and primary manufacturer documentation

| Reference | Document / evidence | Use in this contribution |
| --- | --- | --- |
| E1–E3 | USB acceptance, disconnects, Qt software records | Implemented ground software and exact bench limits |
| E4–E5 | Dual still-image verification and segmented recording | Camera evidence and outstanding acceptance |
| E6–E7 | Payload / airtime and link-budget analysis | RF calculations and unresolved inputs |
| D1 | Draft shared-interface record, 17 November 2026 | Open decisions; not an approved flight ICD |
| M1–M4 | Taoglas TI.92 / OMB; Espressif driver; Semtech SX1276 | Trade, reference patterns and airtime model |
| O1–O2 | Official archived template / scoresheet and item map | Scope mapping; current authenticated aula review unavailable |

Clickable source URLs and Spanish explanation are included in the notes of each relevant slide.

Notas para exposición:

Registro completo de enlaces de evidencia. Los documentos oficiales de terceros se conservan en su ubicación original privada y no se suben al repositorio público. Plantilla PDR Template - V2.pptx SHA256 38122779a5245f5015eb67fd26c7da60a29c6272cbe85b5797cda6bdffb37036. Scoresheet V2.xlsx SHA256 a72559e8d3473d7a40e5737bdabbd9aacf6c8db5e94517df91f4ab0e09c84f97. El documento es una contribución técnica al PDR, no un certificado de cumplimiento ni una aceptación del vuelo. Los cambios posteriores de Edu, pruebas nuevas o aclaraciones oficiales deben incorporarse como una nueva versión.

Fuentes:

- [E1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md)
- [E2](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/2026-10-25-interfaz-y-cortes-usb.md)
- [E3](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/historial/2026-10-26-laboratorio-completo-04.md)
- [E4](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/camaras/2026-10-26-ambas-camaras-sd-y-lector-07.md)
- [E5](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/camaras/2026-10-27-grabacion-segmentada-y-supervision-usb.md)
- [E6](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/interfaces/2026-10-26-payload-sf-confiabilidad-04.md)
- [E7](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/interfaces/2026-10-24-enlace-destinos-y-revision.md)
- [D1](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/pdr/2026-11-17/Interfaz_para_completar_con_Edu.json)
- [M1](https://www.taoglas.com/datasheets/TI.92.2113.pdf)
- [M2](https://www.taoglas.com/datasheets/OMB.915.B05F21.pdf)
- [M3](https://components.espressif.com/components/espressif/esp32-camera/versions/2.1.7/readme)
- [M4](https://cdn.sparkfun.com/assets/7/7/3/2/2/SX1276_Datasheet.pdf)
- [O1](https://educacion.conae.gov.ar/aulavirtual/course/view.php?id=106)
- [O2](https://github.com/edulandoni/astra-cansat/blob/70b9f9d4e495f322b80ecd5bae16df3f8e3290f0/ground-station/docs/aula/2026-10-19/mapa-pdr-groundstation.csv)