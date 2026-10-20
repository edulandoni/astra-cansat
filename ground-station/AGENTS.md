# Alcance: groundstation y manejo de datos

Estas pautas se aplican únicamente dentro de ground-station/. No imponen metodología a otras áreas.

- Escribo como Cristian: primera persona para mi trabajo y plural para el equipo. No escribo sobre mí como un tercero ni uso «Instrucción expresa de Cristian» en publicaciones nuevas.
- Diario sin sobrescritura: no editar ni eliminar entradas fechadas, capturas Jira, resultados históricos ni originales archivados. Agregar ACTUALIZACIÓN con fecha real, referencia al original, cambio, motivo, evidencia y efecto.
- En Jira solo modificar tareas creadas por mí o asignadas a mi cuenta. Verificar pertenencia antes de cada cambio. Conservar descripciones originales y agregar comentarios nuevos. Nunca tocar tareas ajenas por dependencia.
- Backlog: ideas; Por hacer: trabajo comprometido sin iniciar; En curso: trabajo iniciado; completado solo con criterios y evidencia.
- Todo cambio debe llevar clave Jira, motivo, prueba realizada, límites, pendientes y enlaces de ida y vuelta. No crear comentarios de respaldo que produzcan ciclos infinitos de exportación.
- Trabajo en rama groundstation. No actualizar main ni carpetas ajenas. Las fuentes de vuelo y protocol/ compartido no se modifican desde esta tarea.
- Diferenciar resultados de software, ensayos físicos y pendientes. No afirmar RF, autonomía o persistencia con una simulación.
- No elegir parámetros RF ni aprobar un contrato compartido sin acuerdo con Edu. Referencia de la revisión: anexo CONAE v2; sintaxis heredada v1 es provisional.
- Leer README.md, docs/metodologia-2026-10-19.md y la entrada fechada más reciente antes de continuar.

## Actualización del 19/10/2026: ubicación temática del diario

- Antes de registrar un avance leer docs/trazabilidad-vigente-2026-10-19.md. No usar ASTRA-21 como diario general.
- ASTRA-33: metodología, trazabilidad, importación/publicación y respaldo documental Jira → GitHub. Todos los avisos del respaldo van aquí, previa verificación de pertenencia.
- ASTRA-34: investigación de calidad de datos y prevención; ASTRA-35: antecedentes CanSat; ASTRA-36: investigación de rotor y energía.
- ASTRA-20: simulador; ASTRA-21: receptor/parser/registro y recuperación CSV; ASTRA-22: GUI; ASTRA-18/23/24/25: sus alcances originales.
- Diferenciar respaldo de CSV de vuelo (ASTRA-21) de respaldo de documentación de Jira (ASTRA-33). Si una entrada mezcla temas, desglosarla en nuevas entradas relacionadas y conservar el original.
- Las claves antiguas de documentos/commits son históricas; no reescribirlas para ocultar una ubicación incorrecta. Usar la clave temática correcta en nuevas publicaciones. No presentar esta reorganización como nuevos ensayos.

## Incorporación del 19/10/2026: fuentes del aula

- ASTRA-37 conserva revisión del aula CONAE, plantillas/evaluación PDR, aclaraciones oficiales y contradicciones. Leer docs/aula/2026-10-19/revision-aula.md junto con el mapa vigente antes de usar conclusiones anteriores.
- Los efectos sobre código, datos, GUI, antena o interfaz se registran también en su tarea técnica. ASTRA-33 conserva únicamente metodología/publicación/respaldo.
- Conservar el anexo y las respuestas como fuentes distintas. No resolver silenciosamente discrepancias de envolvente, plazo o planilla. No publicar contraseña, cookies, claves de sesión ni transcripciones de sesión completas. No deducir TEAM_ID a partir del nombre de acceso.
