# 25/10/2026 — Mostrar lo que hicimos con la placa

Diario: [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22). Conservo las pruebas anteriores y agrego esta explicación para mostrar el trabajo.

## Para contarlo de humano a humano

Programé la placa para que haga de CanSat durante un vuelo de práctica. Aunque está quieta sobre la mesa, inventa una subida y una bajada y manda un mensaje por segundo a la computadora. La aplicación que hicimos recibe esos mensajes, muestra los cambios y guarda una copia para revisar después.

Además del caso normal, probamos qué pasa cuando faltan mensajes, llegan dañados, desaparece el GPS simulado o se reinicia la placa. La idea es que la estación ayude a entender qué pasó y conserve los datos, incluso cuando algo sale mal.

Ya probamos la comunicación real entre esta placa y la PC por cable USB. Los valores del vuelo siguen siendo inventados. Todavía falta probar radio con Edu, acordar el formato compartido y medir con sensores reales.

## Para mostrarlo

Abrí [Ver demostración](Ver_demostracion.html). Usa una captura de 131 mensajes guardados en la campaña USB del 24/10, que ya estaba verificada. Funciona sin Internet, permite pausar, recorrer y repetir; arranca a 4× (unos 33 segundos). Es reproducción, no recepción en vivo ni otra campaña de aceptación. [Procedencia y huella del CSV](procedencia.json). La [vista rápida animada](Vista_rapida.gif) reproduce esos mismos datos a aproximadamente 8×; es una animación propia, no una filmación de la pantalla o de la placa.

Para recepción en vivo abro el banco USB v0.2 con el puerto comprobado y la placa conectada. Iniciar repite el escenario seleccionado; Parar detiene la simulación. Evito abrir dos receptores para un mismo puerto. Si la placa no está conectada, no presento la reproducción como funcionamiento en vivo.

También abrí una sesión USB física nueva el 25/10. Reinicié una vez por RTS, no cargué firmware ni pedí la secuencia BOOT. La pantalla observada mostró ASCENT, contador 17 y altura sintética de 255 m. El inicio conservó una trama excesiva descartada del parser: está registrada, su causa no quedó determinada y no la oculto. Volví a iniciar la simulación después de conservar 124 muestras del primer RUN; la sesión interactiva contiene ejecuciones y cambios de contexto que quedan separados. No presento esos segmentos interrumpidos como misiones completas ni como pérdida de radio. La animación usa exclusivamente la captura completa del 24/10. Esto no identifica la causa de aquella trama ni certifica RF.

La investigación, los ensayos de fallos y sus límites siguen en [la revisión técnica del 24/10](../../historial/2026-10-24-revision-tareas-y-avances.md). Esta animación explica una prueba; no agrega una validación de vuelo.

## Verificación de la presentación

Contrasté las 131 filas incluidas con el CSV original. Revisé el visor en navegador: avanzó hasta mensaje 71 / altura sintética 233,3 m; la pausa quedó en mensaje 83 / 173,3 m. Corregí un error de avance de la animación detectado antes de publicar y volví a comprobar movimiento y pausa. La [captura del visor](Visor_verificado.png) conserva esa observación previa al ajuste menor del rótulo «Etapa». El GIF tiene 66 cuadros y reproduce los mismos valores; no es una prueba adicional de recepción.

La configuración de Windows de ChatGPT se diagnosticó por separado y queda en un registro privado, sin publicar configuración o registros de la PC en este repositorio. La ejecución de una orden en el nuevo aislamiento pasó; la recarga de la aplicación y desaparición del cartel todavía requieren comprobación.
