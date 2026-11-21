# 28/10/2026 — KoNaR Can: cámaras y alcance de la evidencia

Diario: [ASTRA-35](https://astrateam2026.atlassian.net/browse/ASTRA-35). Profundizo el registro de KoNaR Can del [catálogo](2026-10-19-catalogo-cansat.csv); su clasificación histórica no acredita cada función.

## Fuente y alcance de lectura

Consulté el [CDR 2024 v1.0 del equipo 2050](https://www.cansatcompetition.com/docs/teams/cansat2024_2050_cdr_v01.pdf), alojado por la competencia. Leí focalmente el texto de las páginas 38–39 y 120–121, con contexto de las filas posteriores. El documento tiene 169 páginas: no declaro revisión integral. Los intentos de captura visual de las páginas 38, 39 y 121 fallaron por caché/tiempo de espera; las tablas se analizaron desde texto extraído, con esa limitación.

## Lo que documenta el equipo

Las páginas 38–39 proponen ESP32-CAM/OV2640, JPEG agrupados en AVI sobre SD y control desde el computador principal por I2C. La página 121 marca como probadas la grabación y configuración por interfaz serial, sin métricas numéricas en esas filas. No equiparo esos rótulos con una campaña reproducible ni doy por resuelta la correspondencia entre interfaces. La fila de supervivencia de software a cortes de energía de la página 120 figura sin probar. Son afirmaciones de diseño/estado del CDR, no un PFR auditado ni medidas de nuestras cámaras.

## Qué aporta a nuestro trabajo

Mi conclusión es que deben distinguirse el formato del archivo, la calidad visual y la garantía de conservar una misión. Para nuestro banco, reunir cuadros en un archivo no basta: necesitamos medir cadencia, duración, pérdidas y capacidad de volver a abrirlo, manteniendo los tiempos originales. No uso tasas tabuladas por otro equipo como promesa para nuestras unidades.

Propongo conservar la siguiente relación entre riesgo y prueba propia. Las propuestas no son ensayos ejecutados en esta revisión.

| Riesgo que analizo | Prueba propuesta | Situación de ASTRA al corte |
| --- | --- | --- |
| Confundir orden aceptada con escritura efectiva | Contrastar contador de cuadros, último guardado y archivos recuperados | Hay evidencia de banco en el [informe del 27/10](../camaras/2026-10-27-grabacion-segmentada-y-supervision-usb.md); no repito pruebas ni la amplío a vuelo |
| Perder el cierre del archivo ante interrupción de energía | Interrumpir una campaña controlada y verificar qué segmentos abren y cuáles quedan parciales | Pendiente de campaña física; no se acredita con desconectar el seguimiento USB |
| Afirmar fluidez por un valor nominal | Medir distribución de intervalos y hueco máximo, junto con duración y resolución | Mantener las mediciones reales del banco y sus límites; sin medición nueva hoy |
| Que vuelo y tierra entiendan distinto el inicio/parada | Acordar interfaz y comprobar rechazo, resultado y arranque | Edu define vuelo; el perfil USB permanece experimental |

No adopto el protocolo de KoNaR ni modifico RF, energía o software por este antecedente. La lectura respalda el modo de presentar evidencia para el PDR; no certifica nuestra autonomía, reset o grabación de ambas unidades.

## Láminas y faltantes

El [suplemento visual](2026-10-28-catalogo-visual-konar.csv) conserva enlaces por página, tipo documental, crédito y acceso real. No describo fotos de componentes ni renders porque sus píxeles no cargaron. No descargué ni republiqué imágenes o el PDF. Fecha original y permiso individual de reutilización no verificados.

Quedan pendientes el firmware exacto utilizado, archivos originales de esa campaña y resultados posteriores al vuelo que permitan contrastar las filas declaradas. No atribuyo éxito, fallas o energía generada al sistema a partir de esta lectura.

