# 27/10/2026 — Revisión de estructura y demostración de vuelo recibidas

[ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39) · [ASTRA-24](https://astrateam2026.atlassian.net/browse/ASTRA-24). Reviso efectos sobre cámaras e interfaz desde mi área; no apruebo ni modifico diseño mecánico o software ajenos.

## Material y alcance de la revisión

Recibí un ZIP con cuatro fotos de la estructura y un video de Edu de 119,233 s. Conservé los originales y sus huellas en un conjunto privado, sin mover los archivos de entrada. Las fotos se inspeccionaron completas. Del video generé 24 fotogramas de referencia cada cinco segundos entre 0 y 115 s y revisé tres adicionales en tamaño original para leer la terminal. Decodifiqué el audio completo (119,227 s) y obtuve una transcripción asistida local con segmentos temporales. No es escucha humana ni transcripción infalible; no doy por inspeccionado visualmente cada instante intermedio ni certifico todos los textos de pantalla. Los recursos recibidos son evidencia de una demostración, no logs crudos ni un ensayo repetido por mí.

El video incluye coordenadas de ubicación: no publico las imágenes, el audio, su transcripción completa ni esas coordenadas en GitHub. El análisis y control públicos no necesitan esa información. Tampoco republico las fotos del equipo; conservo la procedencia y conclusiones propias.

## Qué muestra la demostración y cómo nos sirve

| Tramo aproximado | Observación o explicación recibida | Efecto en mi trabajo |
| --- | --- | --- |
| 0–29 s | Banco con placas, conexiones y módulo con antena; Edu explica GPS → placa y placa → PC por UART/USB | Necesito ejemplo de bytes y velocidades de cada interfaz; la apariencia de una placa no certifica su modelo |
| 29–46 s | Configuración del terminal y aparición de líneas de diagnóstico | No copiar el texto de diagnóstico como si ya fuera el paquete de vuelo |
| 46–65 s | Terminal con tiempo, temperaturas, presión y referencia P0; Edu distingue tiempo del microcontrolador | Acordar referencia de reloj y unidades; conservar diferencia entre altura relativa y altitud GPS |
| 65–79 s | Edu describe puesta a cero con Z; cambian los valores de altura mostrados en el entorno de ese tramo | Es un candidato real para interoperabilidad, no autorización para enviar literalmente Z desde tierra. Pedir comando, confirmación, estados y efecto tras reset |
| 79–98 s | Diagnóstico de IMU con valores que cambian al mover el banco; se comenta conversión posterior | Solicitar sensor/configuración, escalas, ejes y signos. Giroscopio se expresará en rad/s y aceleración en m/s² cuando sepamos la conversión; no confundir radianes con velocidad angular |
| 98–119 s | Terminal muestra GPS FIX, satélites, coordenadas y tiempo/altitud; Edu explica el uso de esos datos | Mostrar validez y antigüedad además de posición; pedir tipo de solución, hora y tratamiento de pérdida de GPS |

No medí precisión, frecuencia de muestreo, latencia ni confiabilidad del banco a partir del video. Una posición verosímil no prueba precisión en vuelo. Las etiquetas visibles y el relato no sustituyen calibración ni factores de conversión. Para integrar necesito captura serial original, versión de firmware, campos/unidades, indicadores de validez, reinicios, ejemplos de comandos y respuestas definidos por Edu. No le asigné tareas ni cambié sus tickets.

## Estructura: observaciones para cámaras y comunicaciones

Las cuatro fotos muestran una pieza cilíndrica con paredes longitudinales, ventanas con cruces, extremos con perforaciones y una placa perforada presentada en un compartimiento. Se ven líneas de fabricación y algunas irregularidades locales; no puedo inferir material, resistencia, masa, escala exacta, comportamiento térmico ni función definitiva de cada pared. No uso elementos del fondo como regla de medida.

| Comprobación propuesta | Por qué importa | Cómo la demostraría |
| --- | --- | --- |
| Campo visual de cada lente y orientación cenit/nadir | Paredes, cruces, placas, cables o mecanismo de recuperación podrían ocultar escena | Fotos y video desde ambas cámaras montadas con la envolvente completa; medir área obstruida y revisar despliegue |
| Sujeción de placa, lente/flexible y SD | Movimiento puede cambiar encuadre o interrumpir contactos | Retención y alivio de cables revisados por el equipo; inspección y pruebas ambientales definidas, sin aceptar por apariencia |
| Acceso de mantenimiento | Necesitamos comprobar SD, arrancar y diagnosticar sin desmontar todo | Secuencia de acceso/armado y chequeo final; repetir captura después del cierre |
| Alimentación y recorrido de cables | Dos arranques y posibles movimientos exigen conexiones verificables | Medir tensiones/picos en montaje final; documentar conectores y separación respecto de elementos móviles |
| Antenas y electrónica próximas | La geometría real puede cambiar el enlace; no deducir transparencia RF de una foto | Identificar material y ubicación; medir enlace/perfil acordado con la envolvente completa |
| Espacio, calor y sensores | Compartimientos y obstáculos pueden alterar ventilación o mediciones | CAD/cotas y ensayos de temperatura; coordinar ubicación con responsables sin decidir por ellos |

La siguiente revisión necesita CAD o medidas, material y función de las paredes, posición de las dos cámaras, batería, antenas y recorrido de recuperación. Mi propuesta no es perforar ni modificar la pieza sin ese acuerdo. Una prueba útil inmediata será montar temporalmente las cámaras de forma segura y mirar ambas imágenes antes de fijar el diseño.

## Relación con grabación autónoma

El banco de Edu abre el camino para disparadores y estado desde el OBC. La estructura obliga a comprobar que la imagen registrada sirve una vez todo está armado. Ninguno de los dos materiales demuestra todavía alimentación autónoma de cámaras, inicio de grabación, continuidad ante reset, video de descenso ni transmisión de imágenes. La [propuesta de grabación y supervisión](2026-10-27-video-vivo-y-grabacion-autonoma-19.md) conserva esos pendientes y la campaña necesaria para respaldar cada afirmación en el PDR.
