# Ground Station: antecedentes argentinos y decisiones para el PDR

Autor: Cristian Ponsone. Revisión: 12 de octubre de 2026, hora argentina.

Estado: borrador de investigación para la revisión preliminar de diseño (PDR). Los cálculos son teóricos; todavía no acreditan recepción, autonomía ni funcionamiento de hardware integrado.

## Criterio de trabajo

Mi responsabilidad es recibir, conservar y mostrar los datos, y operar los telecomandos acordados con electrónica. Uso como referencia la [lista electrónica de Drive utilizada para las compras](https://docs.google.com/spreadsheets/d/1PhY-BefCl1SAa7RWicEEAamdvEynt5At/edit). Los presupuestos anteriores son antecedentes. Los HTML de práctica son prescindibles: no condicionan la arquitectura nueva.

Trabajo con el lema «No podemos ganar haciendo lo mismo que el que ganó ayer». Para convertirlo en una propuesta defendible, necesito identificar una mejora, compararla con una alternativa y demostrarla mediante un ensayo. Agregar indicadores o calcular magnitudes conocidas no alcanza, por sí solo, para afirmar innovación.

El relevamiento reúne los diez finalistas nacionales publicados por CONAE para las ediciones secundarias de 2022 y 2023, más BioBit como antecedente técnico complementario. Son cinco seleccionados por edición, no un podio ordenado del primero al quinto. No incluyo ganadores internacionales. Tampoco equiparo esas misiones escolares con los requisitos de nuestra convocatoria universitaria 2026–2027.

## Mapa de antecedentes

| Edición | Equipo e institución | Misión publicada | Evidencia técnica localizada |
| --- | --- | --- | --- |
| 2022 | Caelus, Huergo, CABA | Calidad del aire | Descripción institucional; sin código o esquema completo localizado. |
| 2022 | electroSix, San José, Justiniano Posse | Composición del aire | Descripción institucional; sin calibración o modelo de sensores verificado. |
| 2022 | gVIE, Villada, Córdoba | Perfil atmosférico con posición | Repositorio propio: transmisor, receptor, protocolo y fichas de ensayos. |
| 2022 | MERAKI, EPET 3, Pirané | Información sobre incendios | Objetivo y participación confirmados; arquitectura completa pendiente. |
| 2022 | Ad Astra, EPET 18, Puerto Esperanza | Propuesta sobre niebla/granizo | Entrevista sobre demostración de dispersión; no prueba de eficacia meteorológica. |
| 2023 | ConcorSat, San Roque y Renacer, Concordia | Contaminación acústica | Descripción de misión; sin cadena de calibración o firmware localizado. |
| 2023 | Cóndor Salvaje, Técnico de Aguilares, UNT | Imágenes y descenso guiado | Publicaciones de autores sobre enlace bidireccional y ensayos; premio técnico confirmado por UNT. |
| 2023 | HYPERION, León XIII, CABA | Contaminación lumínica | Descripción de misión; sin diseño técnico completo localizado. |
| 2023 | Novationes, Monserrat, Córdoba | Polvo y contaminación ambiental | Sitio propio con componentes, decisiones, pruebas y limitaciones. |
| 2023 | Roldán 2, EETP 643, Santa Fe | Muestreo para estudiar microplásticos | Descripción provincial de toma de muestras y posterior análisis de laboratorio. |

Fuentes de selección: [CONAE 2022](https://www.argentina.gob.ar/noticias/se-lanzaron-desde-la-conae-cinco-satelites-cansat-construidos-por-estudiantes-de-la) y [CONAE 2023](https://www.argentina.gob.ar/noticias/cansat-2023-cinco-equipos-de-escuelas-secundarias-lanzaron-sus-satelites-en-el-centro). Complementos: [entrevista UNQ de 2022](https://agencia.unq.edu.ar/?p=8601), [Roldán 2](https://www.santafe.gob.ar/noticias/noticia/279787/) y [premio de Cóndor Salvaje](https://medios.unt.edu.ar/2023/10/10/rector-vice-recibieron-alumnos-instituto-tecnico-aguilares-se-destacaron-final-cansat-2023/).

La ausencia de archivos públicos localizados no demuestra que un equipo careciera de diseño, pruebas o resultados. El alcance completo de cada implementación sigue abierto donde sólo encontré descripciones.

## Cuatro referencias que aportan decisiones concretas

### gVIE: receptor simple y ensayos documentados

El [repositorio mCALCAN](https://github.com/its-villada/mCALCAN) permite seguir el recorrido radio–USB–PC. El receptor usa una placa Adafruit LoRa 32u4 y salida serie a 9600 baudios; ambos extremos configuran 915 MHz, SF7, BW 125 kHz y CR 4/5. El transmisor incluye STM32, BMP280, MPU9250, AHT10, MQ135, GPS, microSD y servos. Su protocolo distingue mensajes confirmables y respuestas; sus códigos numéricos no son los comandos de nuestra convocatoria.

Comparé el código actual de TX/RX con versiones anteriores al lanzamiento de 2022: coinciden. Las referencias históricas son [TX, commit 824d636](https://github.com/its-villada/mCALCAN/blob/824d6362f132772a52591840f0d85a3f85d80e3f/src/Lora_TX/Lora_TX.ino) y [RX, commit a934068](https://github.com/its-villada/mCALCAN/blob/a9340688ea3895128fe4eb4e059eb21db2e52fd9/src/Lora_RX/Lora_RX.ino). Esto acredita la versión publicada, no el binario efectivamente instalado en vuelo.

La ficha de ensayo 4 declara dos horas de comunicación a tres metros, con controles cada quince minutos. La ficha 5 declara paquetes de 100 bytes cada 500 ms y recepción fluida hasta unos 600 m en recorrido urbano. Son antecedentes útiles para diseñar pruebas; sin trazas por paquete, antenas y condiciones equivalentes no constituyen garantía de alcance para ASTRA.

Me llevo la separación entre receptor, transporte y visualización, y el hábito de registrar configuración y procedimiento. El PDR y el XLSX de vuelo del repositorio fueron identificados, pero su lectura íntegra sigue pendiente. No los presento como evidencia analizada.

### Cóndor Salvaje: comunicación bidireccional y costo de los duplicados

Los autores describen estación con Node-RED, aplicación App Inventor y enlace bidireccional LoRa, además de imágenes y control del descenso. El [trabajo CATE 2025](https://es.scribd.com/document/889658757/Full-Paper-CATE-2025-Paper1) reporta pérdidas de hasta 20% con acceso aleatorio y hasta 5% después de sincronizar, antes de incorporar duplicados identificados. No extrapolo esas cifras a nuestras radios.

El [artículo del III Congreso Aeroespacial Brasileño](https://static.even3.com/anais/1443303.pdf?v=639041730014778153) es una publicación de este equipo argentino, no una referencia a un ganador extranjero. Reporta ensayos y recepción en vuelo, pero también despliegue parcial del ala por problemas de plegado. La comunicación puede funcionar mientras el mecanismo falla: un eco de comando no prueba ejecución física.

Duplicar paquetes consume tiempo de radio. Hay que presupuestarlo junto con los comandos. Además, la denominación Heltec V2/SX1262 del artículo necesita confirmación frente al [manual de Heltec V2](https://s.heltec.cn/download/Manual%20Old/WiFi%20Lora32Manual.pdf), que identifica SX1276/SX1278. No traslado su pinout sin verificar la placa.

### Novationes: combinar datos y reconocer funciones que no llegaron a validarse

El [sitio técnico conservado en su repositorio](https://github.com/agussbastos/Novationes-CANSAT-web) describe ESP32, LoRa, BMP180/DHT11; para la misión secundaria, sensor óptico Sharp, MQ7 y Raspberry Pi Zero W con cámara y almacenamiento local. La combinación de imágenes, partículas y CO busca contextualizar las mediciones. Un [reporte de UNC](https://www.unc.edu.ar/node/44170) describe la experiencia de lanzamiento.

El propio equipo declara que el sistema de recuperación con MPU6050 y buzzer no quedó funcionando por problemas de programación, calibración y tiempo. También registra rotura estructural en una caída de prueba y dificultad para ver la computadora bajo el sol. Es información valiosa para priorizar ensayos sobre funciones demostradas y operación real de campo.

Combinar dos sensores no convierte automáticamente una hipótesis en una medición selectiva. La denominación abreviada Sharp GP2Y10 no identifica por completo el módulo. El [fabricante diferencia sensores de polvo general de modelos que clasifican partículas](https://global.sharp/products/device/lineup/selection/opto/dust/index.html). No doy por demostrada una concentración exclusiva de PM2.5 ni el origen vehicular por simple coincidencia con CO e imágenes.

El archivo publicado como estación terrena está vacío. Las imágenes DPD localizadas son fotos de preparación, no trece páginas legibles del documento. No atribuyo un framework de estación ni un DPD completo a partir de esos archivos.

### BioBit: cambiar la pregunta puede reducir hardware

BioBit, de la EETP 461 de Reconquista, figura como **semifinalista**, no entre los cinco finalistas anteriores; lo confirma el [programa provincial de 2022, página 7](https://www.santafe.gob.ar/index.php/web/content/download/269559/1406992/file/SDLC2022_Cronograma__web.pdf). Su [presentación propia](https://docs.google.com/presentation/d/15XR-HZV_KwO8mllnHlVJzXEC0yi8QAShSn4GZpE-Y-I/edit) relata que descartaron cámaras y usaron posición GPS para consultar imágenes Landsat y calcular índices de vegetación/agua.

Es un antecedente concreto de reemplazar parte del instrumental por datos externos cuando la pregunta científica lo permite. Esos datos corresponden a otra adquisición: [Landsat 8](https://www.usgs.gov/landsat-missions/landsat-8) tiene resolución multiespectral de 30 m y revisita nominal de 16 días, no una imagen instantánea tomada por el CanSat. En ASTRA no sustituye las dos grabaciones obligatorias.

Revisé también su [estación Python](https://github.com/MisionBioBit/BioBit-EstacionTerrena) y [código asociado](https://github.com/MateoBarcelo/Cansat-MisionBioBit). En `gui.py`, una excepción serie introduce ceros artificiales; los gráficos acumulan datos y hay acceso a la interfaz desde hilos de trabajo. Son advertencias para nuestro diseño: un fallo debe mostrarse como fallo, y la adquisición debe continuar aunque la interfaz se demore. Esta lectura estática no certifica el desempeño de su estación en campo.

## Compras e interfaces de ASTRA

| Elemento de referencia | Interfaz y función prevista | Confirmación necesaria |
| --- | --- | --- |
| STM32F411 BlackPill | Computadora de vuelo; SPI, I2C, UART y USB | Versión de placa, distribución de pines y tensiones reales. |
| SX1276, vuelo y tierra | SPI al microcontrolador; radio hacia el otro extremo | Módulo, antena, alimentación, direccionamiento y parámetros de radio. |
| BMP280, MPU9250/6500, INA3221, DS3231/AT24C32 | Principalmente I2C en estos módulos | Direcciones, pull-ups, chip exacto, shunts y estados de validez. |
| ATGM336H y antena | UART; mensajes GNSS | Sufijo completo, protocolo, constelaciones y alimentación de placa. |
| DS18B20 | Bus 1-Wire; temperatura en ubicación definida | Alimentación, pull-up, CRC y conversión asincrónica. |
| microSD 3,3 V | SPI; registro a bordo | Arbitraje con radio si comparten bus y tolerancia a fallos de escritura. |
| 18650 30Q, TP4056, reguladores | Alimentación y carga | Topología, protección, consumo y autonomía integrada; boost de banco no define el circuito de vuelo. |
| Panel 5 V, aproximadamente 25 mA | Detección solar | Magnitud y resolución de medida; no presumir recarga de batería. |
| Buzzer y batería independiente | Localización tras aterrizaje | Encendido y alimentación independientes del computador de vuelo. |
| Cámaras | Grabaciones obligatorias | La lista actual no cierra modelos, interfaces, consumo ni montaje. |

Cantidades de la lista no acreditan recepción de materiales ni instalación. La IMU puede ser MPU6500 de seis ejes o MPU9250 de nueve; no prometo magnetómetro antes de identificarla. El [fabricante del ATGM336H](https://www.icofchina.com/daohang/danpin/2525.html) distingue variantes: no doy por disponible Galileo ni todas las constelaciones anunciadas en el comercio.

Para tierra evalúo dos caminos con el stock previsto: SX1276 → ESP32 → USB serie → PC, o SX1276 → segunda BlackPill → USB CDC → PC. La [BlackPill F411](https://github.com/WeActStudio/WeActStudio.MiniSTM32F4x1) dispone de USB nativo, pero necesita firmware de gateway; conectar el cable no la convierte automáticamente en receptor serie. La elección debe compararse por disponibilidad, estabilidad y tiempo de implementación.

En la PC propongo un servicio local que reciba bytes, reconstruya paquetes y escriba registros; la interfaz consume esos registros. Git y Drive conservan código y documentos. La recepción en campo debe funcionar sin internet, con batería y respaldo local.

## Dos límites que cambian el diseño

### Capacidad de radio

El [cálculo reproducible](https://github.com/edulandoni/astra-cansat/blob/docs/ground-station-continuidad/verification/ground-station-capacity-analysis.py) usa las ecuaciones contrastadas con el [driver oficial de Semtech](https://github.com/Lora-net/LoRaMac-node/blob/master/src/radio/sx1276/sx1276.c). Sus [resultados](https://github.com/edulandoni/astra-cansat/blob/docs/ground-station-continuidad/verification/ground-station-capacity-analysis.json) incluyen 2304 comparaciones coincidentes de las fórmulas al redondear a milisegundos. Eso verifica el cálculo, no el enlace físico.

Ejemplo: LoRa, BW 125 kHz, CR 4/5, preámbulo de 8 símbolos, cabecera explícita y CRC; telemetría de 200 bytes y comando ilustrativo de 23 bytes, sin delimitador todavía acordado.

| Configuración | Una telemetría | Telemetría + comando | Dos telemetrías + comando |
| --- | ---: | ---: | ---: |
| SF7 | 317,696 ms | 379,392 ms | 697,088 ms |
| SF8 | 563,712 ms | 676,864 ms | 1240,576 ms |
| SF9 | 1004,544 ms | 1210,368 ms | 2214,912 ms |

SF9 con **ese tamaño y configuración** no sostiene una transmisión por segundo. SF8 deja de admitir dos copias más ese comando dentro del segundo. Todavía faltan tiempos de cambio TX/RX, márgenes, encapsulado, respuestas y reintentos. No descarto SX1276: hay que dimensionar el paquete máximo y los parámetros. El ejemplo mínimo del script ocupa 128 bytes, no garantiza el peor caso de los 22 campos.

Propongo ventanas de recepción después de terminar TX, cola de comandos y resincronización tras reinicios. Para cumplir NetID/PanID y evitar broadcast necesito acordar direccionamiento: un sync word de ocho bits no representa por sí solo un número de equipo completo. El cálculo no acredita alcance, presupuesto de enlace ni autorización de emisión.

### Presión, resolución y retardo

El formato transmite presión con resolución de 0,1 kPa. En un ejemplo próximo al nivel del mar, con 288,15 K y 101325 Pa:

$$h=\frac{R_dT}{g}\ln\left(\frac{p_0}{p}\right),\qquad \left|\frac{\mathrm dh}{\mathrm dp}\right|=\frac{R_dT}{gp}.$$

Un salto de 100 Pa representa aproximadamente **8,32 m**; 0,1 m equivale aproximadamente a 1,20 Pa en ese modelo local. Es cuantización, no una afirmación de exactitud del sensor. Hay que calcular ALTITUDE con presión interna sin redondear y conservar la referencia de CAL; la PC no debe reemplazar esa altura por otra calculada desde PRESSURE ya redondeada.

El [BMP280](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp280-ds001.pdf) también puede añadir retardo por filtro: coeficiente 16 requiere 22 muestras para alcanzar aproximadamente 75% de un escalón, es decir 11 s a 2 Hz o 2,2 s a 10 Hz. Son configuraciones hipotéticas. Ese retardo entra en la detección de apogeo y liberación. Su temperatura corresponde al sensor y depende del calentamiento/ubicación; no reemplazo DS18B20 por ella sin validación térmica.

## Innovaciones candidatas, sin agregar sensores por defecto

| Propuesta | Datos existentes | Qué aporta y qué debo demostrar |
| --- | --- | --- |
| Diagnóstico de liberación | Barómetro, IMU, corriente y video | Evidencia compatible con ejecución o atasco; medir falsas alarmas y retardo contra referencia física. |
| Perfil de descenso y transiciones | Altura interna precisa, tiempos y estado | Detectar cambios de régimen sin altímetro adicional; validar referencia, filtrado y huecos. |
| Presupuesto energético medido | INA3221, tiempo y estados | Potencia y energía por fase, sin wattímetro de vuelo adicional; calibrar shunts y medir autonomía real. |
| Estación que conserva y explica fallos | Contadores, bytes, marcas de tiempo y disco | Distinguir pérdida de enlace, sensor inválido y problema local; demostrar recuperación sin inventar mediciones. |

Para potencia y energía uso $P=VI$ y $E=\int P\,\mathrm dt$, con cobertura explícita de intervalos válidos. La tensión sola no entrega un porcentaje confiable de batería sin modelo y ensayo. Un pico de servo puede durar menos de un segundo: si sólo recibo un dato a 1 Hz, puedo perderlo. Haría falta calcular un resumen a mayor frecuencia en vuelo y acordar su envío como extensión, conservando intactos los campos obligatorios.

Mi candidata principal es **diagnóstico de eventos y calidad de datos con los sensores ya previstos**. Tiene relación directa con Ground Station y con la liberación obligatoria. Primero debo demostrar observabilidad: movimiento, corriente o cambio de descenso aislados no prueban que se liberó una pieza. No elimino un sensor o mecanismo obligatorio ni declaro una primicia nacional por no encontrar otro caso público.

## Contrato que debo cerrar con electrónica

La base es el [anexo técnico recibido en Drive](https://drive.google.com/file/d/1ClQ6-2E9n8deEy40NVR0KD00IIEnRNlS/view), junto con las [bases recibidas](https://drive.google.com/file/d/1x8RcHMK4751UtUGjPh8-Xt335ezcfM0J/view). Mantengo estas formas literales; los valores entre ángulos son parámetros:

```text
CMD,<TEAM_ID>,CX,ON
CMD,<TEAM_ID>,CX,OFF
CMD,<TEAM_ID>,ST,<hh:mm:ss>
CMD,<TEAM_ID>,ST,GPS
CMD,<TEAM_ID>,CAL
CMD,<TEAM_ID>,MEC,<DEVICE>,ON
CMD,<TEAM_ID>,MEC,<DEVICE>,OFF
```

El documento compartido deberá precisar DEVICE, estados permitidos, efecto, eco, errores, tiempo de espera, reintentos, duplicados, reinicios y terminador. CR está indicado para telemetría; no lo doy por especificado para comandos. CMD_ECHO es un campo sin comas y no demuestra actuación física. Repetir un comando idéntico puede dejar un eco indistinguible del anterior; CX OFF puede cortar el flujo antes de confirmar. CAL no admite reintentos ciegos durante vuelo.

La telemetría base contiene 22 campos ASCII separados por comas y termina en CR. Los estados publicados son LAUNCH_PAD, ASCENT, APOGEE, DESCENT, PROBE_RELEASE, PAYLOAD_RELEASE y LANDED. No introduzco nombres nuevos como si fueran reglamentarios. La cantidad de paquetes recibidos con éxito en tierra es distinta del contador transmitido por el vehículo.

Consultas prioritarias para la instancia del 14 de octubre o el canal oficial correspondiente:

1. Direccionamiento NetID/PanID y ausencia de broadcast con SX1276 y número completo de equipo.
2. Unidad de ACCEL: el formato indica grados/s², mientras la IMU mide aceleración lineal; representación GPS sur/oeste y datos inválidos.
3. Mapeo de estados a liberaciones reales y activación automática frente a CX ON/OFF, incluidos acuses.
4. Sintaxis no definida de consulta batería/solar y puesta a cero del contador; no inventar comandos obligatorios.
5. Terminador, valores MEC y convenciones de CMD_ECHO/errores.
6. Orientación cenit/nadir frente a referencia a norte; longitud indicada en bases frente al anexo.
7. Definición de contador persistente ante corte de energía y significado exacto del paquete contado.

La AT24C32 de la lista merece evaluación antes de agregar memoria. El diseño necesita registros recuperables y estrategia ante corte, no escribir un contador ingenuamente en la misma celda. El [datasheet AT24C32D](https://ww1.microchip.com/downloads/aemDocuments/documents/MPD/ProductDocuments/DataSheets/AT24C32D-2-Kbit-I2C-Serial-EEPROM-Industrial-Grade-DS20006047.pdf) es una referencia de familia; debo confirmar chip y condiciones reales. RTC y EEPROM no vuelven atómica una transmisión por sí solos.

## Ensayos que convierten el PDR en una propuesta verificable

| Ensayo propuesto | Evidencia que conservaré | Criterio de cierre |
| --- | --- | --- |
| Radio a 1 Hz con paquetes extremos y comandos | Bytes, secuencias, parámetros, pérdidas y latencia | Carga completa dentro del período, márgenes explícitos y límites de pérdidas/latencia acordados. |
| Comandos durante TX, duplicados y reinicios | Solicitud, recepción, eco, efecto y referencia física | Sin actuación repetida accidental; resultado o estado incierto identificable. |
| Sensor inválido, desconexión, CRC y datos atrasados | Registro original y diagnóstico | Ningún cero, interpolación o simulación presentado como medida real. |
| Interfaz congelada, disco lleno y respaldo desconectado | Trazas de adquisición y archivos recuperados | Recepción separada de dibujo; fallos de escritura visibles y procedimiento de recuperación. |
| Dos horas con equipo completo | Consumo, archivos, reinicios y temperatura | Requisitos de autonomía cumplidos en la configuración de uso; incluir portátil, receptor y respaldo. |
| Liberación normal frente a atasco controlado | Video sincronizado, IMU, presión y corriente | Medir falsos positivos, falsos negativos y latencia; definir umbrales antes del ensayo. |
| Operación bajo sol | Capturas, tamaño de texto, tiempos y lista de operación | Vista reglamentaria simultánea, legibilidad y ausencia de dependencia de internet. |

Estas pruebas están propuestas, no ejecutadas. Los umbrales adicionales de calidad deben acordarse; no los atribuyo a CONAE. La IMU prevista no acredita un choque de 30 g si su rango máximo es 16 g; el ensayo estructural exige un método externo adecuado. El DS18B20 puede tardar hasta 750 ms a 12 bits según su [datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ds18b20.pdf): su conversión debe ser asincrónica para no bloquear radio y control.

## Qué llevaré al PDR

Presentaré arquitectura de recepción local, interfaces confirmadas y pendientes, contrato con electrónica, presupuesto de tiempo de radio, estrategia de registro y respaldo, y una hipótesis de mejora con ensayo comparativo. Usaré la plantilla y evaluación de nuestra convocatoria cuando estén disponibles, sin copiar extensión o rúbrica de otro concurso.

Quedan pendientes la identificación de módulos comprados, las cámaras, el contrato aceptado, los binarios públicos aún no leídos y los ensayos físicos. El avance actual permite tomar decisiones justificadas; todavía no permite afirmar que el sistema integrado funciona ni que supera a los anteriores en vuelo.
