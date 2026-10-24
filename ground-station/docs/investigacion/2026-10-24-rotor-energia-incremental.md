# 24/10/2026 — Rotor: energía incremental, consumo propio y condiciones para seguir

Diario: [ASTRA-36](https://astrateam2026.atlassian.net/browse/ASTRA-36). Amplío la [escala gravitatoria original](2026-10-19-rotor-y-generacion.md) y los [riesgos de estabilidad](2026-10-22-rotor-estabilidad-y-evidencia.md), sin reemplazarlos.

## La diferencia que faltaba contabilizar

La energía potencial que podría transformarse no es necesariamente beneficio neto. Agregué el consumo incremental de electrónica incorporada exclusivamente por el rotor y el tiempo durante el que permanece encendida antes del descenso. No resto de nuevo el consumo común del CanSat: al comparar con/sin rotor ese consumo es compartido. La eficiencia global ya incluye las pérdidas de conversión; la carga adicional debe excluirlas para no contarlas dos veces.

Modelo limitado: energía generada=η·m·g·h; duración del tramo=h/v; consumo adicional=Pextra·(duración+espera); beneficio incremental=generación−consumo adicional. No limito el resultado a cero: un balance negativo tiene que quedar visible. No modelo viento, cambios cinéticos, aerodinámica, RPM, torque, estabilidad o despliegue.

## Resultados hipotéticos, no componentes medidos

Mantengo como ejemplo masa total constante 0,5 kg, tramo 400 m, descenso supuesto 5 m/s y eficiencia global supuesta 10 %. El tramo dura 80 s y la escala eléctrica anterior sigue dando 0,054481 Wh.

| Hipótesis adicional | Balance incremental |
|---|---:|
| Sin consumo adicional | +0,054481 Wh |
| Electrónica adicional de 0,2 W sólo durante el descenso | +0,050037 Wh |
| La misma carga extra también encendida 7200 s antes | −0,349963 Wh |
| Sin generación, pero con esa carga durante 80 s | −0,004444 Wh |

No afirmo que un rotor real necesite 0,2 W, que deba estar encendido dos horas o que alcance 10 %. Son hipótesis para mostrar por qué hay que medir consumo, habilitación y tiempo junto con tensión/corriente generadas. La tercera fila exigiría en este modelo una eficiencia global cercana al 74,2 % sólo para empatar; no predigo que sea físicamente alcanzable. Apagar un circuito hasta despliegue es una alternativa para estudiar, no un diseño implementado.

Pasaron dos pruebas: consistencia con la escala previa, conservación del signo negativo y rechazo de eficiencias/costos inválidos. [Herramienta](../../experiments/2026-10-24-rotor-neto/evaluar.py) · [Casos completos](../../evidence/2026-10-24-avances/rotor-neto-01/resultado.json).

## Recomendación al corte

Mantengo el rotor como investigación opcional. No asigno a la batería una energía recuperada que no medimos y no lo uso para resolver autonomía dentro del cohete, cuando no hay flujo de descenso. Tampoco sustituye los paneles o el sistema de recuperación exigido. No afirmo que sea inútil ni que sea novedad mundial: falta comparar geometría, despliegue, masa, consumo real y carga del generador con el descenso requerido.

El ensayo posterior debería comparar rotor libre y cargado bajo condiciones registradas, medir tensión/corriente/tiempo y consumo incremental, integrar energía útil y observar cómo cambia el giro, estabilidad y velocidad. Si no abre, se traba o aumenta un riesgo de recuperación, una señal Hall o un pico de tensión no salvan el criterio. Necesitamos condiciones de aborto y revisión con responsables de mecánica/alimentación; no decido sus diseños ni asigno tareas ajenas.

Esta pasada es cálculo y preparación de medición. ASTRA-36 sigue abierta por geometría, coeficientes, masa, consumo y pruebas faltantes; no cierro una investigación de viabilidad física sólo con ejemplos numéricos.
