# 17/11/2026 — VNT: parser, contrato y evidencia disponible

Diario: [ASTRA-35](https://astrateam2026.atlassian.net/browse/ASTRA-35). Profundizo la referencia localizada el 14/11 y leída documentalmente en el [corte del 16/11](../aula/2026-11-16/Informe_aula_2026-11-16_0855_ART.md). El nuevo acceso es al código, no al aula CONAE.

## Qué aporta

Una descripción de arquitectura y la existencia de archivos CSV no alcanzan para demostrar recepción. Para preparar nuestro PDR conviene mostrar juntos el formato acordado, el parser utilizado y registros con muestras verificadas. Esta lectura no modifica el software ASTRA ni adopta un protocolo ajeno.

## Fuentes y versión

Cuenta publicadora: official-vnt; identidad institucional, edición competitiva efectiva y licencia individual no confirmadas. Consulté metadatos de directorios y leí completos tres archivos, verificando sus textos contra el commit 5cfa0f87c2ef4f6a0f437f3b176b7e47179e3811 (fecha de commit informada: 09/06/2026). Es una revisión estática acotada, sin compilación ni ejecución.

| Archivo primario | Identificador de blob Git | Lectura |
| --- | --- | --- |
| [Modelo interno](https://github.com/official-vnt/Cansat2026-gcs-system/blob/5cfa0f87c2ef4f6a0f437f3b176b7e47179e3811/src/common/TelemetryDef.h) | 0b5b9b3659146dc760ad1f1b5bd30a5b2b75b4d4 | Estructura con objetos Qt y magnitudes; no prueba un layout binario de transporte |
| [Parser](https://github.com/official-vnt/Cansat2026-gcs-system/blob/5cfa0f87c2ef4f6a0f437f3b176b7e47179e3811/src/core/DataParser.cpp) | 3511b8677170a8be3a28c26a365fa84a62d8e199 | Texto por líneas y comas, con 18 campos mínimos |
| [CSV inspeccionado](https://github.com/official-vnt/Cansat2026-gcs-system/blob/5cfa0f87c2ef4f6a0f437f3b176b7e47179e3811/datalogging/telemetry_20260601_230630.csv) | 68dce1d86ef4d8a8153d00096acdc2c041b279b3 | Sólo encabezado, sin muestras |

Los 17 archivos listados en datalogging tienen el mismo tamaño de 145 bytes y blob; leí uno cuyo contenido es el encabezado. La identidad de blob es evidencia de contenido coincidente en Git. No atribuyo eso a toda otra carpeta ni afirmo que el equipo carezca de registros privados.

## Observación e interpretación

El README leído el 16/11 describe tramas binarias y CRC. El parser de esta versión convierte bytes a texto, separa líneas y comas, y convierte campos numéricos. No encontré cálculo de CRC dentro de ese archivo; no extrapolo su ausencia a toda la cadena. Los campos adicionales no se rechazan por la condición de longitud mínima.

La misma variable de resultado se reutiliza en conversiones sucesivas y se comprueba sólo al final. La inspección sugiere que un error anterior podría quedar oculto por una conversión posterior correcta; falta un ensayo ejecutado para caracterizar su efecto. También queda como punto de revisión la acumulación de entrada sin salto de línea. No probé estos casos ni declaro una falla observada en vuelo.

## Aplicación propuesta y límites

Para nuestra evidencia propongo mostrar versión del contrato y del ejecutable, rechazo de cada campo inválido, datos brutos y CSV con conteo coincidente, y distinguir los ensayos físicos de los sintéticos. Nuestro [ensayo USB prolongado](../2026-10-24-aceptacion-banco-usb-actualizacion-09.md) es evidencia de aquella revisión, no una prueba nueva ni una comparación de rendimiento con VNT.

No selecciono antenas, RF, comandos o empaquetado por esta lectura. No hay datos posvuelo verificables en el CSV inspeccionado ni medición de confiabilidad. No inspeccioné píxeles de fotos o láminas nuevas: el acceso al código no acredita un catálogo visual. Conservo enlaces al original; no descargué a Descargas ni republico código, imágenes o grabaciones de terceros. La profundización termina aquí para mantener una pasada acotada.
