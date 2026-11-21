# 28/10/2026 — Peralta: filtrado, validez y tiempo

Diario: [ASTRA-35](https://astrateam2026.atlassian.net/browse/ASTRA-35). Amplío la [ficha del 26/10](2026-10-26-peralta-recepcion-y-analisis.md), conservando sus resultados y límites.

## Fuente y lectura realizada

Leí completo [ground_station/kalman.py](https://github.com/aron-8/CanSat_peralta/blob/4b57c9679da1f1aecef90cb16ace9b5d8ac1044f/ground_station/kalman.py), fijado al commit `4b57c9679da1f1aecef90cb16ace9b5d8ac1044f`. Consulté además el árbol completo de esa revisión, sin truncamiento. Es una fuente primaria del autor del repositorio; no ejecuté su código ni validé registros de vuelo. Esta pasada profundiza una ficha con un módulo nuevo, no audita todo Peralta.

## Qué hace y por qué nos sirve

El módulo incluye un filtro escalar y otro de dos variables para presión y temperatura. Ambos combinan una predicción con una medición y guardan una serie calculada. Una curva más suave puede facilitar la lectura, pero no demuestra mayor exactitud del sensor ni reemplaza una calibración.

La función escalar utiliza Q y R constantes por paso; no recibe tiempos de muestra. La función de dos variables acepta matrices F y H, también sin vector de fechas en su firma. Esto no prueba que todo el proyecto ignore el tiempo: limita lo que puede concluirse de este archivo. Con interrupciones o muestras espaciadas de forma irregular, una misma cantidad de pasos puede representar duraciones distintas.

Ambas funciones toman la primera muestra directamente. No veo validación local para listas vacías, valores no finitos o longitudes incompatibles de presión y temperatura. Tampoco se devuelve una máscara de calidad o causa de descarte. Son precondiciones que otro nivel podría asegurar; sin revisar todas las llamadas no afirmo un fallo operativo del equipo.

El archivo permite parametrizar modelos, pero no aporta aquí una campaña de ajuste, incertidumbre de referencia o validación frente a un patrón. No adopto sus parámetros como adecuados para nuestro sensor ni atribuyo éxito o fallo de vuelo a este módulo.

## Evidencia → riesgo propio → prueba propuesta

| Evidencia leída | Riesgo que debemos considerar | Prueba propuesta / resultado actual |
| --- | --- | --- |
| Filtro por pasos sin tiempos de muestra en la firma | Confundir muestras ausentes con un intervalo regular | Comparar una entrada con tiempos regulares y otra con huecos conservados; pendiente, no ejecutada hoy |
| Primera muestra usada sin validación local | Iniciar una estimación con dato inválido | Inyectar primera muestra inválida/lista vacía y comprobar rechazo explicado; pendiente |
| Dos series indexadas conjuntamente | Desalinear presión y temperatura | Probar longitudes y marcas temporales incompatibles; pendiente |
| Salida estimada sin máscara local de calidad | Mostrar una estimación como medición nueva | Conservar dato original, procedencia, tiempo y estado del cálculo; criterio de diseño, sin cambio de software hoy |
| Parámetros sin ensayo de ajuste en este archivo | Justificar precisión por apariencia del gráfico | Contrastar con referencia y medir error y retardo antes de declarar mejora; pendiente |

Las pruebas propuestas deben incorporarse cuando desarrollemos un filtro propio; no justifican agregar uno por rutina ni reabrir una tarea finalizada sólo para repetir antecedentes. En el PDR puedo citar esta revisión como fundamento de mantener medición y estimación identificadas, sin afirmar que un filtro propio quedó implementado o validado.

## Referencias visuales y límites

Revisé el [catálogo visual de Peralta](2026-10-26-catalogo-visual-peralta.csv) y el árbol de fuentes. Permanecen localizadas una foto de placa, una figura de alturas y un mapa; no abrí imágenes en esta pasada ni republiqué binarios. Sus nombres no prueban componentes, exactitud o trayectoria. Crédito y permisos individuales conservan los pendientes del catálogo.

No apareció en esta lectura evidencia nueva de energía generada por rotor, puntuaciones de un premio ni un PFR completo. No cambié RF, ICD, fuentes de software, tareas ajenas ni datos originales.

