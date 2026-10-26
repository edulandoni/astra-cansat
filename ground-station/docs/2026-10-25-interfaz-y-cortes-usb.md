# 25/10/2026 — ACTUALIZACIÓN: interfaz y cortes USB

Trabajo relacionado: [ASTRA-22, interfaz](https://astrateam2026.atlassian.net/browse/ASTRA-22) y [ASTRA-21, recepción y registro](https://astrateam2026.atlassian.net/browse/ASTRA-21). Conservo la [aceptación previa](2026-10-24-aceptacion-banco-usb-actualizacion-09.md) sin atribuir sus dos horas a esta revisión.

## Problema y objetivo

La pantalla reunía muchas cifras sin explicar su alcance. Al quitar el USB aumentaba la edad del último dato, pero no quedaba claro qué había pasado con los mensajes. Organicé la aplicación para poder entender qué recibo, qué guardo y qué desconozco, sin necesitar leer código ni conocer versiones anteriores.

Mantengo la aplicación de escritorio Tk y su estética sencilla. No agrego una página HTML. La placa genera datos ficticios y los envía por USB; no estamos midiendo un vuelo, sensores físicos, batería o radio.

## Uso de la pantalla

Arriba muestro el estado de la recepción, su explicación y el origen de los datos. Los valores se agrupan en Vuelo, Energía, Ubicación GPS y Movimiento. Cada medición marcada con ⓘ abre una explicación de qué significa, su referencia y su unidad. Por ejemplo, altura sobre el inicio explica el cero y qué significa estar a 100 metros; altura GPS explica su referencia al nivel del mar. Las ayudas describen la operación actual. La historia de cambios queda en este diario y en Jira.

Separo seis contadores: muestras recibidas con formato válido, muestras diferentes, guardadas en CSV, esperando guardado, faltantes detectados y mensajes rechazados. Los rótulos aclaran si abarcan la sesión completa de la PC o sólo la ejecución actual. El detalle de cada destino y del registro bruto está en Datos técnicos, archivos y cortes.

Esperando guardado cuenta datos que ya llegaron y todavía esperan confirmación de escritura. No aumenta por mensajes que nunca recibí. Durante un corte muestro «Por determinar» en faltantes. Si vuelve la misma identidad y el contador pasa de 65 a 84, puedo observar el hueco 66..83: 18 muestras. Si vuelve otra identidad de arranque, no comparo contadores de ejecuciones distintas ni invento una pérdida a partir de los segundos transcurridos. Los mensajes tardíos pueden reducir los huecos actuales; el diario conserva lo observado al reconectar.

Conservo el último valor y su antigüedad, identificado como histórico y con otro color. Un contexto nuevo no hereda mediciones actuales del anterior. Los gráficos muestran número de muestra, unidades, leyendas R/P/Y y cortes de línea donde faltan muestras. Al cambiar de ejecución comienzo gráficos separados.

Los botones describen su acción: iniciar/detener ensayo, poner altura en cero, sincronizar hora UTC y consultar batería/solar sintéticas. Deshabilito acciones incompatibles con el estado o con una reproducción. Cerrar conexión USB libera el puerto, pero no garantiza detener la placa; Conectar USB verifica identidad sin reiniciar por sí solo el ensayo. Una detención confirmada no genera una falsa alarma de falta de datos.

## Evidencia y aceptación

El corte se realizó el 25/10 en Argentina; los registros UTC corresponden al 26/10. Publiqué [métricas normalizadas de los ensayos](../evidence/2026-10-25-ui/ensayos-usb.json), [resultado de pruebas](../evidence/2026-10-25-ui/pruebas.json) y [manifiesto de huellas](../evidence/2026-10-25-ui/manifest.json). Conservo privadamente los diarios originales completos y las capturas CSV; publico sus huellas y cantidades sin rutas personales.

| Comprobación | Resultado observado | Alcance |
|---|---|---|
| Datos organizados y explicados | Cuatro grupos, 22 campos y seis gráficos visibles; ayuda de altura verificada en ventana propia | Inspección visual de la aplicación nativa |
| Desenchufar y reenchufar físicamente | Ensayo 03: un corte detectado de 10,14 s; nuevo arranque confirmado; faltantes desconocidos, sin comparar contadores incompatibles | USB y alimentación de esta placa; duración incluye detección y reapertura de Windows |
| Cierre y apertura desde la aplicación | Ensayo 04: 17,375 s detectados; misma identidad; contador 65 → 84, hueco de 18 | Cierre del puerto, diferente del corte físico |
| Conservación final | Ensayo 03: 312 filas CSV, repartidas entre ejecuciones. Ensayo 04: 113 filas y 18 huecos hasta contador 131. Ambos: cero pendientes, errores y descartes por escritor al cerrar | Confirmación de escritura; no resistencia a corte eléctrico |
| Gráfico y alcance de faltantes | Hueco visible al reconectar; último dato histórico al finalizar, sin presentarlo como actual | Captura del ensayo 04 |
| Automatización | 30 pruebas aprobadas en test_bench, test_quality y test_ui | Regresión de software y casos deterministas, no reemplaza la prueba física |
| Identidad y mensajes tardíos | Casos de misma ejecución, nuevo arranque, nueva ejecución, identidad insuficiente y reparación de huecos | Pruebas automáticas |
| Controles y calidad | Casos de detención, reproducción sin órdenes, respuesta desconocida/tardía y resultado de otra ejecución identificado | Pruebas automáticas |

Capturas finales: [pantalla en vivo](../evidence/2026-10-25-ui/04-interfaz-final.jpg), [ayuda de altura](../evidence/2026-10-25-ui/05-ayuda-altura-final.jpg), [puerto cerrado](../evidence/2026-10-25-ui/06-cierre-manual-final.jpg) y [resultado tras reconectar](../evidence/2026-10-25-ui/07-reconexion-final.jpg).

Las capturas 01..03 son intermedias y se conservan como historia: la 02 todavía decía reconexión automática después de cerrar manualmente; corregí ese mensaje y lo verifiqué en la 06. La 03 conserva las ayudas iniciales, reemplazadas por explicaciones de operación y comprobadas en la 05. Cerré el proceso propio del ensayo intermedio 02 para recargarlo después de comprobar puerto cerrado y colas vacías; no presento ese cierre como cierre normal verificado de la GUI. Los ensayos 03 y 04 sí tienen resumen final de almacenamiento.

## Implementación y reproducción

Separo presentación en [desktop.py](../banco-usb-v0.2/desktop.py) y [ui_model.py](../banco-usb-v0.2/ui_model.py); el receptor y la escritura conservan sus responsabilidades. [test_ui.py](../banco-usb-v0.2/test_ui.py) ejercita las transiciones sin depender de una ventana. Agrego registro de cortes y conservación del último dato en engine.py; ajusto calidad para distinguir una parada esperada de datos vencidos. No cambio firmware ni perfil RF.

Desde banco-usb-v0.2 ejecuto `python app.py --port COM5 --auto-run`. Uso únicamente el puerto identificado y libero cualquier otro receptor antes de abrirlo. `--reset-once` es opcional y provoca un nuevo arranque; no hace falta cargar firmware. `Ctrl+M` minimiza sin detener recepción. Para repetir las pruebas de software ejecuto `python -m unittest -q test_bench test_quality test_ui`.

Las métricas conservan las huellas de las fuentes usadas en cada ensayo. Después normalicé finales de línea CRLF a LF para el repositorio, sin cambiar su contenido ejecutable; la prueba de software registrada usa las fuentes publicadas.

## Límites y pendientes

En el ensayo 03 apareció una trama excesiva después de reconectar. Conservo bytes y aviso; su causa sigue pendiente de diagnóstico. El ensayo 04 no registró tramas excesivas. No presento esta revisión como solución de ese incidente.

No repetí dos horas sobre esta interfaz; la campaña prolongada anterior conserva su revisión y resultado propios. Tampoco verifiqué legibilidad bajo sol, pantalla de campo, RF, sensores, autonomía, STM32 o respaldo externo simultáneo. Las colas, historial visible y registro de cortes tienen límites explícitos: 600 eventos por escritor, 300 muestras por gráfico y 64 cortes visibles; el diario completo conserva los eventos mientras su destino pueda escribir. No cierro ASTRA-21 ni ASTRA-22 por estos avances parciales.

Para el PDR puedo afirmar que probé presentación nativa explicada y dos recuperaciones USB distintas, con datos ficticios y conservación comprobada de lo recibido. No puedo afirmar recuperación de mensajes ausentes, número de pérdidas durante un reinicio ni validación del enlace de vuelo.
