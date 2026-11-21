# 19/10/2026 — Qué necesito acordar con vuelo

Relaciono esta ficha con [ASTRA-18](https://astrateam2026.atlassian.net/browse/ASTRA-18) y [ASTRA-24](https://astrateam2026.atlassian.net/browse/ASTRA-24). Es una explicación y lista de pendientes de tierra; no es un ICD aprobado.

## Qué significa ICD

Es el documento donde dejamos escrito cómo se entienden el CanSat y la estación de tierra. Se parece a una ficha de un enchufe: ambos lados necesitan saber qué entra y qué sale. En nuestro caso el «enchufe» transporta datos y comandos.

Por ejemplo, si recibo `123.4`, necesito saber si representa altura en metros, presión u otra cosa. Si mando una orden de calibración, ambos lados necesitan reconocer la misma orden y distinguir recibido, rechazado y ejecutado. Un eco del texto no demuestra por sí solo una actuación física.

## Pendientes que llevo desde groundstation

| Tema | Qué necesito resolver con Edu | Estado |
| --- | --- | --- |
| Datos | Orden, nombres, unidades, signos y ejes de cada campo | TBD: por definir. |
| Identificación | TEAM_ID real, origen, destino y descarte de paquetes ajenos | TBD; 1000 es ficticio. |
| Validez | Cómo expresar GPS sin solución, datos viejos y sensores fallados | TBR: revisar convención de banco. |
| Integridad | Qué protege CRC, dónde se verifica y cómo reporto un rechazo | TBD. |
| Comandos | Formato, confirmación, rechazo, duplicados y ejecución | TBD; funciones v2 siguen exigidas. |
| Reinicios | Cómo reconocer una nueva sesión y conservar contador, tiempo y configuración | TBD; no demostrado por RESET del banco. |
| Radio | Frecuencia exacta, modo, ancho de banda o tasa, potencia, Sync Word y direccionamiento | TBD; sin valores elegidos en esta ficha. |
| Inicio de misión | Quién envía y recibe el comando referido por X3 v2 | TBR por ambigüedad del anexo. |

Primero llevamos estas preguntas al acuerdo de interfaz. Después documentamos la decisión y su prueba en una actualización nueva. No cambio protocol/ ni el firmware de vuelo desde esta carga.

Filtrar TEAM_ID en la aplicación ayuda a no mezclar datos; no hace que una antena físicamente reciba solo nuestra señal. La prohibición de broadcast sigue vigente aunque el anexo v2 retire la exigencia anterior de NetID/PANID. La solución de direccionamiento queda pendiente de acuerdo y verificación.
