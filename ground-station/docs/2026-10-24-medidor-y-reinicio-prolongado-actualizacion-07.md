# 24/10/2026 — ACTUALIZACIÓN 07: corregí el medidor de memoria y reinicié el ensayo prolongado

Diarios: [ASTRA-21](https://astrateam2026.atlassian.net/browse/ASTRA-21), [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22) y [ASTRA-34](https://astrateam2026.atlassian.net/browse/ASTRA-34). Continúo las actualizaciones [05](2026-10-24-cadencia-identidad-e-inicio-prolongado-actualizacion-05.md) y [06](2026-10-24-gps-presentacion-actualizacion-06.md), sin reemplazarlas.

## Problema comprobado

Durante la corrida vi crecer la memoria residente. Aislé el medidor: definía una estructura de ctypes y su tipo de puntero en cada consulta. Python conservaba esos tipos en su caché global. En una prueba separada de 501 consultas, el número de tipos pasó de 3 a 521; esa cuenta incluye inicialización diferida. La memoria residente observada pasó de 24555520 a 28954624 bytes. No era evidencia suficiente para atribuir la acumulación al receptor o al almacenamiento: identifiqué una causa concreta dentro de la instrumentación.

La primera corrida recibió y conservó 1906 muestras en 1905,063 segundos entre la primera y última. La detuve deliberadamente; no alcanzó dos horas y su resultado de aceptación es false. La memoria residente durante flujo pasó de 39,23 a 47,88 MiB. Tener historial y colas acotados no demostraba por sí solo memoria total acotada. Conservo el [resultado original](../evidence/2026-10-24-banco02/prolongado-interrumpido-10.json) y la [serie de salud](../evidence/2026-10-24-banco02/prolongado-interrumpido-health-10.csv). Los diarios y CSV originales quedan intactos en el directorio privado del intento.

La captura cerró con escritores drenados; no hubo rechazos, desbordes de encuadre, desconexiones ni conflictos en su segmento nominal. Esos resultados parciales no convierten la corrida interrumpida en aprobada. La inhibición transitoria de suspensión se liberó al cerrar.

## Corrección y control

Defino una sola vez el tipo y las firmas de la API de Windows y los reutilizo mediante una fábrica con caché de una entrada. Cada consulta crea sólo su instancia de datos. Pasaron 17 pruebas de software; la nueva hace 500 consultas después de inicializar y exige que no crezca la caché de tipos de puntero y que la fábrica se haya inicializado una vez.

Agregué a gui_health el número de inicializaciones del medidor. Antes de iniciar el intento nuevo, amplié el analizador para exigir que ese número sea 1 en cada control durante el flujo. Conservo la versión del analizador anterior y su resultado mediante Git y las huellas del intento; no recalculo el informe viejo con reglas nuevas para esconder la incidencia. Esta comprobación específica y las medidas de memoria no son una prueba universal de ausencia de fugas.

## Segundo intento iniciado

Cerré únicamente la GUI USB observada, volví al chat y cerré el control de pantalla. Con el puerto libre envié STOP de banco y confirmé ejecución; así no intento calibrar una misión anterior todavía activa. No reinicié físicamente el ESP32, no cargué firmware ni pedí otra secuencia BOOT. La identidad de ejecución nueva evita confundir este intento con el anterior.

Inicié la segunda corrida el 24/10/2026 a las 01:09:00 ART, con otra copia congelada del código, que incluye la corrección GPS y la del medidor. Solicité 7261 muestras a cadencia normal y cierre a 7280 segundos, previsto cerca de las 03:10:20 ART. Ese horario es una previsión, no un resultado. Debo comprobar duración monotónica, secuencia, archivos, memoria, contenedores y progreso de GUI al cerrar.

No activo el control del escritorio para leer archivos. El proceso conserva una inhibición transitoria de suspensión por inactividad, con liberación al terminar, sin cambiar ajustes persistentes. Sigo sin acreditar autonomía, radio ni respaldo externo simultáneo.

[Diagnóstico, prueba, huellas y configuración del segundo intento](../evidence/2026-10-24-banco02/memoria-y-reinicio-prolongado-11.json). El resultado del segundo intento queda pendiente y se publicará en otra actualización, aunque falle. No cierro tareas con criterios externos todavía pendientes.
