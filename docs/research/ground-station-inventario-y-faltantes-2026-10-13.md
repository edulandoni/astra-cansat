# Ground Station inventario disponible y faltantes para el PDR

Autor: Cristian Ponsone. Revisión: 13 de octubre de 2026.

## Fuentes y criterio de disponibilidad

Tomo Jira ASTRA como fuente principal de decisiones, tareas, dependencias y trazabilidad del PDR. El XLSX de compras acredita disponibilidad según el criterio acordado: ambos tonos verdes significan que ya tenemos esos componentes; los demás renglones siguen pendientes. Git conserva implementación y versiones; Drive conserva archivos de referencia y evidencias. El reglamento sigue definiendo los requisitos obligatorios.

La revisión usa el [XLSX original de compras](https://docs.google.com/spreadsheets/d/1PhY-BefCl1SAa7RWicEEAamdvEynt5At/edit), de 54 361 bytes, modificado el 13/10/2026 a las 02:39 UTC, equivalente al 12/10 a las 23:39 en Argentina. Leí valores y estilos del archivo original: una hoja Sheet1, 24 renglones de hardware en A2:F25 y sin reglas de formato condicional. Los colores verdes son 92D050 y 00B050.

Hay 17 renglones disponibles y 7 pendientes. La columna Estado conserva textos como COMPRAR, ESPERAR/PROTO y USAR SI YA TENÉS en filas verdes; esos textos no invalidan la disponibilidad confirmada. No modifiqué el libro.

La lectura de [Jira ASTRA](https://astrateam2026.atlassian.net/jira/software/projects/ASTRA/boards/1/backlog) sigue pendiente de acceso autenticado. No atribuyo decisiones, estados ni tareas a cristianponsone9 o cristianponsone hasta verificar ambas identidades y sus incidencias. No hice cambios en Jira.

## Material disponible

| Fila | Componente | Cantidad indicada | Uso y verificación antes de asignarlo |
| --- | --- | ---: | --- |
| 2 | WeAct BlackPill STM32F411CEU6 | 2 | Computadora de vuelo y repuesto/banco; confirmar revisión de placa. |
| 3 | ST-Link V2 | 1 | Programación y depuración SWD; equipo de desarrollo. |
| 4 | Samsung INR18650-30Q 3000 mAh | 2 | La lista propone una para ensayo/vuelo y una de repuesto; no implica conexión redundante. |
| 5 | TP4056 USB-C con protección | 2 | Carga/protección; confirmar circuito y función en el montaje real. |
| 6 | SX1308/MT3608 | 2 | La lista los reserva para prototipo/banco. No definen la regulación final. |
| 7 | BMP280 | 2 | Presión y altura; uno puede quedar como repuesto y referencia de banco. |
| 8 | DS18B20 TO-92 | 2 | Temperatura en ubicación definida; conversión y CRC. |
| 9 | MPU9250/6500 | 2 | Identificar chip antes de declarar magnetómetro o cerrar prestaciones. |
| 10 | ATGM336H con antena | 1 | Confirmar sufijo, alimentación de módulo y mensajes UART. |
| 11 | INA3221 de tres canales | 2 | Tensión/corriente; verificar shunts y calibración. |
| 12 | DS3231 con AT24C32 | 1 | Tiempo y persistencia de configuración; comprobar respaldo del reloj y EEPROM real. |
| 13 | Adaptador microSD SPI 3,3 V | 1 | Interfaz de almacenamiento a bordo; probar alimentación y arbitraje SPI. |
| 14 | Tarjeta microSD High Endurance 16/32 GB | 1 | Registro de vuelo; comprobar capacidad y recuperación tras cortes. |
| 15 | Panel 5 V, aproximadamente 25 mA | 1 | Detección solar; no presupone recarga de la batería. |
| 18 | ESP32 | 1 | Gateway terrestre disponible; identificar placa, flash y conversor USB. |
| 19 | Servo MG90S | 1 | Disponible, aunque su utilización depende del mecanismo seleccionado. |
| 23 | LED con resistencia | 1 | Indicación de encendido. |

Disponibilidad no equivale a validación funcional ni determina qué piezas están instaladas. Los repuestos duplicados permiten sustituir y comparar en banco; no los agrego a vuelo por defecto. Instalar dos sensores en el mismo bus y alimentación mantiene fallas comunes y aumenta consumo, masa y trabajo de integración.

## Pendientes de la lista

| Fila | Elemento pendiente | Prioridad de análisis | Cierre necesario |
| --- | --- | --- | --- |
| 16 | SX1276 de vuelo | Enlace obligatorio | Módulo exacto, banda, antena, alimentación y direccionamiento X2/X3. |
| 17 | SX1276 de tierra | Enlace obligatorio | Compatibilidad con vuelo y conexión SPI al ESP32 disponible. |
| 20 | Buzzer activo con batería independiente | Recuperación obligatoria | Funcionamiento separado del computador y batería de vuelo. |
| 21 | Interruptor principal | Integración eléctrica | Corriente, accesibilidad y esquema definitivo. |
| 22 | Interruptor de baliza | Independencia de baliza | Montaje y operación independientes. |
| 24 | Capacitores 470 µF, 100 µF y 100 nF | Integración y estabilidad | Valores y distribución derivados del circuito y mediciones. |
| 25 | Conectores, cable y termocontraíble | Integración de vuelo | Longitudes, conexiones, retención y montaje definidos. |

Primero cierro radios, antenas y alimentación; no priorizo una tercera radio terrestre antes de tener un enlace completo probado. El texto SX1276 915 MHz no reemplaza la ficha del módulo y de su etapa RF. El enlace comercial incluido no permitió verificar aquí precio actual ni especificaciones completas.

## Qué puede faltar fuera del XLSX

| Necesidad | Evidencia actual | Acción antes de comprar |
| --- | --- | --- |
| Dos grabaciones de video obligatorias | Cámaras no identificadas en esta lista | Consultar selección y tareas en Jira; confirmar resolución, orientación, continuidad, consumo y almacenamiento. |
| Regulación y distribución de energía finales | Convertidores señalados como sólo prototipo | Revisar esquema de electrónica y picos de servo/radio; identificar si falta un componente concreto. |
| Antenas y conexiones RF | Antena GNSS explícita; antenas de LoRa no desglosadas | Confirmar contenido de los módulos y montaje; no comprar conectores incompatibles. |
| Archivo independiente del receptor | ESP32 disponible, capacidad de flash sin identificar | Medir memoria y particiones utilizables, retención y tolerancia a cortes antes de agregar una SD. |
| Respaldo CSV en otro soporte | No inventariado en este XLSX | Comprobar disco externo/pendrive disponible y ensayar escritura, desconexión y recuperación. |
| Autonomía terrestre | No inventariada aquí | Identificar portátil, fuente del receptor y conmutación; medir dos horas de operación. |
| Estructura, placas y sistemas de descenso | Fuera de esta lista electrónica | Incorporar BOM de las áreas correspondientes desde Jira y sus evidencias. |

La ausencia de una pieza en esta planilla no demuestra que no exista en otra área. Estas verificaciones pendientes evitan comprar dos veces o cerrar una arquitectura que contradiga decisiones del proyecto.

## Ahorros y límites de reutilización

Uso el ESP32 disponible para la primera opción de gateway; no necesito comprar otro microcontrolador sólo para conectar radio a PC. Mantengo la segunda BlackPill disponible como repuesto/banco hasta acordar su asignación.

Evalúo un archivo en la flash del ESP32 antes de comprar memoria terrestre adicional. El modelo previo estima 1 612 800 bytes para dos horas de registros de 224 bytes. Debo descontar firmware, particiones, metadatos y margen, y probar escrituras y cortes. NVS está orientado a pares clave–valor y funciona mejor con valores pequeños; no doy por resuelto un archivo continuo guardando todos los paquetes como un único blob. [Referencia Espressif](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/nvs_flash.html).

La AT24C32 es una familia de 32 Kbit: aproximadamente 4096 bytes, no 32 KB. A 224 bytes por registro entrarían sólo 18 registros antes de reservar espacio de configuración. Sirve para evaluar contador, CAL y estado persistente, no para respaldar dos horas de telemetría. Confirmo el chip del módulo antes de aplicar límites de escritura. [Referencia de familia Microchip](https://www.microchip.com/en-us/product/AT24C32E).

El INA3221 puede aportar canales para batería, señal solar y otra rama acordada; no necesito un segundo medidor para cada magnitud por defecto. Con un shunt hipotético de 0,1 ohm y el paso de 40 µV de su conversor:

$$\Delta I = \frac{40\,\mu\mathrm{V}}{0{,}1\,\Omega}=0{,}4\,\mathrm{mA}.$$

Es resolución nominal, no exactitud. Debo verificar resistencia real, offset, topología y comportamiento del panel bajo carga. No prometo concentración de radiación ni porcentaje de batería a partir de una lectura aislada. [Datasheet TI](https://www.ti.com/lit/ds/symlink/ina3221.pdf).

Los capacitores previstos no acreditan respaldo de un segundo. Bajo el ejemplo ideal de 100 mA y caída admisible de 0,5 V:

$$\Delta t = \frac{C\,\Delta V}{I}.$$

470 µF darían aproximadamente 2,35 ms; 100 µF, 0,50 ms. Faltan ESR, regulación, tolerancia y carga real. Pueden ayudar con transitorios; la continuidad y el cierre de escrituras requieren un diseño y ensayo propios.

No priorizo por ahora sensores adicionales, una FRAM o una segunda estación completa sin una falla demostrada que los justifique. Cámaras y elementos obligatorios mantienen prioridad sobre esas ampliaciones.

## Control de presupuesto

C9 exige costo del CanSat inferior a ARS 1 000 000 y excluye herramientas de análisis y soporte en tierra. Separo tres registros: costo de componentes instalados en vuelo, equipo terrestre y herramientas/repuestos de desarrollo. Debo confirmar el criterio de valorización de material propio; tener una pieza disponible no permite declararla de costo cero sin criterio aceptado.

El XLSX contiene precios aproximados como texto, no importes de compra ni un total calculado. No calculo presupuesto libre a partir del presupuesto histórico de otro hardware.

Sólo para orientar prioridades, las dos radios y la baliza pendientes suman según la planilla:

| Asignación | Estimación textual ARS |
| --- | ---: |
| Radio de vuelo y baliza | 18 800–20 800 |
| Radio terrestre | 16 800 |
| Ambas radios y baliza | 35 600–37 600 |

Faltan antenas si no están incluidas, interruptores, capacitores, conectores y otras partidas sin precio. Son referencias del XLSX, no cotizaciones actuales verificadas.

Otro cálculo ilustrativo, con una unidad instalada de cada componente electrónico de vuelo listado y precios interpretados como unitarios, da ARS 98 600–105 400. Usar el MG90S agregaría ARS 7200. Este subtotal excluye tarjeta de memoria, cámaras, regulación/protección final, placas, estructura, mecanismos, sistemas de descenso y partidas auxiliares. No demuestra que el CanSat completo cumpla el tope.

Antes de recomendar una compra nueva cierro la función, requisito, cantidad instalada, pieza disponible, costo y falla que cubre. Reservo margen en el presupuesto completo; no comprometo el saldo que sólo parece libre porque faltan subsistemas.

## Cruce con Jira al habilitar lectura

Revisaré ambas cuentas por identificador de Atlassian, sin unirlas por parecido de nombre. Para las tareas de Ground Station y sus dependencias registraré clave de incidencia, requisito, decisión, estado, responsable, criterio de aceptación, evidencia y enlace a código/archivo. Revisaré descripciones, comentarios relevantes, subtareas, épicas y dependencias del backlog.

Una tarea pendiente puede contener una decisión de diseño válida para el PDR; una tarea terminada no acredita por sí sola un ensayo aprobado. El documento debe distinguir diseño acordado, implementación y evidencia de verificación.

Hasta completar esa lectura, las prioridades de compras de este análisis son provisionales. No creé, comenté, reasigné ni modifiqué incidencias.
