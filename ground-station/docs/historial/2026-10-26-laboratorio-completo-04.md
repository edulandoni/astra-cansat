# 26/10/2026 — ACTUALIZACIÓN 04: banco completo dentro del Laboratorio

[ASTRA-41](https://astrateam2026.atlassian.net/browse/ASTRA-41) · [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22) · [ASTRA-39](https://astrateam2026.atlassian.net/browse/ASTRA-39). Continúo la [entrega Qt](2026-10-26-laboratorio-qt-03.md), sin reemplazar su evidencia.

## Motivo y resultado

La integración anterior dejaba una sola curva visible y varias funciones del banco fuera de la navegación principal. Amplié el Laboratorio para operar y revisar el trabajo desde la misma aplicación nativa: telemetría, comandos, almacenamiento, diagnóstico, fotografías, recuperación, cálculos y evidencia completa. No modifiqué el firmware ni el contrato de vuelo de Edu.

## Cobertura de la interfaz

| Área | Función disponible | Procedencia y límite |
| --- | --- | --- |
| Telemetría / Variables | Los 22 campos con valor, unidad, condición y explicación al posar el cursor | Perfil de banco; conversión explícita de giro a rad/s, originales conservados |
| Telemetría / Gráficos | Once gráficos: altura, presión, temperatura, batería, corriente, giro XYZ, aceleración XYZ, altura GPS, satélites, latitud y longitud | Quince canales numéricos, últimas 180 muestras del segmento; no uno huecos ni dibujo posiciones sin solución |
| Telemetría / Comandos | Inicio, parada, altura cero, hora UTC, batería/solar y repetición del mismo ID | Banco USB/PC; deshabilitados en reproducción, sin reintentos automáticos |
| Telemetría / Guardado | Escritores original/CSV por destino, guardados, pendientes, descartes y errores; segundo destino para próxima sesión | Dos carpetas no acreditan soportes independientes; no formateo |
| Telemetría / Diagnóstico | Identidad de sesión/arranque/misión, segmentos, cortes, duplicados, conflictos e inválidos | Faltantes durante un corte pueden quedar indeterminados |
| Telemetría / Tramas | Últimos 300 eventos con recepción ASCII y datos originales | Espejo acotado de pantalla; el diario en disco conserva el flujo completo |
| Telemetría / Estado | Mediciones principales, etapa, contadores y antigüedad | Sin fuente no hay datos; desconectar USB no activa simulación |
| Fuentes | USB explícito, cinco escenarios PC y reproducción de JSONL a ×1/×5/×10 | Cada inicio conserva una sesión nueva; no sustituye archivos originales |
| Cámaras | Foto USB y Foto + microSD por unidad desde sus botones | Identidad esperada y puerto explícitos; bloqueo si telemetría ocupa el mismo puerto |
| Cámaras / Secuencia | Visor Qt con comprobación de archivos, tiempos, pausa e inicio | Reproduce un archivo verificado; no es video en vivo ni carga el candidato de firmware |
| Enlace RF | Tamaño de 1–255 bytes, BW 125/250/500 kHz, CR 4/5–4/8, SF7–SF12 | Cálculo de tiempo de aire existente; no mide confiabilidad ni configura RF |
| Recuperación | Tres casos ejecutables: fuentes complementarias, ausencia y conflicto | Archivos sintéticos nuevos; originales conservados |
| Ensayos / Enlace | Presupuesto de enlace con entradas TBD y ejemplo explícitamente hipotético | Reutiliza el evaluador existente; no convierte hipótesis en perfil acordado |
| Ensayos / Rotor | Balance energético incremental con entradas y resultado conservados | Modelo hipotético; mantiene resultados negativos, sin validar mecanismo real |
| Ensayos / Calidad y direccionamiento | Campaña ejecutable de seis casos de calidad y once vectores de destino | Reloj virtual y metadatos ficticios, sin puertos ni RF |
| Ensayos / Resultados y fuentes | Árbol filtrable de todos los archivos textuales de evidence/, config/ y docs/, contenido completo y tablas de registros | Sólo lectura; límite explícito de 8 MiB por apertura, sin truncar silenciosamente |
| Documentación | Informes seleccionados más acceso al archivo completo | No se limita la consulta a los doce informes de entrada |

## Pruebas y evidencia

Pasaron **14 pruebas del Laboratorio y 34 del banco de cámaras**. El [control final 04](../../evidence/2026-10-26-laboratorio-qt/control-04.json) conserva salidas y huellas. El control 03 corresponde al corte previo, antes de integrar el visor Qt de secuencias y completar SF8. Corregí además una colisión entre módulos llamados app en la importación del test de cierre; el test apunta ahora explícitamente a la aplicación Qt.

Comprobé los 22 valores y once series con el emisor PC, cuatro escritores al configurar dos destinos, tramas, confirmación de comandos, desconexión sintética e inhibición de comandos, y rechazo de compartir puerto con cámaras. Verifiqué los cuatro botones de fotografía mediante un sustituto del capturador: unidad, identidad, puerto y solicitud SD correctos, más el tratamiento del fallo. Esto comprueba la conexión del botón al capturador existente, no una foto física nueva.

La campaña ejecutable volvió a obtener seis de seis casos de calidad y once de once vectores de destino correctos. Conserva todas las trazas en su salida nueva. Sus tiempos son de reloj virtual; no son latencia física. El visor Qt mostró cuadros de una secuencia creada en PC y detuvo la reproducción al cambiar un archivo. La selección de cámara exige el registro privado y rechaza una muestra de PC como si fuese suya.

La suite también ejecutó cinco misiones completas: NOMINAL 131 válidos/0 inválidos/0 huecos; PACKET_LOSS 118/0/13; CORRUPTED_PACKET 121/10/10; GPS_LOSS 131/0/0; RESET lógico 128/0/3. Las pruebas existentes conservan reconstrucción, conflictos, procedencia y cierre durante trabajos.

Revisé renders de widgets Qt fuera de pantalla, incluidos variables, gráficos, comandos, cámaras y archivo de ensayos. No abrí ventanas en el escritorio, no controlé la PC y no abrí puertos físicos. El acceso existente del escritorio utiliza la misma entrada laboratorio/app.py y carga esta implementación al volver a abrirla.

## Qué puedo mostrar y qué falta

Puedo presentar la estación funcionando con simulación explícita, explorar los canales y registros, ejecutar recuperación y ensayos de software, consultar los resultados históricos y explicar sus límites. Las capturas físicas anteriores de ambas cámaras y su lectura independiente siguen siendo la evidencia de hardware disponible.

Falta comprobar físicamente los botones nuevos Qt con cada unidad preparada, revisar la interfaz en uso con el equipo y ensayar reconexiones reales desde esta versión. No hice una campaña nueva de fotos, video, energía, autonomía ni RF. El candidato de secuencia permanece sin cargar; audio, arranque estable y comandos/eventos de vuelo conservan sus dependencias. No cierro las tareas por esta ampliación de interfaz.
