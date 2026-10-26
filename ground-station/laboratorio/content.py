"""ASTRA-41: guion de reunión, evidencia y límites dentro de la aplicación."""
CHAPTERS = [
('Recorrido', 'De una placa a un laboratorio de pruebas',
'''Estamos construyendo la parte de tierra: recibir lo que envía el CanSat, entenderlo, guardarlo y saber cuándo algo salió mal. El Laboratorio reúne las demostraciones y las explicaciones para discutir avances con evidencia.

Recorrido sugerido de 8–10 minutos:
1. Telemetría: iniciar una misión nominal y observar el ascenso y descenso.
2. Repetir con pérdida de paquetes, datos corruptos o GPS ausente. Explicar qué detectamos y qué no podemos inferir.
3. Paquete: mostrar la línea que recibe la aplicación y sus 22 campos.
4. Cámaras: mostrar fotos conservadas y explicar cómo verificamos la tarjeta.
5. Radio LoRa: comparar 55, 100 y 255 bytes a distintos SF.
6. Recuperación: probar copias complementarias y después un conflicto.
7. Evidencias: cerrar con lo comprobado y los próximos ensayos. Diseño y PDR reúne el fundamento de los avances teóricos.

Cada prueba indica su origen. La simulación de PC sirve para probar el programa; los ensayos físicos anteriores conservan sus informes. No hace falta conectar placas para este recorrido.''',
'''Organización: el Laboratorio coordina módulos; el banco USB conserva receptor, parser, almacenamiento y GUI. La interfaz de vuelo y sus comandos los define Edu; adaptamos tierra al acuerdo compartido. ASTRA-41 registra esta integración. Las tareas técnicas y sus originales siguen en Jira.

Para el PDR: sirve como demostración y acceso a evidencia, no como certificado de cumplimiento de toda la misión. No hemos probado RF, vuelo ni autonomía mediante este recorrido.'''),
('Telemetría', 'Una misión inventada para probar problemas reales',
'''La telemetría es el conjunto de mediciones que nos cuenta qué está pasando. Aquí una PC hace de emisor y el receptor procesa sus mensajes con el mismo motor del banco USB.

Iniciá una misión. La altura sube y después baja. Probá otro escenario para ver huecos de contador, mensajes inválidos o GPS sin posición. Cada inicio crea registros nuevos; los anteriores se conservan.

Recibido, válido y guardado no significan lo mismo: podemos recibir texto que no entendemos, o entender una medición que todavía espera su escritura. Un paquete perdido en el enlace no es un paquete pendiente de guardar.

Nos aporta una forma repetible de revisar el receptor antes del vuelo. Para el PDR, acompaña pruebas de software; no demuestra alcance de radio ni sensores físicos.''',
'''Origen PC_BENCH, perfil bench-usb-0.2 y TEAM_ID ficticio 1000. Velocidad 5×: cada segundo simulado tarda aproximadamente 0,2 s reales, sin garantía de tiempo real. El modelo llega a 500 m y usa descenso ilustrativo de 15 y 5 m/s; no es una predicción de vuelo.

RESET de este emisor es una omisión lógica de muestras; no simula cortar alimentación ni acredita reconexión física. El banco completo contiene la prueba de identidad y reconexión USB. Las colas de escritura son acotadas; los errores y descartes se registran por destino. Los giros originales del perfil conocido se convierten de grados/s a rad/s para mostrarlos.'''),
('Paquete', 'Cómo se convierte una línea en mediciones',
'''Lo que usamos en el banco es una línea de texto: valores separados por comas y un final de línea. Cada posición tiene un significado. Al mover el tiempo podemos ver una muestra de otra etapa y cómo cambia su tamaño.

No dividimos esta línea en rangos fijos de bits. El formato binario de vuelo lo define Edu y después adaptamos el receptor. Reducir texto a números binarios puede ahorrar bytes, pero exige acordar escala, unidades, valores inválidos y versión.

Nos aporta una referencia concreta para conversar sobre la interfaz y evitar interpretar temperatura como presión. Para el PDR, respalda la explicación del banco; el contrato final sigue pendiente de acuerdo.''',
'''Perfil heredado de 22 campos ASCII, delimitador coma, terminador CR. El tamaño mostrado incluye ese terminador. La longitud es variable: signos, decimales, contador y estado cambian los bytes. @BENCH JSON transporta control/metadatos separado de la telemetría. No es el protocolo RF aprobado.

El dato mostrado en la tabla conserva la unidad original; en particular GYRO está en grados/s en este perfil. La pantalla de telemetría usa conversión explícita a rad/s. No extrapolo esa conversión a otro perfil desconocido.'''),
('Cámaras', 'Comprobar una foto antes de confiar en la grabación',
'''Las dos cámaras produjeron fotos y guardaron archivos en microSD. También retiramos la tarjeta y verificamos los archivos desde un lector independiente: no nos quedamos sólo con el aviso de la cámara.

Las imágenes de esta sección son evidencia conservada, con fecha y origen: no son una vista en vivo ni un chequeo nuevo. El panel físico permite pedir una captura por unidad cuando tengamos el equipo preparado.

Nos aporta un procedimiento para confirmar imagen y almacenamiento. Para el PDR, podemos respaldar fotos y lectura de tarjeta; no afirmar video continuo, audio, apagado total o autonomía. El arranque todavía requirió recuperación en los ensayos.''',
'''ESP32-CAM y sensor identificado en banco; control por USB y JPEG con longitud, CRC y decodificación comprobados. Dos unidades ensayadas por turnos con una tarjeta: no una prueba de simultaneidad. Nueve fotos verificadas desde el lector y 24 archivos anteriores intactos.

La política de energía y el disparador de grabación deben coordinarse con vuelo. Arranque estable, video, medición de consumo y circuito de corte siguen pendientes. No asumo micrófono instalado. El panel no cuenta una imagen antigua como nueva captura de la ronda.'''),
('Radio LoRa', 'Más bytes ocupan el aire durante más tiempo',
'''Una señal no tarda mucho más en recorrer la distancia por tener más bytes: lo que crece es el tiempo que la radio permanece transmitiendo. Ese tiempo afecta cuánto margen queda para órdenes, otras transmisiones y reintentos.

Compará 55, 100 y 255 bytes. Aumentar SF suele ayudar a recibir señales débiles, a cambio de transmisiones más largas. Eso no garantiza por sí solo menos pérdidas: también importan interferencia, antenas y configuración.

Nos aporta números reproducibles para elegir qué probar con Edu. Para el PDR permite justificar hipótesis; la confiabilidad y el consumo necesitan mediciones. No estamos eligiendo un perfil RF definitivo.''',
'''Cálculo de tiempo de aire LoRa con la fórmula de Semtech SX1276: cabecera explícita, CRC activo, preámbulo de 8 símbolos y optimización de baja tasa automática cuando el símbolo supera 16 ms. Se compara SF7/9/10/11/12; BW y CR son hipótesis modificables.

El payload debe incluir nuestros encabezados propios; no sumo de nuevo la cabecera física y CRC de la fórmula. 255 bytes es un máximo de payload del modo considerado, no una reserva que debamos rellenar. La ocupación a 1 Hz no incluye ACK, guardas, comandos ni reintentos y no autoriza potencia/régimen de emisión.

Pendiente: ensayar tasa de pérdidas, latencia, energía, distancia y condiciones con el módulo real. No deducimos esas magnitudes de esta calculadora.'''),
('Evidencias', 'Qué podemos demostrar y qué falta',
'''Comprobado en ensayos anteriores:
• Recepción física USB prolongada: 7261 paquetes durante aproximadamente 2 h 1 min. Eso no acredita batería ni radio.
• Fotos de ambas cámaras y lectura independiente de nueve archivos desde microSD. Las unidades se probaron por turnos.
• Escenarios de software, detección de conflictos y reconstrucción conservando originales, con sus controles de aceptación.

En este Laboratorio: simulación de PC y cálculo LoRa. Los informes detallan condiciones, versiones y límites; una pantalla bonita no reemplaza esos registros.

Próximos pasos: arranque estable y video de cámaras, interfaz/comandos acordados con Edu, radio real, antenas, presupuesto de enlace y ensayos comparables. El rotor y generación de energía siguen como investigación separada.

Ante una pregunta que todavía no resolvimos, mostramos el pendiente en vez de presentar una hipótesis como prueba.''',
'''La reconstrucción usa identidad de sesión/segmento y procedencia por registro; si dos fuentes discrepan bloquea la salida automática. No puede recuperar información ausente en todas las fuentes. Dos carpetas en un disco no acreditan respaldo en soportes independientes.

Fuentes de la reunión: aceptación USB del 24/10; campaña de cámaras del 26/10; matriz de 108 hipótesis LoRa del 26/10. Las mediciones originales no se reejecutan ni modifican al abrir esta aplicación. Los vínculos al repositorio conservan el detalle; el texto necesario para presentar está disponible sin Internet.''')]

CHAPTERS.append(('Diseño y PDR', 'Lo que aprendimos también cuenta como avance',
'''Antecedentes: estudiamos documentación de otras estaciones para convertir sus decisiones en pruebas propias. Separar recepción y archivo, conservar el dato original y probar fallos son ideas útiles aunque no se vean como una función nueva. Que un equipo haya ganado no prueba todas las funciones de su diseño.

Antenas: una antena que cubre alrededor puede exigir menos seguimiento; una direccional puede concentrar más la recepción, pero hay que apuntarla. Comparamos candidatas y preparamos el cálculo del enlace. Todavía no demostramos alcance ni elegimos una antena final.

Rotor: producir electricidad durante el descenso es una idea para investigar. El beneficio depende de cuánta energía recuperamos menos lo que agregamos de consumo, masa y riesgo. Una hélice girando o un pico de tensión no demuestra energía útil ni innovación mundial.

Requisitos: conservamos la comparación v1/v2 y su procedencia. Quitar Net ID no autoriza broadcast. La línea ASCII del banco no es automáticamente el formato obligatorio de vuelo. Edu define el empaquetado y los comandos; adaptamos tierra.

Para el PDR esto aporta razones, alternativas y planes de verificación. Presentamos por separado requisito, propuesta y evidencia. El Laboratorio facilita explicarlo; no sustituye la matriz de cumplimiento ni los ensayos de vuelo.''',
'''Antecedentes: fichas de ITBA/Daedalus, código PWr/COSMOS y análisis RSX conservan páginas, fuentes, resultados y límites de lectura. No afirmamos auditoría completa de todos los competidores. El informe del 23/10 conserva su estado de ese corte; la recepción USB prolongada posterior se acredita con su propio informe del 24/10.

Antenas candidatas documentadas: Taoglas OMB.915.B05F21 y Digi A09-Y11NF. Ganancias de catálogo no equivalen a alcance. Presupuesto preliminar exige pérdidas, orientación, sensibilidad/perfil, altura, distancia y márgenes; entradas desconocidas continúan TBD/TBR.

Rotor: modelo limitado E=η·m·g·h; tiempo h/v; consumo adicional Pextra·(tiempo+espera). Con masa hipotética 0,5 kg, tramo 400 m y eficiencia 10 %, la escala eléctrica es 0,054481 Wh. No es medición: faltan aerodinámica, despliegue, generador y carga. La espera de electrónica adicional puede volver negativo el balance. No sustituye recuperación ni autonomía antes del descenso.

Referencia histórica de requisitos: análisis del 19/10 sobre anexo v2, G1–G15 para estación y X4 para 1 Hz. El emisor acelerado del Laboratorio no acredita cadencia física. Debemos revalidar cualquier aclaración oficial posterior y conservar contradicciones sin resolverlas por intuición.'''))

CHAPTERS.insert(5,('Recuperación','Recuperar lo que existe, sin inventar lo que falta',
'''Guardar dos copias puede ayudarnos cuando una queda incompleta. Esta demostración crea dos archivos ficticios con partes de diez mediciones y usa nuestro recuperador para compararlos.

Complementarias: a cada archivo le faltan datos distintos; entre ambos podemos reconstruir las diez mediciones.
Ausente en ambas: una medición no aparece en ninguna fuente. Recuperamos nueve y mostramos que falta una; no la inventamos.
Conflicto: dos versiones del mismo contador dicen cosas distintas. Bloqueamos la reconstrucción automática para que nadie tome una elección silenciosa como dato verdadero.

Cada clic conserva fuentes nuevas, resultado y procedencia. Son carpetas en el mismo disco: esto prueba el algoritmo, no la independencia de dos soportes. Nos aporta una demostración del criterio de recuperación para el PDR; el respaldo físico necesita su propia evidencia.''',
'''Reutilizo recover.py del banco USB. La identidad incluye sesión de PC, segmento, equipo y contador; no mezclo vuelos diferentes. Verifico las huellas de las fuentes antes y después, y genero CSV y provenance.jsonl únicamente cuando no hay conflictos ni errores de lectura.

El número esperado de diez muestras lo conocemos porque construimos este escenario sintético. En una captura real no siempre sabemos cuántas se emitieron: no inferimos pérdidas durante un corte sin identidad/contador suficientes. La reconstrucción no calcula valores faltantes ni sobrescribe las fuentes. El caso ausente en ambas permite crear un CSV parcial; eso no significa que la misión esté completa.'''))

REPORTS = [
('Ensayo USB prolongado', 'docs/2026-10-24-aceptacion-banco-usb-actualizacion-09.md'),
('Fotos verificadas desde el lector', 'docs/camaras/2026-10-26-lector-campana-panel-12.md'),
('Chequeo por turnos y límites', 'docs/camaras/2026-10-26-panel-ambas-camaras-11.md'),
('Comparación LoRa y fuentes', 'docs/interfaces/2026-10-26-payload-sf-confiabilidad-04.md'),
('Objetivo y prioridades', 'docs/historial/2026-10-26-objetivo-laboratorio.md'),
('Requisitos v1/v2 de mi área', 'docs/requisitos/v1-v2-groundstation-2026-10-19.md'),
('Antecedentes convertidos en pruebas', 'docs/investigacion/2026-10-23-antecedentes-a-pruebas.md'),
('Antenas y presupuesto de enlace', 'docs/interfaces/2026-10-23-antenas-y-link-budget-preliminar.md'),
('Rotor: energía incremental y límites', 'docs/investigacion/2026-10-24-rotor-energia-incremental.md')]
