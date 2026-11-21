# ASTRA-22 · Verificación de operación G12 y G13

20 de noviembre de 2026 · Actualización de [Actualización v0.3.7](Actualizacion_v037.md).

## Resultado de software

Probé la [revisión 78b735d](https://github.com/edulandoni/astra-cansat/commit/78b735db71b943e4d1bffa6912f890668c23c40a) en Colab, sobre Linux, Python 3.13.18 y PySide6 6.12.0 con Qt offscreen. La prueba de aceptación terminó correctamente. La ventana de 1600 × 1000 mostró a la vez los 22 campos del perfil de banco y los cinco grupos de gráficos. La prueba comprobó la geometría visible, el ajuste vertical de los valores y la ausencia de pestañas visibles, y que la ventana archivó el resumen al cerrar. Los comandos permanecieron deshabilitados en reproducción. Inyecté antigüedad de muestra, GPS con cero satélites y un error de escritor en una instantánea para comprobar la indicación de cada estado en la interfaz.

La [captura Qt del PDR, lámina 74](https://docs.google.com/presentation/d/1ouatMaYsKT0uvwUrXoirT0H-dkGsFZff3Q1YFQW8iuk/edit#slide=id.p90) muestra una reproducción a 1× con 15 RX válidos, 0 huecos y 15 filas guardadas en el destino principal. El registro proviene de un emisor sintético usado en el banco. La captura identifica su origen como reproducción. Su SHA-256 original es `34f03e44d4c16ee65a8d980a4bee3d277690fbfbf50d653949a4a9dd02929252`. La [entrada archivada](../../../evidence/2026-10-24-banco02/replay-tramas-aceptadas-entrada-04.jsonl) tiene SHA-256 `523a326d971ab77062e779207056ac1b5ecaaf6db131934ec78942de572a6897`.

Al revisar la primera captura encontré cifras cortadas a la izquierda y leyendas superpuestas. Ajusté la geometría a las métricas reales de la fuente, separé contador y leyenda y reforcé ejes y curvas. La revisión final sitúa las herramientas con pestañas en una ventana de banco separada. Al arrancar la estación no hay fuente seleccionada y el operador tiene toda la telemetría de banco en la pantalla principal. Reutilizar el motor reduce el cambio sobre el registro y la interpretación de la trama. La GUI del laboratorio queda disponible para investigar discrepancias y revisar el diario.

```sh
cd ground-station
python -m pip install PySide6==6.12.0 pyserial
python -m unittest -v test_station_mission
```

## Ensayo G12 preparado para el equipo

| Paso | Configuración o evidencia | Aceptación propuesta |
| --- | --- | --- |
| Preparación | Registrar revisión GCS, equipo y panel previstos, resolución, escala, brillo, batería, hora, orientación y condiciones de iluminación. Usar el mismo diario de referencia, con la estación portátil en su montaje propuesto. | Configuración identificada y reproducible. |
| Inspección en interior | Fotografiar pantalla y escala. Revisar texto de operación de al menos 14 pt, texto oscuro sobre fondo claro, ejes y curvas destacados, cinco gráficos y 22 lecturas al mismo tiempo. | Cada dato, unidad, escala y leyenda se lee completo a la resolución de uso. |
| Demostración exterior | Hacer correr la misma reproducción bajo sol directo y consignar distancia de operación, orientación y reflejos. Pedir al operador que lea temperatura, posición, RX, huecos, estado, contador y la tendencia de cada gráfico. Repetir con las orientaciones previstas y conservar foto de la pantalla en el montaje real. | El operador identifica los datos y unidades sin acercarse ni navegar, y distingue la fuente, los avisos y cada serie. Registrar cualquier diferencia contra la referencia. |
| Cierre | Guardar fecha, operador, foto, resultado por punto y configuración. Repetir con el enlace y la definición de telemetría de vuelo acordados. | El dato respaldado por cada ensayo queda trazado a su revisión y condiciones. |

La aceptación en software cubre el perfil de banco y la revisión identificada. Quedan la legibilidad en el equipo exterior, la comparación completa contra el ICD de vuelo, el enlace RF y el comportamiento con medios físicos independientes. El error de escritor inyectado sólo verifica la señal al operador. La comprobación de persistencia ante desconexión necesita un ensayo físico.
