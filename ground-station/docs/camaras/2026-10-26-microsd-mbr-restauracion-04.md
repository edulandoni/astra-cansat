# 26/10/2026 — ACTUALIZACIÓN: microSD preparada y archivos repuestos

Diario: [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39). Actualizo el [diagnóstico de montaje](2026-10-26-camara-2-sd-03.md), conservando ese corte anterior.

Autoricé expresamente formatear la tarjeta para las pruebas de cámara, aceptando perder su estructura de arranque anterior. Identifiqué la unidad USB de 15552479232 bytes por número de serie y comprobé que no fuera disco de arranque ni de sistema. El disco interno no participó de la operación.

El intento sin privilegios fue bloqueado. Con permisos de administrador se eliminaron las particiones; Windows conservó la tabla GPT y rechazó inicializarla como si fuera un disco RAW. Conservé ese resultado fallido y comprobé que no hubiera particiones antes de continuar: convertí la tabla vacía a MBR y creé un volumen FAT32 con etiqueta `ASTRA_CAM`. Verifiqué MBR, FAT32 y capacidad desde Windows.

Repuse los cinco archivos de la antigua primera partición en sus rutas originales y los diecinueve de la segunda dentro de `Original_particion_E`. La primera pasada de reposición se interrumpió por el límite de longitud de rutas de Windows; conservé los archivos ya copiados y continué usando rutas extendidas, sin sobrescribirlos. Verifiqué los 24 archivos por SHA-256 contra sus manifiestos: todos coinciden. Mantengo además las copias privadas anteriores al formato.

Esto acredita preparación de la tarjeta y conservación de archivos, no restauración de su antiguo arranque ni grabación por la ESP32-CAM. El siguiente ensayo requiere pasar la tarjeta a la cámara 2, solicitar una foto nueva con guardado y comprobar la lectura. Hasta obtener ese resultado, el almacenamiento de cámara sigue pendiente.
