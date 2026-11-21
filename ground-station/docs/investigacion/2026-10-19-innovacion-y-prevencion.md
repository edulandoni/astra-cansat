# 19/10/2026 — Qué puedo investigar e innovar sin el microcontrolador

Jira principal: [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21). Dependencias propias: [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20), [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22). Continúo el diario de mi área y conservo el [estado publicado anterior](../estado-2026-10-19.md).

## Conclusión de esta investigación

Puedo avanzar con datos sintéticos, fallas controladas y reproducción de mensajes antes de conectar la placa. La oportunidad más sólida que identifico es una estación que explique la calidad y la procedencia del dato y que permita comprobar sus avisos frente a fallas conocidas. Para sostenerlo necesito comparar el comportamiento actual con la mejora y medir detecciones, demoras y falsas alarmas.

No presento el enfoque como una invención mundial ni como una innovación ya validada por CONAE. Hay antecedentes de monitoreo e inyección de fallas. Mi posible aporte sería la implementación y evaluación reproducible adaptada a nuestra misión. La valoración como innovación del concurso sigue pendiente de los criterios oficiales aplicables.

## Qué comprobé ahora

Ejecuté [un sondeo reproducible](../../experiments/2026-10-19-prevencion/README.md) sobre el banco publicado, sin modificar sus fuentes. Conservo [JSON](../../evidence/2026-10-19-investigacion-prevencion/resultados.json) y [CSV](../../evidence/2026-10-19-investigacion-prevencion/resumen.csv), con fecha UTC y huellas de los módulos.

| Caso | Resultado observado | Consecuencia para el siguiente diseño |
| --- | --- | --- |
| Control nominal | Acepta 131 paquetes sintéticos | Tengo una referencia de funcionamiento básico. |
| Equipo ajeno | Rechaza el TEAM_ID ficticio distinto | El filtrado de aplicación existe; no prueba direccionamiento RF ni seguridad. |
| Salto de altura a 3000 m | El parser acepta el número | La forma del mensaje no alcanza para evaluar coherencia temporal. |
| Temperatura 999 °C | El parser acepta el número | Necesito rangos y contexto acordados; un extremo bien escrito no debe confundirse con una medición corroborada. |
| Giro 9999 °/s | El parser acepta el número | Necesito modelo real del sensor, escala y unidades; no fijo ese número como umbral. |
| Altura congelada | Acepta 20 valores iguales mientras cambian 12 valores distintos de presión | Puedo investigar consistencia y congelamiento; eso no identifica por sí solo qué componente falló. |
| Hora de misión congelada | Acepta 10 paquetes con la misma hora y contador creciente | Puedo comprobar avance temporal además del formato de la hora. |
| Mismo contador con contenido distinto | Cuenta un duplicado y conserva ambos raw; no avisa específicamente la contradicción | Conviene distinguir retransmisión idéntica de mensajes conflictivos. |
| Contador que vuelve al inicio | Avisa ambigüedad; recibe 12 paquetes y mantiene latest en 106 | Necesito distinguir sesión y antigüedad del dato mostrado; no reinicio contadores automáticamente. |
| Excepción al escribir raw | El worker termina con ERROR antes de contar una recepción | Investigar continuidad degradada, cola durable y errores por destino es trabajo prioritario. |

Los tres valores extremos y los dos congelamientos son entradas deliberadas, no medidas reales. El parser cumple una función de estructura; este sondeo no demuestra que todas las alarmas deban vivir dentro del parser. Propongo conservarlo separado del análisis de calidad.

## 1. Calidad de datos explicada — primera mejora propuesta

Quiero poder indicar «reciente», «retenido», «sospechoso» o «sin datos» junto al motivo. Por ejemplo: «siguen llegando paquetes, pero la hora de misión no avanza» o «la altura mostrada pertenece a la sesión anterior». Conservo el paquete original y registro el diagnóstico en un archivo de análisis aparte. No corrijo ni relleno mediciones sin dejar constancia.

Distingo tres tiempos: llegada a la PC, emisión y medición del sensor. El primero puede medirse aquí; los otros necesitan datos y semántica acordados con vuelo. No deduzco que un sensor está actualizado solo porque recibí un paquete recién. Tampoco asigno un porcentaje de confianza sin calibración.

Primero evaluaría reglas sencillas y visibles; no necesito entrenar un modelo con datos ficticios para llamarlo inteligente. Compararía escenarios etiquetados y separados entre desarrollo y evaluación. Mediría tiempo hasta el aviso, anomalías omitidas, falsas alarmas y duración de datos ambiguos mostrados como actuales. No fijé umbrales operativos: dependen de sensores, fases y acuerdos de interfaz.

La presión y la altura barométrica pueden venir del mismo sensor; su comparación es de consistencia, no una redundancia independiente. Un valor constante puede ser correcto en plataforma. Un salto real o un cambio de fase tampoco debe disparar una conclusión automática de falla.

## 2. Campaña de fallas repetible — soporte de la mejora

Puedo variar pérdidas aisladas y por ráfagas, retrasos, duplicados idénticos y conflictivos, fragmentación, mensajes ajenos, horas congeladas, reinicios y saturación. Registro exactamente qué inyecté y cuándo, con semilla cuando haya azar. Esa verdad del experimento permite comparar el antes y el después sin elegir solo ejemplos favorables.

La estación v04 ya tiene fallas simuladas y reproducción de sesiones. Aprovecho ese antecedente en vez de presentarlo como una función inventada hoy. El banco USB actual necesita su propia reproducción verificable y campañas más amplias. No implementé esa integración en esta investigación.

## 3. Conservación de datos frente a fallos de la computadora

Puedo ensayar excepciones por escritura, respaldo no disponible, lentitud y terminación de un proceso propio, usando directorios temporales. Compararía paquetes entregados al programa, confirmados por cada destino y recuperados al volver a abrir. Así separo «recibido» de «guardado» y de «recuperable».

El sondeo confirma una ruta donde un fallo raw termina el worker. La mejora debería definir qué sigue funcionando si falla un destino, cómo se avisa y cómo se recupera una cola. No puedo prometer pérdida cero si se corta la energía antes de persistir o fallan todos los soportes. Dos directorios de prueba no certifican independencia física ni resistencia real a cortes.

## 4. Simulador de misión útil para verificar

Antes de usar sus gráficos para el PDR, necesito corregir y documentar el perfil de descenso del banco. C3 del anexo v2 conserva el tramo de 15 ± 3 m/s; el perfil actual no demuestra ese régimen sostenido. Ensayaría alturas, presión, eventos y tiempos consistentes, con controles en los límites y configuración declarada.

La simulación física es un modelo bajo supuestos, no un vuelo comprobado. Las condiciones y eventos que necesiten acuerdo de vuelo quedan pendientes. Tampoco cierro dos horas de autonomía ejecutando dos horas de mensajes de manera acelerada: eso solo probaría procesamiento.

## 5. Ensayo de operación y de comandos en dos programas de PC

Puedo separar un emisor de práctica y la estación, simular conexión y cortes, y ensayar comandos pendientes sin accionar hardware. Distingo orden enviada, recibida, rechazada y ejecución ficticia confirmada; no cuento un eco como actuación física. El formato final sigue pendiente del ICD con Edu.

pySerial ofrece loop:// para eco local en pruebas. No lo confundo con un CanSat simulado completo ni con USB físico. Además, el banco actual abre serial.Serial; usar ese manejador requiere un adaptador de prueba o cambiar explícitamente la fábrica de conexiones. No afirmo que pasar loop:// como argumento ya funcione en el código actual.

Con los mismos escenarios puedo entrenar al operador: mostrar una falla sin revelar la etiqueta y medir cuánto tarda en reconocerla y qué decisión toma. Conservo condiciones comparables y tamaño del ensayo; no concluyo una mejora humana a partir de una única demostración.

## 6. Aporte experimental con datos de despliegue

Puedo preparar el análisis que más adelante relacione eventos de despliegue, altura, descenso y giro con video o contacto independiente. Ahora puedo probar los cálculos y comprobar si recuperan eventos sintéticos con tiempos conocidos. Con hardware necesitaré evidencia independiente, sincronización y comparación entre ensayos para atribuir cambios al mecanismo.

Esto permite investigar una contribución científica de mi área además de la robustez del software. No declaro despliegue físico exitoso a partir de un cambio de estado del simulador.

## Prioridad que propongo

Primero resolvería las rutas de pérdida de registro y la identificación de datos actuales; después desarrollaría el monitor de calidad y su campaña de evaluación. En paralelo corregiría el perfil de misión. Dejaría la predicción de lugar de aterrizaje para una investigación posterior: necesita supuestos de viento, descenso, incertidumbre y posición que todavía no están validados.

Esta entrada documenta trabajo de investigación realizado y propuestas. No creo tareas nuevas ni paso ideas a En curso por el solo hecho de mencionarlas. ASTRA-21 conserva el trabajo de análisis actual; las implementaciones propuestas siguen pendientes de selección.

## Fuentes y alcance

- [NASA Ames: General Purpose Data-Driven Monitoring for Space Operations, 2009](https://ntrs.nasa.gov/citations/20090037065): antecedente de monitoreo e inyección controlada; plantea inicialmente informar al operador sin actuación correctiva automática. Lo uso como antecedente técnico, no como requisito CONAE ni validación de nuestro sistema.
- [pySerial: URL Handlers](https://pyserial.readthedocs.io/en/latest/url_handlers.html): comportamiento documentado de loop:// para pruebas de eco local.
- [Comparación v1/v2 de groundstation](../requisitos/v1-v2-groundstation-2026-10-19.md) y [matriz de requisitos](../requisitos/matriz-groundstation-2026-10-19.json): referencia reglamentaria ya revisada, con C3 y G/F aplicables. No uso requisitos internacionales como obligaciones locales.

Las fuentes anteriores se consultaron o reutilizaron en la investigación del 19/10/2026. No hice una búsqueda exhaustiva de novedad mundial ni validé la clasificación de innovación ante el jurado.
