# 19/10/2026 — Requisitos v1/v2 aplicados a groundstation

Derivo esta entrada de la revisión del 17/10 y la limito a recepción, datos, visualización y comunicaciones de mi área. No apruebo diseño mecánico, electrónica de vuelo ni presupuesto.

Fuentes: [anexo v1](https://www.argentina.gob.ar/sites/default/files/2026/08/anexo_requerimientos_tecnicos_-_cansat_universitario_2026-2027.pdf), [anexo v2](https://www.argentina.gob.ar/sites/default/files/2026/08/anexo_requerimientos_tecnicos_-_cansat_universitario_2026-2027_v2.pdf), [revisión original del 17/10](https://docs.google.com/document/d/1WwZ83me8W0qA7T8eum6xSrYxVtpbYoT9OYq1Z0WPMNI/edit). Las huellas de las fuentes consultadas están en fuentes-2026-10-19.json. No afirmo haber comprobado documentos nuevos posteriores a esa revisión.

| Cambio o conservación | Consecuencia para mi trabajo |
| --- | --- |
| X2 v1, NetID/PANID con número de equipo, desaparece | Dejo de presentarlo como exigencia de v2. La identificación y el destino siguen pendientes del acuerdo. |
| X3 v1 pasa a X2 v2 | Sigue prohibido broadcast; retirar NetID no autoriza broadcast. |
| X4 v1 pasa a X3 v2 y cambia de redacción | Dejo el inicio automático de misión TBR: necesito aclarar quién origina y recibe ese comando. |
| X5 v1 pasa a X4 v2 | Conservo la transmisión de telemetría una vez por segundo. |
| X6 v1 pasa a X5 v2 | Conservo aceleración y giro de los tres ejes, con unidades y ejes claros. |
| X7 v1 pasa a X6 v2 | Sigue pendiente pedir batería y señal solar por telecomando. |
| G1–G15 no cambian de contenido | Mantengo calibración, CSV y respaldo, tiempo, pantalla, gráficos, contadores, comandos, portabilidad y autonomía. |
| F1–F5 no cambian de contenido | Necesito coordinar y probar persistencia, tiempo UTC y configuración con vuelo; la simulación lógica no basta. |
| La sección detallada 3.1 de v1 no aparece en v2 | ASCII22, CR, TEAM_ID de cuatro dígitos, nombres de estados, comandos CX/ST/CAL/MEC y Flight_<TEAM_ID>.csv quedan como convenciones heredadas de banco, pendientes del ICD o especificación vigente. |

## Qué falta en mi banco

Me falta completar telecomandos, calibración e información solar; revisar SI en pantalla (incluido giro); probar recepción y reconexión USB físicas; verificar CSV en dos soportes independientes; demostrar dos horas de operación y legibilidad al sol; y acordar la semántica de datos inválidos y reinicios. El perfil ficticio de descenso todavía no demuestra el régimen de C3.

La matriz JSON adjunta conserva únicamente G1–G15, X1–X7 históricos, F1–F5 como dependencias y C3 por su efecto en el simulador. Es una selección del análisis previo, no una nueva norma ni una declaración de cumplimiento.

Jira: [ASTRA-18](https://astrateam2026.atlassian.net/browse/ASTRA-18), [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20), [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21), [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22).
