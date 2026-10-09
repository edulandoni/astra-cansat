# ASTRA TEAM — CanSat Universitario 2026/2027

ASTRA TEAM es un equipo universitario dedicado al diseño, desarrollo, integración y validación de un sistema CanSat.

Este repositorio contiene el desarrollo del **CanSat Universitario 2026/2027**. Está organizado como un monorepo para mantener en un único lugar el software, el hardware y la documentación de ingeniería del proyecto.

## Estructura

- `flight-software/`: software embarcado del CanSat.
- `ground-station/`: software de la estación terrena.
- `protocol/`: contrato compartido de telemetría, comandos, estados y errores.
- `hardware/`: diseño electrónico y mecánico.
- `verification/`: planes, procedimientos, resultados y datos de verificación.
- `simulations/`: modelos y simulaciones del sistema.
- `tools/`: herramientas auxiliares del proyecto.
- `docs/`: requisitos, arquitectura, interfaces y demás documentación de ingeniería.
- `.github/`: plantillas y futura automatización del repositorio.

Flight Software y Ground Station deben implementar el mismo protocolo, cuya definición autoritativa se mantiene en [`protocol/`](protocol/).

## Estado

Estructura inicial del proyecto. Las tecnologías y especificaciones técnicas se definirán posteriormente.
