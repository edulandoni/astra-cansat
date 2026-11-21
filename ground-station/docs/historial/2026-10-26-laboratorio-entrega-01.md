# 26/10/2026 — Laboratorio: primera integración para reuniones

Diario: [ASTRA-41](https://astrateam2026.atlassian.net/browse/ASTRA-41). [Objetivo vigente](2026-10-26-objetivo-laboratorio.md) · [Aplicación e instrucciones](../../laboratorio/README.md).

## Qué nos aporta

Reuní las demostraciones y el razonamiento en una aplicación nativa. Puedo presentar avances sin recorrer todo Jira: una misión de PC, fallos, el paquete de datos, fotos conservadas de ambas cámaras, comparación LoRa y antecedentes/diseño/PDR. Cada sección explica primero utilidad y límites, y después el fundamento técnico. Los informes locales conservan el detalle.

No cambié firmware ni abrí puertos físicos en esta integración. El recorrido funciona sin placas ni Internet. La consulta al fabricante requiere Internet; las explicaciones y la fórmula ya están disponibles localmente. El acceso local «ASTRA Laboratorio» usa la instalación de Python existente; no es un ejecutable autónomo para otra PC.

## Implementación

La simulación reutiliza Engine, Store y PCBench del banco USB, con sesiones nuevas, colas acotadas y cierre de escritores. El gráfico conserva hasta 180 muestras. La calculadora reutiliza airtime_lora. La inspección de paquetes muestra los 22 campos y su tamaño ASCII, sin inventar un empaquetado binario de vuelo.

Las imágenes se leen desde una configuración privada, con fecha/origen y aviso de evidencia conservada. No publiqué fotos nuevas, identificadores físicos ni rutas privadas en el repositorio. Sin configuración, el programa explica que falta evidencia local. El panel de cámaras y la estación completa son ventanas independientes accesibles desde el Laboratorio. La recepción USB requiere elección explícita de puerto; no se activa al iniciar la app.

## Verificación realizada

Prueba integrada de las cinco misiones completas, 131 instantes por escenario, aceleración 10× para ensayar software. No es prueba de tiempo real ni de hardware:

| Escenario | Válidos | Inválidos | Huecos al finalizar |
|---|---:|---:|---:|
| NOMINAL | 131 | 0 | 0 |
| PACKET_LOSS | 118 | 0 | 13 |
| CORRUPTED_PACKET | 121 | 10 | 10 |
| GPS_LOSS | 131 | 0 | 0 |
| RESET lógico | 128 | 0 | 3 |

Los diarios contienen paquetes, las colas terminan sin pendientes/descartes y los hilos de emisor/escritura cierran. La prueba GPS de esta integración acredita la misión procesada; la semántica de retención conserva sus pruebas en el banco, no se deduce del contador de válidos.

Otros controles: muestra inicial de 124 bytes terminada en CR y 22 campos; 55 bytes/SF7/BW125k/CR4/5 = 107,776 ms; 100 bytes/SF10 bajo las mismas hipótesis supera un segundo. Importación y construcción nativa de siete secciones, existencia de los nueve informes enlazados, apertura/cierre sin hardware.

Revisión visual: recorrido, misión nominal avanzando con gráfico y contadores, fotos conservadas, paquete y calculadora LoRa; desplegué el detalle técnico. El ensayo nominal desde la interfaz produjo 131 CSV y 676 eventos de diario, pendientes y descartes finales cero, sin errores de escritura. Las capturas privadas y registros permanecen locales. No ensayé aquí los botones de recepción física ni repetí las fotos.

## Qué puedo afirmar para el PDR

Dispongo de una herramienta reproducible para explicar y mostrar el banco. La simulación y la calculadora están identificadas; las pruebas físicas anteriores conservan sus propios informes. El Laboratorio aporta presentación y acceso a evidencia, no una declaración automática de cumplimiento de requisitos.

## Pendientes

Revisar el recorrido con el equipo en la reunión. Mantener contenido y fuentes al incorporar avances, conservando historial en Jira. Video, audio, consumo, apagado, arranque estable de cámaras y pruebas RF siguen pendientes en sus tareas. RESET de PC es lógico; no acredita recuperación ante pérdida de energía. El formato y los comandos de vuelo siguen bajo coordinación de Edu. Cámaras permanece como objetivo secundario.
