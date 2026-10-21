# 20/10/2026 — DJS Arya: vuelo, recuperación y evidencia de tierra

Diario: [ASTRA-35](https://astrateam2026.atlassian.net/browse/ASTRA-35). Amplío el [relevamiento anterior](2026-10-20-antecedentes-codigo-y-fotos.md). Esta pasada profundiza una ficha con dos fuentes primarias nuevas, sin cambiar software.

## Qué encontré

Leí el texto extraído de las 15 páginas del [artículo institucional de DJSCE](https://www.djsce.ac.in/docs/DJS%20Arya%20Article.pdf). Las páginas 10–13 relatan la edición internacional **2025**: telemetría XBee a 1 Hz, GUI con estados y modos SIM/FLIGHT, autogiro, video de liberación y pérdida parcial de carga útil durante recuperación. Son afirmaciones de la institución, sin CSV crudo ni protocolo de ensayo reproducible en este documento. La foto de la página 12 muestra conjunto abierto con palas; no acredita energía generada. No confundo este vuelo con el premio Ground Station **2026**, confirmado anteriormente por el organizador.

La primera parte mezcla una referencia nacional «2024» con enlaces periodísticos fechados en 2025. Conservo esa inconsistencia; no fijo el año nacional ni traslado sus velocidades y geometría a CONAE. El texto extraído tiene páginas casi vacías con imágenes: no lo presento como lectura de texto incrustado en cada foto ni auditoría audiovisual.

En el [portafolio de Kshayik Doshi](https://kshayik.com/projects/djs-arya-cansat-gcs/) se describe GCS de aproximadamente 1 Hz y más de 22 parámetros. Es una descripción del autor: no identifiqué commit de vuelo, CSV, pruebas de fallo, fecha de edición inequívoca ni criterios del premio 2026. Sus tres enlaces de galería apuntan a images.unsplash.com; no los cuento como capturas técnicas verificadas del equipo.

## Para qué nos sirve en ASTRA

La recuperación física puede fallar aunque se haya recibido telemetría. Por eso propongo que nuestra estación conserve última posición válida con hora y antigüedad, raw y CSV recuperables, y un resumen posterior que distinga datos recibidos de hardware recuperado. Es una inferencia de diseño propia, no una función que haya comprobado hoy en DJS ni una implementación nueva de ASTRA. La revisión de calidad queda enlazada a ASTRA-34 y la recuperación de datos a ASTRA-21, sin atribuir a este relato una causa técnica que no documenta.

También conviene separar SIM y FLIGHT de forma visible y conservar el origen del dato al cambiar de modo. Un PFR honesto puede documentar una falla y lo que pudo analizarse; los elogios del artículo no convierten el descenso en seguro ni prueban cobertura RF o ausencia de pérdidas.

## Dos fotografías inspeccionadas

Observé las imágenes incrustadas de páginas 11 y 12: conjunto exterior cerrado identificado DJS Arya/team 3109 y conjunto abierto con palas desplegadas. Se registran F08/F09 en el [suplemento visual](2026-10-20-catalogo-visual-suplemento-diario.csv). La atribución proviene del documento y rótulo visible; autor individual y permiso de reutilización siguen sin confirmar. No republico imágenes ni el PDF. No identifiqué una foto comprobada de su estación de tierra; esa búsqueda sigue pendiente.

## Control y próximos pasos

PDF: 16.996.872 bytes, 15 páginas; SHA-256 `73c892e3a6d73d1f2f1c6b85a5953a3bd0d12caad325762ddfcc35f647dcda53`. Original conservado en Descargas dentro de la carpeta de este corte. Extracción textual local y vista individual de dos imágenes; no compilé software, no ejecuté vuelo ni medí generación. Faltan datos crudos, pérdidas cuantificadas, validación de la GUI y causas verificadas de recuperación. La pasada agrega un antecedente documentado de falla parcial y referencias visuales, no un sistema aprobado para ASTRA.
