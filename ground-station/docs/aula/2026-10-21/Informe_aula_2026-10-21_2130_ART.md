# Aula CONAE — corte diario PARCIAL

Corte: 21/10/2026 21:30:25 ART. Diario: [ASTRA-38](https://astrateam2026.atlassian.net/browse/ASTRA-38). Cobertura: [ASTRA-37](https://astrateam2026.atlassian.net/browse/ASTRA-37).

## Qué pude comprobar hoy

No pude acceder al curso ni a la página oficial de ingreso: ambas navegaciones finalizaron por tiempo de espera. No ingresé credenciales, no cambié seguridad ni envié consultas o entregas. El fallo desde este acceso no demuestra que el sitio esté caído para todos. No puedo declarar el aula sin cambios ni confirmar sus mensajes, adjuntos o versiones actuales.

Leí las páginas públicas oficiales de [cronograma](https://www.argentina.gob.ar/ciencia/conae/cansat-argentina/requisitos-cansat-universitario/cronograma) y [cómo me inscribo](https://www.argentina.gob.ar/ciencia/conae/cansat-argentina/requisitos-cansat-universitario/como-me-inscribo). El cronograma mantiene PDR 17–21/11, selección 23–27/11, CDR 31/03 y 5–9/04, documentación ambiental 31/05 y campaña/PFR en junio. Conserva la referencia heredada a reunión del 14/10 y revisiones virtuales; no resuelve las diferencias con el aula. La página de inscripción conserva seguimiento por aula y anexo v2 del 16/10. No revalidé sus descargas binarias.

El [último corte con acceso](../2026-10-20/Informe_aula_2026-10-20_2103_ART.md) fue el 20/10 a las 21:03: once debates, 19 mensajes y cuatro preguntas nuevas sin respuesta en aquel momento. Esos números no son un relevamiento de hoy.

## Prioridad inmediata: recuperar cobertura — alta

Necesito retomar lectura completa de secciones, foros y adjuntos, entrega/calendario y archivos cuando vuelva el acceso. Hasta entonces mantengo las decisiones pendientes y no cierro requisitos por ausencia de novedades observables. El material del vector/perfiles estaba anunciado al corte anterior; hoy no pude saber si fue publicado. El [control de este corte](control-del-corte-2130-ART.json) enumera todos los faltantes.

## Panorama acumulado por prioridades

Los apartados siguientes conservan el estado documentado al **20/10/2026 21:03 ART**. Cada respuesta y pregunta es histórica: no pude revalidarla hoy. La prioridad es mi evaluación para groundstation, interfaz, pruebas y PDR. Conservo todo el contexto para que el informe se entienda sin confundirlo con novedades de hoy.

### 1. Promedio de velocidad de descenso — prioridad alta

Origen: Consulta de 050 SATERO. Fecha de la fuente: 20/10/2026 13:50. Estado registrado al corte anterior: NOVEDAD: pregunta sin respuesta oficial. **No revalidado hoy.**

Pregunta/publicación: Si los 5 m/s son promedio del descenso completo, incluyendo el primer tramo a 15 m/s, o sólo de la segunda etapa.

Respuesta o estado conocido al 20/10: La pregunta no tiene respuesta al corte. La ventana de promedio sigue pendiente; sus cifras son parte de la consulta y no una nueva aclaración.

Por qué nos sirve: Condiciona cómo calculamos y demostramos la velocidad en simulación, gráficos y PDR.

Acción propuesta y pendiente: Conservar el cálculo por tramos y global como conceptos separados; no elegir una interpretación como confirmada ni cambiar el simulador desde esta revisión.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2967#p50100).

### 2. Liberación de paracaídas o partes — prioridad alta

Origen: Consulta de 001 ZENITH. Fecha de la fuente: 20/10/2026 16:08. Estado registrado al corte anterior: NOVEDAD: pregunta sin respuesta oficial. **No revalidado hoy.**

Pregunta/publicación: Si se permite desprender un paracaídas o componente, o todo debe regresar junto.

Respuesta o estado conocido al 20/10: Sin respuesta. Conservo la aclaración previa de conjunto unido; no la amplío automáticamente a todos los mecanismos de desprendimiento.

Por qué nos sirve: Afecta el estudio del rotor y la interpretación de eventos de recuperación, aunque el diseño mecánico pertenece a otra área.

Acción propuesta y pendiente: Mantener alternativas como hipótesis y seguir la respuesta; no dar por aprobado un desprendimiento.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2968#p50101).

### 3. PDR y comunicación simultánea en dos bandas — prioridad alta

Origen: Consulta de 042 AS SIDERA. Fecha de la fuente: 20/10/2026 18:04. Estado registrado al corte anterior: NOVEDAD: pregunta sin respuesta oficial. **No revalidado hoy.**

Pregunta/publicación: Si se presenta plantilla PDF justificada y/o video, qué significa carcasa y si pueden usar dos transmisores simultáneos en las bandas permitidas.

Respuesta o estado conocido al 20/10: Sin respuesta. La actividad vigente pide PDF y enlace de video; la pregunta no lo reemplaza. Tampoco concede permiso para dos radios.

Por qué nos sirve: Puede afectar entrega y arquitectura de comunicaciones; debe distinguirse de la respuesta anterior sobre transmisores auxiliares.

Acción propuesta y pendiente: Mantener PDF y video previstos, conservar las dos preguntas de radio como pendientes y no seleccionar otro transmisor ni perfil RF.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2969#p50102).

### 4. Entrega PDR: fecha inconsistente — prioridad alta

Origen: Actividad de entrega y cronograma público. Fecha de la fuente: Configuración observada en este corte. Estado registrado al corte anterior: Contradicción abierta; reobservada hoy. **No revalidado hoy.**

Pregunta/publicación: Qué entregamos, cómo y hasta cuándo.

Respuesta o estado conocido al 20/10: La actividad pide un PDF llamado username - PDR y un enlace al video. Su texto dice 17–21/11, hasta las 23:59; la configuración sigue mostrando apertura y vencimiento el 17/11 a las 00:00.

Por qué nos sirve: La discrepancia puede afectar la entrega aunque el documento esté listo. Es un problema de plazo, no una mejora opcional de software.

Acción propuesta y pendiente: Planificar con margen y dejar preparada la consulta sobre la configuración; no asumir que el formulario estará abierto hasta el 21 ni enviar nada desde esta revisión.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/assign/view.php?id=5467).

### 5. Comandos desde tierra: aclaración acumulada — prioridad alta

Origen: Consulta del equipo 006. Fecha de la fuente: 20/10/2026 08:28, fecha mostrada por el aula. Estado registrado al corte anterior: Respondido; acumulado del corte 11:56, revalidado en este corte. **No revalidado hoy.**

Pregunta/publicación: Si todas las acciones deben ser autónomas o pueden enviarse órdenes desde la estación.

Respuesta o estado conocido al 20/10: CONAE permite comandos para acciones específicas si justificamos su uso y cumplimos los requisitos de misión primaria.

Por qué nos sirve: Actualiza la pregunta que estaba sin respuesta el 19/10. Nos permite estudiar acciones concretas; no habilita a reemplazar cualquier automatismo de vuelo con intervención del operador.

Acción propuesta y pendiente: Llevar al acuerdo con Edu una lista de acciones, restricciones y confirmaciones; ensayar envío, recepción, rechazo y ejecución simulada como estados distintos en ASTRA-24. No elegir un formato unilateralmente.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2965#p50098).

### 6. Formato propio y destinatario de los paquetes — prioridad alta

Origen: Consultas de equipos 003 y 092. Fecha de la fuente: 19/10/2026. Estado registrado al corte anterior: Respondido; acumulado. **No revalidado hoy.**

Pregunta/publicación: Si la plantilla obliga a un formato heredado y cómo cumplir la prohibición de broadcast.

Respuesta o estado conocido al 20/10: El equipo define y justifica su telemetría; para X2 alcanza con dirección de destino según lo que definamos.

Por qué nos sirve: El formato fijo de nuestro banco es provisional. Filtrar por equipo en la aplicación no evita que la antena reciba otras señales ni constituye cifrado.

Acción propuesta y pendiente: Documentar con Edu campos, unidades, origen/destino y descartes en ASTRA-18/24; conservar el banco de prueba sin presentarlo como requisito CONAE.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2963#p50093).

### 7. Inicio de misión y ascenso — prioridad alta

Origen: Consulta del equipo 003. Fecha de la fuente: 19/10/2026. Estado registrado al corte anterior: Respondido; acumulado. **No revalidado hoy.**

Pregunta/publicación: Quién genera el inicio de misión y si se puede transmitir antes.

Respuesta o estado conocido al 20/10: El CanSat detecta la separación real y envía el comienzo de misión; la telemetría puede transmitirse durante el ascenso.

Por qué nos sirve: Aclara la dirección del evento X3. No debemos hacer depender ese evento real de un botón de la PC ni interpretar el primer paquete como separación por sí solo.

Acción propuesta y pendiente: Separar recepción del evento, fase de vuelo y antigüedad del dato; acordar semántica y pruebas de simulación con vuelo en ASTRA-20/24.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2960#p50090).

### 8. Envolvente y continuidad física del conjunto — prioridad alta

Origen: Consulta del equipo 092. Fecha de la fuente: 19/10/2026. Estado registrado al corte anterior: Respondido; acumulado. **No revalidado hoy.**

Pregunta/publicación: Si se separa la carga útil y qué medidas rigen.

Respuesta o estado conocido al 20/10: La respuesta fija conjunto unido y envolvente máxima total de 90 mm × 200 mm.

Por qué nos sirve: La grabación y otros textos contienen diferencias ya documentadas. Esta respuesta posterior condiciona la interpretación de nuestro estudio del rotor; no es una aprobación de un mecanismo concreto.

Acción propuesta y pendiente: Mantener la contradicción trazada, usar la aclaración para estudiar compatibilidad y esperar el plano del vector. No modificar tareas de estructura o vuelo desde mi área.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2963#p50093).

### 9. Vector y ensayos ambientales anunciados — prioridad alta

Origen: Consultas de equipos 003 y 023. Fecha de la fuente: 19/10/2026. Estado registrado al corte anterior: Anunciado; todavía no publicado al corte. **No revalidado hoy.**

Pregunta/publicación: Plano de integración, curva de impulso y perfiles de choque/vibración.

Respuesta o estado conocido al 20/10: CONAE anunció documentación del vector y de ensayos para esta semana; no aparece un recurso nuevo con esos documentos en el curso revisado.

Por qué nos sirve: Sin esos perfiles no podemos justificar que un ensayo inventado verifica el requisito. Sin curva del vector, el perfil de ascenso del simulador seguirá siendo un supuesto.

Acción propuesta y pendiente: Seguir estos dos documentos como pendientes y actualizar simulación/ensayos sólo al disponer de sus fuentes; no importar perfiles internacionales como obligaciones locales.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2964#p50096).

### 10. Incerteza, apogeo y referencia de altura — prioridad alta

Origen: Consultas de equipos 003 y 023. Fecha de la fuente: 16/10/2026; repregunta del 19/10. Estado registrado al corte anterior: Parcial: falta respuesta a p50094. **No revalidado hoy.**

Pregunta/publicación: Precisión exigida, referencia barométrica/GPS, tramo de promedios y umbrales restantes.

Respuesta o estado conocido al 20/10: CONAE remite precisión a sensores/calibración, indica cero barométrico en lanzamiento y considera ambos datos de altura. Para apogeo responde ±2 m. La repregunta por una tabla completa sigue sin respuesta.

Por qué nos sirve: Una gráfica con valores razonables no acredita precisión. Barómetro y GPS deben identificarse con referencia y validez; no intercambiamos sus alturas sin contexto.

Acción propuesta y pendiente: Conservar unidades/referencia, datos originales y calibración. Dejar TBR la ventana para promediar velocidades y los umbrales no aclarados; no aplicar ±2 m a todos los sensores.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2959#p50085).

### 11. Planilla de evaluación y plantilla PDR — prioridad alta

Origen: Archivos del aula ya auditados. Fecha de la fuente: Archivos revalidados hoy; auditoría del 19/10. Estado registrado al corte anterior: Análisis propio previo; aclaración oficial pendiente. **No revalidado hoy.**

Pregunta/publicación: Qué pide cada ítem y si la planilla permite reproducir el puntaje.

Respuesta o estado conocido al 20/10: No hay respuesta oficial nueva sobre las inconsistencias detectadas. Los cuatro archivos conservan sus huellas.

Por qué nos sirve: Hay criterios y filas ocultas heredadas; G2 usa dos columnas de jurado aunque existe una tercera. El audio habla de tres evaluadores. La plantilla no debe reemplazar al anexo y sus aclaraciones.

Acción propuesta y pendiente: Usar la auditoría anterior para preparar preguntas y mapear evidencia de tierra. No corregir la planilla oficial ni declarar un puntaje validado. La excepción de calidad hasta 10 está corroborada en la apertura.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/resource/view.php?id=5466).

### 12. Recuperación de carcasa y fibra de vidrio — prioridad media

Origen: Consulta de 109 CALLISTERNIANOS. Fecha de la fuente: 20/10/2026 12:54. Estado registrado al corte anterior: NOVEDAD: pregunta sin respuesta oficial. **No revalidado hoy.**

Pregunta/publicación: Si la carcasa debe recuperarse junto al CanSat y si puede fabricarse con fibra de vidrio.

Respuesta o estado conocido al 20/10: Sin respuesta específica. La libertad de otros materiales del 19/10 sigue condicionada a cumplir requisitos; no aprueba por sí sola este diseño.

Por qué nos sirve: Permite seguir una duda relacionada con envolvente/recuperación sin invadir decisiones de estructura.

Acción propuesta y pendiente: Enlazar la consulta y esperar aclaración; no convertir una pregunta de otro equipo en una decisión nuestra.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2966#p50099).

### 13. Espera en rampa y energía — prioridad media

Origen: Consulta del equipo 003. Fecha de la fuente: 19/10/2026. Estado registrado al corte anterior: Respondido; acumulado. **No revalidado hoy.**

Pregunta/publicación: Qué significa STAND-BY y qué actividad se espera durante las dos horas.

Respuesta o estado conocido al 20/10: Espera con CanSat activado y consumo mínimo; no exige transmitir continuamente y la cámara depende de la opción adoptada.

Por qué nos sirve: No confundir autonomía eléctrica con procesar 7200 mensajes en segundos. La estación debe distinguir espera prevista de pérdida inesperada de enlace.

Acción propuesta y pendiente: Definir fases y avisos con el equipo; conservar como pendientes los ensayos físicos de consumo y energía. No dar por eliminadas las exigencias de autonomía.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2960#p50090).

### 14. Segundo sistema de descenso — prioridad media

Origen: Consultas de equipos 003 y 092. Fecha de la fuente: 19/10/2026. Estado registrado al corte anterior: Respondido; acumulado. **No revalidado hoy.**

Pregunta/publicación: Si tiene que ser un parapente o puede ser otro mecanismo.

Respuesta o estado conocido al 20/10: Admiten un sistema activo o pasivo y un segundo paracaídas.

Por qué nos sirve: Podemos investigar autorrotación sin que eso la convierta en la mejor alternativa ni en misión aprobada. Debe ser compatible con el conjunto unido y la expulsión.

Acción propuesta y pendiente: Mantener rotor en ASTRA-36 y comparar beneficio, masa, riesgo y pruebas. Una propuesta no reemplaza la solución principal.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2961#p50091).

### 15. Altitud del vector y canal de radio — prioridad media

Origen: Consulta del equipo 092. Fecha de la fuente: 19/10/2026. Estado registrado al corte anterior: Respuesta parcial; sin canal asignado. **No revalidado hoy.**

Pregunta/publicación: Altitud de lanzamiento y posible canal asignado a cada equipo.

Respuesta o estado conocido al 20/10: Se esperan alturas superiores a 500 m e inferiores a 1 km. La respuesta no asigna canal ni publica un perfil RF final.

Por qué nos sirve: El rango orienta escenarios, pero no define un apogeo exacto, una frecuencia ni una configuración de radio.

Acción propuesta y pendiente: Mantener parámetros como acordados o TBD según la evidencia; no seleccionar frecuencia por una noticia o por el equipo ganador de otro certamen.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2963#p50093).

### 16. Transmisores auxiliares y señal del panel — prioridad media

Origen: Consulta del equipo 092. Fecha de la fuente: 19/10/2026. Estado registrado al corte anterior: Respondido; acumulado. **No revalidado hoy.**

Pregunta/publicación: Si se permiten otras radios y qué medir del panel solar.

Respuesta o estado conocido al 20/10: Sólo admiten los transmisores destinados a datos telemétricos; basta la tensión del panel, sin exigir carga de batería.

Por qué nos sirve: No proponer un enlace auxiliar fuera de lo permitido. La recepción necesita identificar la magnitud y sus unidades, sin inferir energía aprovechada por medir tensión.

Acción propuesta y pendiente: Incluir esa señal en el acuerdo de datos. Un experimento energético con rotor necesita medidas propias y no cumple por sí solo el requisito solar.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2963#p50093).

### 17. Qué debe demostrar el PDR — prioridad media

Origen: Entrada de la Etapa 2 y plantilla. Fecha de la fuente: 19/10/2026. Estado registrado al corte anterior: Entrada del curso; reobservada hoy. **No revalidado hoy.**

Pregunta/publicación: Qué nivel de definición esperan antes de pasar a diseño detallado.

Respuesta o estado conocido al 20/10: El aula pide comprensión de requisitos, asignación a subsistemas, concepto de operación, diseño, alternativas, prototipos/pruebas, presupuesto y cronograma.

Por qué nos sirve: Podemos mostrar pruebas de software y pendientes con evidencia; no necesitamos disfrazar un prototipo como sistema de vuelo terminado.

Acción propuesta y pendiente: Relacionar cada afirmación de groundstation con su requisito, versión, prueba y límite. Preparar el video con demostraciones propias y fuentes verificables.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/course/view.php?id=106#section-2).

### 18. Formato e idiomas de la presentación — prioridad media

Origen: Grabación oficial de apertura. Fecha de la fuente: Apertura del 16/10; analizada el 19/10. Estado registrado al corte anterior: Acumulado del análisis audiovisual del 19/10. **No revalidado hoy.**

Pregunta/publicación: Duración del video, idioma del documento y relato.

Respuesta o estado conocido al 20/10: La lectura asistida documentada del 19/10 identifica video de 10–20 minutos, documento en inglés y presentación oral en español; inglés oral permitido sin premio adicional.

Por qué nos sirve: Actualiza nuestro recuerdo de aproximadamente quince minutos. No confundir este resumen con una escucha nueva del audio hoy.

Acción propuesta y pendiente: Preparar guion con tiempo por demostración y verificar novedades antes de cerrar la entrega; conservar los límites de la transcripción asistida.

[Fuente estable](https://www.youtube.com/watch?v=m4-HQMSi2Wo).

### 19. Materiales y fabricación — prioridad informativa

Origen: Consulta del equipo 109. Fecha de la fuente: 19/10/2026. Estado registrado al corte anterior: Respondido; acumulado. **No revalidado hoy.**

Pregunta/publicación: Si la estructura tiene que fabricarse exclusivamente mediante impresión 3D.

Respuesta o estado conocido al 20/10: Pueden usarse otros materiales y técnicas si cumplen los requisitos.

Por qué nos sirve: Ayuda a comparar alternativas reales; la libertad de fabricación no prueba resistencia ni habilita trasladar a nuestra misión una solución de otro certamen.

Acción propuesta y pendiente: Conservar la referencia para nuestros análisis; las decisiones de estructura siguen en el área correspondiente.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2962#p50092).

### 20. Misión opcional y presupuesto — prioridad informativa

Origen: Consulta del equipo 092 y antecedente del 023. Fecha de la fuente: 19/10/2026. Estado registrado al corte anterior: Respondido; acumulado. **No revalidado hoy.**

Pregunta/publicación: Cómo se valora una misión adicional y qué costos se consideran.

Respuesta o estado conocido al 20/10: La misión opcional sirve para desempatar. En costo se incluyen envíos/impuestos; equipo existente se excluye y donaciones se estiman. La conversión indicada es dólar oficial del día del presupuesto.

Por qué nos sirve: No asignar al rotor una ventaja de puntaje garantizada. Conservo la aclaración de costos sin reabrir aquí el análisis de presupuesto que dejamos para después.

Acción propuesta y pendiente: Mantener la idea como investigación y justificarla por beneficio verificable. No cambiar presupuestos ni tareas de otros subsistemas.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/discuss.php?d=2963#p50093).

### 21. Avisos y presentación de equipos — prioridad informativa

Origen: Foros del curso. Fecha de la fuente: 19/10/2026. Estado registrado al corte anterior: Sin publicaciones al corte. **No revalidado hoy.**

Pregunta/publicación: Si hay anuncios o presentaciones nuevas fuera del foro técnico.

Respuesta o estado conocido al 20/10: Avisos muestra que no hay novedades; el foro de presentaciones sigue sin temas.

Por qué nos sirve: Deja constancia de que miramos ambos espacios y no sólo las consultas técnicas.

Acción propuesta y pendiente: Revisarlos cada día y registrar cualquier publicación nueva con su fuente, aunque no tenga forma de pregunta.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/mod/forum/view.php?id=5134).

### 22. Bienvenida e institucional — prioridad informativa

Origen: Sección General. Fecha de la fuente: 19/10/2026. Estado registrado al corte anterior: Acumulado; referencia visible, audio no reprocesado hoy. **No revalidado hoy.**

Pregunta/publicación: Qué aporta el video institucional y la descripción de la convocatoria.

Respuesta o estado conocido al 20/10: La sección introduce el certamen; el análisis audiovisual anterior documenta misiones, centros y actividades CONAE, sin parámetros nuevos de nuestra radio.

Por qué nos sirve: Aporta contexto para el relato del proyecto; no demuestra alcance, frecuencia o prestaciones de ASTRA.

Acción propuesta y pendiente: Enlazar como contexto y conservar el inventario. No republicar una grabación completa ni presentarla como prueba nuestra.

[Fuente estable](https://educacion.conae.gov.ar/aulavirtual/course/view.php?id=106#section-0).

## Contradicciones y preguntas abiertas heredadas

Conservo la diferencia de plazo: el texto de entrega decía hasta el 21/11 23:59 y la configuración/calendario señalaban 17/11 00:00. Conservo diferencias de envolvente y los problemas de fórmulas/criterios heredados de la planilla ya documentados. Hoy no hay evidencia para afirmar que persisten o que fueron corregidos. No cambio fuentes ni presupuestos para resolverlas artificialmente.

Las cuatro consultas del 20/10 sobre carcasa/fibra de vidrio, promedio de descenso, desprendimientos y PDR/dos transmisores quedan como **respuesta actual desconocida** por falta de acceso. Eliminar Net ID de la v1 no concede broadcast ni fija direccionamiento/perfil RF; no adopto configuraciones por iniciativa de esta revisión.

## Investigación complementaria de esta ejecución

Analicé una ficha de COSMOS 2025, con CSV y módulo de comunicación publicados por sus autores, y observé su captura de GCS. El [informe y métricas](../../investigacion/2026-10-21-cosmos-csv-y-estacion.md) distingue huecos observados de pérdidas RF, datos GPS ausentes y límites de la evidencia. Es un antecedente extranjero, no un requisito CONAE ni un ensayo propio de ASTRA.

## Límites del corte

No se revisaron hoy cuerpos de mensajes del aula, archivos, nuevos adjuntos, calendario, entrega ni grabaciones. Los audiovisuales conservan el análisis asistido del 19/10 y sus límites; no presento esa herencia como escucha nueva. No afirmo 100% ni corte sin novedades. Conservo todos los informes previos y el siguiente corte deberá comparar desde la última lectura válida, no desde esta falla.
