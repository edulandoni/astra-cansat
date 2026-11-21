# Ground Station: estado y continuidad
Autor: Cristian Ponsone. Revisión: 12 de octubre de 2026.

## Responsabilidad y alcance

Me encargo de la recepción, el registro y la visualización de telemetría, y de la interfaz de telecomandos. La revisión de esta fecha reconstruye el estado del trabajo previo, contrasta el código con los documentos y deja identificados los pasos para desarrollar la estación operativa. No modifica las aplicaciones originales ni cierra la elección de tecnología.

## Prioridades actualizadas

Jira ASTRA pasa a ser la fuente principal de decisiones, tareas y trazabilidad del PDR. La lista electrónica de Drive utilizada para las compras acredita disponibilidad: ambos tonos verdes significan material ya disponible y los demás renglones siguen pendientes, según el criterio acordado. El [inventario y los faltantes al 13/10](https://github.com/edulandoni/astra-cansat/blob/docs/ground-station-continuidad/docs/research/ground-station-inventario-y-faltantes-2026-10-13.md) documentan 17 renglones verdes y 7 pendientes. La lectura de Jira sigue pendiente de acceso autenticado; no se modificaron incidencias. Los HTML de prueba son antecedentes prescindibles y no fijan la arquitectura nueva. La prioridad es preparar el PDR, cerrar las interfaces con electrónica y fundamentar una mejora mediante ensayos. El [relevamiento argentino y los cálculos de capacidad](https://github.com/edulandoni/astra-cansat/blob/docs/ground-station-continuidad/docs/research/ground-station-relevamiento-argentino-2026-10-12.md) desarrollan este avance.

## Fuentes y ubicación

| Fuente | Ubicación |
| --- | --- |
| Código y contratos del equipo | [Repositorio ASTRA](https://github.com/edulandoni/astra-cansat) |
| Carpeta de trabajo | [Ground Station en Drive](https://drive.google.com/drive/folders/1A0cwBwNxL71eGML2LtCtk9gcUtgK1u50) |
| Paquete original y versiones anteriores | [Archivo original](https://drive.google.com/drive/folders/1fP87iRnI99sJf3BuwS-V5zAXWfBRCnYM) |
| Estación v04 y documentación | [Iteracion_04](https://drive.google.com/drive/folders/1vcr9KgbrnaA7b23bmk3VltzrHXlAAtPV) |
| Laboratorio, presupuesto y análisis v05 | [Iteracion_05](https://drive.google.com/drive/folders/1SKKEGmYGELbBF5yhSfbnjvvJG8qsXx_7) |
| Lista electrónica del equipo | [electronica.xlsx](https://docs.google.com/spreadsheets/d/1PhY-BefCl1SAa7RWicEEAamdvEynt5At/edit) |
| Reglamento técnico | [Anexo CONAE 2026–2027](https://www.argentina.gob.ar/sites/default/files/2026/08/anexo_requerimientos_tecnicos_-_cansat_universitario_2026-2027.pdf) |
| Condiciones generales | [Bases CONAE 2026–2027](https://www.argentina.gob.ar/sites/default/files/2026/08/bases_y_condiciones_-_cansat_universitario_2026-2027.pdf) |

El inventario del nuevo Drive contiene 93 archivos y 17 subcarpetas internas, contando versiones y duplicados. Se recuperaron 81 archivos de código, documentación, datos y texto; se obtuvo extracción textual de los 10 PDF y se inspeccionaron las dos capturas de referencia. El análisis se concentra en la estación y sus dependencias. La extracción textual de un PDF no equivale a una inspección visual completa de cada página.

Se cotejaron 34 archivos con bytes disponibles contra los SHA-256 del manifest original: todos coinciden. No se extiende esa comprobación a los archivos obtenidos mediante extracción de texto. La copia independiente de la estación coincide con los 13 archivos de la v04 del paquete en las copias de trabajo recuperadas.

## Estado verificado

| Elemento | Resultado de la revisión |
| --- | --- |
| GitHub | Estructura inicial; todavía no contiene la implementación de Ground Station. |
| Contrato compartido | Telemetría, comandos, estados y errores en protocol/ siguen como TBD. |
| Estación v04 | Aplicación offline con recepción de bytes simulados, validación, contadores, gráficos, ayudas y exportación. |
| Laboratorio v05 | Aplicación separada con altura barométrica, pendiente de descenso, potencia e integración de energía. |
| Entrada real | No hay adaptador de puerto serie ni recepción de radio. El parser rechaza MODE=F deliberadamente. |
| Persistencia terrestre | Exportación manual JSON/CSV; no hay escritura continua ni segunda copia física verificada. |
| Telecomandos | Emisor ficticio; un eco cambia el estado del pedido, pero no acredita ejecución física. |
| Hardware | La documentación no acredita un conjunto integrado ni ensayos físicos. |
| Jira | Proyecto ASTRA identificado como fuente principal de trazabilidad. El navegador requiere autenticación; la lectura de incidencias sigue pendiente. No se hicieron cambios en Jira. |

La estación independiente no incluye la carpeta hermana Referencias que usa la ayuda. Para ejecutarla con esas fuentes, conservar la estructura completa de Iteracion_04.

## Arquitectura existente

- **core.js**: modelo interno CS-SIM/1, generador, reconstrucción por fragmentos, validación, rangos, contadores, registro y reproducción.
- **protocol.js**: adaptador de práctica CONAE-ASCII-S/0.1, 22 campos base separados por comas, CR como cierre y opcionales después de un campo vacío.
- **app.js**: controles, presentación y exportación. Consume el receptor; no toma los valores directamente del generador.
- **learning.js**: explicaciones de los datos, gráficos, controles y límites del ensayo.
- **mediciones.js**: cuatro funciones independientes para cálculos; todavía no integradas en la pantalla de la estación.
- **laboratorio.js**: interfaz de aprendizaje de esos cálculos y escenarios de datos inválidos.

Los identificadores de transporte del prototipo son internos; no son versiones oficiales del reglamento. TEAM_ID=0000 es ficticio. El tiempo de recepción del ensayo y los campos UTC del paquete deben seguir siendo conceptos distintos.

## Verificación repetida en esta revisión

| Comprobación | Resultado | Alcance |
| --- | --- | --- |
| Pruebas existentes de estación v04 | 13 casos aprobados | Fragmentación, ASCII/CR, validación, ausencia GPS, duplicados, tardíos, reinicio, eco, reproducción, CSV y límites. |
| Pruebas existentes de mediciones v05 | 12 casos aprobados | Referencia de presión, pendiente con tiempos reales, huecos, potencia, integración y cobertura. |
| Presupuesto JSON v05 | 44 partidas reconciliadas | Suma independiente de cantidad por precio presupuestado. |
| Aplicaciones originales | Sin modificaciones | Se trabajó sobre copias recuperadas. |

El lanzador de pruebas de Node con aislamiento de procesos fue bloqueado por el entorno; las mismas pruebas se ejecutaron directamente y aprobaron. No se repitió la prueba visual en navegador: la apertura del archivo local fue rechazada por la política del navegador. Los ensayos visuales consignados en el paquete siguen siendo evidencia previa, no ensayos repetidos en esta revisión.

El XLSX se pudo leer mediante extracción de contenido. No se obtuvieron sus bytes originales para verificar fórmulas, recálculo o presentación en Excel. La reconciliación de esta revisión corresponde al JSON, no a una certificación del libro.

## Brechas para una estación operativa

1. **Contrato de vuelo**: acordar telemetría, comandos, estados, unidades, ausencia de datos, reinicios y opcionales con Flight Software. No aceptar F simplemente quitando una restricción del demo.
2. **Transporte**: implementar entrada y salida reales, desconexión/reconexión y registro de bytes. Una lectura del puerto puede traer medio paquete o varios.
3. **Registro continuo**: escribir durante la recepción, detectar errores de escritura y conservar respaldo en otro soporte. Exportar al terminar no sustituye ese registro.
4. **Independencia de interfaz**: abrir una ayuda hoy pausa la simulación. En operación, recepción y escritura deben continuar aunque la interfaz muestre ayudas o deje de dibujar.
5. **Cálculos y calidad**: integrar las funciones del laboratorio con origen, unidad, parámetros, validez y cobertura. La edad de un paquete no acredita frescura individual de sensores.
6. **Límites de sesión**: el prototipo limita la generación a 3600 segundos y guarda registros en memoria. Revisar retención y escritura para sesiones prolongadas; no trasladar esos límites a operación sin dimensionarlos.
7. **CSV de entrega**: implementar el nombre Flight_<TEAM_ID>.csv, encabezados acordados y procedimiento de entrega; conservar por separado los ensayos llamados SIMULACION.
8. **Interfaz y campo**: repetir G12/G13 con el portátil real, viewport, escala, sol y distancia de lectura; verificar energía y receptor físicos para G9–G11.

No se decidió todavía entre aplicación web, aplicación de escritorio o interfaz web con servicio local. Primero necesito definir acceso al puerto y escritura de respaldo en los equipos de uso. El trabajo en la nube permite mantener código y documentación disponibles; la recepción de radio seguirá necesitando un equipo local junto al receptor.

## Requisitos que guían Ground Station

| Requisitos | Evidencia actual | Cierre pendiente |
| --- | --- | --- |
| G1, G15 | CAL y otros telecomandos ficticios | Salida real, eco y resultado cuando corresponda. |
| G2 | Exportación manual | Escritura continua, respaldo y recuperación ante interrupción. |
| G3, F2, F3 | UTC sintético y reloj de sesión separados | Sincronización, fecha, medianoche y persistencia del vehículo. |
| G4, G5, G7, G8 | Código propio y presentación de datos simulados | Flujo real y validación integrada. |
| G6 | Unidades explícitas en el prototipo | Resolver ACCEL y correspondencia entre regla general y formato. |
| G9–G11 | Sin evidencia física de esta revisión | Portátil, receptor, antena y autonomía de campo. |
| G12, G13 | Diseño claro, fuente base de 19 px y vista sin pestañas | Prueba visual de la versión final en el equipo de operación. |
| G14 | Conteos separados; duplicados y tardíos registrados | Acordar la definición de recepción exitosa y pérdidas. |

## Diferencias de hardware y presupuesto

La referencia actual es la lista electrónica de Drive utilizada para las compras: STM32F411, ATGM336H, INA3221 y SX1276, con ESP32 como gateway terrestre ya disponible según el renglón verde de compras. El presupuesto v05 con ESP32 principal, GY-NEO6MV2 e INA219 es histórico y no define la arquitectura actual. Debo confirmar versiones de módulos, pines, alimentación y disponibilidad física; las cantidades de la lista no acreditan instalación.

El manual E220 incluido documenta una dirección de comunicación y filtrado; eso no demuestra por sí solo cumplimiento de NetID/PanID. Tampoco se presume interoperabilidad con SX1276 o XBee por compartir banda.

Reconciliación histórica del presupuesto JSON v05 al 10/10/2026; no es el presupuesto actualizado de la lista de compras:

| Alcance | Base ARS | Con reserva del 20% ARS |
| --- | ---: | ---: |
| Vuelo | 660.784,32 | 792.941,18 |
| Tierra, desarrollo y logística | 393.000,00 | 471.600,00 |
| Conjunto | 1.053.784,32 | 1.264.541,18 |

Son precios de referencia y asignaciones de planificación de esa fecha. No se actualizaron cotizaciones ni stock en esta revisión. No se verificaron compras o componentes instalados.

## Consultas que deben resolverse

- Magnitud y unidad de ACCEL: el formato describe grados por segundo al cuadrado; la IMU del prototipo representa aceleración lineal.
- Signos GPS para sur/oeste y codificación de medidas ausentes.
- Activación automática al separarse frente a CX ON y telemetría antes del lanzamiento.
- Puesta a cero del contador: se menciona un comando, pero no se especifica uno en la lista.
- Mapeo de estados de liberación a los mecanismos reales.
- Señal solar: campo, unidad y comando adicional acordados.
- Número completo de equipo en NetID/PanID para la radio y firmware concretos.
- Cenit/nadir frente a la referencia a norte; longitud en bases frente a anexo.

Estas consultas se preparan para el equipo y el docente. No se enviaron a terceros.

## Próximo paso de Ground Station

Preparar el contrato compartido y los criterios de aceptación del registro para el PDR antes de implementar transporte real. Los prototipos HTML no son un punto de partida obligatorio. La nueva arquitectura debe conservar el dato recibido y permitir reconstruir la sesión; la presentación consume ese registro. El relevamiento argentino identifica alternativas de gateway, límites de radio y un ensayo de diagnóstico de eventos con sensores existentes.

## Cambio de historial y colaboración

Se retiró de la ascendencia de main el commit de prueba eee5f19df6696c43ffd47797ed3468800d07d3b7 y su único archivo. El cambio posterior de Edu se reconstruyó conservando los blobs de las dos imágenes de STM32; el nuevo commit es eacf308a5101f0c12b05d63e749b3a1cb6930690 y acredita a Edu como coautor. Se verificó que la única diferencia entre los árboles anterior y nuevo es la eliminación de la prueba.

La actualización se realizó condicionada al SHA anterior de main. Las copias locales que ya tenían el historial anterior deben sincronizarse antes de volver a subir cambios, preservando cualquier trabajo sin publicar. Quitar un commit de las ramas no garantiza que GitHub deje de servir inmediatamente su URL o que desaparezca de clones anteriores.

