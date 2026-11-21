# ASTRA-22 · Pantalla de misión y aceptación

La vista Operación reúne los 22 campos del perfil de banco junto con altura, tensión, corriente, aceleración y velocidad angular. Mantiene fuente, edad, contador RX válido, huecos y estado de escritura. El contador TX sigue visible como campo del emisor. El texto de operación usa 14 pt sobre fondo claro. La vista detallada conserva diagnóstico y configuración. La entrada es `python station.py`.

La vista anterior obligaba a abrir las pestañas de variables y gráficos. Mantener una sola pantalla de operación reduce los cambios de vista. Reutilizamos los gráficos y el motor de adquisición para conservar unidades, separación de segmentos y trazabilidad del diario.

**Validación pendiente de la nueva revisión.** El [PDR v0.3.7](https://docs.google.com/presentation/d/1ouatMaYsKT0uvwUrXoirT0H-dkGsFZff3Q1YFQW8iuk/edit) conserva la captura de la revisión anterior y agrega la lámina 74A. La captura corresponde a reproducción de banco de una versión anterior, con guardado y bloqueo de comandos observados. El cambio actual se publicó desde el conector GitHub, sin ejecución Qt.

Para verificar la revisión actual, correr `python -m unittest test_station_mission` desde ground-station en un entorno Qt autorizado. La prueba usa el diario de banco y verifica geometría, recepción de muestras, bloqueo de comandos, indicaciones con estados inyectados y resumen de sesión. La inyección de un estado de escritor comprueba el aviso de la interfaz. La desconexión de un disco debe probarse físicamente. El ensayo exterior, la interoperabilidad RF y los medios independientes conservan sus criterios de aceptación.
