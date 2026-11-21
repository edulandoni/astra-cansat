# 20/10/2026 — Actualización: antecedentes, código de tierra y referencias visuales

Diario: [ASTRA-35](https://astrateam2026.atlassian.net/browse/ASTRA-35). Continúo el [relevamiento de 35 registros del 19/10](2026-10-19-antecedentes-cansat.md) sin reemplazarlo. La investigación de rotor permanece en [ASTRA-36](https://astrateam2026.atlassian.net/browse/ASTRA-36). Este avance añade lectura de fuentes y código, no ensayos de vuelo ni modificaciones a nuestros programas.

## Qué vale la pena estudiar primero

| Caso | Qué pude respaldar | Para qué nos sirve | Evidencia que todavía falta |
| --- | --- | --- | --- |
| PWr Aerospace 2024 | Primer puesto en el [organizador](https://www.cansatcompetition.com/winners.html); proyecto propio y repositorio de tierra público | Leer decisiones y rutas de recepción/guardado, sin adoptar software por su premio | Demostrar que este commit exacto fue el usado en competencia, datos crudos y pruebas de todas sus rutas |
| SEDS ITBA 2025 | Primer puesto oficial, [nota de la institución](https://www.itba.edu.ar/orgullo-itba-estudiantes-ganaron-la-competencia-cansat-organizado-por-la-nasa/) y galería de premiación | Vincular resultado, demostraciones y trabajo previo del equipo | Separar lo relatado de registros reproducibles de vuelo; confirmar reutilización de imágenes |
| DJS Arya 2026 | El [organizador](https://www.cansatcompetition.com/winners.html) confirma el premio específico Ground Station | Referencia prioritaria para nuestra área | No localicé criterios técnicos del jurado ni identifiqué una foto verificada de su estación en esta pasada |

El [proyecto PWr 2024 publicado por sus autores](https://aerospace.pwr.edu.pl/portfolio/cansat-2024/) describe integración modular, estabilización de cámara y varias iteraciones. Es una descripción de diseño/preparación, no un log completo de prestaciones. Sus dimensiones y misión son de otra edición: no las convierto en requisitos de ASTRA.

La nota ITBA relata prestaciones y el triunfo. Su afirmación sobre video en tiempo real no modifica el requisito CONAE: no copio esa prestación a nuestra misión ni la considero acreditada sólo por una fotografía. Conservo diferencias entre relatos institucionales y el material técnico cuando existan; una entrevista, una noticia y un PDR no tienen el mismo alcance.

## Lectura estática de cinco archivos de tierra de PWr

Fijé el commit `c8ecb98e0d5f4b44880525a8d97e1a4af609459b` para que la referencia no dependa de una rama que cambie. Revisé SerialPortWatchdog.cpp, SerialPort.cpp, Logger.cpp, TelemetryCache.cpp y ParserTest.cpp. No compilé ni ejecuté este proyecto, no copié su código a ASTRA y no atribuyo al equipo fallas ocurridas en vuelo a partir de esta lectura.

1. En [SerialPortWatchdog.cpp](https://github.com/PWr-Aerospace/CanSat2024_Ground_Station/blob/c8ecb98e0d5f4b44880525a8d97e1a4af609459b/src/SerialPortWatchdog.cpp) un temporizador consulta errores de puerto y emite un aviso. Es un antecedente para separar estado de conexión y estado del dato. No demuestra por sí solo reconexión automática ni continuidad de registro.
2. En [SerialPort.cpp](https://github.com/PWr-Aerospace/CanSat2024_Ground_Station/blob/c8ecb98e0d5f4b44880525a8d97e1a4af609459b/src/SerialPort.cpp) la ruta de recepción busca un identificador fijo, extrae una trama y luego vacía el buffer. Eso merece un ensayo específico con varias tramas en una lectura, fragmentos y prefijos ajenos. Es una hipótesis de riesgo derivada del código, no una pérdida que haya medido hoy. Para ASTRA me interesa comprobar que fragmentar o agrupar lecturas no cambia los paquetes recuperados, sin adoptar su identificador ni sus parámetros.
3. En [TelemetryCache.cpp](https://github.com/PWr-Aerospace/CanSat2024_Ground_Station/blob/c8ecb98e0d5f4b44880525a8d97e1a4af609459b/src/TelemetryCache.cpp) el registro abre un CSV en modo agregado y escribe/realiza flush por trama. En esa función no veo comprobación explícita de apertura o error de escritura. Esto refuerza nuestra necesidad de distinguir recibido, guardado por destino y recuperable. No concluyo que el proyecto carezca de toda protección fuera de esta función, ni que flush acredite durabilidad eléctrica.
4. En [Logger.cpp](https://github.com/PWr-Aerospace/CanSat2024_Ground_Station/blob/c8ecb98e0d5f4b44880525a8d97e1a4af609459b/src/Logger.cpp) distingo niveles de registro y salida a pantalla/consola. El log de diagnóstico y la persistencia de la telemetría son problemas distintos; mostrar un mensaje no demuestra que el dato de misión quedó guardado.
5. En [ParserTest.cpp](https://github.com/PWr-Aerospace/CanSat2024_Ground_Station/blob/c8ecb98e0d5f4b44880525a8d97e1a4af609459b/src/ParserTest.cpp) hay casos de formato correcto, cantidad de separadores y longitud. El caso llamado NumberError usa el mismo texto de entrada que el nominal y espera un resultado válido. Un nombre de prueba no acredita que realmente inyecte ese error. La lección para nuestras pruebas es describir entradas y resultados esperados, conservando evidencia de qué falla se introdujo.

Estas observaciones nos sirven para diseñar verificaciones propias; no justifican cambiar ahora a C++/Qt ni declarar que nuestro banco ya está resuelto. Las rutas problemáticas de raw/CSV que identificamos en nuestros ensayos siguen siendo un pendiente propio.

## Fotos y láminas: catálogo de consulta con estados reales

Agregué [siete referencias visuales](2026-10-20-catalogo-visual-cansat.csv), con fuente, equipo/edición cuando está identificado, tipo de imagen, acceso real, utilidad, crédito y estado de reutilización. La [galería oficial AAS 2025](https://astronautical.org/events/cansat/cansat-2025-photos/) está ordenada por los cuatro días del evento y tiene una sección que identifica a SEDS ITBA como primer puesto. Abrí y observé su fotografía de celebración P6080293-2. Sirve para contextualizar el resultado, no para medir fiabilidad, identificar componentes internos o demostrar generación eléctrica.

Localicé dos referencias del día de lanzamiento, pero no les atribuyo un equipo o mecanismo sin una vista individual concluyente. La página PWr enlaza una lámina CONOPS y detalles de su sistema; los visores fallaron al cargarlos. La foto enlazada por la noticia ITBA devolvió 404 en la navegación directa. La galería 2026 quedó localizada, con acceso incompleto en esta pasada. Registro esos límites en lugar de decir que todas las imágenes fueron inspeccionadas.

Conservo enlaces al material original; no descargué un banco de imágenes ni subí fotografías de terceros a GitHub o Drive. Los créditos individuales y permisos que no pude confirmar figuran como pendientes. Si seleccionamos imágenes para el video, primero verificaré la foto concreta, su atribución y condiciones de reutilización. Nuestros gráficos, capturas y ensayos propios deben sostener las afirmaciones sobre ASTRA.

## Próximas pasadas útiles

Priorizaría resultados posteriores al vuelo y datos crudos de estos casos, evidencia específica de la estación premiada DJS Arya y verificación de imágenes de mecanismos en vez de acumular fotos de premiación. Para rotor buscaría energía eléctrica efectivamente medida y problemas de despliegue; un autogiro o hélice fotografiado no prueba generación.

La revisión diaria incorpora una pasada complementaria acotada: hasta tres fuentes primarias nuevas o una ficha ampliada con evidencia sustantiva, consultando lo ya registrado para evitar repetir búsquedas. Cada avance se agrega con fecha en su tema y tarea; las ideas no pasan a implementación por aparecer en un informe. No modifico proyectos ajenos ni afirmo una búsqueda exhaustiva mundial.
