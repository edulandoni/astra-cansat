# 23/10/2026 — Dos antenas y presupuesto de enlace preliminar

Diarios: [ASTRA-25](https://astrateam2026.atlassian.net/browse/ASTRA-25) y dependencias de [ASTRA-18](https://astrateam2026.atlassian.net/browse/ASTRA-18). Preparo una comparación para revisar con Edu. No selecciono antena final, frecuencia, modulación ni potencia; no ejecuté RF. Una ganancia de catálogo no acredita alcance real.

## Comparación de dos candidatas

| Criterio | Taoglas OMB.915.B05F21 | Digi A09-Y11NF |
|---|---|---|
| Fuente primaria | [Datasheet SPE-22-8-119-A](https://www.taoglas.com/datasheets/OMB.915.B05F21.pdf), revA | [Página del fabricante](https://www.digi.com/products/models/antennas/a09-y11nf) |
| Declaración fabricante | 902–928MHz; 5,9dBi de pico; omni lineal; 50Ω | Yagi900MHz; 11,1dBi; N hembra |
| Montaje | Poste/pared; largo1094±30mm; antena500g + soporte70g | Montaje definitivo, peso y resistencia: TBR con ficha del modelo suministrado |
| Patrón disponible | PDFp8 lista2D/3D915MHz XY/XZ/YZ; lectura visual del gráfico pendiente | Observé patrón direccional H/V reproducido en PDR ITBAp118; procedencia exacta de gráfico fabricante TBR |
| Uso que evaluaría | Cobertura azimutal sin apuntar continuamente; comprobar elevación y paso alto | Más ganancia sobre eje; requiere apuntado y tolerancia a movimiento |
| Riesgo | Confundir omni en azimut con cobertura uniforme en toda elevación | Perder el lóbulo principal al seguir el CanSat; conectores/cable no coincidentes |
| Acción antes de elegir | Patrón visual completo y prueba sobre montaje real | Confirmar banda exacta, patrón oficial, conector de la unidad y pérdida del conjunto |

La ficha Taoglas se pudo leer por el buscador, pero su descarga directa devolvió403. No afirmo haber inspeccionado sus curvas por ver el título de la página. Los intentos de L-com HG905RD/HG909Y devolvieron HTML de mantenimiento en vez de PDF: quedan excluidos como especificaciones verificadas. Conservo el registro privado de descarga y los intentos, sin sortear bloqueos.

En el PDR ITBA aparece RP-SMA para A09-Y11NF, mientras Digi identifica N-female. Mantengo la discrepancia; no compro adaptadores sobre esa tabla. Los patrones vistos en un documento de equipo no equivalen a una ficha del lote que vayamos a usar. No transfiero sus cifras de alcance a ASTRA. La resta de ganancias de pico es5,2dB, pero sólo sería ventaja en direcciones y polarización equivalentes, con pérdidas iguales: no es margen asegurado.

## Presupuesto calculable sin inventar entradas

Uso la pérdida de espacio libre de [ITU-R P.525-5](https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.525-5-202411-I%21%21PDF-E.pdf):

`FSPL = 20 log10(4π d f / c)` con d en m, f en Hz, c=299792458m/s.

Los siguientes puntos son un barrido ilustrativo de distancia oblicua, no altura nominal ni frecuencia seleccionada:

| Frecuencia ilustrativa | 500m oblicuos | 1000m oblicuos |
|---|---:|---:|
| 915MHz | 85,656dB | 91,676dB |
| 928MHz | 85,778dB | 91,799dB |

`Prx = Ptx + Gtx(orientación) + Grx(orientación) − Ltx − Lrx − FSPL − Lpol − Lotras`

`Margen = Prx − Sensibilidad(modo/BW/bitrate/criterio BER o PER)`

| Entrada | Estado y evidencia que necesito |
|---|---|
| Frecuencia exacta, modulación, BW/bitrate, potencia | TBD Radio Profile acordado con Edu y requisitos CONAE |
| Sensibilidad | TBD del módulo exacto y perfil acordado; no tomo el mejor número genérico del chip |
| Antena de vuelo, orientación y montaje | TBD; no uso ganancia de pico como mínimo durante giro |
| Cable/conectores de ambos extremos | TBD medir o documentar pérdida a frecuencia real |
| Polarización y ocultamiento | TBD geometría de misión y ensayo en orientaciones |
| Distancia oblicua máxima y sitio | TBD trayectoria/vector y ubicación de GS; no confundir altura con distancia |
| Margen objetivo | TBD conforme a disponibilidad y pruebas; no fijo uno arbitrario |

Por ejemplo, a915MHz/1000m queda `Margen = Ptx + Gtx + Grx − pérdidas − 91,676 − sensibilidad`. Es una expresión pendiente, no un enlace cerrado. Espacio libre no incluye suelo, obstáculos, reflexiones, desadaptación ni interferencia. Las autorizaciones regulatorias de otros países o módulos no son autorización local ni parámetros elegidos para nuestro SX1276.

## Ensayo que propongo cuando tengamos el enlace

Conservo mismo payload y números de secuencia para comparar TX/RX/guardados. Registro perfil y versiones, distancia y alturas, cable/adaptadores, orientación y polarización, RSSI/SNR si el modo los entrega, tasa de paquetes únicos, rechazos, huecos, comandos confirmados y tiempos. Comparo ambas antenas sobre el mismo montaje y recorrido; pruebo barridos de orientación, paso alto, movimiento y pérdida/reconexión. Separaré prueba quieta de seguimiento y no daré por cumplida cobertura con un único punto.

La comparación y fórmula ya permiten preparar el PDR, pero faltan curvas verificadas, hardware RF, perfil compartido y ensayos. La tarea sigue abierta. El banco USB no mide sensibilidad ni certifica cumplimiento X1–X6.
