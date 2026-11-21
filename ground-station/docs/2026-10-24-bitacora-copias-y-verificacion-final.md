# 24/10/2026 — Bitácora: conservo la fotografía del evento al recibirlo

Diarios: [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21) y [ASTRA-34](https://astrateam2026.atlassian.net/browse/ASTRA-34). Complemento la [campaña de órdenes](2026-10-24-ordenes-negativas-usb.md), sin modificar sus archivos originales.

Al probar una orden dirigida deliberadamente al equipo ajeno revisé el límite entre el productor y los escritores asíncronos. Validar que un diccionario se pueda serializar no lo independiza de sus listas anidadas: el productor podía modificar un dato después de emit y antes de que el escritor lo guardara. Eso también importa para listas de rangos de pérdidas que continúan creciendo.

Ahora copio el contenido completo al emitir y devuelvo al llamador otra copia independiente. Los escritores leen la fotografía que se tomó al emitir, no una referencia mutable del productor. No reescribo archivos previos ni concluyo que una captura histórica tenga corrupción por haber identificado este riesgo de API.

La prueba nueva retiene una escritura, modifica la lista original y la copia devuelta y comprueba que el diario conserva la lista inicial. Pasaron las 22 pruebas del banco. Después ejecuté una segunda campaña física de órdenes con la revisión final; su resultado y huellas se conservan en [usb-guardas-02](../evidence/2026-10-24-avances/usb-guardas-02/resultado.json), separados de la primera pasada.

En la prueba de equipo ajeno la herramienta prepara una orden propia y cambia su destinatario de equipo bajo el bloqueo del motor antes de transmitir. El registro de encolado representa la intención previa y el de envío representa los bytes lógicos que realmente se mandaron; el caso RUN_WRONG_TEAM del informe identifica la inyección. No es una función de envío a equipos ajenos expuesta por la GUI ni un contrato de vuelo.

Volví a ejecutar las seis trazas de calidad con la revisión final en [calidad-02](../evidence/2026-10-24-avances/calidad-02/resultado.json): mantienen resultados y límites, con nuevas huellas. Conservo calidad-01 como primera ejecución. La demostración de dos horas se mantiene atribuida a su snapshot anterior: esta verificación final es una misión corta adicional, no dos horas nuevas ni una prueba de radio.
