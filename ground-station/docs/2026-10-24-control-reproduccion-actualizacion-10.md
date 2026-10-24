# 24/10/2026 — ACTUALIZACIÓN 10: alcance del manifiesto y reproducción desde Git

Diarios: [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21) y [ASTRA-33](https://astrateam2026.atlassian.net/browse/ASTRA-33). Aclaro el procedimiento de la [aceptación 09](2026-10-24-aceptacion-banco-usb-actualizacion-09.md), sin reemplazarla ni alterar resultados.

En el control de publicación comprobé que el manifiesto del directorio congelado contiene también 22 productos de compilación ignorados por Git, de los sketches v0.1 y v0.2. Una comparación que intentó buscarlos en Git se detuvo porque esos archivos no están versionados. No son módulos importados por la adquisición ni representan por sí solos el firmware cargado; sus huellas se conservaron por copiar el árbol local completo. No uso esos binarios heredados para volver a programar la placa.

Amplié el control: los 29 archivos versionados de la copia congelada coinciden byte a byte con el commit de fuente del ensayo, sin diferencias. El CSV publicado en Git también conserva exactamente la huella del original. El archivo de aplicación cargado en la última programación se conserva por separado, con su tamaño y huella en el control. El manifiesto original queda intacto; no elimino sus entradas para aparentar que era un inventario exclusivo de Git.

La exportación con git archive del procedimiento 09 reproduce la fuente necesaria para el banco Python; no reproduce esos 22 productos ignorados. Si recompilo firmware, uso el sketch/versiones documentados y genero artefactos nuevos con sus propias huellas. No presento compilación reproducible binariamente ni restauración de flash como pruebas realizadas.

[Control completo, archivos coincidentes y exclusiones](../evidence/2026-10-24-banco02/control-fuentes-reproduccion-14.json). La aceptación de 7261 paquetes, su duración, CSV, memoria y reconstrucción no cambió por esta aclaración. Mantengo la distinción entre fuente ejecutada, artefacto de carga y archivos auxiliares copiados.
