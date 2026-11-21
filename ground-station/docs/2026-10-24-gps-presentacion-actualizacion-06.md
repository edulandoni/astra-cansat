# 24/10/2026 — ACTUALIZACIÓN 06: posición GPS válida y presentación de datos sin solución

Diarios: [ASTRA-22](https://astrateam2026.atlassian.net/browse/ASTRA-22) y [ASTRA-34](https://astrateam2026.atlassian.net/browse/ASTRA-34). Continúo la [actualización 05](2026-10-24-cadencia-identidad-e-inicio-prolongado-actualizacion-05.md), sin modificar sus resultados ni la copia que está ejecutando el ensayo prolongado.

## Qué encontré y corregí

El banco conserva la última solución GPS en el motor de datos, y nuestro emisor de GPS_LOSS repite esa posición. Al revisar la GUI encontré un caso que esa simulación no exponía: otro emisor puede declarar cero satélites y mandar coordenadas numéricas distintas, por ejemplo ceros. La pantalla anterior mostraba esos campos de la trama sin sustituirlos por la última solución válida, aunque el aviso decía posición retenida.

Separé la presentación del contenido recibido. Con GPS_SATS=0, muestro hora, altitud y coordenadas de la última solución válida con el texto «última válida» y su edad. Si no hubo una solución anterior, muestro «— SIN FIX» y aviso que no existe posición válida anterior. Mantengo el número de satélites declarado en el mensaje. Cuando vuelve el fix, recupero la presentación del dato nuevo.

No modifico los valores originales del paquete, el CSV, la identificación de sesión, la adquisición ni el firmware. No declaro válido un GPS real sólo por tener satélites: esta regla pertenece al perfil de banco; los indicadores de calidad de vuelo deben acordarse en el ICD.

## Pruebas y evidencia

Pasaron las 16 pruebas de software. El caso nuevo comprueba ausencia de fix sin posición anterior, coordenadas sin fix diferentes de la última válida, conservación de los valores originales y retorno del fix. En la primera preparación del test usé un contador menor y, correctamente, el motor lo trató como dato tardío: corregí el orden de la entrada de prueba antes de comprobar el caso de presentación. No cambié la regla de ordenamiento para hacer pasar el test.

También abrí una reproducción sintética de dos mensajes: uno válido y otro sin fix con coordenadas cero. Observé la pantalla con origen REPLAY, contador 51, satélites 0 y cuatro campos GPS identificados como última solución válida; las seis gráficas y las unidades quedaron legibles, y los comandos estaban deshabilitados. Cerré sólo esa reproducción, volví al chat y cerré el control del escritorio. El receptor USB prolongado siguió separado y activo.

[Resultado, huellas y alcance de observación](../evidence/2026-10-24-banco02/gps-presentacion-09.json). La comprobación visual es una observación de esta reproducción en pantalla; no la presento como prueba de un receptor GPS físico ni como captura de vuelo. No guardé un archivo de imagen adicional en este bloque.

## Relación con el ensayo prolongado

La corrida USB iniciada a las 00:36:19 ART sigue usando su snapshot congelado anterior. Su resultado corresponderá a esas huellas y no acredita esta corrección posterior de presentación sin fix. La prueba nueva es independiente; no reinicio ni altero la campaña nominal para atribuirle cambios que no ejecutó. Su cierre y resultado se registrarán en otra actualización.
