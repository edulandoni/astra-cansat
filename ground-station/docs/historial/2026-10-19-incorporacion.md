# 19/10/2026 — Incorporación de mi trabajo a GitHub

## Motivo y objetivo

Necesito reconstruir desde Jira y GitHub por qué hice cada simulador, qué pude comprobar y qué falta, para preparar el PDR sin depender de recuerdos del chat. Concentro esta incorporación en groundstation y datos.

## Qué incorporo

Conservo el banco Python/sketch ESP32 del 17/10 sin modificar sus fuentes. Recupero desde Drive el código histórico de estación v04 y laboratorio v05 y lo identifico como DEPRECATED. Agrego método de diario, guía de entrada, comparación v1/v2 de mi área, evidencia de software, mapa de tareas y una explicación de las interfaces pendientes.

Creo la rama groundstation a partir de main observado en a9f65ee71cc8317ca66835b41b8ff374eaddb0bf. Las modificaciones de esta carga quedan dentro de ground-station/. El PR 1 anterior se conserva como antecedente enlazado. No cambio sus archivos ni el protocolo compartido.

La copia original del README del subsistema queda en archive/README-original-repositorio-2026-10-19.md; el índice actual permite encontrar los nuevos registros. Las entradas fechadas permanecen intactas.

## Verificación y límites

El [registro de pruebas](../pruebas-2026-10-19.md) contiene nueve pruebas del banco, trece del archivo v04 y cuatro del guardado del historial. Registro también el fallo inicial de una comprobación de la prueba del historial y su corrección. No realizo nuevas pruebas de hardware ni doy por aprobado el Radio Profile o el ICD.

## Próximo trabajo

Identificar la placa; compilar y cargar el simulador USB; ensayar recepción y reconexión físicas; completar comandos y solar; revisar unidades y perfil de descenso; verificar doble soporte y autonomía; y acordar interfaces con Edu. Son trabajos pendientes, no resultados de esta carga.

Jira: [ASTRA-18](https://astrateam2026.atlassian.net/browse/ASTRA-18), [ASTRA-20](https://astrateam2026.atlassian.net/browse/ASTRA-20), [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21), [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22), [ASTRA-23](https://astrateam2026.atlassian.net/browse/ASTRA-23), [ASTRA-24](https://astrateam2026.atlassian.net/browse/ASTRA-24), [ASTRA-25](https://astrateam2026.atlassian.net/browse/ASTRA-25).
