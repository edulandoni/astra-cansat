# 24/10/2026 — ACTUALIZACIÓN: criterios generales del premio de estación de tierra

Diario: [ASTRA-35](https://astrateam2026.atlassian.net/browse/ASTRA-35). Amplío la [lectura de antecedentes del 23/10](2026-10-23-antecedentes-a-pruebas.md) y la [ficha DJS anterior](2026-10-20-djs-arya-vuelo-y-recuperacion.md), sin reemplazarlas.

## Fuente nueva y alcance

Encontré en el sitio del organizador el [Mark Walker Portable Ground Station Design Award](https://cansatcompetition.com/docs/Mark%20Walker%20Portable%20Ground%20Station%20Design%20Award.pdf). Leí el texto completo y observé las tres páginas, incluida su rúbrica. Describe un premio opcional para una estación integrada, transportable por una persona, menor de 15 libras y sin notebook ni notebook reempaquetada. Pide unidad lista sin montaje salvo antena, fuente propia, un mando de encendido, inicio automático del software, pantalla, entradas de usuario, radio y guardado en memoria USB; excluye operación remota.

La tabla puntúa de 0 a 10 funcionalidad/FRR, construcción, artesanía, interfaz, facilidad de uso, calidad de presentación y estilo. No contiene puntajes otorgados a DJS, acta de deliberación, código o datos crudos de vuelo. Tampoco identifiqué fecha/edición explícita en estas páginas: registro la versión consultada por su huella, sin atribuirla automáticamente a una edición particular.

Esto precisa el faltante anterior: ahora tengo criterios generales publicados; sigue faltando evidencia técnica y puntuación aplicada al ganador. La [clasificación oficial](https://cansatcompetition.com/winners.html) confirma el premio 2026 a DJS Arya, pero no demuestra cómo puntuó en cada rubro.

## Cómo lo uso para mi trabajo

No convierto condiciones de este premio internacional en requisitos CONAE ni cambio nuestra arquitectura de notebook+ESP32 para imitarlas. Para nuestro PDR sigo la fuente oficial CONAE y el alcance acordado con el equipo. Puedo usar el premio como referencia de usabilidad, sin afirmar elegibilidad ni compararme con una puntuación que no tengo.

| Pregunta propia | Evidencia o siguiente prueba de ASTRA |
|---|---|
| ¿Puedo distinguir recibir de guardar y explicar un fallo? | Cinco escenarios, RST/reconexión y bytes conservados; causa de ráfaga malformada todavía pendiente |
| ¿La copia externa se puede verificar? | Reproducción de 131 tramas en dos discos con huellas iguales y reconstrucción equivalente; no recepción física simultánea |
| ¿Se entiende origen, unidades y antigüedad? | GUI de banco con origen explícito, conversión SI y datos actuales separados del histórico; legibilidad al sol pendiente |
| ¿La operación continua tiene evidencia? | Ensayo USB prolongado iniciado; resultado todavía pendiente en este corte; no es autonomía |
| ¿Puedo pasar de propuesta a una estación integrada? | Estudio futuro de arranque, alimentación, montaje y procedimiento; no implementé ni validé un equipo portátil por leer la rúbrica |

La utilidad nueva es orientar preguntas de verificación, no agregar una función visual sólo porque existe un premio. La investigación de rotor sigue separada; este documento no demuestra energía generada ni seguridad de un mecanismo.

## Conservación

PDF de 73521 bytes, tres páginas, SHA256 `f6c047e8cf6348aa3dbfd73ee58aca4a35366cd1ccd04b8358c674ee03c808ed`. Original y render de lectura quedan en la carpeta temática de Descargas del trabajo, con registro de origen/destino y sin movimientos. No republico el PDF ni su tabla como imagen: conservo enlace al original y mi análisis. La [referencia visual](2026-10-24-catalogo-visual-criterios-premio.csv) registra que se trata de un documento/tabla, no de una foto de la estación ganadora.
