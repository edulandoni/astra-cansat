# 19/10/2026 — Actualización: compruebo conservación y recuperación de datos

Amplío [la investigación de prevención](2026-10-19-innovacion-y-prevencion.md), sin modificarla. Jira: [ASTRA-21, antecedente de investigación](https://astrateam2026.atlassian.net/browse/ASTRA-21?focusedCommentId=10049).

## Qué avancé

Pasé de identificar riesgos del banco a ejecutar tres experimentos de integración y una demostración offline de recuperación. No modifiqué el banco USB, los acuerdos de interfaz ni las otras áreas. Conservo código, resultados y registros del ensayo en [experiments/2026-10-19-resiliencia](../../experiments/2026-10-19-resiliencia/README.md).

| Experimento | Resultado observado | Qué puedo afirmar |
| --- | --- | --- |
| 7200 paquetes sin consumidor de pantalla | 7200 registros únicos en CSV y raw; quedan 250 actualizaciones en cola | En este ensayo, que la presentación no consuma la cola no elimina registros del archivo. No ejecuté ni bloqueé una GUI real. |
| Diez escrituras principales fallan y luego vuelven | De 31 mensajes, principal conserva 21; respaldo y raw conservan 31 | La adquisición continúa ante este fallo de CSV y deja error. No hay relleno automático de los huecos del principal. |
| Apertura fallida, corte y reconexión virtual | Tres aperturas solicitadas, dos eventos de desconexión y dos paquetes completos conservados | El bucle serie descarta el fragmento previo al corte y procesa los paquetes de la nueva conexión bajo el sustituto de prueba. |
| Reconciliación offline del caso CSV | Creo un archivo nuevo con 31 registros y procedencia; recupero del respaldo los contadores 11–20 | Puedo reconstruir esa copia conocida sin modificar los originales. No recupero datos ausentes en todas las copias. |
| Control negativo con contenido contradictorio | Detecto una altitud distinta para el mismo equipo/contador | No considero dos copias contradictorias como una recuperación limpia. El programa bloquea la escritura del candidato cuando hay conflictos. |

Los [resultados de integración](../../evidence/2026-10-19-resiliencia/resultados.json) conservan conteos, observaciones y huellas del código. El [reporte de reconciliación](../../evidence/2026-10-19-resiliencia-reconciliacion/resultado.json) conserva el origen de lo recuperado y las huellas originales. El [archivo de procedencia](../../evidence/2026-10-19-resiliencia-reconciliacion/procedencia.csv) permite revisar fila por fila qué copia aportó el dato.

## Aporte que propongo desarrollar

Quiero una estación que pueda explicar, por cada paquete, cuatro cosas diferentes: si lo recibió, en qué soporte lo guardó, si se puede recuperar y si presenta inconsistencias. Un contador de «recibidos» no debería dar a entender que todos esos registros están a salvo en todas las copias.

La demostración actual es independiente de la GUI y opera solo sobre una sesión de laboratorio conocida. Para convertirla en una función operativa me falta identidad de sesión acordada, detección de huecos y contradicciones, recuperación durable y avisos por cada destino de guardado. Debo conservar el original y separar cualquier reconstrucción con su procedencia.

Esto complementa el indicador de calidad propuesto antes: una alerta se apoyaría en evidencia que pueda revisarse. El posible aporte está en integrar y evaluar esas funciones para nuestra misión; no afirmo que el concepto sea nuevo en el mundo ni que el jurado ya lo considere innovación.

## Qué conviene prever ahora

Primero distinguiría «recibidos» de «guardados por destino» y resolvería la continuidad del registro raw, cuya excepción detenía el worker en el sondeo anterior. Después incorporaría reconciliación y calidad de datos con escenarios reproducibles. El respaldo de Jira a GitHub conserva decisiones del proyecto; esta recuperación de CSV trata los datos de una misión y resuelve otro problema.

La prueba de la cola tiene un resultado favorable concreto. La prueba de escritura muestra el riesgo pendiente concreto: que vuelva a funcionar un archivo no significa que los registros faltantes aparezcan solos. No necesito adivinar eso con el hardware: ya puedo definir y probar el comportamiento deseado en PC.

## Límites que mantengo

- Dos carpetas del mismo disco no acreditan dos soportes independientes.
- El sustituto del puerto no prueba USB, conectores, controladores, ruido RF ni espera real de reconexión.
- 7200 mensajes equivalen al volumen de dos horas a 1 Hz; el ensayo duró segundos y no verifica batería, autonomía ni operación sostenida real.
- La carga reutiliza valores de práctica; no representa una trayectoria física coherente durante dos horas.
- El fallo se inyecta antes de completar una fila CSV; no simula todos los tipos de corrupción, escritura parcial, cachés ni corte eléctrico.
- Conservar y releer archivos en esta ejecución no acredita resistencia ante pérdida de energía.
- El recuperador usa equipo y contador dentro de una sesión declarada del laboratorio; no puede separar vuelos o reinicios por sí solo. Conservo esa necesidad de interfaz pendiente con Edu.
- Las fuentes del banco mantienen sus huellas. Solo agregué herramientas de experimento y documentación.

## Fuentes técnicas

La documentación oficial de [unittest.mock](https://docs.python.org/3.12/library/unittest.mock-examples.html) describe sustitución controlada de dependencias e inyección de excepciones. La uso para ejecutar las rutas reales del banco con un puerto ficticio, sin convertir al sustituto en evidencia de hardware.

La documentación oficial de [os.fsync](https://docs.python.org/3.12/library/os.html#os.fsync) distingue el vaciado del buffer del archivo y la solicitud de sincronización al sistema. El banco sincroniza sus CSV, pero raw usa flush; esa diferencia debe estudiarse con pruebas de interrupción propias antes de prometer durabilidad. Una llamada de sincronización por sí sola no certifica la alimentación ni el soporte físico.
