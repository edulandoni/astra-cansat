# Alcance: groundstation y manejo de datos

## Evaluación de trama y perfil LoRa — 26/10/2026

- ASTRA-40 conserva el análisis específico de bytes, SF/BW/CR, tiempo de aire, confiabilidad y energía para justificar decisiones en el PDR. ASTRA-18/25/24 mantienen requisitos RF, link budget e interoperabilidad.
- El objetivo ampliado está en docs/historial/2026-10-26-objetivo-ampliado-camaras-radio.md. Continúo cámaras y grabación en ASTRA-39; audio es un extra sujeto a hardware. Edu define empaquetado/comandos de vuelo y adapto tierra; los cálculos offline no aprueban un perfil compartido.

## Identificación pública de cámaras — 26/10/2026

- Uso «cámara 1» y «cámara 2» en la aplicación, GitHub, Drive y Jira. Mantengo la correspondencia física en el registro privado del banco.
- Publico configuración, pruebas, fallos observados y límites técnicos. La información interna de manipulación no se incorpora a entregables ni etiquetas públicas.
- La corrección expresamente solicitada de denominaciones alcanza documentos y comentarios existentes; conservo resultados, fechas y evidencias técnicas. Las nuevas capturas de Jira parten de los comentarios corregidos.

## Interacción con ventanas — actualización del24/10/2026

- Después de revisar u operar la interfaz del banco, vuelvo al chat actual en la app deGPT/Codex antes de pedir una maniobra o esperar respuesta. No dejo otra ventana tapando las preguntas.
- Uso la navegación propia de la app para mostrar el chat actual. No manipulo el contenido deGPT mediante automatización de pantalla ni cierro el receptor para recuperar foco cuando debe seguir ensayando.
- Si necesito observar otra vez laGUI, la identifico y reviso; al terminar repito el retorno al chat. No doy por hecha una maniobra física por tiempo transcurrido: compruebo su efecto y solicito respuesta cuando hace falta.
- Cierro la sesión de control de pantalla al terminar la operación; no la mantengo abierta en espera. La adquisición USB, el procesamiento de archivos y las consultas por API continúan sin activar control del escritorio. Sólo vuelvo a activarlo cuando necesito una operación concreta en la interfaz.

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

## Organización estable de Drive — actualización del 20/10/2026

- Leer docs/organizacion-drive/2026-10-20/Mantenimiento_y_mejora_continua_2026-10-20.md y el mapa de esa carpeta antes de publicar archivos o reorganizar mi Drive. Seguir actualizaciones fechadas posteriores sin borrar las anteriores.
- Mantener carpetas principales por función; agregar pruebas/versiones dentro de su tema. Una nueva publicación no justifica mover o renumerar la estructura. Revisarla sólo ante confusión real o al preparar un hito.
- Publicar un original por tema y enlazar desde otros; conservar versiones fechadas. Para movimientos verificar padres e identificadores y registrar origen/destino sin reemplazar contenido ni cambiar permisos.
- El diario de organización sigue en ASTRA-33. Las novedades oficiales van a ASTRA-37 y su carpeta temática de requisitos; las pruebas y decisiones técnicas siguen en sus tareas. No usar la carpeta general de decisiones como depósito de todos los análisis.
- El banco USB es experimental con formato heredado; no archivar toda herramienta provisional como DEPRECATED. El histórico y las versiones previas conservan su valor de evidencia, sin presentarse como la línea de desarrollo vigente.

## Análisis diario priorizado del aula — actualización del 20/10/2026

- ASTRA-37 conserva fuentes, versiones, cobertura y cambios oficiales; ASTRA-38 conserva informes diarios priorizados y su diario al corte. No reemplazar ni renombrar ASTRA-37.
- Leer docs/aula/2026-10-20/Metodo_analisis_diario_2026-10-20.md y la actualización posterior más reciente. Conservar un informe nuevo por ejecución diaria con hora Argentina, novedades separadas del panorama acumulado, utilidad, prioridades justificadas y fuentes. Si falta acceso o evidencia, identificar el corte como parcial.
- El informe y comentario diarios en ASTRA-38 se generan aunque no haya novedades, indicando sin cambios. Esta pauta específica actualiza la anterior de no publicar nada sin novedades sólo para ese informe de corte. Investigación y avisos de respaldo siguen evitando duplicados sin avance real.
- Fotos y antecedentes van a ASTRA-35 y su carpeta de investigación; rotor a ASTRA-36. Registrar tipo, fuente, crédito, permisos y acceso visual real; no convertir referencias localizadas en imágenes inspeccionadas ni premios en validación de cada función.
