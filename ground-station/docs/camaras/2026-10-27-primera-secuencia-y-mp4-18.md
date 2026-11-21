# 27/10/2026 — ACTUALIZACIÓN 18: primera secuencia física y MP4

[ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39) · [ASTRA-41](https://astrateam2026.atlassian.net/browse/ASTRA-41). Actualizo la [preparación y foto Qt](2026-10-27-foto-qt-fisica-y-secuencia-17.md), sin modificar sus resultados ni los cortes anteriores.

## Qué conseguí

Confirmé que una foto nueva aparece desde la ventana visible del Laboratorio, con una demora perceptible; la medición de 3,172 s pertenece al ensayo anterior y no la reutilizo como otra medición. Después cargué el candidato de grabación en cámara 1, solicité doce cuadros desde el botón Qt, los leí desde la microSD con un lector independiente y generé un MP4 reproducible. Es el primer recorrido físico completo de esta secuencia corta, no video continuo de misión ni emisión RF.

La cámara guarda JPEG y sus marcas temporales en SD. El MP4 se deriva en la PC después de verificar esos archivos. Conservo los JPEG, manifiesto, archivos laterales, recepción y controles; el video exportado no reemplaza la evidencia original. Fotografías y video permanecen privados.

## Carga y captura

Con la app cerrada y la unidad preparada, comprobé la identidad de cámara 1 por el cargador. Verifiqué el binario contra su huella revisada y la igualdad de tablas de partición. Escribí sólo la aplicación en 0x10000; esptool terminó correctamente y verificó el hash de lo escrito. No reescribí bootloader o particiones ni formateé la tarjeta. Los respaldos originales siguen conservados.

El botón de prueba solicitó CLIP a través del adaptador del Laboratorio y del puerto real; los widgets de esta solicitud se ejecutaron fuera de pantalla. La operación completa tardó 7,828 s y recibió reporte de doce cuadros con cierre COMPLETE. Ese reporte por sí solo no se tomó como lectura independiente: desconecté la unidad antes de pasar la tarjeta al lector para la siguiente comprobación.

## Lectura independiente y tiempos

El lector expuso el volumen FAT32 ASTRA_CAM sobre soporte USB/MBR. Verifiqué identidad, cierre, orden, doce JPEG VGA RGB decodificables, longitud, CRC y SHA-256, sin errores. Los doce archivos tienen huellas distintas; eso no prueba por sí solo movimiento de escena. Copié los 26 archivos de la carpeta a una ubicación nueva en PC y comprobé igualdad de huellas, conservando el origen.

| Medida | Resultado |
| --- | --- |
| Cuadros comprobados | 12 de 12 |
| Intervalo entre primero y último | 6,077584 s |
| Cadencia media por N−1 intervalos | 1,80993 cuadros/s |
| Primer intervalo | 0,119970 s |
| Intervalos restantes | Entre 0,559778 y 0,599765 s |
| Foto Qt de este día | Coincide desde el lector con su recepción USB |
| Nueve fotos de la campaña anterior | Conservan sus huellas en la tarjeta |

La cadencia no es uniforme. El intervalo inicial corto queda registrado; no lo oculto con una tasa nominal de 2 fps. Las marcas proceden del controlador desde el arranque, no son UTC ni exposición exacta. No aislé la causa de ese primer intervalo y no afirmo continuidad perfecta por esta prueba breve.

## MP4 y reproducción

Agregué `sequence_video.py` y Exportar MP4 al visor Qt. Con PyAV 19.0.1/libx264 genero un archivo H.264 derivado con recompresión, sin audio ni interpolación. Asigno las marcas relativas de cada cuadro y después decodifico el resultado completo: los doce cuadros conservan sus tiempos, con diferencia máxima observada de 0 µs. La verificación rechaza exportaciones con cuadros o tiempos incompatibles.

El MP4 dura 6,117584 s. Los 40 ms añadidos al último cuadro son duración de presentación del contenedor, no un tramo de adquisición medido. La tasa 25 usada por el codificador no significa captura a 25 fps: las doce marcas reales permanecen separadas como se registraron. El campo de tiempos y sus unidades se apoya en la [documentación de PyAV](https://pyav.org/docs/stable/api/time.html); los valores anteriores proceden de nuestra comprobación local con la versión instalada.

La exportación crea otra carpeta y conserva estado, tiempos, huellas y explicación. El visor permite Reproducir, Pausa, Inicio, Exportar MP4 y abrir el resultado. Si cierro durante una exportación, espera su verificación. Abrí el Laboratorio solicitado con la copia de cámara 1 y reproducción local; la observación de la ventana de video sigue pendiente de confirmación. La reproducción no abre el puerto ni necesita la tarjeta conectada.

## Conservación histórica: alcance comprobado

Además de las nueve fotos anteriores, comparé las referencias de los 24 archivos que se habían respaldado antes de preparar la SD. En la tarjeta actual encontré cinco coincidentes y diecinueve ausentes, correspondientes a la antigua partición E; las 24 copias locales sí conservan sus huellas. No dispongo de un inventario independiente de esta tarjeta inmediatamente anterior a la captura: no puedo fechar ni atribuir esa ausencia a una operación concreta. No los repuse, borré ni oculté en el informe. Esta diferencia no impide verificar los doce cuadros nuevos y evita afirmar falsamente que los 24 continúan en la tarjeta.

## Pruebas y siguientes pasos

Pasaron **40 pruebas del banco de cámaras y 16 del Laboratorio**. Las nuevas cubren exportación con tiempos irregulares, cantidad, conservación de originales, salidas nuevas y rechazo de fuente incompleta, más cierre de la ventana mientras exporta. Los tests usan imágenes de PC; la campaña de cámara 1 es la evidencia física separada.

[Control de software](../../evidence/2026-10-27-camara-qt/control-02-software.json) · [Control físico, tiempos y exportación](../../evidence/2026-10-27-camara-qt/control-03-secuencia-fisica.json).

Quedan pendientes escena con movimiento controlado, repetir en ambas unidades, duración mayor, mejorar y medir cadencia, recuperación de archivos incompletos/reset, audio, energía y eventos de misión de Edu. La prueba de doce cuadros es finita y no admite STOP durante CLIP; no la habilito como grabación de misión. El perfil sigue siendo de banco USB y no configura RF. No cierro el objetivo completo por esta primera secuencia.
