# 26/10/2026 — ACTUALIZACIÓN: pantalla nativa para comprobar las cámaras

Diario: [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39). Continúo los [ensayos de fotos y microSD de ambas unidades](2026-10-26-ambas-camaras-sd-y-lector-07.md). Esta entrada agrega interfaz de banco; no repite ni amplía por sí sola aquellos resultados físicos.

Preparé `camera_panel.py`, una ventana nativa con una ficha por cámara. Elijo explícitamente un puerto y puedo pedir sólo foto o foto más comprobación de SD. La aplicación no selecciona un puerto, registra unidades nuevas ni reinicia placas automáticamente. Antes de pedir captura o escritura comprueba que la identidad corresponda a la unidad registrada. Mantengo ese registro privado; no publico identificadores de hardware en el código.

Cada petición ejecuta una sola vez el receptor existente en otro proceso, conserva resultado y diagnóstico en una carpeta nueva y vuelve a verificar archivo, identidad, pedido, longitud, CRC, huella y decodificación. No reenvío órdenes automáticamente. La interfaz admite una operación a la vez y espera su finalización antes de cerrar; no termino un proceso mientras podría estar cerrando un archivo en la tarjeta. Las dos unidades tienen resultados propios y puedo comprobarlas por turnos usando una sola base.

Una foto válida y una SD fallida se presentan por separado. Una foto conservada muestra fecha, antigüedad y la aclaración de que no confirma la ronda actual. Abrir un resultado anterior vuelve a comprobarlo, pero no lo cuenta como chequeo nuevo. Iniciar otra ronda conserva las fotos anteriores y pone en cero las confirmaciones actuales. El resumen sólo cuenta las unidades con foto y SD confirmadas en esa ronda; una falla individual no aprueba el conjunto.

## Pruebas y revisión

Pasaron diecinueve pruebas: las doce del receptor y siete de sesión/identidad/conservación. Incluyen identidad duplicada, unidad o pedido distintos, foto conservada alterada, captura correcta con SD fallida, falta de resultado sin reenvío y conservación del diagnóstico, exclusión de operaciones simultáneas y ausencia de reutilización de éxitos de otra ronda.

Construí la ventana y cargué las fotos reales conservadas de ambas cámaras sin abrir puertos: las fotos aparecieron como históricas y el resumen siguió en cero. Revisé visualmente esa pantalla. El primer tamaño cortaba texto inferior; reduje las imágenes y reservé espacio para las aclaraciones. La revisión corregida mostró completas las fotos, fechas, antigüedad y alcance. Después retiré el control de reinicio de la ventana: las maniobras de diagnóstico explícitas siguen separadas en el receptor de consola. Cerré las ventanas de prueba al terminar.

El [control de software](../../evidence/2026-10-26-camera-panel/control.json) conserva pruebas, huellas y límites. No publiqué fotos del entorno como parte de esta revisión de interfaz.

## Qué falta

Todavía no pedí una captura física nueva desde los botones de esta pantalla. La operación física del receptor de consola está documentada en la entrada anterior; no la traslado como aprobación de la nueva interfaz. La ventana permanece separada de la aplicación de telemetría, cuyos fuentes no modifiqué. Queda pendiente probar los botones con cada unidad e integrar el acceso desde groundstation.

No hay grabación, corte de alimentación ni comandos de vuelo implementados por esta pantalla. Video continuo, recuperación, medición de energía y adaptación al contrato definido por Edu siguen pendientes en ASTRA-39/ASTRA-24. Las fotos por turnos no acreditan simultaneidad ni una microSD por cámara.
