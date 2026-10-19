# 19/10/2026 — Escala energética de un rotor durante descenso

En [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21) registro el motivo y los límites. El [análisis](../../docs/investigacion/2026-10-19-rotor-y-generacion.md) explica los antecedentes y requisitos.

Con Python 3, sin dependencias, desde la raíz del repositorio:

```text
python ground-station/experiments/2026-10-19-rotor/escala_energetica.py --help
```

La ayuda indica los parámetros y el destino requerido. Usar siempre una carpeta nueva para otra ejecución; el programa rechaza un destino existente. Los resultados iniciales están en [evidence](../../evidence/2026-10-19-rotor-escala/escala.json).

Compruebo energía gravitatoria, tiempo y conversiones de unidades, y que potencia por tiempo coincida con energía. Las fracciones de conversión de 1%, 5%, 10% y 20% son una sensibilidad hipotética. No pruebo aerodinámica, estabilidad, despliegue, autonomía, energía neta real ni cumplimiento de vuelo. Si se separan masas hay que recalcular por fase.
