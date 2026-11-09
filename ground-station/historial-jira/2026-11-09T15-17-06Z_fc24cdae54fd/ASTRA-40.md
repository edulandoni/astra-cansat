# ASTRA-40 — COMMS — Justificar tamaño de paquete y perfil LoRa con tiempos y confiabilidad

[Abrir en Jira](https://astrateam2026.atlassian.net/browse/ASTRA-40)

Estado observado: En curso. Asignación: Cristian Ponsone. Creación: Cristian Ponsone.

## Descripción original consultada

Analizo con Edu el compromiso entre tamaño de la trama de vuelo, tiempo en el aire, margen de enlace, confiabilidad y energía para justificar el Radio Profile en el PDR.

Contexto del 26/10/2026: el banco actual usa telemetría ASCII de 22 campos. Edu define el empaquetado y los comandos del extremo de vuelo; adapto groundstation. En la conversación se propuso una trama de unos 55 bytes y un máximo de 255 bytes. Los 55 bytes siguen siendo una estimación: falta confirmar si incluyen versión, equipo/destino, arranque/misión, contador, validez y CRC de aplicación. El límite del payload LoRa no es una obligación de llenarlo ni debe confundirse con la FIFO o con límites de LoRaWAN.

Trabajo iniciado:

1. Comparar payloads completos de 50/55/60/100/124/255 bytes, SF7/SF9/SF10 y BW 125/250/500 kHz, con CR 4/5 y 4/8. Registrar preámbulo, encabezado, CRC físico y optimización de baja tasa. Son hipótesis de cálculo, no configuración de radio aprobada.
2. Separar tiempo de propagación, tiempo de transmisión y latencia extremo a extremo. Separar portadora, BW, SF y cadencia de 1 Hz.
3. Presupuestar el segundo completo: telemetría, cambio TX/RX, comandos/ACK si se acuerdan, guardas y recuperación. El tiempo libre aritmético no prueba capacidad de operación ni habilitación regulatoria.
4. Comparar redundancia útil: FEC físico, CRC de detección, identificación de versiones/sesiones/contador/validez y repetición selectiva justificada; no rellenar hasta 255 bytes por disponibilidad.
5. Acordar con Edu campos, unidades, rangos, precisión, signo, orden de bytes y vectores de referencia. No implementar unilateralmente el formato compartido.
6. Diseñar ensayos reproducibles con misma alimentación/antenas/ubicación, variando una condición por vez: longitud, SF/BW/CR, distancia/atenuación, orientación y movimiento/interferencia cuando se pueda controlar. Medir recibidos/esperados, PER/PRR, RSSI/SNR, ráfagas de pérdida, latencia y antigüedad de datos, comandos y energía. Conservar condiciones y suficiencia estadística; una recepción nominal no demuestra confiabilidad de vuelo.
7. Revisar límites de fabricante, potencia/régimen, variante física y restricciones aplicables antes de transmitir. No asumir operación continua a +20 dBm ni trasladar reglas LoRaWAN de otra región.

Primer contraste calculado, BW125 kHz, CR4/5, preámbulo 8, encabezado explícito y CRC activo: 55 bytes ocupan 107,776 ms en SF7, 349,184 ms en SF9 y 657,408 ms en SF10. En las mismas condiciones, 100 bytes ocupan 174,336 / 553,984 / 1026,048 ms. SF10/100 bytes ya supera un segundo antes de comandos. Es tiempo de aire calculado, sin ensayo RF ni medición de CPU.

Entregables: matriz reproducible de hipótesis/resultados, campaña de ensayos y criterios a acordar, registro de decisión con opciones descartadas y por qué, y material PDR que distinga cálculo de ensayo. Los umbrales de aceptación y perfil final quedan TBD hasta acordarlos; no elijo SF sólo por ser el mayor o por minimizar bytes.

Relaciono este trabajo con ASTRA-18 (viabilidad/requisitos RF), ASTRA-25 (link budget) y ASTRA-24 (interoperabilidad/ICD). Llevo aquí el diario específico de este compromiso, conservando el historial temático de las otras tareas.

Fuentes iniciales:

* Hoja Semtech SX1276 revisión 7, sección 4.1.1.7: https://cdn.sparkfun.com/assets/7/7/3/2/2/SX1276_Datasheet.pdf
* FAQ Semtech sobre SF, FEC y compromiso sensibilidad/tiempo: https://www.semtech.com/design-support/faq/faq-lora
* FAQ Semtech sobre duración, fading e interferencia: https://www.semtech.com/design-support/faq/P100

La tarea se inicia con análisis offline; no configura ni transmite RF y permanece abierta hasta completar evidencia y acuerdo.

## Comentarios conservados

### 2026-10-26T02:39:21.472-0300 — comentario 10184

Autoría original: Cristian Ponsone. [Abrir original](https://astrateam2026.atlassian.net/browse/ASTRA-40?focusedCommentId=10184). Última edición informada: 2026-10-26T02:39:21.472-0300.

26/10/2026 — COMENTARIO 1 — Comparación inicial reproducible de payload y perfiles LoRa

Creé esta tarea específica y la pasé de Backlog a Por hacer y luego En curso porque ya inicié el análisis. Conservo la descripción original. Edu define el empaquetado y los comandos de vuelo; adapto tierra. Los 55 bytes son una estimación pendiente del layout completo, no una trama aprobada.

Generé 108 hipótesis con el calculador existente: payloads completos de 50/55/60/100/124/255 bytes, SF7/9/10, BW125/250/500 kHz y CR4/5 o 4/8; preámbulo 8, encabezado explícito y CRC físico activo. Revalidé la fórmula de Semtech revisión 7 y contrasté tres resultados con aritmética independiente; pasaron las dos pruebas existentes del calculador. No configuré ni transmití RF.

En BW125 kHz y CR4/5, 55 bytes ocupan 107,776 / 349,184 / 657,408 ms en SF7/9/10; 100 bytes ocupan 174,336 / 553,984 / 1026,048 ms. Reducir de 100 a 55 ahorra 38,18 / 36,97 / 35,93 % del tiempo de aire, usando como denominador el caso de 100 bytes. No es ahorro medido de batería ni CPU. SF10/100 bytes supera el segundo antes de comandos, ACK o guardas.

Separé propagación de transmisión/latencia y portadora de BW/cadencia. Mayor SF mejora sensibilidad pero cuesta duración; no equivale a mayor confiabilidad en toda interferencia o movimiento. FEC aporta redundancia con costo; CRC detecta, no corrige. Bytes de versión/equipo/sesión/contador/validez pueden estar justificados; rellenar hasta el máximo no es protección ante pérdida del paquete entero.

Agregué revisión de potencia/régimen: la hoja Semtech revisión 7 mantiene 1 % TX en operación a +20 dBm, bajo sus condiciones. No lo convierto en límite de toda potencia ni en regla regulatoria argentina. La variante de módulo y condiciones aplicables siguen pendientes.

Dejé campaña y criterios a acordar con Edu: trama máxima completa, tiempo para órdenes, PER/PRR y ráfagas, RSSI/SNR, latencia/antigüedad y energía, con condiciones y muestra suficientes. El perfil final y umbrales quedan TBD. La tabla de tiempos no acredita recepción de vuelo ni elige SF por sí sola.

[Informe y fuentes](https://github.com/edulandoni/astra-cansat/blob/b0494f17201b8d0ac22e5980c69b7523eefee96a/ground-station/docs/interfaces/2026-10-26-payload-sf-confiabilidad-04.md)
[Matriz de 108 hipótesis](https://github.com/edulandoni/astra-cansat/blob/b0494f17201b8d0ac22e5980c69b7523eefee96a/ground-station/evidence/2026-10-26-comparacion-lora/matriz-01.json)
[Programa reproducible](https://github.com/edulandoni/astra-cansat/blob/b0494f17201b8d0ac22e5980c69b7523eefee96a/ground-station/tools/comparar_perfiles_lora.py)
[Plan ampliado: cámaras y enlace](https://github.com/edulandoni/astra-cansat/blob/b0494f17201b8d0ac22e5980c69b7523eefee96a/ground-station/docs/historial/2026-10-26-objetivo-ampliado-camaras-radio.md)
[Informe y plan en Drive verificados](https://drive.google.com/file/d/1LX-Sa0CDjiPWH59eSR5sBJYCgUUsUIcT/view)

## Historial de cambios de campos

### 2026-10-26T02:34:13.827-0300 — cambio 10157

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Backlog

Después: Por hacer

### 2026-10-26T02:34:51.219-0300 — cambio 10158

Autoría original: Cristian Ponsone.

Campo: status.

Antes: Por hacer

Después: En curso

