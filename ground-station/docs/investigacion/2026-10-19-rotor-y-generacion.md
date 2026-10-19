# 19/10/2026 — Descenso con rotor y generación eléctrica

Bitácora: [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21). Registro una exploración para discutir con el equipo; no apruebo ni modifico el diseño de recuperación. Complementa el [relevamiento de antecedentes](2026-10-19-antecedentes-cansat.md).

## Qué idea estoy evaluando

Podemos estudiar que el aire haga girar un rotor durante la caída, que ese rotor contribuya a frenar el descenso y que un generador aproveche parte del giro. Es autorrotación: no necesitamos un motor que sostenga el aparato como un helicóptero. Generar electricidad introduce resistencia al giro; por eso debemos estudiar juntos descenso, estabilidad y carga eléctrica.

Son tres opciones distintas: rotor de descenso conectado a un generador; turbina adicional bajo un paracaídas; o superficie flexible giratoria tipo rotachute. La segunda desacopla parte del problema del descenso, pero agrega masa, resistencia y posibles enredos. No afirmo que las tres funcionen igual ni que una sea mejor sin compararlas.

## ¿Ya se hizo?

- La [misión oficial AAS 2025](https://cansatcompetition.com/docs/CanSat_Mission_Guide_2025d.pdf) pedía un descenso con autogiro: primero paracaídas y luego autorrotación al 75% del apogeo, con objetivo de 5 m/s. Era una misión distinta, de aproximadamente 1,4 kg; no copiamos su dimensionamiento a nuestros 500 g. [SEDS ITBA ganó esa edición](https://www.cansatcompetition.com/winners.html). Esto acredita un antecedente competitivo, no generación de electricidad.
- [ICARE, Telecom SudParis, 2013](https://www.planete-sciences.org/espace/IMG/pdf/Icare_CanSat_T3_Milestone.pdf) documentó un CanSat con un pequeño generador eólico, usando un ventilador como generador y rectificación. El informe es previo al vuelo: demuestra que la idea ya se propuso y desarrolló, pero no acredita energía neta obtenida ni autonomía sin batería.
- Existe [investigación universitaria sobre autorrotación y extracción simultánea de energía](https://stars.library.ucf.edu/etd/4918/). Su sistema está sujeto mediante un cable y aprovecha viento: ayuda a estudiar el acoplamiento, pero no valida un CanSat en caída libre.

No puedo afirmar que seamos los primeros. Tampoco encontré aquí una demostración suficientemente documentada de nuestra combinación exacta, con las dimensiones y restricciones CONAE actuales. La innovación defendible puede estar en medir cuánto obtenemos y a qué costo en descenso, estabilidad y fiabilidad.

## Qué permite estudiar nuestra v2

Uso la copia del anexo oficial v2 conservada en nuestra revisión del 17/10, SHA-256 `27932c87654b64b443d41483c9b48adb06d7d1379dd7a01d54e4ea0035057bc7`. La [comparación de requisitos de tierra](../requisitos/v1-v2-groundstation-2026-10-19.md) conserva el contexto de esa fuente.

| Requisito | Consecuencia para la idea |
| --- | --- |
| C3: paracaídas automático, 15 ± 3 m/s | La primera etapa exige paracaídas. No la reemplazo unilateralmente por hélices. |
| C4: otro sistema de descenso al 80% de la altura máxima; media 5 ± 3 m/s | El texto no exige explícitamente un segundo paracaídas. Un rotor es candidato para estudiar, pendiente de confirmación de admisibilidad y cumplimiento. |
| S1: masa conjunta 500 ± 10 g; S2/S3: 90 mm y 200–250 mm | Importan masa del generador, mecanismo y volumen plegado; si se separan masas, cambia el cálculo por fase. |
| E3: paneles solares para detección de radiación | Un generador eólico no sustituye esa función obligatoria. |
| E7: funcionamiento de dos horas dentro del cohete | Durante ese período no contamos con viento para el rotor; no elimina la necesidad de alimentación autónoma. |

Pregunta pendiente para el canal formal del equipo: ¿se admite un rotor autorrotativo como sistema C4 y bajo qué condiciones de despliegue, envolvente y seguridad? No envié esta consulta ni doy por obtenida su aprobación.

## Cuánta energía podría representar: cálculo ilustrativo

Preparé un [cálculo reproducible](../../experiments/2026-10-19-rotor/README.md), con [resultados JSON](../../evidence/2026-10-19-rotor-escala/escala.json) y [tabla CSV](../../evidence/2026-10-19-rotor-escala/escenarios.csv). No es una simulación aerodinámica.

Supongo una masa descendente constante de 0,5 kg, un apogeo ficticio de 500 m y rotor activo desde 400 m, descendiendo a 5 m/s constantes. **Los 500 m y las eficiencias siguientes son hipótesis, no valores confirmados de nuestra misión ni prestaciones medidas.** La escala gravitatoria es `m × g × h`: 1961,33 J, equivalentes a 0,5448 Wh durante esa fase de 80 s. Esa energía no queda enteramente disponible en el eje: buena parte se disipa en el aire y hay pérdidas adicionales.

| Fracción global hipotética convertida a electricidad | Energía eléctrica | Potencia media durante 80 s | Equivalencia ideal de consumo a 1 W |
| --- | --- | --- | --- |
| 1% | 0,00545 Wh | 0,245 W | 0,33 min |
| 5% | 0,02724 Wh | 1,226 W | 1,63 min |
| 10% | 0,05448 Wh | 2,452 W | 3,27 min |
| 20% | 0,10896 Wh | 4,903 W | 6,54 min |

Estas fracciones incluyen tanto energía no captada como pérdidas mecánicas y eléctricas. No son eficiencias atribuidas a un rotor real. A 1 W durante dos horas harían falta 2 Wh: el caso hipotético del 10% aportaría aproximadamente el 2,7% de ese presupuesto. Nuestro consumo real sigue pendiente; no estoy dimensionando su batería con este ejemplo.

El balance supone caída sin aporte adicional de viento ni cambio relevante de energía cinética. No predice rpm, par, velocidad real ni arranque. La potencia gravitatoria de referencia, 24,52 W, **no es la potencia del generador**. No debo sustituirla por una promesa de salida eléctrica.

## Por qué es difícil y cuándo tendría sentido

El generador frena el eje. Una carga eléctrica mayor puede cambiar las rpm, la fuerza aerodinámica, el descenso y el giro del cuerpo. Un circuito abierto, cortocircuito, trabado o cambio brusco de carga son estados de ensayo diferentes. También debemos evaluar despliegue tardío, tiempo de arranque, contacto con cuerdas, vibraciones, balanceo y efecto sobre cámaras y antena.

Ver voltaje sin carga no demuestra energía útil. Debemos medir simultáneamente tensión, corriente, tiempo, rpm y descenso; descontar consumo de la electrónica de conversión y evaluar masa agregada. El registro rápido del rotor debe estudiarse aparte: la telemetría de 1 Hz no basta por sí sola para observar fenómenos rápidos, y no cambio el protocolo compartido sin acuerdo.

Como experimento científico puede ser valioso: comparar energía obtenida y degradación del descenso con y sin generación. Como fuente principal de alimentación no lo justifico con la evidencia actual. La ausencia de una adopción generalizada no prueba imposibilidad ni inutilidad; el balance de beneficio y complejidad requiere mediciones.

## Qué puedo avanzar sin microcontrolador físico

1. Comparar en papel tres configuraciones: paracaídas de referencia, rotor sin generador y rotor cargado. Definir masa, volumen, duración disponible y métricas antes de dibujar mecanismos.
2. Barrer escenarios de altura, masa descendente y consumo con el cálculo publicado. Los coeficientes aerodinámicos quedan pendientes, no inventados como datos validados.
3. Preparar un modelo acoplado: `m·dv/dt = mg − fuerza aerodinámica` y `I·dω/dt = par aerodinámico − par del generador − pérdidas`. Necesita geometría y coeficientes respaldados antes de predecir prestaciones.
4. Definir ensayos futuros de arranque, carga escalonada, circuito abierto, cortocircuito y despliegue. Comparar repetibilidad y comportamiento ante falla eléctrica con el rotor libre.
5. Guardar señales sintéticas de esos escenarios para comprobar cómo la estación identifica datos ausentes, inconsistentes o fuera de rango. Es una propuesta; este registro no declara implementados esos nuevos escenarios.

## Resultado de esta entrada y criterio para continuar

Quedaron ejecutados el cálculo de escala y sus comprobaciones aritméticas. No hubo prueba física, CFD, túnel de viento ni validación de recuperación. Para proponer vuelo necesito admisibilidad confirmada, presupuesto de masa y energía, despliegue repetible, descenso dentro de C4 y comportamiento aceptable ante fallo eléctrico. Mientras tanto conservo la idea como investigación, con beneficio medible pendiente.

Una actualización posterior debe referirse a esta entrada y explicar qué hipótesis cambió y con qué evidencia. No reemplaza el original ni convierte una posibilidad en requisito del equipo.
