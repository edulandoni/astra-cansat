# 19/10/2026 — Investigo fallas antes de conectar hardware

Relaciono este sondeo con [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21) y las dependencias de [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20) y [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22).

Uso el banco existente para observar qué distingue hoy y qué necesita una capa adicional de diagnóstico. No modifico sus fuentes ni conecto hardware. Esta carpeta es un experimento de investigación; no incorpora las mejoras propuestas a la aplicación de operación.

## Reproducción

Desde la raíz del repositorio ejecuto, eligiendo una carpeta de salida nueva:

```text
python ground-station/experiments/2026-10-19-prevencion/explorar.py --salida ground-station/evidence/MI_NUEVA_EJECUCION
```

El sondeo usa la biblioteca estándar de Python. No necesita paquetes adicionales, puerto COM, microcontrolador ni antena. Se ejecuta sin esperar una misión en tiempo real. Las escrituras de prueba quedan en directorios temporales; el informe permanece en la carpeta de salida. El programa rechaza una salida ya existente para conservar resultados anteriores.

El fallo de registro se produce mediante una excepción controlada en el método de guardado. No lleno el disco ni desconecto dispositivos.

## Evidencia y resultados

Los [resultados JSON](../../evidence/2026-10-19-investigacion-prevencion/resultados.json) y el [resumen CSV](../../evidence/2026-10-19-investigacion-prevencion/resumen.csv) conservan diez casos y las huellas de los módulos examinados. La [evaluación](../../docs/investigacion/2026-10-19-innovacion-y-prevencion.md) explica las oportunidades y sus límites.

No interpreto diez sondeos como diez requisitos aprobados ni como una estimación de confiabilidad en vuelo. Las entradas se eligen deliberadamente para explorar comportamientos. Los valores extremos no son límites operativos acordados.
