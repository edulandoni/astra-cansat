# 26/10/2026 — ACTUALIZACIÓN 15: reproducir la secuencia conservada

[ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39) · [ASTRA-41](https://astrateam2026.atlassian.net/browse/ASTRA-41). Continúo el [candidato compilado](2026-10-26-candidato-secuencia-14.md), que sigue sin carga ni ensayo físico nuevo.

## Qué nos aporta

Agregué un visor nativo de secuencias guardadas, accesible desde Cámaras en el Laboratorio. Al elegir cámara 1 o cámara 2 y una carpeta, primero verifico identidad, imágenes y cierre; después puedo reproducir los cuadros con sus intervalos declarados, pausar y volver al inicio. Es material conservado, identificado como tal, y no una transmisión en vivo.

Este paso permite revisar movimiento y continuidad cuando tengamos una secuencia física. No convierte las fotos sueltas anteriores en una grabación, no las concatena como si fueran video real y no abre puertos ni envía órdenes. La escena y la cadencia de cámara siguen pendientes del ensayo.

## Implementación y comprobación

`sequence_player.Archive` usa el verificador existente, conserva los tiempos relativos a la primera imagen y vuelve a comprobar la huella de cada cuadro al cargarlo. Rechaza secuencia abierta/inconsistente y archivos cambiados después de verificar. Cuando selecciono una cámara del registro privado, una carpeta marcada como muestra de PC no puede pasar por esa unidad.

El reloj de reproducción usa tiempo monótono, conserva la posición al pausar y no inventa una duración para el último cuadro. El intervalo informado va del primer al último instante. La reproducción sigue las marcas; si la pantalla se demora puede saltar cuadros al mostrar, sin cambiar archivos. El visor no contiene audio ni acredita un formato de video exportado.

Pasaron 34 pruebas del banco de cámaras. Las tres nuevas prueban intervalos irregulares y selección temporal, pausas/reanudación/inicio, rechazo de secuencia incompleta, archivo modificado y muestra de PC usada como cámara. Las pruebas usan imágenes y relojes ficticios de PC. La comprobación de sintaxis/importación de los módulos también pasó. El [control de esta actualización](../../evidence/2026-10-26-secuencia-preparacion/control-02-reproduccion.json) conserva alcance, huellas y vínculo a la compilación anterior sin reemplazar su registro.

No abrí ninguna ventana para esta comprobación. La revisión visual del visor y de sus botones nuevos queda pendiente, respetando que la PC está en uso. No digo que los tests de reloj demuestren dibujo en pantalla o reproducción física correcta.

## Alcance para el PDR y siguiente paso

Puedo mostrar el código y la prueba del cálculo temporal, junto con las fotos físicas anteriores y sus límites. Para demostrar una grabación necesito cargar el candidato con la unidad preparada, obtener la secuencia y leerla desde la tarjeta; después inspeccionar la escena y el visor. El circuito/medición de energía, la estabilidad de arranque/reset, grabación prolongada, exportación de video, audio y comandos/eventos de Edu siguen pendientes.

El objetivo completo no está terminado: falta evidencia de esos pasos. El Laboratorio conserva el recorrido sin placas y todos los informes anteriores.
