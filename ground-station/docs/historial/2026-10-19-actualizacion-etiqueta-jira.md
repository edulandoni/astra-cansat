# 19/10/2026 — Actualización del control de avisos del respaldo

Actualizo [el cierre anterior](2026-10-19-cierre-publicacion.md) y [las pruebas](../pruebas-2026-10-19.md), conservando ambos documentos originales.

En la comprobación real del comentario de cierre detecté que Jira devuelve la etiqueta como `\[JIRA-GITHUB-SYNC\]`. La comparación inicial reconocía la versión sin escapes y por eso generó una captura adicional del propio aviso. Durante la corrección conservé otra captura con la comparación corregida. Mantengo ambas, con su contenido y huellas, además de las dos capturas iniciales: no borro el resultado del problema.

Corregí la comparación para reconocer ambas formas de la etiqueta y para comparar capturas anteriores con la regla actual, sin reescribir sus manifest históricos. Esto evita una captura extra al cambiar la versión de la regla de comparación. No cambio el texto original de Jira ni la copia conservada; normalizo solo el cálculo que decide si existe un cambio real.

Agregué casos de prueba para la etiqueta escapada y para huellas producidas por una regla anterior. La ejecución final aprobó cinco pruebas del historial. Junto con las nueve del banco y las trece de lógica v04, quedan veintisiete pruebas aprobadas en los conjuntos actuales. Las [salidas de la etiqueta](../../evidence/2026-10-19/pruebas-bitacora-v3-etiqueta-jira.txt) y de la [verificación final de compatibilidad](../../evidence/2026-10-19/pruebas-bitacora-v4-compatibilidad.txt) se conservan por separado.

La repetición con la lectura real que incluye el comentario 10045 devolvió «Sin cambios: conservo la captura anterior» y no creó otra carpeta. Eso comprueba el control de este caso; la programación diaria sigue sin ser un ensayo de ejecución futura.

La entrada local de continuidad escrita antes de esa comprobación afirmaba prematuramente que el primer control no había creado otra captura. Esta actualización deja el resultado real: hubo capturas adicionales, corregí la comparación y el control posterior sí evitó la repetición.

Jira: [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20), [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21). Los avisos del propio respaldo se incorporan al archivo con la siguiente captura por cambios reales y no disparan por sí solos una secuencia infinita.
