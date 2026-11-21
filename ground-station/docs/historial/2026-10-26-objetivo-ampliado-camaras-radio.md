# 26/10/2026 — Objetivo ampliado de mi área: cámaras y evaluación del enlace

Continúo el trabajo de cámaras de [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39) y agrego la evaluación específica de [ASTRA-40](https://astrateam2026.atlassian.net/browse/ASTRA-40). Conservo el objetivo y todas las evidencias previas; no doy la etapa completa por las fotos correctas.

## Resultado que busco

Poner en marcha y verificar ambas ESP32-CAM, con fotos nuevas, guardado y lectura microSD sin perder originales, chequeo dual y desarrollo de grabación, recuperación y control/medición de energía. Evaluar sonido como extra: primero identificar si tenemos micrófono, interfaz y recursos compatibles; no asumir que el sensor de imagen lo proporciona.

En paralelo, evaluar con Edu el compromiso entre bytes reales de la trama, SF/BW/CR, tiempo en el aire, confiabilidad, energía y capacidad de telemetría a 1 Hz con comandos. Conservar fuentes, cálculos, ensayos y criterios para justificar el perfil en el PDR. Edu define empaquetado y comandos del extremo de vuelo; adapto groundstation y mantengo los acuerdos en ASTRA-24. No selecciono RF o contrato compartido unilateralmente.

## Próximos bloques

1. Cámaras: preparar grabación local reproducible en color mínimo 640×480, con marcas de tiempo, medición de cuadros/intervalos y archivos recuperables. Unir JPEG sin temporización no acredita video. Mantener el chequeo sin interrumpir una grabación activa y medir arranque antes de definir el disparador de misión. Continuar después con consumo/picos, circuito de apagado y continuidad ante reset. Audio es opcional y no debe comprometer video, energía o requisitos.
2. Comunicaciones: continuar [matriz y campaña de ASTRA-40](../interfaces/2026-10-26-payload-sf-confiabilidad-04.md). Los 55 bytes son una estimación pendiente de layout completo. Acordar umbrales y perfil con Edu, medir en hardware cuando esté disponible y conservar los desacuerdos/TBD sin convertirlos en requisitos.
3. Cierre por evidencia: documentos, fuentes y registros reproducibles; distinguir cálculo, simulación, ensayo físico y pendientes. Fotos/SD ya comprobadas conservan su alcance y no certifican video, audio, consumo, RF o arranque estable.

Trabajo sólo en mi rama groundstation y ground-station/, con publicaciones en Drive propio y Jira temático, en primera persona y con diario sin sobrescritura. Mantengo los bancos de telemetría y fotos, los archivos originales y las tareas ajenas intactos.
