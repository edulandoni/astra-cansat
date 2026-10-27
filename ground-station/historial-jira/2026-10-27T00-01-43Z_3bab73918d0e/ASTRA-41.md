# ASTRA-41 — LAB — Integrar Laboratorio de demostraciones y guía de avances para reuniones

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-41)

Estado observado: En curso. Asignación: Cristian Ponsone. Creación: Cristian Ponsone.

## Descripción original consultada

Preparo un Laboratorio nativo para la reunión: una entrada común para demostrar telemetría, fallos, paquetes, cámaras, recuperación y comparación LoRa, con explicaciones accesibles seguidas de detalles/fuentes y alcance verificado. Las funciones con hardware quedan a demanda; la reunión debe poder recorrerse sin placas ni Internet. Conservo los bancos existentes y sus registros; no cambio firmware ni configuro RF durante esta integración.

Prioridad actual: el Laboratorio y un recorrido de demostración para la reunión. Video/audio/energía de cámaras quedan en segundo plano en ASTRA-39, sin dar ese trabajo por completado. ASTRA-40 conserva la evaluación LoRa; Edu define formato y comandos de vuelo.

Entregables: aplicación ejecutable desde un acceso claro, módulos interactivos de simulación y cálculos, evidencias reales privadas consultables cuando existan, guía integrada para explicar avances, límites y próximos ensayos; pruebas de operación sin hardware, cierre limpio y recorrido visual. Cada evidencia debe identificarse como cálculo, simulación, ensayo físico o pendiente. No afirmar RF, video, sonido o consumo a partir de demos.

Registraré aquí integración, navegación, uso en reunión y validación. Los avances técnicos de cada subsistema conservan sus tareas temáticas. Trabajo en groundstation y sólo ground-station/, escribiendo como parte del equipo y conservando el diario.

## Comentarios conservados

### 2026-10-26T03:09:40.573-0300 — comentario 10186

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-41?focusedCommentId=10186). Última edición informada: 2026-10-26T03:09:40.573-0300.

26/10/2026 — COMENTARIO 1: Laboratorio como objetivo primario y primera entrega

Priorizo el Laboratorio para facilitar las reuniones: reúno demostraciones y avances teóricos en una aplicación nativa. Cada tema explica qué nos aporta, por qué lo hicimos, qué evidencia ofrece para el PDR y sus límites; debajo queda el fundamento técnico. Cámaras continúa como objetivo secundario en ASTRA-39/24, sin dar por probados video, apagado, consumo, audio o tolerancia a reset.

Implementé siete secciones: recorrido de 8–10 minutos, telemetría con cinco escenarios, inspección de los 22 campos ASCII, fotos conservadas de ambas cámaras, cálculo LoRa, informes/evidencias y diseño/PDR (antecedentes, antenas, rotor y requisitos). Conservo los bancos existentes, accesibles como ventanas independientes. Abrir el Laboratorio no abre puertos ni carga firmware. Recepción USB exige elegir una placa explícitamente; no la probé físicamente en esta integración.

Probé cinco misiones completas con el motor real del receptor y registros nuevos: NOMINAL 131 válidos/0 inválidos/0 huecos; PACKET_LOSS 118/0/13; CORRUPTED_PACKET 121/10/10; GPS_LOSS 131/0/0; RESET lógico 128/0/3. Los escritores cerraron con cero pendientes/descartes. Dos pruebas integradas pasaron; además construí las siete secciones y comprobé los nueve informes locales. En la revisión visual observé misión, gráfico/contadores, fotos conservadas, paquete, calculadora y detalle desplegable. La misión iniciada desde la interfaz conservó 131 filas CSV y 676 eventos, sin errores al cierre. No es una campaña física nueva ni una prueba de tiempo real: la simulación está acelerada y RESET es lógico.

Dejé el acceso «ASTRA Laboratorio» en el escritorio de la notebook, con configuración privada de fotos/registro; no publiqué imágenes nuevas ni identificadores físicos. No es un ejecutable autónomo para otra PC. El recorrido, las explicaciones y los cálculos funcionan sin placas ni Internet; el enlace externo del fabricante requiere conexión.

Código y procedimiento: https://github.com/edulandoni/astra-cansat/tree/13352165b57d64c5ed83da766f3f827ce479b4a5/ground-station/laboratorio  
Commit verificado: https://github.com/edulandoni/astra-cansat/commit/13352165b57d64c5ed83da766f3f827ce479b4a5  
Informe con resultados y límites: https://drive.google.com/file/d/1MobNYM58CQbzmqpIkS4-IG8oGJBv2oiz/view  
Objetivo vigente: https://github.com/edulandoni/astra-cansat/blob/13352165b57d64c5ed83da766f3f827ce479b4a5/ground-station/docs/historial/2026-10-26-objetivo-laboratorio.md

Para el PDR puedo mostrar software, cálculos y acceso a evidencia previa; no afirmar cumplimiento total, RF, autonomía o grabación. Pendientes: recorrerlo con el equipo, probar controles físicos cuando estemos disponibles y mantener contenido/fuentes al incorporar avances. No modifico tareas ajenas ni cierro dependencias de vuelo.

### 2026-10-26T03:16:25.180-0300 — comentario 10187

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-41?focusedCommentId=10187). Última edición informada: 2026-10-26T03:16:25.180-0300.

26/10/2026 — ACTUALIZACIÓN COMENTARIO 1 / COMENTARIO 2: recuperación interactiva y gráfico

Amplié el Laboratorio a ocho secciones con Recuperación. Creo dos fuentes sintéticas nuevas y ejecuto el recuperador del banco: copias complementarias reconstruyen diez registros; una medición ausente en ambas deja nueve sin inventarla; una discrepancia bloquea la salida y no genera CSV. Los originales conservan sus huellas y los resultados registran procedencia. Son dos archivos en el mismo disco: no acredita soportes independientes ni recuperación de información que nunca llegó.

Corregí el gráfico de la primera integración: tomaba sólo el último valor de cada refresco y podía unir contadores faltantes. Ahora dreno la cola acotada de muestras, conservo contador/segmento y separo las líneas ante huecos o identidad distinta. Mantengo la ventana de 180 muestras.

Pasaron cuatro pruebas de integración (incluidas las cinco misiones completas y recuperación/conflictos/procedencia) y dos pruebas nativas de cierre durante misión y durante recuperación. Desde la pantalla ejecuté el caso complementario: diez datos, cero conflictos, originales intactos. No abrí puertos ni hice ensayos físicos nuevos. El acceso del escritorio utiliza esta versión.

Commit remoto verificado: https://github.com/edulandoni/astra-cansat/commit/fdc68972b7a687014e2c325902362bc58852f4ce  
Informe nuevo conservando el anterior: https://drive.google.com/file/d/1zNG1wWPL61U5WK0WpejZQyZwQRUagNqW/view  
Código/procedimiento: https://github.com/edulandoni/astra-cansat/tree/fdc68972b7a687014e2c325902362bc58852f4ce/ground-station/laboratorio

Puedo demostrar recuperación del algoritmo y sus límites para el PDR. Falta revisar el recorrido con el equipo; cámaras mantiene sus pendientes de arranque, video y energía en segundo plano, y RF requiere hardware y acuerdo con Edu.

### 2026-10-26T03:26:42.483-0300 — comentario 10189

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-41?focusedCommentId=10189). Última edición informada: 2026-10-26T03:26:42.483-0300.

26/10/2026 — COMENTARIO 3: preparación de grabación accesible desde el Laboratorio

Agregué a Cámaras y Evidencias el procedimiento de la próxima campaña y el alcance real del verificador offline de secuencias. El desarrollo y sus 26 pruebas quedan registrados en ASTRA-39, comentario 13; todavía no hay secuencia física nueva ni firmware de grabación cargado.

Reemplacé los botones de informes por una lista desplazable con apertura del seleccionado, para sumar documentación sin desbordar la pantalla. Pasaron las dos pruebas nativas de cierre y construcción: ocho secciones y diez informes presentes. La revisión visual anterior de las demostraciones se conserva; no atribuyo a este cambio una campaña física.

Commit verificado: https://github.com/edulandoni/astra-cansat/commit/60345488a19ad9098b5d72122e64d806611f11b1  
Informe: https://drive.google.com/file/d/1OxbefiIWUdJof-XBNhP8RwvRA07sUq-8/view  
Pruebas y pendientes de cámaras: https://astrateam2026.atlassian.net/browse/ASTRA-39?focusedCommentId=10188

El recorrido mantiene prioridad y sigue utilizable sin hardware; los pasos físicos quedan pendientes de disponibilidad y la interfaz de vuelo sigue bajo coordinación de Edu.

### 2026-10-26T12:14:12.849-0300 — comentario 10191

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-41?focusedCommentId=10191). Última edición informada: 2026-10-26T12:14:12.849-0300.

26/10/2026 — COMENTARIO 4: publicación pendiente completada y comprobaciones sin escritorio

Publiqué el candidato de secuencia y su procedimiento, accesibles desde Cámaras/Evidencias. La implementación, compilación y 31 pruebas están en ASTRA-39, comentario 14; el candidato no se cargó y no hay una secuencia física nueva. El Laboratorio conserva sus ocho secciones y ahora once informes locales.

Dejé en AGENTS.md la pauta vigente de comprobar por código, archivos y API, sin control de pantalla, apertura de ventanas de prueba ni cambios de foco mientras uso la PC. La revisión visual nueva de la lista de informes quedó pendiente al interrumpirse el control; no la presento como ejecutada. Las revisiones visuales anteriores de misión, paquete, fotos, LoRa y recuperación conservan su alcance. Los controles del código y las huellas coinciden y la copia de Drive se verificó contra el informe y la carpeta de destino.

Commit remoto: https://github.com/edulandoni/astra-cansat/commit/5d67592c7b77b9763ce684e4f81f3c450394d75a  
Informe: https://drive.google.com/file/d/1bxg-vf5MyXea8-wz7efWckq66-IKtYGx/view  
Desarrollo y límites: https://astrateam2026.atlassian.net/browse/ASTRA-39

El objetivo completo sigue abierto por pruebas físicas y dependencias de circuito/interfaz. No sustituyo esas pruebas con una compilación o un test de PC.

### 2026-10-26T12:22:45.495-0300 — comentario 10193

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-41?focusedCommentId=10193). Última edición informada: 2026-10-26T12:22:45.495-0300.

26/10/2026 — COMENTARIO 5: visor preparado y corte de verificaciones

Incorporé los accesos explícitos a secuencias guardadas de cámara 1 y cámara 2 y el informe nuevo en Evidencias. El desarrollo y sus límites están en ASTRA-39, comentario 15. El Laboratorio conserva ocho secciones y doce informes. No ejecuté interfaz ni abrí ventanas para esta actualización; sólo comprobé código, sintaxis, archivos y pruebas temporales. La revisión visual de los botones y del visor queda pendiente.

El recorrido, simulación, paquete, fotos conservadas, cálculo LoRa y recuperación mantienen su evidencia anterior. Las nuevas pruebas de reproducción son de PC y no acreditan grabación física. El candidato de cámara no se cargó, no cambié conexiones ni inicié periféricos.

Commit verificado: https://github.com/edulandoni/astra-cansat/commit/be79c8c0065f5c43cdca67db565090990302a8e9  
Informe: https://drive.google.com/file/d/1WTNFnf0hlfTj-tsBgQkIf-n7n1d_hm9C/view

Para el cierre del objetivo faltan las revisiones que requieren escritorio habilitado y preparación física de cámaras/tarjeta, además de acuerdos/circuito de vuelo. Mantengo esos puntos abiertos; no los sustituyo por tests ni por una declaración de cumplimiento.

### 2026-10-26T13:06:44.364-0300 — comentario 10194

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-41?focusedCommentId=10194). Última edición informada: 2026-10-26T13:06:44.364-0300.

26/10/2026 — COMENTARIO 6: Laboratorio Qt, presentación por subsistema y origen explícito

Rehice la entrada del Laboratorio con Qt Widgets/PySide6 y una presentación sobria: Avances del proyecto, Telemetría, Cámaras, Enlace RF, Recuperación de datos y Documentación. El recorrido organiza siete subsistemas mediante implementación, estado de verificación y prueba disponible. Eliminé títulos retóricos, hooks y textos publicitarios; el detalle técnico queda desplegable. No es una interfaz HTML ni un navegador.

La entrada continúa en laboratorio/app.py y el acceso del escritorio apunta al entorno dedicado de Qt. Conservé la copia Tk en el histórico y los bancos/registros existentes. La interfaz nueva inicia sin fuente ni mediciones. USB, simulación PC y reproducción requieren selección explícita. Una interrupción USB conserva valores históricos y no crea un emisor PC; pendientes de escritura y mensajes ausentes son magnitudes distintas. Los datos del firmware de banco siguen siendo sintéticos aunque se reciban físicamente por USB.

Integré adquisición, comandos de inicio de banco, métricas y estado de misión, gráfico sin unir huecos, contadores, trama original y variables, chequeo nuevo de cámaras bajo demanda, cálculo LoRa, recuperación e informes. Durante una sesión activa oculto la selección de fuentes para priorizar los datos. La reproducción conserva el registro original y escribe otra sesión.

Pasaron diez pruebas del Laboratorio y 34 del banco de cámaras. Qt se ejecutó y renderizó fuera de pantalla, sin ventanas en el escritorio ni apertura de puertos físicos. Revisé los renders generados por los widgets. La desconexión de esta actualización usa transporte simulado: no es una campaña USB física. Verifiqué fuente, navegación, arranque vacío, reproducción sin alterar originales y cierre durante misión/recuperación. El control final conserva salidas y huellas.

Commit remoto verificado: https://github.com/edulandoni/astra-cansat/commit/2ec5f14ac67013419b621dabe80db65f789ee91d  
Informe: https://drive.google.com/file/d/1xjyXdTRGrbRHotr_UmtU2hH3VxnEphuT/view  
Control: https://github.com/edulandoni/astra-cansat/blob/2ec5f14ac67013419b621dabe80db65f789ee91d/ground-station/evidence/2026-10-26-laboratorio-qt/control-02.json

Pendientes: revisión de uso con el equipo y ensayo físico de conexión/desconexión de la interfaz nueva. No afirmo RF, video continuo, consumo, autonomía o cumplimiento total del PDR por este rediseño. No cambié el contrato de vuelo ni cargué firmware.

### 2026-10-26T13:39:27.939-0300 — comentario 10196

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-41?focusedCommentId=10196). Última edición informada: 2026-10-26T13:39:27.939-0300.

26/10/2026 — COMENTARIO 7: banco completo, ensayos y cámaras dentro del Laboratorio

Amplié la integración Qt porque la vista anterior dejaba una sola curva y parte del banco fuera de la navegación. Telemetría ahora contiene siete áreas: 22 variables, once gráficos de los quince canales numéricos, comandos, guardado por destino, diagnóstico, tramas y estado. Mantengo unidades, condición actual/histórica, identidad de sesión/arranque/misión y cortes sin inventar continuidad. PC y reproducción permiten ×1/×5/×10; USB no se reemplaza por simulación al desconectarlo.

Integré los controles de banco: inicio/parada, altura cero, hora UTC, consulta sintética de batería/solar e identificación de resultados; repetir una orden utiliza el mismo ID y no activa reintentos automáticos. El segundo destino se configura para la siguiente sesión y muestra escritores original/CSV independientes. Las ventanas de gráficos y eventos son acotadas; el archivo conserva el flujo completo.

Ensayos y análisis permite ejecutar los seis casos existentes de calidad con reloj virtual y once vectores de destino; también calcular presupuesto de enlace con TBD y balance incremental de rotor, guardando archivos nuevos. El archivo filtrable da acceso completo a los documentos, configuraciones y evidencias textuales, con tablas de registros. Enlace RF compara SF7–SF12, BW y CR sin emitir. Las tres pruebas de recuperación siguen integradas.

Cámaras ofrece Foto USB y Foto + microSD por unidad, puerto e identidad explícitos; impide compartir el puerto activo de telemetría. Incorporé el visor Qt de secuencias conservadas con comprobación de integridad y tiempos, sin convertir fotos sueltas en una grabación ni abrir puertos.

Pasaron 14 pruebas del Laboratorio y 34 del banco de cámaras. Incluyen cinco misiones completas, todas las variables/series, guardado, corte sintético, comandos y las cuatro rutas de captura mediante sustituto del hardware. La campaña obtuvo 6/6 casos de calidad y 11/11 vectores correctos. Revisé renders Qt fuera de pantalla sin ocupar el escritorio. No hice fotos ni reconexiones físicas nuevas, no cargué firmware ni cambié el contrato de vuelo.

Commit remoto verificado: https://github.com/edulandoni/astra-cansat/commit/7713a4f6dcb95ac1dd8c6c1e825f344321f80b59  
Cobertura, resultados y límites: https://github.com/edulandoni/astra-cansat/blob/7713a4f6dcb95ac1dd8c6c1e825f344321f80b59/ground-station/docs/historial/2026-10-26-laboratorio-completo-04.md  
Control final y huellas: https://github.com/edulandoni/astra-cansat/blob/7713a4f6dcb95ac1dd8c6c1e825f344321f80b59/ground-station/evidence/2026-10-26-laboratorio-qt/control-04.json  
Copia de Drive verificada: https://drive.google.com/file/d/1nx08o0w5nks4paOe-By2I7upJycqMB0b/view?usp=drivesdk

Para el PDR puedo mostrar funcionamiento de software y evidencia previa, separando cálculo, simulación y pruebas físicas. Quedan pendientes uso con el equipo, captura/conexión física de esta versión, RF, video continuo, energía y acuerdos de interfaz. Mantengo las tareas abiertas.

## Historial de cambios de campos

### 2026-10-26T02:54:40.145-0300 — cambio 10160

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Backlog

Después: Por hacer

### 2026-10-26T02:55:41.762-0300 — cambio 10161

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Por hacer

Después: En curso

