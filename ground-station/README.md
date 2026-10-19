# Groundstation y manejo de datos

Me encargo de recibir, registrar y mostrar la telemetría en tierra. Esta carpeta reúne mi código, pruebas y decisiones. La rama `groundstation` es mi línea de trabajo del subsistema; no establece reglas para las otras áreas del equipo.

## Por dónde empezar

| Necesidad | Ubicación |
| --- | --- |
| Probar sin placa ni antena | [Banco USB v0.1](banco-usb-v0.1/README.md) |
| Saber qué funciona y qué falta | [Estado al 19/10/2026](docs/estado-2026-10-19.md) |
| Entender cómo guardo la historia | [Metodología](docs/metodologia-2026-10-19.md) |
| Revisar las pruebas | [Resultados y límites](docs/pruebas-2026-10-19.md) |
| Entender el cambio de reglamento | [Comparación v1/v2 para tierra](docs/requisitos/v1-v2-groundstation-2026-10-19.md) |
| Entender qué necesito acordar con vuelo | [Ficha de interfaz pendiente](docs/interfaces/pendientes-groundstation-2026-10-19.md) |
| Ir del código a su motivo en Jira | [Mapa de trazabilidad](docs/trazabilidad-2026-10-19.md) |
| Leer las capturas de Jira | [Historial de Jira](historial-jira/README.md) |
| Revisar simuladores anteriores | [Archivo DEPRECATED](archive/DEPRECATED/README.md) |
| Entender el respaldo diario | [Automatización](docs/respaldo-jira-2026-10-19.md) |

## Estado de esta incorporación

Conservo el banco Python y el sketch ESP32 del 17/10 sin alterar sus fuentes. El banco puede generar datos ficticios en la computadora. El sketch todavía no tiene compilación ni prueba física acreditadas. No hay validación de radio, antena, alcance, dos horas de autonomía ni persistencia ante corte real.

El formato de 22 campos y TEAM_ID de cuatro dígitos es una convención heredada de v1 para practicar; no lo presento como formato obligatorio del anexo v2 ni como protocolo acordado con Edu. `1000` es ficticio.

Las entradas fechadas y las capturas se conservan. Una conclusión nueva se agrega en otro documento o comentario con referencia al anterior. Este índice puede incorporar enlaces a nuevas entradas; su versión inicial queda en Git.

Jira es la bitácora principal: [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20), [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21), [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22).
