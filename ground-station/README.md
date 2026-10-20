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
| Investigar mejoras sin hardware | [Prevención de fallas y oportunidades](docs/investigacion/2026-10-19-innovacion-y-prevencion.md) |
| Revisar desconexiones y recuperación de archivos | [Ensayos de resiliencia](docs/investigacion/2026-10-19-resiliencia-y-recuperacion.md) |

## Estado de esta incorporación

Conservo el banco Python y el sketch ESP32 del 17/10 sin alterar sus fuentes. El banco puede generar datos ficticios en la computadora. El sketch todavía no tiene compilación ni prueba física acreditadas. No hay validación de radio, antena, alcance, dos horas de autonomía ni persistencia ante corte real.

El formato de 22 campos y TEAM_ID de cuatro dígitos es una convención heredada de v1 para practicar; no lo presento como formato obligatorio del anexo v2 ni como protocolo acordado con Edu. `1000` es ficticio.

Las entradas fechadas y las capturas se conservan. Una conclusión nueva se agrega en otro documento o comentario con referencia al anterior. Este índice puede incorporar enlaces a nuevas entradas; su versión inicial queda en Git.

Jira es la bitácora principal: [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20), [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21), [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22).

## Investigación agregada el 19/10/2026

- [Antecedentes CanSat y catálogo de 35 registros](docs/investigacion/2026-10-19-antecedentes-cansat.md).
- [Autorrotación y generación eléctrica: antecedentes, límites y cálculo](docs/investigacion/2026-10-19-rotor-y-generacion.md).

## Ubicación de los temas — actualización del 19/10/2026

Para continuar el diario uso el [mapa vigente](docs/trazabilidad-vigente-2026-10-19.md). Los enlaces de las entradas anteriores conservan su contexto histórico.

- [ASTRA-33: diario, trazabilidad y respaldo](docs/temas/diario-y-respaldo/README.md).
- [ASTRA-34: investigación de calidad de datos](docs/temas/calidad-de-datos/README.md).
- [ASTRA-35: antecedentes CanSat](docs/temas/antecedentes-cansat/README.md).
- [ASTRA-36: rotor y generación eléctrica](docs/temas/rotor-y-energia/README.md).
- [Revisión de los 35 comentarios y corrección de referencias](docs/historial/2026-10-19-orden-comentarios.md).

El receptor y los ensayos de CSV siguen en ASTRA-21; el respaldo de documentación de Jira continúa en ASTRA-33. Los originales permanecen íntegros.

## Incorporación del 19/10/2026 — Aula CONAE

[Revisión del aula oficial, plantillas PDR y aclaraciones](docs/aula/2026-10-19/revision-aula.md), con bitácora propia en [ASTRA-37](https://astrateam2026.atlassian.net/browse/ASTRA-37). Los informes anteriores se conservan.
